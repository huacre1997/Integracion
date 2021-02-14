#!/usr/bin/env python
# -*- coding: utf8 -*-

from django import forms
from .models import Usuario
from Web.models import (Persona, Usuario, Ubicacion, ModeloRenova,
    MarcaRenova, AnchoBandaRenova, MarcaLlanta, ModeloLlanta, MedidaLlanta,
    Almacen, Lugar, EstadoLlanta, TipoServicio, TipoPiso, MarcaVehiculo, ModeloVehiculo, Vehiculo,
    Llanta, TipoVehiculo,Departamento,Provincia,Distrito)
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.models import Group

from django import forms
from django.contrib.auth.forms import  PasswordResetForm, SetPasswordForm


class UserPasswordResetForm(SetPasswordForm):
    """Change password form."""
    new_password1 = forms.CharField(label='Password',
        help_text="<ul class='errorlist text-muted'><li>Your password can 't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can 't be a commonly used password.</li> <li>Your password can 't be entirely numeric.<li></ul>",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'type': 'password',
            'id': 'user_password',
        }))

    new_password2 = forms.CharField(label='Confirm password',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'confirm password',
            'type': 'password',
            'id': 'user_password',
        }))


class UserForgotPasswordForm(PasswordResetForm):
    """User forgot password, check via email form."""
    email = forms.EmailField(label='Email address',
        max_length=254,
        required=True,
        widget=forms.TextInput(
        attrs={'class': 'form-control',
                'placeholder': 'email address',
                'type': 'text',
                'id': 'email_address'
                }
        ))
class LoginForm(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(
        attrs={
        'class': 'form-control form-control-user',
        'autofocus': 'autofocus',
        'placeholder': 'Nombre de usuario',
        'autocapitalize': 'none'
        })
    )
    clave = forms.CharField(widget=forms.TextInput(
        attrs={
        'class': 'form-control form-control-user',
        'autofocus': 'autofocus',
        'placeholder': 'Clave',
        'autocapitalize': 'none',
        'type': 'password'
        })
    )

    def clean_usuario(self):
        # import ipdb; ipdb.set_trace()
        data = self.cleaned_data['usuario']
        if data is None:
            raise forms.ValidationError("Debe Ingresar un usuario")
        return data


class PersonaForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), empty_label="Seleccione departamento...")

    class Meta:
        model = Persona
        exclude = ["uuid","created_at","modified_at","created_by","modified_by","eliminado","uuid"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })
       
    
class CalendarWidget(forms.TextInput):
    class Media:
        js = ('jQuery.js', 'calendar.js', 'noConflict.js',
              'SelectFilter2.js', 'SelectBox.js')


class UserGroupForm(forms.ModelForm):
    
    class Media:
        css = {
                'all': ('/static/admin/css/widgets.css',),
            }
        js = ('/admin/jsi18n',)    
    class Meta:
        
        model = Group
        fields = '__all__'
      
    

# class UserForm(forms.ModelForm):
# 	# password2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'password'	}))
    
# 	class Meta:
# 		model = Usuario
# 		fields = ('username', 'password', 'email',"password2")
# 		widgets = {
# 			'username': forms.TextInput( attrs={'class':'form-control'}),
# 			'password': forms.TextInput( attrs={'class':'form-control', 'type':'password'}),
# 			'email': forms.TextInput( attrs={'class':'form-control','type':'email'}),
# 		}


class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ["username","password","groups","persona"]
        # widgets = {
        # 	'perfil': forms.SelectMultiple( attrs={'class':'selectpicker',}),
        # }
        widgets = {
                'password':forms.PasswordInput(render_value=True, attrs={
                
                    "placeholder": "Contraseña",
                    'class': 'form-control',
                }),
                'password2':forms.PasswordInput(render_value=True, attrs={
                
                    "placeholder": "Contraseña",
                    'class': 'form-control',
                }),
                'username':forms.TextInput(attrs={
                
                    "placeholder": "Usuario",
                    'class': 'form-control',
                }),
                'groups': FilteredSelectMultiple("Permission", False, attrs={'class':'form-control'}),
            }


    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                print("us")
                passwd=self.cleaned_data["password"]
                print(passwd)
                u = form.save(commit=False)
                if u.pk is None:
                    print("entro al if")
                    u.set_password(passwd)
                else:
                    user = User.objects.get(pk=u.pk) 
                    if user.password != passwd:
                       u.set_password(passwd)
                u.save()
                self.save_m2m()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
            


# class UsuarioMultiForm(MultiModelForm):
#     form_classes = {
#         'persona': PersonaForm,
#         # 'user': UserForm,
#         'usuario': UsuarioForm
#     }


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }


class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }


class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }


class MarcaRenovaForm(forms.ModelForm):
    class Meta:
        model = MarcaRenova
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }


