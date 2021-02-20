#!/usr/bin/env python
# -*- coding: utf8 -*-

from django import forms
from .models import Usuario
from Web.models import (Persona, Usuario, Ubicacion, ModeloRenova,
    MarcaRenova, AnchoBandaRenova, MarcaLlanta, ModeloLlanta, MedidaLlanta,
    Almacen, Lugar, EstadoLlanta, TipoServicio, TipoPiso, MarcaVehiculo, ModeloVehiculo, Vehiculo,
    Llanta, TipoVehiculo,Departamento,Provincia,Distrito,CubiertaLlanta)
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.models import Group

from django import forms
from django.contrib.auth.forms import  PasswordResetForm, SetPasswordForm


class UserPasswordResetForm(SetPasswordForm):
    class Meta:
        model = Usuario
        fields="__all__"   
    def __init__(self,user,*args, **kwargs):

        self.user = user
     
       
       
        super(UserPasswordResetForm, self).__init__(user,*args, **kwargs)

    
    def clean(self):
        cleaned_data = super(UserPasswordResetForm,self).clean()

        n_pass = cleaned_data.get("new_pass")
        r_pass = cleaned_data.get("new_pass_repeat")
       
        if r_pass != n_pass:
            raise ValidationError("Las contraseñas no coinciden.")

   
        return self.cleaned_data
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
       
        self.fields['correo'].required = True
        self.fields['nom'].required = True
        self.fields['celular'].required = True
        self.fields['apep'].required = True
        self.fields['apem'].required = True
        self.fields['fech_inicio'].required =True
        self.fields['fech_fin'].required = True
        self.fields['direccion'].required =True
        self.fields['provincia'].required = True
        self.fields['distrito'].required = True

        self.fields['area'].required =True
        self.fields['cargo'].required =True
    def clean_correo(self):
        
        data=self.cleaned_data["correo"]
        if self.instance.correo!=data:
            if Persona.objects.filter(correo=data).exists():
                raise forms.ValidationError(f"El correo {data} ya se encuentra registrado .")
        return data
class CalendarWidget(forms.TextInput):
    class Media:
        js = ('jQuery.js', 'calendar.js', 'noConflict.js',
              'SelectFilter2.js', 'SelectBox.js')


class UserGroupForm(forms.ModelForm):
    
   
    class Meta:
        
        model = Group
        fields = '__all__'
      
        widgets = {
            
                'permissions': FilteredSelectMultiple("Permission", False,  attrs={'rows':'10'}),}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })
                 
    def clean_permissions(self):
        data=self.cleaned_data["permissions"]
        if not data:
            raise forms.ValidationError("Debe asignar al menos un permiso.")
        return data
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

from django.utils.translation import gettext_lazy as _

class UsuarioForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirmar contraseña',
       
        widget=forms.PasswordInput(
        attrs={
            
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'type': 'password',
            'id': 'id_password2',
        }))

    class Meta:
        model = Usuario
        fields = ["username","password","groups","persona"]
        # widgets = {
        # 	'perfil': forms.SelectMultiple( attrs={'class':'selectpicker',}),
        # }
        error_messages = {
            'persona': {
                'unique': _("Esta Persona ya tiene asignada un Usuario"),
            },
        }
        widgets = {
                'password':forms.PasswordInput(render_value=True, attrs={
                
                    'class': 'form-control',
                }),
             
                'username':forms.TextInput(attrs={
                
                    "placeholder": "Usuario",
                    'class': 'form-control',
                }),
                'groups': FilteredSelectMultiple("Permission", False,  attrs={'rows':'10'}),
                'persona': forms.Select(attrs={'class': 'form-select'}),

            }
    def clean_password2(self):
        data=self.cleaned_data["password2"]
        data2=self.cleaned_data["password"]
        if data!=data2:
            raise forms.ValidationError("Las constraseñas deben coincidir.")

        return data    
    def clean_groups(self):
        data=self.cleaned_data["groups"]
        if not data:
            raise forms.ValidationError("Debe asignar al menos un permiso.")

        return data    
    def clean_persona(self):
        data=self.cleaned_data["persona"]
        if data=="":
            raise forms.ValidationError("Este campo es obligatorio.")

        return data 
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                passwd=self.cleaned_data["password"]
                u = form.save(commit=False)
                if u.pk is None:
                    print("if")
                    u.set_password(passwd)
                    if("Administrador" in [i.name for i in self.cleaned_data["groups"]]):
                        u.is_staff=True
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
            print(e)
        return data
            
