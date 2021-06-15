# -*- encoding: utf-8 -*-
from django.contrib import admin
from Web.models import *
from django import forms

from django.contrib.auth.models import Permission
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
class PermisosAdmin(admin.ModelAdmin):
	pass
admin.site.register(Permission, PermisosAdmin)
# class EstadoLlantaAdmin(admin.ModelAdmin):
# 	pass
# admin.site.register(EstadoLlanta, EstadoLlantaAdmin)

class TipoPisoAdmin(admin.ModelAdmin):
	pass
admin.site.register(TipoPiso, TipoPisoAdmin)
class UbicacionADmin(admin.ModelAdmin):
	pass
admin.site.register(Ubicacion, UbicacionADmin)
class AlmacenAdmin(admin.ModelAdmin):
	pass
admin.site.register(Almacen, AlmacenAdmin)
class MarcaVehiculoAdmin(admin.ModelAdmin):
	pass
admin.site.register(MarcaVehiculo, MarcaVehiculoAdmin)
class VehiculoAdmin(admin.ModelAdmin):
	pass
admin.site.register(Vehiculo, VehiculoAdmin)
class TipoServicioAdmin(admin.ModelAdmin):
	pass
admin.site.register(TipoServicio, TipoServicioAdmin)
class ModeloVehiculoAdmin(admin.ModelAdmin):
	pass
admin.site.register(ModeloVehiculo, ModeloVehiculoAdmin)
class LlantaAdmin(admin.ModelAdmin):
	pass
admin.site.register(Llanta, LlantaAdmin)
class InspeccionADmin(admin.ModelAdmin):
	pass
admin.site.register(InpeccionLlantas, InspeccionADmin)
class DetalleInspeccionadmin(admin.ModelAdmin):
	pass
admin.site.register(DetalleInspeccion, DetalleInspeccionadmin)
class HistorialAdmin(admin.ModelAdmin):
	pass
admin.site.register(Movimientos_Historial, HistorialAdmin)
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
	pass

admin.site.register(TipoVehiculo, TipoVehiculoAdmin)
class Posiciones(admin.ModelAdmin):
	pass

admin.site.register(PosicionesLlantas, Posiciones)
admin.site.register(CubiertaLlanta)
admin.site.register(Conductor)
admin.site.register(Abastecimiento)
admin.site.register(Ruta)
admin.site.register(Rendimiento)
admin.site.register(DetalleAbastecimiento)
admin.site.register(Estaciones)
admin.site.register(Producto)
admin.site.register(UnidadMedida)
