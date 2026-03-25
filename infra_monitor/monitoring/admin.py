from django.contrib import admin

from .models import Device, Event, Metric, Port, Rack, ServiceCheck, Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'floor')


class PortInline(admin.TabularInline):
    model = Port
    extra = 0


class ServiceCheckInline(admin.TabularInline):
    model = ServiceCheck
    extra = 0


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'management_ip', 'status', 'site', 'last_seen')
    list_filter = ('device_type', 'status', 'site')
    search_fields = ('name', 'management_ip', 'vendor', 'model')
    inlines = [PortInline, ServiceCheckInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('device', 'severity', 'message', 'created_at', 'resolved_at')
    list_filter = ('severity',)


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('device', 'cpu_percent', 'memory_percent', 'disk_percent', 'created_at')