class  UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username","groups"]
        # widgets = {
        # 	'perfil': forms.SelectMultiple( attrs={'class':'selectpicker',}),
        # }
      
        widgets = {
              
                'groups': FilteredSelectMultiple("Permission", False,  attrs={'rows':'10'}),

            }
    def clean_groups(self):
        data=self.cleaned_data["groups"]
        if not data:
            raise forms.ValidationError("Debe asignar al menos un permiso.")

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
        fields = ["descripcion"]
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }
    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if self.instance.descripcion!=data:
            if MarcaLlanta.objects.filter(descripcion=data).exists():
                raise forms.ValidationError(f"La marca {data} ya se encuentra registrada .")
        return data
class TipoVehiculoForm(forms.ModelForm):
    class Meta:
        model = TipoVehiculo
        fields = ('descripcion', "croquis",'activo')
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

    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if TipoPiso.objects.filter(descripcion=data).exists():
            raise forms.ValidationError(f"El piso {data} ya se encuentra registrada .")
        return data
class MarcaVehiculoForm(forms.ModelForm):
    class Meta:
        model = MarcaVehiculo
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }

    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if MarcaLlanta.objects.filter(descripcion=data).exists():
            raise forms.ValidationError(f"La marca {data} ya se encuentra registrada .")
        return data
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
    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if MarcaLlanta.objects.filter(descripcion=data).exists():
            raise forms.ValidationError(f"El modelo {data} ya se encuentra registrada .")
        return data
class CubiertaForm(forms.ModelForm):
    class Meta:
        model=CubiertaLlanta
        exclude=["created_by","modified_by","created_at","modified_at","eliminado"]
        widgets = {
                'password':forms.PasswordInput(render_value=True, attrs={
                
                    'class': 'form-control',
                }),
             
                'username':forms.TextInput(attrs={
                
                    "placeholder": "Usuario",
                    'class': 'form-control',
                }),
        'fech_ren': forms.DateInput(format=('%Y-%m-%d'), attrs={ 'type':'date'}),
                'ancho_banda': forms.Select(attrs={'class': 'form-select'}),
                'categoria': forms.Select(attrs={'class': 'form-select'}),

                'modelo_renova': forms.Select(attrs={'class': 'form-select'}),

            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })
    def clean_categoria(self):
        data=self.cleaned_data["categoria"]
        if data=="2":  
            self.fields['renovadora'].required = True
            self.fields['ancho_banda'].required = True
            self.fields['modelo_renova'].required =True
            self.fields['nro_ren'].required =True
        return data

class LlantaForm(forms.ModelForm):
    marca_llanta = forms.ModelChoiceField(queryset=MarcaLlanta.objects.filter(eliminado=0), required=True,
        widget=forms.Select( attrs={'class':'form-select', 'onchange':'actualizar_modelo();'}) )
    estado = forms.ModelChoiceField(queryset=EstadoLlanta.objects.filter(eliminado=0), required=True,
        widget=forms.Select( attrs={'class':'form-select'}) )
    class Meta:	
        model = Llanta
        fields = ('vehiculo', 'modelo_llanta','ubicacion','almacen', 'estado','obs', 'medida_llanta',"codigo","posicion","acciones","marca_llanta")
        widgets = {
            'vehiculo': forms.Select(attrs={'class':'form-select'}),
            'modelo_llanta': forms.Select( attrs={'class':'form-select'}),
            'medida_llanta': forms.Select( attrs={'class':'form-select'}),
            'ubicacion': forms.Select( attrs={'class':'form-control'}),
            'almacen': forms.Select( attrs={'class':'form-control'}),
            'codigo': forms.TextInput( attrs={'class':'form-control'}),
            'posicion': forms.TextInput( attrs={'class':'form-control'}),
            'obs': forms.Select( attrs={'class':'form-select'}),
            'acciones': forms.Select( attrs={'class':'form-select'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(eliminado=False)
        self.fields['vehiculo'].required = True
        self.fields['modelo_llanta'].queryset = ModeloLlanta.objects.filter(eliminado=False)
        self.fields['medida_llanta'].queryset = MedidaLlanta.objects.filter(eliminado=False)
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(eliminado=False)
        self.fields['almacen'].queryset = Almacen.objects.filter(eliminado=False)
        self.fields['almacen'].required = False
        self.fields['codigo'].required = True
        self.fields['posicion'].required = True

        self.fields['obs'].required = True
    # def clean_posicion(self):
    #     data=self.cleaned_data["posicion"]
    #     auto=self.cleaned_data["vehiculo"]
        
    #     obj=Vehiculo.objects.get(id=auto)
    #     obj.nro_llantas
        
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
