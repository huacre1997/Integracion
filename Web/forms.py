#!/usr/bin/env python
# -*- coding: utf8 -*-

from django import forms
from .models import Usuario
from Web.models import *
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.models import Group
from django.conf import settings

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
        'autofocus': 'autofocus',
        'autocapitalize': 'none'
        })
    )
    clave = forms.CharField(widget=forms.TextInput(
        attrs={
        'autofocus': 'autofocus',
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
    def clean_nro_doc(self):
        
        data=self.cleaned_data["nro_doc"]
        if self.instance.nro_doc!=data:
            if Persona.objects.filter(nro_doc=data).exists():
                raise forms.ValidationError(f"El documento {data} ya se encuentra registrado .")
        return data
    
    def clean_celular(self):
        
        data=self.cleaned_data["celular"]
        if self.instance.celular!=data:
            if Persona.objects.filter(celular=data).exists():
                raise forms.ValidationError(f"El celular {data} ya se encuentra registrado .")
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
                        "activo":forms.CheckboxInput(attrs={"class":"form-check-input"})

        }
    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if self.instance.descripcion!=data:
            if Ubicacion.objects.filter(descripcion=data).exists():
                self.add_error("descripcion",f" : La ubicación {data} ya se encuentra registrada .")
        return data  

class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
                        "activo":forms.CheckboxInput(attrs={"class":"form-check-input"})

        }

    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if self.instance.descripcion!=data:
            if Almacen.objects.filter(descripcion=data).exists():
                self.add_error("descripcion",f" : El almacén {data} ya se encuentra registrada .")
        return data  
class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
                        "activo":forms.CheckboxInput(attrs={"class":"form-check-input"})

        }

    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if self.instance.descripcion!=data:
            if Lugar.objects.filter(descripcion=data).exists():
                self.add_error("descripcion",f" : La ubicación {data} ya se encuentra registrada .")
        return data
class MarcaRenovaForm(forms.ModelForm):
    class Meta:
        model = MarcaRenova
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
                                    "activo":forms.CheckboxInput(attrs={"class":"form-check-input"})

        }

    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if self.instance.descripcion!=data:
            if MarcaRenova.objects.filter(descripcion=data).exists():
                self.add_error("descripcion",f" : La marca de renovación {data} ya se encuentra registrada .")
        return data
class ModeloRenovaForm(forms.ModelForm):

    class Meta:
        model = ModeloRenova
        fields = ('descripcion', 'marca_renova',"profundidad" ,'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            'profundidad': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            "activo":forms.CheckboxInput(attrs={"class":"form-check-input"})
        }

    def __init__(self, *args, **kwargs):
        super(ModeloRenovaForm, self).__init__(*args, **kwargs)
    def clean(self):
        subject = self.cleaned_data.get('descripcion')
        subject1 = self.cleaned_data.get('marca_renova')
        if self.instance.descripcion!=subject:
            if ModeloRenova.objects.filter(descripcion=subject,marca_renova=subject1).exists():
                self.add_error("descripcion",f" : La marca {subject1} ya tiene un modelo {subject} .")
        return self.cleaned_data

class AnchoBandaRenovaForm(forms.ModelForm):
  
    class Meta:	
        model = AnchoBandaRenova
        fields = ('descripcion', 'modelo_renova', 'ancho_banda', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            'ancho_banda': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'modelo_renova': forms.Select( attrs={'class':'form-select'}),
            "activo":forms.CheckboxInput(attrs={"class":"form-check-input"})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()

        data=cleaned_data.get("descripcion")
        data2=cleaned_data.get('modelo_renova')
        data3=cleaned_data.get("ancho_banda")

        print(data2)
        if self.instance.descripcion!=data:
            if AnchoBandaRenova.objects.filter(descripcion=data,modelo_renova=data2,ancho_banda=data3).exists():
                self.add_error("ancho_banda",f" : El ancho de banda {data3} ya se encuentra registrado .")
        return self.cleaned_data  


class MarcaLlantaForm(forms.ModelForm):
    class Meta:
        model = MarcaLlanta
        exclude = ["created_by","modified_by"]
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            "activo":forms.CheckboxInput(attrs={"class":"form-check-input"})

        }
    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if self.instance.descripcion!=data:
            if MarcaLlanta.objects.filter(descripcion=data).exists():
                self.add_error("descripcion",f" : La marca {data} ya se encuentra registrada .")
        return data
