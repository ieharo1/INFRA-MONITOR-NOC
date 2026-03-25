from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('city', models.CharField(max_length=120)),
                ('country', models.CharField(default='Ecuador', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('floor', models.CharField(blank=True, max_length=60)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='racks', to='monitoring.site')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('device_type', models.CharField(choices=[('server', 'Servidor'), ('switch', 'Switch'), ('router', 'Router'), ('camera', 'Cámara'), ('firewall', 'Firewall'), ('storage', 'Storage'), ('ap', 'Access Point'), ('other', 'Otro')], max_length=20)),
                ('management_ip', models.GenericIPAddressField(protocol='IPv4')),
                ('vendor', models.CharField(blank=True, max_length=100)),
                ('model', models.CharField(blank=True, max_length=120)),
                ('serial', models.CharField(blank=True, max_length=120)),
                ('os_version', models.CharField(blank=True, max_length=120)),
                ('status', models.CharField(choices=[('up', 'Operativo'), ('degraded', 'Degradado'), ('down', 'Caído')], default='up', max_length=20)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', to='monitoring.rack')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='devices', to='monitoring.site')),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_percent', models.FloatField(default=0)),
                ('memory_percent', models.FloatField(default=0)),
                ('disk_percent', models.FloatField(default=0)),
                ('rx_mbps', models.FloatField(default=0)),
                ('tx_mbps', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='monitoring.device')),
            ],
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('vlan', models.PositiveIntegerField(default=1)),
                ('speed_mbps', models.PositiveIntegerField(default=1000)),
                ('mac_address', models.CharField(blank=True, max_length=50)),
                ('state', models.CharField(choices=[('up', 'UP'), ('down', 'DOWN'), ('blocked', 'BLOQUEADO')], default='up', max_length=10)),
                ('connected_device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incoming_links', to='monitoring.device')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ports', to='monitoring.device')),
            ],
            options={'unique_together': {('device', 'name')}},
        ),
        migrations.CreateModel(
            name='ServiceCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('check_type', models.CharField(choices=[('ping', 'Ping ICMP'), ('tcp', 'TCP Port')], default='ping', max_length=10)),
                ('target_host', models.CharField(max_length=120)),
                ('target_port', models.PositiveIntegerField(blank=True, null=True)),
                ('timeout_seconds', models.PositiveIntegerField(default=2)),
                ('interval_seconds', models.PositiveIntegerField(default=60)),
                ('enabled', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('up', 'UP'), ('down', 'DOWN')], default='up', max_length=10)),
                ('latency_ms', models.FloatField(blank=True, null=True)),
                ('checked_at', models.DateTimeField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='monitoring.device')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('severity', models.CharField(choices=[('info', 'Info'), ('warning', 'Warning'), ('critical', 'Critical')], max_length=12)),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='monitoring.device')),
                ('service_check', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.servicecheck')),
            ],
        ),
    ]
