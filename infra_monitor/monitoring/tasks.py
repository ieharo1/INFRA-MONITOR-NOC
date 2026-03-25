import random
import socket
import subprocess
import time

from celery import shared_task
from django.db.models import Q
from django.utils import timezone

from .models import Device, Event, Metric, ServiceCheck


def _run_ping(host: str, timeout_seconds: int) -> tuple[bool, float]:
    started = time.perf_counter()
    cmd = ['ping', '-c', '1', '-W', str(timeout_seconds), host]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    latency = (time.perf_counter() - started) * 1000
    return result.returncode == 0, latency


def _run_tcp(host: str, port: int, timeout_seconds: int) -> tuple[bool, float]:
    started = time.perf_counter()
    with socket.create_connection((host, port), timeout=timeout_seconds):
        latency = (time.perf_counter() - started) * 1000
    return True, latency


@shared_task
def run_monitoring_cycle() -> dict:
    checks = ServiceCheck.objects.select_related('device').filter(enabled=True)
    up_count = 0
    down_count = 0

    for check in checks:
        ok = False
        latency = None

        if check.check_type == ServiceCheck.CheckType.PING:
            ok, latency = _run_ping(check.target_host, check.timeout_seconds)
        elif check.check_type == ServiceCheck.CheckType.TCP and check.target_port:
            try:
                ok, latency = _run_tcp(check.target_host, check.target_port, check.timeout_seconds)
            except OSError:
                ok = False

        old_status = check.status
        check.status = ServiceCheck.Status.UP if ok else ServiceCheck.Status.DOWN
        check.latency_ms = latency
        check.checked_at = timezone.now()
        check.save(update_fields=['status', 'latency_ms', 'checked_at'])

        device = check.device
        if not ok:
            down_count += 1
            device.status = Device.DeviceStatus.DOWN
            Event.objects.create(
                device=device,
                service_check=check,
                severity=Event.Severity.CRITICAL,
                message=f'Check {check.name} falló en {check.target_host}',
            )
        else:
            up_count += 1
            if old_status == ServiceCheck.Status.DOWN:
                Event.objects.create(
                    device=device,
                    service_check=check,
                    severity=Event.Severity.INFO,
                    message=f'Check {check.name} recuperado en {check.target_host}',
                )

        has_down = device.checks.filter(status=ServiceCheck.Status.DOWN, enabled=True).exists()
        device.status = Device.DeviceStatus.DOWN if has_down else Device.DeviceStatus.UP
        device.last_seen = timezone.now()
        device.save(update_fields=['status', 'last_seen'])

        Metric.objects.create(
            device=device,
            cpu_percent=round(random.uniform(10, 95), 2),
            memory_percent=round(random.uniform(20, 90), 2),
            disk_percent=round(random.uniform(15, 98), 2),
            rx_mbps=round(random.uniform(5, 1200), 2),
            tx_mbps=round(random.uniform(5, 950), 2),
        )

    return {'checks_total': checks.count(), 'up': up_count, 'down': down_count}