class TipoVehiculoForm(forms.ModelForm):
    class Meta:
        model = TipoVehiculo
        exclude=["created_by","modified_by","created_at","modified_at","eliminado"]
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            'nro_llantas': forms.NumberInput( attrs={'class':'form-control',"min":"0"}),
            'activo': forms.CheckboxInput ( attrs={'class':'form-check-input'}),
            'max_rep': forms.NumberInput( attrs={'class':'form-control',"min":"0"}),

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].required = True
        self.fields['image'].required = True
        self.fields['image2'].required = True
        self.fields['nro_llantas'].required = True
    def clean(self):
        data=self.cleaned_data.get('descripcion')
        data2=self.cleaned_data.get('nro_llantas')
        print(data2)
        print(data)
        if self.instance.descripcion!=data:
            if TipoVehiculo.objects.filter(descripcion=data,nro_llantas=data2).exists():
                self.add_error("descripcion",f" : El tipo de vehiculo {data} ya se encuentra registrado .")
        return self.cleaned_data
class ModeloLlantaForm(forms.ModelForm):

    class Meta:
        model = ModeloLlanta
        fields = ('descripcion', 'marca_llanta', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        subject = self.cleaned_data.get('descripcion')
        subject1 = self.cleaned_data.get('marca_llanta')
        if self.instance.descripcion!=subject:
            if ModeloLlanta.objects.filter(descripcion=subject,marca_llanta=subject1).exists():
                self.add_error("descripcion",f" : La marca {subject1} ya tiene una modelo {subject} .")
        return self.cleaned_data
class MedidaLlantaForm(forms.ModelForm):
 
    
    class Meta:	
        model = MedidaLlanta
        fields = ('modelo_llanta', 'medida','profundidad','capas', 'activo')
        widgets = {
            # 'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            'medida': forms.TextInput( attrs={'class':'form-control'}),
            'profundidad': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'capas': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'modelo_llanta': forms.Select( attrs={'class':'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def clean(self):
        subject = self.cleaned_data.get('medida')
        subject1 = self.cleaned_data.get('modelo_llanta')
        if self.instance.medida!=subject:
            if MedidaLlanta.objects.filter(medida=subject,modelo_llanta=subject1).exists():
                self.add_error("medida",f" : La medida {subject1} ya tiene una modelo {subject} .")
        return self.cleaned_data   
# class EstadoLlantaForm(forms.ModelForm):
#     class Meta:
#         model = EstadoLlanta
#         fields = ('descripcion', 'activo')
#         widgets = {
#             'descripcion': forms.TextInput( attrs={'class':'form-control'}),
#         }
#     def clean_descripcion(self):
#         data=self.cleaned_data["descripcion"]
#         if self.instance.descripcion!=data:
#             if EstadoLlanta.objects.filter(descripcion=data).exists():
#                 self.add_error("descripcion",f" : El estado {data} ya se encuentra registrado .")
#         return data

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
        if self.instance.descripcion!=data:

            if TipoPiso.objects.filter(descripcion=data).exists():
                self.add_error("descripcion",f" : El piso {data} ya se encuentra registrado .")
        return data
class MarcaVehiculoForm(forms.ModelForm):
    class Meta:
        model = MarcaVehiculo
        fields = ('descripcion', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            "activo":forms.CheckboxInput(attrs={"class":"form-check-input"})
        }

    def clean_descripcion(self):
        data=self.cleaned_data["descripcion"]
        if self.instance.descripcion!=data:
            if MarcaVehiculo.objects.filter(descripcion=data).exists():
                self.add_error("descripcion",f" : La marca de vehículo {data} ya se encuentra registrada .")
        return data
class ModeloVehiculoForm(forms.ModelForm):

    class Meta:
        model = ModeloVehiculo
        fields = ('descripcion', 'marca_vehiculo', 'activo')
        widgets = {
            'descripcion': forms.TextInput( attrs={'class':'form-control'}),
            "activo":forms.CheckboxInput(attrs={"class":"form-check-input"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
     
    def clean(self):
        data=self.cleaned_data.get("descripcion")
        data2=self.cleaned_data.get("marca_vehiculo")
        if self.instance.descripcion!=data:

            if ModeloVehiculo.objects.filter(descripcion=data,marca_vehiculo=data2).exists():
                self.add_error("descripcion",f" : La marca {data2} ya tiene registrado un modelo {data} .")
        return self.cleaned_data

class CubiertaForm(forms.ModelForm):
    class Meta:
        model=CubiertaLlanta
        exclude=["created_by","modified_by","created_at","modified_at","eliminado"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })
    def clean(self):
        subject = self.cleaned_data.get('llanta')
        subject1 = self.cleaned_data.get('nro_ren')
        
        if self.instance.nro_ren!=subject1:
            print("if")
            if CubiertaLlanta.objects.filter(nro_ren=subject1,llanta=subject).exists():
                print("if2")
                self.add_error("nro_ren",f" : Ya se ingresó el reencauche {subject1} del neumático {subject}.")
        if int(subject1)>6:
            self.add_error("nro_ren",f" : Ingrese un número de reencauche menor a 7")
        return self.cleaned_data   
    # def clean_categoria(self):
    #     data=self.cleaned_data["categoria"]
    #     if data=="2":  
    #         self.fields['renovadora'].required = True
    #         self.fields['ancho_banda'].required = True
    #         self.fields['modelo_renova'].required =True
    #         self.fields['nro_ren'].required =True
    #     return data

class LlantaForm(forms.ModelForm):
 
 

    repuesto = forms.BooleanField(initial=False, required=False)

    class Meta:	
        model = Llanta
        exclude=["ubicacion","posicion","vehiculo","created_by","modified_by","created_at","modified_at","eliminado"]
        widgets = {
            'modelo_llanta': forms.Select( attrs={'class':'form-select'}),
            'medida_llanta': forms.Select( attrs={'class':'form-select'}),
            'costo': forms.NumberInput( attrs={'class':'form-control'}),
            'codigo': forms.NumberInput( attrs={'class':'form-control'}),
            'estado': forms.Select( attrs={'class':'form-select'}),
            'fech_ren': forms.DateInput(format=('%Y-%m-%d'), attrs={ 'type':'date','class':'form-control'}),
            'a_inicial': forms.NumberInput( attrs={'class':'form-control'}),
            'a_final': forms.NumberInput( attrs={'class':'form-control'}),

        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['codigo'].required = True
            # self.fields['ubicacion'].required = True

    # def clean_ubicacion(self):
    #     data=self.cleaned_data["ubicacion"]
    #     if data!=None:
    #         if data.descripcion=="MONTADO" :
    #             print("aaea")
    #             self.fields['vehiculo'].required = True

    #             self.fields['posicion'].required = True
    #     else:
    #         self.add_error("ubicacion",f" : Este campo es requerido.")
  
    #     return data
    # def clean_vehiculo(self):
    #     data=self.cleaned_data["vehiculo"]
    #     if data.id!=None:
    #         self.fields['posicion'].required = True

    # def clean(self):
    #     if self.cleaned_data['ubicacion']!=None:
    #         if self.cleaned_data['ubicacion'].descripcion=="MONTADO":
    #             print("Entro al if")
    #             subject = self.cleaned_data.get('posicion')
    #             subject1 = self.cleaned_data.get('vehiculo')
    #             repuesto = self.cleaned_data.get('repuesto')

    #             if self.instance.posicion!=subject:
    #                 dataLlanta=Llanta.objects.filter(vehiculo=subject1,posicion=subject)
                
    #                 if dataLlanta.exists():
    #                     self.add_error("posicion",f"El vehiculo {subject1} ya tiene asiganada un neumático en la posición {subject} .")
                
    #                 else:

    #                     data=Vehiculo.objects.get(pk=subject1.id)
    #                     nrollantas=data.tipo_vehiculo.nro_llantas
    #                     nrorepuesto=data.tipo_vehiculo.max_rep
    #                     total=int(nrollantas)+int(nrorepuesto)
    #                     print(total)
    #                     if repuesto:
    #                         a=""
    #                         for i in range(nrollantas,total):
    #                             a+=str(i+1)+" "
    #                         if not (subject<=int(total) and subject>int(nrollantas)):
    #                             print("repuesto")
    #                             self.add_error("posicion",f"Este neumático de repuesto solo puede ocupar las posiciones {a}.")

    #                     else:
    #                         print("else")
    #                         if subject > total :
    #                             self.add_error("posicion",f"El vehiculo {subject1} no puede tener mas de {total} neumáticos totales.")
    #                         elif subject > nrollantas :
    #                             self.add_error("posicion",f"El vehiculo {subject1} solo tiene {nrollantas} neumáticos.")
                        
                        
    #         return self.cleaned_data
    
    
    def clean_codigo(self):
        data=self.cleaned_data["codigo"]
        if data!=None:
            if self.instance.codigo!=data:
                if Llanta.objects.filter(codigo=data).exists():
                    self.add_error("codigo",f" : El código {data} ya se encuentra registrado .")
        else:
            self.add_error("codigo",f" : Este campo es requerido.")

        return data
class VehiculoForm(forms.ModelForm):

    class Meta:	
        model = Vehiculo
        exclude=["nro_ejes","vehiculo","eliminado","modified_at","created_at","modified_by"]

        widgets = {
            'ano': forms.TextInput( attrs={'class':'form-control','type':'number', 'step':'1'}),
            'modelo_vehiculo': forms.Select( attrs={'class':'form-control'}),
            'tipo_vehiculo': forms.Select( attrs={'class':'form-control'}),
            'propiedad': forms.TextInput( attrs={'class':'form-control'}),
            'placa': forms.TextInput( attrs={'class':'form-control',"maxlength":"8"}),
            'operacion': forms.TextInput( attrs={'class':'form-control'}),
            'nro_chasis': forms.TextInput( attrs={'class':'form-control'}),
            'nro_motor': forms.TextInput( attrs={'class':'form-control'}),

            'km': forms.TextInput( attrs={'class':'form-control','type':'number', 'min':'0', 'step':'0.01'}),
            'obs': forms.Textarea( attrs={'class':'form-control',"cols":"3","rows":"2"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_vehiculo'].queryset = TipoVehiculo.objects.filter(eliminado=False,activo=True)
        self.fields['obs'].required = False
    def clean(self):
        subject = self.cleaned_data.get('placa')
        subject1 = self.cleaned_data.get('tipo_vehiculo')
        m=Llanta.objects.filter(vehiculo__placa=subject)
        if self.instance.tipo_vehiculo_id!=None:
            if self.instance.tipo_vehiculo!=subject1:
                if m.exists():
                    self.add_error("tipo_vehiculo",f" : Desmonte todas los neumáticos antes de cambiar la configuración vehicular .")
        return self.cleaned_data
        
    def clean_placa(self):
        data=self.cleaned_data["placa"]
        
        if self.instance.placa!=data:
            if Vehiculo.objects.filter(placa=data).exists():
                self.add_error("placa",f" : La placa {data} ya se encuentra registrada .")
        return data
   
class InspeccionForm(forms.ModelForm):

    tecnico = forms.ModelChoiceField(queryset=Usuario.objects.filter(groups__name="Técnico"),empty_label="Seleccione técnico..",
                                     widget=forms.Select( attrs={'class':'form-select'}))

    class Meta:	
        model = InpeccionLlantas
        exclude=["vehiculo","eliminado","modified_at","created_at","modified_by"]
        widgets = {
            'operacion': forms.Select( attrs={'class':'form-control'}),
        }
