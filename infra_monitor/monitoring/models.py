from django.db import models
from django.utils import timezone


class Site(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Ecuador')

    def __str__(self) -> str:
        return f'{self.name} ({self.city})'


class Rack(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='racks')
    name = models.CharField(max_length=120)
    floor = models.CharField(max_length=60, blank=True)

    def __str__(self) -> str:
        return f'{self.site.name} - {self.name}'


class Device(models.Model):
    class DeviceType(models.TextChoices):
        SERVER = 'server', 'Servidor'
        SWITCH = 'switch', 'Switch'
        ROUTER = 'router', 'Router'
        CAMERA = 'camera', 'Cámara'
        FIREWALL = 'firewall', 'Firewall'
        STORAGE = 'storage', 'Storage'
        ACCESS_POINT = 'ap', 'Access Point'
        OTHER = 'other', 'Otro'

    class DeviceStatus(models.TextChoices):
        UP = 'up', 'Operativo'
        DEGRADED = 'degraded', 'Degradado'
        DOWN = 'down', 'Caído'

    name = models.CharField(max_length=120)
    device_type = models.CharField(max_length=20, choices=DeviceType.choices)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, related_name='devices')
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True, blank=True, related_name='devices')
    management_ip = models.GenericIPAddressField(protocol='IPv4')
    vendor = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=120, blank=True)
    serial = models.CharField(max_length=120, blank=True)
    os_version = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=DeviceStatus.choices, default=DeviceStatus.UP)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.management_ip})'


class Port(models.Model):
    class PortState(models.TextChoices):
        UP = 'up', 'UP'
        DOWN = 'down', 'DOWN'
        BLOCKED = 'blocked', 'BLOQUEADO'

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='ports')
    name = models.CharField(max_length=80)
    vlan = models.PositiveIntegerField(default=1)
    speed_mbps = models.PositiveIntegerField(default=1000)
    mac_address = models.CharField(max_length=50, blank=True)
    connected_device = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incoming_links',
    )
    state = models.CharField(max_length=10, choices=PortState.choices, default=PortState.UP)

    class Meta:
        unique_together = ('device', 'name')

    def __str__(self) -> str:
        return f'{self.device.name}::{self.name}'


class ServiceCheck(models.Model):
    class CheckType(models.TextChoices):
        PING = 'ping', 'Ping ICMP'
        TCP = 'tcp', 'TCP Port'

    class Status(models.TextChoices):
        UP = 'up', 'UP'
        DOWN = 'down', 'DOWN'

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='checks')
    name = models.CharField(max_length=120)
    check_type = models.CharField(max_length=10, choices=CheckType.choices, default=CheckType.PING)
    target_host = models.CharField(max_length=120)
    target_port = models.PositiveIntegerField(null=True, blank=True)
    timeout_seconds = models.PositiveIntegerField(default=2)
    interval_seconds = models.PositiveIntegerField(default=60)
    enabled = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UP)
    latency_ms = models.FloatField(null=True, blank=True)
    checked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.device.name} - {self.name}'


class Metric(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='metrics')
    cpu_percent = models.FloatField(default=0)
    memory_percent = models.FloatField(default=0)
    disk_percent = models.FloatField(default=0)
    rx_mbps = models.FloatField(default=0)
    tx_mbps = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)


class Event(models.Model):
    class Severity(models.TextChoices):
        INFO = 'info', 'Info'
        WARNING = 'warning', 'Warning'
        CRITICAL = 'critical', 'Critical'

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='events')
    service_check = models.ForeignKey(ServiceCheck, on_delete=models.SET_NULL, null=True, blank=True)
    severity = models.CharField(max_length=12, choices=Severity.choices)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_open(self) -> bool:
        return self.resolved_at is None

    def __str__(self) -> str:
        return f'[{self.severity}] {self.message}'
