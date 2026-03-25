from django import forms

from .models import Device


class DeviceFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Buscar')
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + list(Device.DeviceStatus.choices),
        label='Estado',
    )
    device_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + list(Device.DeviceType.choices),
        label='Tipo',
    )