class ModeloRenovaForm(forms.ModelForm):

    class Meta:
        model = ModeloRenova
        fields = ('descripcion', 'marca_renova', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            'marca_renova': forms.Select( attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ModeloRenovaForm, self).__init__(*args, **kwargs)
        self.fields['marca_renova'].queryset = MarcaRenova.objects.filter(eliminado=False)


class AnchoBandaRenovaForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=MarcaRenova.objects.filter(eliminado=0),
        widget=forms.Select( attrs={'class':'form-control', 'onchange':'actualizar_modelo();'}) )
    
    class Meta:	
        model = AnchoBandaRenova
        fields = ('descripcion', 'modelo_renova', 'ancho_banda', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            'ancho_banda': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'modelo_renova': forms.Select( attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modelo_renova'].queryset = ModeloRenova.objects.filter(eliminado=False)
    


class MarcaLlantaForm(forms.ModelForm):
    class Meta:
        model = MarcaLlanta
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }


class ModeloLlantaForm(forms.ModelForm):

    class Meta:
        model = ModeloLlanta
        fields = ('descripcion', 'marca_llanta', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            'marca_llanta': forms.Select( attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['marca_llanta'].queryset = MarcaLlanta.objects.filter(eliminado=False)


class MedidaLlantaForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=MarcaLlanta.objects.filter(eliminado=0),
        widget=forms.Select( attrs={'class':'form-control', 'onchange':'actualizar_modelo();'}) )
    
    class Meta:	
        model = MedidaLlanta
        fields = ('modelo_llanta', 'medida','profundidad','capas', 'activo')
        widgets = {
            # 'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            'medida': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'profundidad': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'capas': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'modelo_llanta': forms.Select( attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modelo_llanta'].queryset = ModeloLlanta.objects.filter(eliminado=False)


class EstadoLlantaForm(forms.ModelForm):
    class Meta:
        model = EstadoLlanta
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }


class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }


class TipoPisoForm(forms.ModelForm):
    class Meta:
        model = TipoPiso
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }


class MarcaVehiculoForm(forms.ModelForm):
    class Meta:
        model = MarcaVehiculo
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }


class ModeloVehiculoForm(forms.ModelForm):

    class Meta:
        model = ModeloVehiculo
        fields = ('descripcion', 'marca_vehiculo', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            'marca_vehiculo': forms.Select( attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['marca_vehiculo'].queryset = MarcaVehiculo.objects.filter(eliminado=False)


class LlantaForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=MarcaLlanta.objects.filter(eliminado=0), required=True,
        widget=forms.Select( attrs={'class':'form-control', 'onchange':'actualizar_modelo();'}) )
    
    class Meta:	
        model = Llanta
        fields = ('vehiculo', 'modelo_llanta','ubicacion','almacen', 'estado', 'costo', 'km','obs', 'medida_llanta')
        widgets = {
            'vehiculo': forms.Select(attrs={'class':'form-control'}),
            'modelo_llanta': forms.Select( attrs={'class':'form-control'}),
            'medida_llanta': forms.Select( attrs={'class':'form-control'}),
            'ubicacion': forms.Select( attrs={'class':'form-control'}),
            'almacen': forms.Select( attrs={'class':'form-control'}),
            'estado': forms.Select( attrs={'class':'form-control'}),
            'costo': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'km': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'obs': forms.Textarea( attrs={'class':'form-control','rows':'3',}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(eliminado=False)
        self.fields['vehiculo'].required = False
        self.fields['modelo_llanta'].queryset = ModeloLlanta.objects.filter(eliminado=False)
        self.fields['medida_llanta'].queryset = MedidaLlanta.objects.filter(eliminado=False)
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(eliminado=False)
        self.fields['almacen'].queryset = Almacen.objects.filter(eliminado=False)
        self.fields['almacen'].required = False
        self.fields['obs'].required = False


class VehiculoForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=MarcaVehiculo.objects.filter(eliminado=0), required=True,
        widget=forms.Select( attrs={'class':'form-control', 'onchange':'actualizar_modelo();'}) )
    
    class Meta:	
        model = Vehiculo
        fields = ('ano','modelo_vehiculo','tipo_vehiculo','propiedad','placa',
            'operacion','km','nro_llantas','nro_llantas_repuesto','obs', 'ubicacion', 'almacen' )
        widgets = {
            'ano': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'1950', 'step':'1'}),
            'modelo_vehiculo': forms.Select( attrs={'class':'form-control'}),
            'tipo_vehiculo': forms.Select( attrs={'class':'form-control'}),
            'propiedad': forms.TextInput( attrs={'class':'form-control'}),
            'placa': forms.TextInput( attrs={'class':'form-control'}),
            'ubicacion': forms.Select( attrs={'class':'form-control'}),
            'almacen': forms.Select( attrs={'class':'form-control'}),
            'operacion': forms.TextInput( attrs={'class':'form-control'}),
            'km': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'nro_llantas': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'1'}),
            'nro_llantas_repuesto': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'1'}),
            'obs': forms.Textarea( attrs={'class':'form-control','rows':'3',}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modelo_vehiculo'].queryset = ModeloVehiculo.objects.filter(eliminado=False)
        self.fields['tipo_vehiculo'].queryset = TipoVehiculo.objects.filter(eliminado=False)
        self.fields['obs'].required = False
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(eliminado=False)
        self.fields['almacen'].queryset = Almacen.objects.filter(eliminado=False)
        self.fields['almacen'].required = False
        self.fields['nro_llantas_repuesto'].required = False
