from django import forms

from .models import Cliente

class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('razonSocial', 'tipoIdentificacion', 'identificacion', 'tipoCliente', 'direccion', 'telefocnoConvencional', 'extension','telefonoCelular','correoElectronico')
        widgets = {
            'direccion': forms.Textarea(attrs={'rows':'3'}),
        }