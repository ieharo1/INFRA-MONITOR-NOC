from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .forms import DeviceFilterForm
from .models import Device, Event, Metric, Port, ServiceCheck


@login_required
def dashboard(request):
    devices = Device.objects.all()
    total_devices = devices.count()
    up_devices = devices.filter(status=Device.DeviceStatus.UP).count()
    down_devices = devices.filter(status=Device.DeviceStatus.DOWN).count()
    degraded_devices = devices.filter(status=Device.DeviceStatus.DEGRADED).count()
    open_events = Event.objects.filter(resolved_at__isnull=True).select_related('device')[:10]
    last_metrics = Metric.objects.select_related('device').order_by('-created_at')[:15]

    type_stats = list(devices.values('device_type').annotate(total=Count('id')).order_by('-total'))

    context = {
        'total_devices': total_devices,
        'up_devices': up_devices,
        'down_devices': down_devices,
        'degraded_devices': degraded_devices,
        'open_events': open_events,
        'last_metrics': last_metrics,
        'type_stats': type_stats,
    }
    return render(request, 'monitoring/dashboard.html', context)


@login_required
def device_list(request):
    form = DeviceFilterForm(request.GET or None)
    devices = Device.objects.select_related('site', 'rack').all().order_by('name')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        status = form.cleaned_data.get('status')
        device_type = form.cleaned_data.get('device_type')

        if q:
            devices = devices.filter(name__icontains=q)
        if status:
            devices = devices.filter(status=status)
        if device_type:
            devices = devices.filter(device_type=device_type)

    return render(request, 'monitoring/device_list.html', {'devices': devices, 'form': form})


@login_required
def device_detail(request, pk: int):
    device = get_object_or_404(Device.objects.select_related('site', 'rack'), pk=pk)
    ports = Port.objects.filter(device=device).select_related('connected_device')
    checks = ServiceCheck.objects.filter(device=device)
    events = Event.objects.filter(device=device).order_by('-created_at')[:20]
    metrics = Metric.objects.filter(device=device).order_by('-created_at')[:20]

    return render(
        request,
        'monitoring/device_detail.html',
        {
            'device': device,
            'ports': ports,
            'checks': checks,
            'events': events,
            'metrics': metrics,
        },
    )


@login_required
def topology(request):
    ports = Port.objects.select_related('device', 'connected_device').exclude(connected_device__isnull=True)
    return render(request, 'monitoring/topology.html', {'links': ports})
