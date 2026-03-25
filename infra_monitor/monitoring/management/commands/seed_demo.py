from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from monitoring.models import Device, Port, Rack, ServiceCheck, Site


class Command(BaseCommand):
    help = 'Crea datos demo para Infra Monitor'

    def handle(self, *args, **kwargs):
        site, _ = Site.objects.get_or_create(name='DC Quito', city='Quito', country='Ecuador')
        rack_core, _ = Rack.objects.get_or_create(site=site, name='RACK-CORE', floor='Piso 1')

        core_sw, _ = Device.objects.get_or_create(
            name='SW-CORE-01',
            defaults={
                'device_type': Device.DeviceType.SWITCH,
                'site': site,
                'rack': rack_core,
                'management_ip': '10.10.0.2',
                'vendor': 'Cisco',
                'model': 'C9500',
                'os_version': 'IOS XE',
            },
        )
        app_srv, _ = Device.objects.get_or_create(
            name='APP-SRV-01',
            defaults={
                'device_type': Device.DeviceType.SERVER,
                'site': site,
                'rack': rack_core,
                'management_ip': '10.10.0.10',
                'vendor': 'Dell',
                'model': 'R740',
                'os_version': 'Ubuntu 24.04',
            },
        )
        cam01, _ = Device.objects.get_or_create(
            name='CAM-LOBBY-01',
            defaults={
                'device_type': Device.DeviceType.CAMERA,
                'site': site,
                'management_ip': '10.10.5.15',
                'vendor': 'Hikvision',
                'model': 'DS-2CD',
            },
        )

        Port.objects.get_or_create(device=core_sw, name='Gi1/0/1', defaults={'vlan': 10, 'connected_device': app_srv})
        Port.objects.get_or_create(device=core_sw, name='Gi1/0/10', defaults={'vlan': 20, 'connected_device': cam01})

        ServiceCheck.objects.get_or_create(
            device=app_srv,
            name='Ping APP-SRV-01',
            defaults={
                'check_type': ServiceCheck.CheckType.PING,
                'target_host': app_srv.management_ip,
            },
        )
        ServiceCheck.objects.get_or_create(
            device=app_srv,
            name='HTTP APP-SRV-01',
            defaults={
                'check_type': ServiceCheck.CheckType.TCP,
                'target_host': app_srv.management_ip,
                'target_port': 80,
            },
        )
        ServiceCheck.objects.get_or_create(
            device=cam01,
            name='RTSP CAM-LOBBY-01',
            defaults={
                'check_type': ServiceCheck.CheckType.TCP,
                'target_host': cam01.management_ip,
                'target_port': 554,
            },
        )

        user_model = get_user_model()
        if not user_model.objects.filter(username='admin').exists():
            user_model.objects.create_superuser('admin', 'admin@example.com', 'admin1234')

        self.stdout.write(self.style.SUCCESS('Datos demo creados. Usuario: admin / admin1234'))
