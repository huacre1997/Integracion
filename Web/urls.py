from django.urls import include, path

from . import views
app_name = 'Web'
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("password_reset/", auth_views.PasswordResetView.as_view(success_url=reverse_lazy("Web:password_reset_done")), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy("Web:password_reset_complete")), name="password_reset_confirm"),
    path("password-reset-complete/",auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('login/', views.LogueoView.as_view(), name='login'),
    path('inicio/', views.HomePageView.as_view(), name='inicio'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('403/', views.Error403.as_view(), name='error403'),
    path("Provincia/",views.ProvinciaComboBox,name="Provincia"),
    path("Distrito/",views.DistritoComboBox,name="Distrito"),
    
    
    
    
    path("reportes/",views.ReportesView.as_view(),name="reportes"),

    
    path("seguridad/",views.SeguridadView.as_view(),name="seguridad"),
    path('seguridad/Personas/', views.PersonaListView.as_view(), name='Personas'),
    path('seguridad/Persona/add', views.PersonaCreateView.as_view(), name='PersonaAdd'),
    path('seguridad/Persona/<int:pk>/', views.PersonaUpdateView.as_view(), name='Persona'),
    path('seguridad/Usuarios/', views.UsuariosListView.as_view(), name='Usuarios'),
    path('seguridad/Usuario/', views.UsuarioCreateView.as_view(), name='Usuario'),
    path('seguridad/Usuario/changepassword/<int:pk>/', views.UsuarioUpdatePasswordView.as_view(), name='UsuarioChangePassword'),
    path('seguridad/Usuario/desactivate/<int:pk>/', views.UsuarioDesactivate, name='UsuarioDesactivate'),
    path('seguridad/Usuario/activate/<int:pk>/', views.UsuarioActivate, name='UsuarioActivate'),
    path('seguridad/Usuario/<int:pk>/', views.UsuarioUpdateView.as_view(), name='Usuario'),
    path('seguridad/Perfiles/', views.PerfilesTemplateView.as_view(), name='Perfiles'),
    path('seguridad/Perfil/', views.PerfilCreateView.as_view(), name='Perfil'),
    path('seguridad/Perfil/<int:pk>/', views.PerfilUpdateView.as_view(), name='Perfil'),
    
    
    path("catalogos/",views.CatalogosView.as_view(),name="catalogos"),
    path('catalogos/Ubicaciones/', views.ListUbicacionesListView.as_view(), name='Ubicaciones'),
    path('catalogos/Ubicacion/', views.UbicacionCreateView.as_view(), name='Ubicacion'),
    path('catalogos/Ubicacion/<int:pk>/', views.UbicacionUpdateView.as_view(), name='Ubicacion'),
    path('catalogos/Ubicacion/<int:pk>/delete/', views.UbicacionDeleteView.as_view(), name='Ubicacion-delete'),

    path('catalogos/almacenes/', views.AlmacenesListView.as_view(), name='almacenes'),
    path('catalogos/almacen/', views.AlmacenCreateView.as_view(), name='almacen'),
    path('catalogos/almacen/<int:pk>/', views.AlmacenUpdateView.as_view(), name='almacen'),
    path('catalogos/almacen/<int:pk>/delete/', views.AlmacenDeleteView.as_view(), name='almacen-delete'),

    path('catalogos/ubicaciones-vehiculos/', views.LugaresListView.as_view(), name='lugares'),
    path('catalogos/ubicacion-vehiculo/', views.LugarCreateView.as_view(), name='lugar'),
    path('catalogos/ubicacion-vehiculo/<int:pk>/', views.LugarUpdateView.as_view(), name='lugar'),
    path('catalogos/ubicacion-vehiculo/<int:pk>/delete/', views.LugarDeleteView.as_view(), name='lugar-delete'),

    path('catalogos/marca-renovaciones/', views.MarcaRenovacionesListView.as_view(), name='marca-renovaciones'),
    path('catalogos/marca-renovacion/', views.MarcaRenovacionCreateView.as_view(), name='marca-renovacion'),
    path('catalogos/marca-renovacion/<int:pk>/', views.MarcaRenovacionUpdateView.as_view(), name='marca-renovacion'),
    path('catalogos/marca-renovacion/<int:pk>/delete/', views.MarcaRenovacionDeleteView.as_view(), name='marca-renovacion-delete'),

    path('catalogos/modelo-renovaciones/', views.ModeloRenovacionesListView.as_view(), name='modelo-renovaciones'),
    path('catalogos/modelo-renovacion/', views.ModeloRenovacionCreateView.as_view(), name='modelo-renovacion'),
    path('catalogos/modelo-renovacion/<int:pk>/', views.ModeloRenovacionUpdateView.as_view(), name='modelo-renovacion'),
    path('catalogos/modelo-renovacion/<int:pk>/delete/', views.ModeloRenovacionDeleteView.as_view(), name='modelo-renovacion-delete'),

    path('catalogos/ancho-banda-renovaciones/', views.AnchoBandaRenovacionesListView.as_view(), name='ancho-banda-renovaciones'),
    path('catalogos/ancho-banda-renovacion/', views.AnchoBandaRenovacionCreateView.as_view(), name='ancho-banda-renovacion'),
    path('catalogos/ancho-banda-renovacion/<int:pk>/', views.AnchoBandaRenovacionUpdateView.as_view(), name='ancho-banda-renovacion'),
    path('catalogos/ancho-banda-renovacion/<int:pk>/delete/', views.AnchoBandaRenovacionDeleteView.as_view(), name='ancho-banda-renovacion-delete'),
    path('catalogos/render-option', views.RenderOption, name="render-option"),

    path('catalogos/marca-llantas/', views.MarcaLlantasListView.as_view(), name='marca-llantas'),
    path('catalogos/marca-llanta/', views.MarcaLlantaCreateView.as_view(), name='marca-llanta'),
    path('catalogos/marca-llanta/<int:pk>/', views.MarcaLlantaUpdateView.as_view(), name='marca-llanta'),
    path('catalogos/marca-llanta/<int:pk>/delete/', views.MarcaLlantaDeleteView.as_view(), name='marca-llanta-delete'),

    path('catalogos/modelo-llantas/', views.ModeloLlantasListView.as_view(), name='modelo-llantas'),
    path('catalogos/modelo-llanta/', views.ModeloLlantaCreateView.as_view(), name='modelo-llanta'),
    path('catalogos/modelo-llanta/<int:pk>/', views.ModeloLlantaUpdateView.as_view(), name='modelo-llanta'),
    path('catalogos/modelo-llanta/<int:pk>/delete/', views.ModeloLlantaDeleteView.as_view(), name='modelo-llanta-delete'),

    path('catalogos/medida-llantas/', views.MedidaLlantasListView.as_view(), name='medida-llantas'),
    path('catalogos/medida-llanta/', views.MedidaLlantaCreateView.as_view(), name='medida-llanta'),
    path('catalogos/medida-llanta/<int:pk>/', views.MedidaLlantaUpdateView.as_view(), name='medida-llanta'),
    path('catalogos/medida-llanta/<int:pk>/delete/', views.MedidaLlantaDeleteView.as_view(), name='medida-llanta-delete'),
    path('catalogos/render-option-llanta', views.RenderOptionLlanta, name="render-option-llanta"),

    # path('estado-llantas/', views.EstadoLlantasListView.as_view(), name='estado-llantas'),
    # path('estado-llanta/', views.EstadoLlantaCreateView.as_view(), name='estado-llanta'),
    # path('estado-llanta/<int:pk>/', views.EstadoLlantaUpdateView.as_view(), name='estado-llanta'),
    # path('estado-llanta/<int:pk>/delete/', views.EstadoLlantaDeleteView.as_view(), name='estado-llanta-delete'),

    path('tipo-servicios/', views.TipoServiciosListView.as_view(), name='tipo-servicios'),
    path('tipo-servicio/', views.TipoServicioCreateView.as_view(), name='tipo-servicio'),
    path('tipo-servicio/<int:pk>/', views.TipoServicioUpdateView.as_view(), name='tipo-servicio'),
    path('tipo-servicio/<int:pk>/delete/', views.TipoServicioDeleteView.as_view(), name='tipo-servicio-delete'),

    path('tipo-pisos/', views.TipoPisosListView.as_view(), name='tipo-pisos'),
    path('tipo-piso/', views.TipoPisoCreateView.as_view(), name='tipo-piso'),
    path('tipo-piso/<int:pk>/', views.TipoPisoUpdateView.as_view(), name='tipo-piso'),
    path('tipo-piso/<int:pk>/delete/', views.TipoPisoDeleteView.as_view(), name='tipo-piso-delete'),

    path('catalogos/marca-vehiculos/', views.MarcaVehiculosListView.as_view(), name='marca-vehiculos'),
    path('catalogos/marca-vehiculo/', views.MarcaVehiculoCreateView.as_view(), name='marca-vehiculo'),
    path('catalogos/marca-vehiculo/<int:pk>/', views.MarcaVehiculoUpdateView.as_view(), name='marca-vehiculo'),
    path('catalogos/marca-vehiculo/<int:pk>/delete/', views.MarcaVehiculoDeleteView.as_view(), name='marca-vehiculo-delete'),

    path('catalogos/modelo-vehiculos/', views.ModeloVehiculosListView.as_view(), name='modelo-vehiculos'),
    path('catalogos/modelo-vehiculo/', views.ModeloVehiculoCreateView.as_view(), name='modelo-vehiculo'),
    path('catalogos/modelo-vehiculo/<int:pk>/', views.ModeloVehiculoUpdateView.as_view(), name='modelo-vehiculo'),
    path('catalogos/modelo-vehiculo/<int:pk>/delete/', views.ModeloVehiculoDeleteView.as_view(), name='modelo-vehiculo-delete'),

    path('catalogos/llantas/',views.LlantasListView.as_view(), name='llantas'),
    path('catalogos/llanta/', views.LlantaCreateView.as_view(), name='llanta'),
    path('catalogos/llanta/<int:pk>/', views.LlantaUpdateView.as_view(), name='llanta'),
    path('catalogos/llanta/<int:pk>/delete/', views.LlantaDeleteView.as_view(), name='llanta-delete'),
    
    path('catalogos/tipo-vehiculos/', views.TipoVehiculosListView.as_view(), name='tipo-vehiculos'),
    path('catalogos/tipo-vehiculo/', views.TipoVehiculoCreateView.as_view(), name='tipo-vehiculo'),
    path('catalogos/tipo-vehiculo/<int:pk>/', views.TipoVehiculoUpdateView.as_view(), name='tipo-vehiculo'),
    path('catalogos/tipo-vehiculo/<int:pk>/delete/', views.TipoVehiculoDeleteView.as_view(), name='tipo-vehiculo-delete'),

    path('catalogos/posiciones/<int:pk>/', views.DetalleTipoVehiculo.as_view(), name='posiciones'),

    path('catalogos/vehiculos/', views.VehiculosListView.as_view(), name='vehiculos'),
    path('catalogos/vehiculo/', views.VehiculoCreateView.as_view(), name='vehiculo'),
    path('catalogos/vehiculo/<int:pk>/', views.VehiculoUpdateView.as_view(), name='vehiculo'),
    path('catalogos/vehiculo/<int:pk>/delete/', views.VehiculoDeleteView.as_view(), name='vehiculo-delete'),
    path('catalogos/render-option-vehiculo', views.RenderOptionVehiculo, name="render-option-vehiculo"),

    path('catalogos/ver-vehiculo/<int:pk>/', views.VerVehiculoView.as_view(), name='ver-vehiculo'),
    path('agregar-llanta/<int:pk>/', views.AgregarLlantaCreateView.as_view(), name='agregar-llanta'),
    path('searchRenovadora/', views.AnchoBandaRenovaSearch, name='search-renovadora'),
    path('viewCondicion/', views.view_condicion, name='view-condicion'),
    path('viewRenova/', views.view_renova, name='view-renova'),
    path('viewLlanta/<int:pk>/', views.DetalleLlantaView.as_view(), name='ver-llanta'),
    path('desmontaje/', views.DesmontajeLlantaView.as_view(), name='ver-desmontaje'),
    path('montaje/', views.MontajeLlantasView.as_view(), name='ver-montaje'),
    path('searchLlanta/', views.LlantaSearch, name='search-llanta'),
    
    path('operaciones/', views.OperacionesView.as_view(), name='operaciones'),

    path('operaciones/hoja-movimientos/', views.HojaDeMovimientosView.as_view(), name='hoja-movimientos'),
    path('operaciones/inspeccion-llantas/', views.InspeccionLlantasView.as_view(), name='inspeccion-llantas'),

    
    path('operaciones/inspeccion-llantas/detalles/<int:pk>/', views.InsepccionDetalleView.as_view(), name='inspeccion-detalle'),
    path('inspeccion-agregar/', views.AgregarInspeccion, name='inspeccion-agregar'),
    path('getTipo/<int:id>/', views.getTipo, name='get-tipo'),

    path('Reportes/historial/', views.HistorialLlantas.as_view(), name='ver-historial'),

    # path('get-vehiculo/', views.getVehiculo, name='ver-vehiculo'),

]

