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
    # path('select_perfil/', views.SelectPerfilTemplateView.as_view(), name='select_perfil'),
    path('Personas/', views.PersonaListView.as_view(), name='Personas'),
    path('Persona/add', views.PersonaCreateView.as_view(), name='PersonaAdd'),
    path('Persona/<int:pk>/', views.PersonaUpdateView.as_view(), name='Persona'),
    path("Provincia/",views.ProvinciaComboBox,name="Provincia"),
    path("Distrito/",views.DistritoComboBox,name="Distrito"),
    path('Usuarios/', views.UsuariosListView.as_view(), name='Usuarios'),
    path('Usuario/', views.UsuarioCreateView.as_view(), name='Usuario'),
    path('Usuario/changepassword/<int:pk>/', views.UsuarioUpdatePasswordView.as_view(), name='UsuarioChangePassword'),
    path('Usuario/desactivate/<int:pk>/', views.UsuarioDesactivate, name='UsuarioDesactivate'),
    path('Usuario/activate/<int:pk>/', views.UsuarioActivate, name='UsuarioActivate'),
    path('Usuario/<int:pk>/', views.UsuarioUpdateView.as_view(), name='Usuario'),

    path('Perfiles/', views.PerfilesTemplateView.as_view(), name='Perfiles'),
    path('Perfil/', views.PerfilCreateView.as_view(), name='Perfil'),
    path('Perfil/<int:pk>/', views.PerfilUpdateView.as_view(), name='Perfil'),

    path('Ubicaciones/', views.ListUbicacionesListView.as_view(), name='Ubicaciones'),
    path('Ubicacion/', views.UbicacionCreateView.as_view(), name='Ubicacion'),
    path('Ubicacion/<int:pk>/', views.UbicacionUpdateView.as_view(), name='Ubicacion'),
    path('Ubicacion/<int:pk>/delete/', views.UbicacionDeleteView.as_view(), name='Ubicacion-delete'),

    path('almacenes/', views.AlmacenesListView.as_view(), name='almacenes'),
    path('almacen/', views.AlmacenCreateView.as_view(), name='almacen'),
    path('almacen/<int:pk>/', views.AlmacenUpdateView.as_view(), name='almacen'),
    path('almacen/<int:pk>/delete/', views.AlmacenDeleteView.as_view(), name='almacen-delete'),

    path('ubicaciones-vehiculos/', views.LugaresListView.as_view(), name='lugares'),
    path('ubicacion-vehiculo/', views.LugarCreateView.as_view(), name='lugar'),
    path('ubicacion-vehiculo/<int:pk>/', views.LugarUpdateView.as_view(), name='lugar'),
    path('ubicacion-vehiculo/<int:pk>/delete/', views.LugarDeleteView.as_view(), name='lugar-delete'),

    path('marca-renovaciones/', views.MarcaRenovacionesListView.as_view(), name='marca-renovaciones'),
    path('marca-renovacion/', views.MarcaRenovacionCreateView.as_view(), name='marca-renovacion'),
    path('marca-renovacion/<int:pk>/', views.MarcaRenovacionUpdateView.as_view(), name='marca-renovacion'),
    path('marca-renovacion/<int:pk>/delete/', views.MarcaRenovacionDeleteView.as_view(), name='marca-renovacion-delete'),

    path('modelo-renovaciones/', views.ModeloRenovacionesListView.as_view(), name='modelo-renovaciones'),
    path('modelo-renovacion/', views.ModeloRenovacionCreateView.as_view(), name='modelo-renovacion'),
    path('modelo-renovacion/<int:pk>/', views.ModeloRenovacionUpdateView.as_view(), name='modelo-renovacion'),
    path('modelo-renovacion/<int:pk>/delete/', views.ModeloRenovacionDeleteView.as_view(), name='modelo-renovacion-delete'),

    path('ancho-banda-renovaciones/', views.AnchoBandaRenovacionesListView.as_view(), name='ancho-banda-renovaciones'),
    path('ancho-banda-renovacion/', views.AnchoBandaRenovacionCreateView.as_view(), name='ancho-banda-renovacion'),
    path('ancho-banda-renovacion/<int:pk>/', views.AnchoBandaRenovacionUpdateView.as_view(), name='ancho-banda-renovacion'),
    path('ancho-banda-renovacion/<int:pk>/delete/', views.AnchoBandaRenovacionDeleteView.as_view(), name='ancho-banda-renovacion-delete'),
    path('render-option', views.RenderOption, name="render-option"),

    path('marca-llantas/', views.MarcaLlantasListView.as_view(), name='marca-llantas'),
    path('marca-llanta/', views.MarcaLlantaCreateView.as_view(), name='marca-llanta'),
    path('marca-llanta/<int:pk>/', views.MarcaLlantaUpdateView.as_view(), name='marca-llanta'),
    path('marca-llanta/<int:pk>/delete/', views.MarcaLlantaDeleteView.as_view(), name='marca-llanta-delete'),

    path('modelo-llantas/', views.ModeloLlantasListView.as_view(), name='modelo-llantas'),
    path('modelo-llanta/', views.ModeloLlantaCreateView.as_view(), name='modelo-llanta'),
    path('modelo-llanta/<int:pk>/', views.ModeloLlantaUpdateView.as_view(), name='modelo-llanta'),
    path('modelo-llanta/<int:pk>/delete/', views.ModeloLlantaDeleteView.as_view(), name='modelo-llanta-delete'),

    path('medida-llantas/', views.MedidaLlantasListView.as_view(), name='medida-llantas'),
    path('medida-llanta/', views.MedidaLlantaCreateView.as_view(), name='medida-llanta'),
    path('medida-llanta/<int:pk>/', views.MedidaLlantaUpdateView.as_view(), name='medida-llanta'),
    path('medida-llanta/<int:pk>/delete/', views.MedidaLlantaDeleteView.as_view(), name='medida-llanta-delete'),
    path('render-option-llanta', views.RenderOptionLlanta, name="render-option-llanta"),

    path('estado-llantas/', views.EstadoLlantasListView.as_view(), name='estado-llantas'),
    path('estado-llanta/', views.EstadoLlantaCreateView.as_view(), name='estado-llanta'),
    path('estado-llanta/<int:pk>/', views.EstadoLlantaUpdateView.as_view(), name='estado-llanta'),
    path('estado-llanta/<int:pk>/delete/', views.EstadoLlantaDeleteView.as_view(), name='estado-llanta-delete'),

    path('tipo-servicios/', views.TipoServiciosListView.as_view(), name='tipo-servicios'),
    path('tipo-servicio/', views.TipoServicioCreateView.as_view(), name='tipo-servicio'),
    path('tipo-servicio/<int:pk>/', views.TipoServicioUpdateView.as_view(), name='tipo-servicio'),
    path('tipo-servicio/<int:pk>/delete/', views.TipoServicioDeleteView.as_view(), name='tipo-servicio-delete'),

    path('tipo-pisos/', views.TipoPisosListView.as_view(), name='tipo-pisos'),
    path('tipo-piso/', views.TipoPisoCreateView.as_view(), name='tipo-piso'),
    path('tipo-piso/<int:pk>/', views.TipoPisoUpdateView.as_view(), name='tipo-piso'),
    path('tipo-piso/<int:pk>/delete/', views.TipoPisoDeleteView.as_view(), name='tipo-piso-delete'),

    path('marca-vehiculos/', views.MarcaVehiculosListView.as_view(), name='marca-vehiculos'),
    path('marca-vehiculo/', views.MarcaVehiculoCreateView.as_view(), name='marca-vehiculo'),
    path('marca-vehiculo/<int:pk>/', views.MarcaVehiculoUpdateView.as_view(), name='marca-vehiculo'),
    path('marca-vehiculo/<int:pk>/delete/', views.MarcaVehiculoDeleteView.as_view(), name='marca-vehiculo-delete'),

    path('modelo-vehiculos/', views.ModeloVehiculosListView.as_view(), name='modelo-vehiculos'),
    path('modelo-vehiculo/', views.ModeloVehiculoCreateView.as_view(), name='modelo-vehiculo'),
    path('modelo-vehiculo/<int:pk>/', views.ModeloVehiculoUpdateView.as_view(), name='modelo-vehiculo'),
    path('modelo-vehiculo/<int:pk>/delete/', views.ModeloVehiculoDeleteView.as_view(), name='modelo-vehiculo-delete'),

    path('llantas/',views.LlantasListView.as_view(), name='llantas'),
    path('llanta/', views.LlantaCreateView.as_view(), name='llanta'),
    path('llanta/<int:pk>/', views.LlantaUpdateView.as_view(), name='llanta'),
    path('llanta/<int:pk>/delete/', views.LlantaDeleteView.as_view(), name='llanta-delete'),
    
    path('tipo-vehiculos/', views.TipoVehiculosListView.as_view(), name='tipo-vehiculos'),
    path('tipo-vehiculo/', views.TipoVehiculoCreateView.as_view(), name='tipo-vehiculo'),
    path('tipo-vehiculo/<int:pk>/', views.TipoVehiculoUpdateView.as_view(), name='tipo-vehiculo'),
    path('tipo-vehiculo/<int:pk>/delete/', views.TipoVehiculoDeleteView.as_view(), name='tipo-vehiculo-delete'),


    path('vehiculos/', views.VehiculosListView.as_view(), name='vehiculos'),
    path('vehiculo/', views.VehiculoCreateView.as_view(), name='vehiculo'),
    path('vehiculo/<int:pk>/', views.VehiculoUpdateView.as_view(), name='vehiculo'),
    path('vehiculo/<int:pk>/delete/', views.VehiculoDeleteView.as_view(), name='vehiculo-delete'),
    path('render-option-vehiculo', views.RenderOptionVehiculo, name="render-option-vehiculo"),

    path('ver-vehiculo/<int:pk>/', views.VerVehiculoView.as_view(), name='ver-vehiculo'),
    path('agregar-llanta/<int:pk>/', views.AgregarLlantaCreateView.as_view(), name='agregar-llanta'),
    path('searchRenovadora/', views.AnchoBandaRenovaSearch, name='search-renovadora'),
    path('viewCondicion/', views.view_condicion, name='view-condicion'),
    path('viewRenova/', views.view_renova, name='view-renova'),
    path('viewLlanta/<int:pk>/', views.DetalleLlantaView.as_view(), name='ver-llanta'),
    path('desmontaje/', views.DesmontajeLlantaView.as_view(), name='ver-desmontaje'),
    path('montaje/', views.MontajeLlantasView.as_view(), name='ver-montaje'),
    path('searchLlanta/', views.LlantaSearch, name='search-llanta'),

    path('hoja-movimientos/', views.HojaDeMovimientosView.as_view(), name='hoja-movimientos'),
    path('inspeccion-llantas/', views.InspeccionLlantasView.as_view(), name='inspeccion-llantas'),

    
    path('inspeccion-llantas/detalles/<int:pk>/', views.InsepccionDetalleView.as_view(), name='inspeccion-detalle'),
    path('inspeccion-agregar/', views.AgregarInspeccion, name='inspeccion-agregar'),
    path('getTipo/<int:id>/', views.getTipo, name='get-tipo'),

    path('historial/', views.HistorialLlantas.as_view(), name='ver-historial'),

    # path('get-vehiculo/', views.getVehiculo, name='ver-vehiculo'),

]

