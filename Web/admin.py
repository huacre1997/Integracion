# -*- encoding: utf-8 -*-
from django.contrib import admin
from Web.models import *
from django import forms


# admin.site.register(User, UserAdmin)

admin.site.register(Persona)



class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(UsuariosForm, self).__init__(*args, **kwargs)
    #     if self.instance: # Editing and existing instance
    #         self.fields['perfil'].queryset = Perfil.objects.filter(aplicacion=APP_GESTION)


class UsuariosAdmin(admin.ModelAdmin):
	# form = UsuariosForm
	# list_display = ('user', ) 
	# search_fields = ('user__username',)
	# fieldsets = (
	# 	(None, {
	# 		'fields': ('user', 'persona' ),
	# 		}),
	# 	)
	# raw_id_fields = ("user", "persona" ) 
	pass
admin.site.register(Usuario, UsuariosAdmin)
class DepartamentoAdmin(admin.ModelAdmin):
	pass
admin.site.register(Departamento, DepartamentoAdmin)

class ProvinciaAdmin(admin.ModelAdmin):
	pass
admin.site.register(Provincia, ProvinciaAdmin)
class DistritoAdmin(admin.ModelAdmin):
	pass
admin.site.register(Distrito, DistritoAdmin)

""""
class PermisoPerfilMenuOpcionAdmin(admin.ModelAdmin):
	#form = UsuariosForm
	model = PermisoPerfilMenuOpcion
	list_display = ('perfil','menu','opcion') # campos que se muestran en el listado en el admin 
	#list_display_links = ('usuario', 'perfil',)
	list_filter = ('perfil',) # filtros
	#ordering = ('-id_persona',)
	search_fields = ('perfil', 'menu', )
	#fieldsets = (
	#	(None, {
	#		'fields': ('usuario', 'perfil','aplicacion','perfil_micpa' ),
	#		}),
	#	)
	#raw_id_fields = ("usuario", ) # para cambia el select por una ventana para escoger 
admin.site.register(PermisoPerfilMenuOpcion, PermisoPerfilMenuOpcionAdmin)
"""


class TipoVehiculoAdmin(admin.ModelAdmin):
	#model = Usuarios
	list_display = ('descripcion','croquis','activo',)
	#list_filter = ('perfil',) # filtros
	#ordering = ('-id_persona',)
	search_fields = ('descripcion',)

admin.site.register(TipoVehiculo, TipoVehiculoAdmin)