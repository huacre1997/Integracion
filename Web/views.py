#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.urls import reverse_lazy
from django.core import serializers
from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import FormView, CreateView, ListView, UpdateView,DetailView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.serializers.json import DjangoJSONEncoder

from django.utils.decorators import method_decorator
from .forms import *
from django.http.response import HttpResponseRedirect
from django.contrib import messages, auth
from .common import LoginView, LoginSelectPerfilView
from django.urls import reverse
from .models import *
from django.db import transaction	
from datetime import datetime, timedelta
from Web.constanst import ACCION_NUEVO, ACCION_EDITAR, ACCION_ELIMINAR
import json

from django.db.models import Count,OuterRef, Subquery,Q,Sum,F,Case,When

from .mixins import ValidateMixin
from six import text_type
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

from .many_load import *
def imports(request):
    if request.method=="GET":
        return render(request,"Web/imports.html")

def importTipos(request):
    if request.method=="POST":
        file=request.FILES['FILE']
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo cargado no es .csv')
        else:
            if importExcel(file):
                messages.success(request, 'Archivo cargando...')
        return HttpResponseRedirect(reverse_lazy("Web:tipo-vehiculos"))
def importPosiciones(request):
    if request.method=="POST":
        file=request.FILES['posi']
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo cargado no es .csv')
        else:
            if importPosi(file):
                messages.success(request, 'Archivo cargando...')
        return HttpResponseRedirect(reverse_lazy("Web:tipo-vehiculos"))
def importVehiculos(request):
    if request.method=="POST":
        file=request.FILES['vehi']
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo cargado no es .csv')
        else:
            if importVehi(file):
                messages.success(request, 'Archivo cargando...')
        return HttpResponseRedirect(reverse_lazy("Web:tipo-vehiculos"))
def importMedidas(request):
    if request.method=="POST":
        file=request.FILES['medidas']
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo cargado no es .csv')
        else:
            if importMedi(file):
                messages.success(request, 'Archivo cargando...')
        return HttpResponseRedirect(reverse_lazy("Web:tipo-vehiculos"))
def importLlantas(request):
    if request.method=="POST":
        file=request.FILES['llantas']
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo cargado no es .csv')
        else:
            if importLLan(file):
                messages.success(request, 'Archivo cargando...')
        return HttpResponseRedirect(reverse_lazy("Web:llantas"))
def importCubiertas(request):
    if request.method=="POST":
        file=request.FILES['cubiertas']
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo cargado no es .csv')
        else:
            if importCub(file):
                messages.success(request, 'Archivo cargando...')
        return HttpResponseRedirect(reverse_lazy("Web:llantas"))
def ProvinciaComboBox(request):
    if request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        qs=Provincia.objects.filter(departamento_id=post).only("descripcion","id")
        qs_json = serializers.serialize('json', qs)
        return HttpResponse(qs_json, content_type='application/json')
def DistritoComboBox(request):
    if request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        qs=Distrito.objects.filter(provincia_id=post)
        qs_json = serializers.serialize('json', qs)
        return HttpResponse(qs_json, content_type='application/json')
class PasswordReset(PasswordResetView):
    email_template_name = 'Web/password_reset_email.html'

    template_name="Web/password_reset_form.html"
class PasswordResetDone(PasswordResetDoneView):
    template_name="Web/password_reset_done.html"
class PasswordResetConfirm(PasswordResetConfirmView):
    # template_name="Web/password_reset_confirm.html"
    success_url=reverse_lazy("Web:password_reset_complete")
class PasswordResetComplete(PasswordResetCompleteView):
    template_name="Web/password_reset_complete.html"
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.profile.email_confirmed)
        )


class PasswordResetToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.profile.reset_password)
        )


account_activation_token = AccountActivationTokenGenerator()
password_reset_token = PasswordResetToken()
class CatalogosView(LoginRequiredMixin,ValidateMixin,TemplateView):
    template_name="Web/Catalogos/catalogos_base.html"
    permission_required=["auth.view_catalogos"]
class SeguridadView(LoginRequiredMixin,ValidateMixin,TemplateView):
    template_name="Web/Seguridad/seguridad_base.html"
    permission_required=("auth.view_seguridad")

class OperacionesView(LoginRequiredMixin,ValidateMixin,TemplateView):
    template_name="Web/Operaciones/operaciones_base.html"
    permission_required=["auth.view_procesos"]

class ReportesView(LoginRequiredMixin,TemplateView):
    template_name="Web/Reportes/reportes_base.html"
    

class CombustibleView(LoginRequiredMixin,TemplateView):
    template_name="Web/Combustible/combustible_base.html"
class LogueoView(FormView):
    form_class = LoginForm
    template_name = "Web/login.html"
    success_url=reverse_lazy("Web:inicio")
    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form ):
        # import pdb; pdb.set_trace()
        username = form.cleaned_data['usuario']
        password = form.cleaned_data['clave']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(self.request, user)
            messages.success(self.request,f"Bienvenido {self.request.user}",extra_tags="login")

            return redirect(self.success_url)
        else:
            auth.logout(self.request)    
            messages.error(self.request, 'El usuario o la clave es incorrecto.')
            return redirect(reverse_lazy("Web:login"))            
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'El usuario o la clave es incorrecto.')
        return super().form_invalid(form)

class HomePageView(LoginRequiredMixin,TemplateView):
    template_name = "Web/base.html"
  
class Error403(TemplateView):
    template_name = 'Web/403.html'


class LogoutView(LoginSelectPerfilView, View):
    template_name = 'Web/logout.html'

    def get(self, request):
        auth.logout(request)
        return render(request, self.template_name)

class DepartamentoCreateView(LoginRequiredMixin,TemplateView):
    template_name = "Web/Catalogos/departamento.html"

    model=Departamento
    form_class=DepartamentoForm
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.save()
                data={"status":200,"id":instance.id,"descripcion":instance.descripcion}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
class PerfilesTemplateView(LoginRequiredMixin,ValidateMixin ,TemplateView):
    template_name = "Web/Seguridad/perfiles.html"
    context_object_name = 'perfiles'
    login_url=reverse_lazy("Web:login")
    permission_required=["auth.view_group"]

    def post(self, request, *args, **kwargs):
        #import pdb; pdb.set_trace()
        try:
            
            #persona = Persona.objects.get(id_usuario=self.request.user)
            # request.session['perfil_id'] = int(request.POST['perfil'])
            return HttpResponseRedirect(reverse_lazy("Web:perfiles"))            
        except Exception as e:
            messages.error(request, str(e))
            return HttpResponseRedirect(reverse_lazy("Web:login"))            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #import ipdb; ipdb.set_trace()
        # usuario = Usuario.objects.filter(user=self.request.user).first()
        context['perfiles'] = Group.objects.all()
        # context['perfiles'] = usuario.perfil.all()
        #context['url_foto'] = settings.URL_FOTO
        return context
class PerfilCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    model=Group
    form_class = UserGroupForm
    template_name = 'Web/Seguridad/perfil.html'
    success_url = reverse_lazy("Web:Perfiles") 
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["auth.add_group"]

    def post(self,request,*args, **kwargs):
        data={}
        try:
            form = self.get_form()

            if form.is_valid():
                form.save()
                data={"status":200,"url":self.success_url}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)
  


class PerfilUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = UserGroupForm
    model = Group
    template_name = "Web/Seguridad/perfil.html"
    context_object_name="perfil"
    success_url = reverse_lazy("Web:Perfiles")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["auth.change_group"]
    def dispatch(self,request,*args, **kwargs):
        self.object=self.get_object() 
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            form = self.get_form()

            if form.is_valid():
                form.save()
              
                return JsonResponse({"status":200,"url":self.success_url})
            else:
                return JsonResponse({"status":500,"form":form.errors})

        except Exception as e:
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

class PersonaListView(LoginRequiredMixin,ValidateMixin,ListView):
    template_name = 'Web/Seguridad/personas.html'
    model = Persona
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_persona"]

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in Persona.objects.filter(eliminado=False):
                    data.append(i.toJSON())
            else:
                data["error"]="Ha ocurrido un error"
            return JsonResponse(data,safe=False)
        except Exception as e:
            messages.error(self.request, 'Algo salió mal.Intentelo nuevamente.')
            return HttpResponseRedirect(self.success_url)
   
class PersonaUpdateView(LoginRequiredMixin,ValidateMixin,UpdateView):
    model = Persona
    template_name="Web/Seguridad/persona.html"
    context_object_name = "persona" 
    form_class = PersonaForm
    permission_required=["Web.change_persona"]
    login_url=reverse_lazy("Web:login")

    def dispatch(self,request,*args, **kwargs):
        self.object=self.get_object() 
        return super().dispatch(request,*args,**kwargs)
    
    def post(self,request,*args, **kwargs):
        data={}

        try:
            action=request.POST["action"]
            if action=="edit":
                form = self.get_form()

                if form.is_valid():
                    form.instance.changed_by = self.request.user

                    form.save()

                    data = {
                    'status': 200
                   }
                else:
                    data = {
                    "error":form.errors,
                    'status': 500,
                    }
                return JsonResponse(data)
            else:
                data["error"]="Nose ha ingresado nada"
                return JsonResponse(data)

        except Exception as e:
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["provincia"] = Provincia.objects.filter(departamento=self.object.departamento)
        context["distrito"] = Distrito.objects.filter(provincia=self.object.provincia)
 
        return context
    
class PersonaCreateView(LoginRequiredMixin,ValidateMixin,CreateView):
    model=Persona
    template_name = 'Web/Seguridad/persona.html'
    form_class=PersonaForm
    login_url=reverse_lazy("Web:login")
    action = ACCION_NUEVO
    permission_required=["Web.add_persona"]

    def post(self,request,*args, **kwargs):
        data={}
        try:
            form = self.get_form()

            if form.is_valid():
                form.instance.changed_by = self.request.user
                form.save()
                data = {
                    'status': 200,"error":{}
                   }
                return JsonResponse(data,safe=False)
            else:
                data = {
                    "error":form.errors,
                    'status': 500,
                    }
                return JsonResponse(data,safe=False)
            
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)




class UsuariosListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/Seguridad/list_usuarios.html'
    model = Usuario
    context_object_name = 'usuarios'
    permission_required=["Web.view_usuario"]
    login_url=reverse_lazy("Web:login")
    success_url=reverse_lazy("Web:inicio")
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 

    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                
                data=[]
                for i in Usuario.objects.all():
                    if i.persona:
                        data.append(i.toJSON())
                return JsonResponse(data,safe=False)

            else:
               
                data["error"]="Ha ocurrido un error"
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)


class UsuarioCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    model=Usuario
    template_name = 'Web/Seguridad/usuario.html'
    success_url = reverse_lazy("Web:Usuarios")
    action = ACCION_NUEVO
    form_class=UsuarioForm
    permission_required=["Web.change_usuario"]

    login_url=reverse_lazy("Web:login")

    def post(self,request,*args, **kwargs):
        data={}
        try:
            form = self.get_form()

            if form.is_valid(): 
           
                form.changed_by = self.request.user
          
                
                form.save()    
                return JsonResponse({"status":200,"url":self.success_url})
            else:
                return JsonResponse({"status":500,"form":form.errors})

        
        except Exception as e:
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)
     

    # def form_invalid(self, form):
    #     messages.warning(self.request, form.errors)
    #     return super().form_invalid(form)

    # def get_context_data(self, **kwargs):
    #     if 'formUsuario' not in kwargs:
    #         kwargs['formUsuario'] = UsuarioForm()
    #     if 'formPersona' not in kwargs:
    #         kwargs['formPersona'] = PersonaForm()
    #     return kwargs
from .forms import UsuarioEditForm
class UsuarioUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    login_url=reverse_lazy("Web:login")

    model = Usuario
    template_name = 'Web/Seguridad/usuarioEdit.html'
    context_object_name="usuario"
    form_class=UsuarioEditForm
    success_url=reverse_lazy("Web:Usuarios")
    permission_required=["Web.change_usuario"]
    def dispatch(self,request,*args, **kwargs):     
        self.object=self.get_object() 
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args, **kwargs):
        data={}
        
        try:
            form = self.get_form()

            if form.is_valid():
                
                self.object.groups.clear()
                self.object.groups.set(form.cleaned_data["groups"])  
                
                instance=form.save(commit=False)
                if("Administrador" in [i.name for i in self.object.groups.all()]):
                    instance.is_staff=True
                instance.changed_by = self.request.user
                
                instance.save()    

                persona=Persona.objects.filter(id=self.object.persona.id)
                if persona.exists():
                    data=persona.first()
                    data.nom=self.request.POST["name"]
                    data.apep=self.request.POST["apep"]
                    data.apem=self.request.POST["apem"]
                    data.changed_by=self.request.user
                    
                    data.save()
                return JsonResponse({"status":200,"url":self.success_url})

            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
                return JsonResponse(data)
          

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

class UsuarioUpdatePasswordView(LoginRequiredMixin,ValidateMixin,UpdateView):
    # login_url=reverse_lazy("Web:login")
    model = Usuario
    template_name = 'Web/Seguridad/usuarioChangePassword.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy("Web:Usuarios")
    permission_required=["Web.change_usuario"]

    def dispatch(self,request,*args, **kwargs):     
        self.object=self.get_object() 
        return super().dispatch(request,*args,**kwargs)
    
    def get(self,*args, **kwargs):
        form = UserPasswordResetForm(user=self.object)
        return render(self.request,self.template_name,{"usuario":self.object,"form":form})
    def post(self,*args, **kwargs):
        try:
            form = UserPasswordResetForm(user=self.object,data=self.request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({"status":200})
            else:
                data = {
                    "form":form.errors,
                    'status': 500,
                    }
                return JsonResponse(data)
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)
def UsuarioDesactivate(request,pk):
    if request.method=="POST":
        user=Usuario.objects.filter(id=pk)
        if user.exists():
            data=user.first()
            data.is_active=False
            data.changed_by=request.user
            data.save()
            return JsonResponse({"status":200})
        else:
            return JsonResponse({"status":404})
def UsuarioActivate(request,pk):
    if request.method=="POST":
        user=Usuario.objects.filter(id=pk)
        if user.exists():
            data=user.first()
            data.is_active=True
            data.changed_by=request.user

            data.save()
            return JsonResponse({"status":200})
        else:
            return JsonResponse({"status":404})

            
            
        
class ListUbicacionesListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/Catalogos/ubicaciones.html'
    model = Ubicacion
    context_object_name = 'ubicaciones'
    permission_required=["Web.view_ubicacion"]
    login_url=reverse_lazy("Web:login")

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
    
        return qs.order_by('created_at').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UbicacionCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = UbicacionForm
    template_name = 'Web/Catalogos/ubicacion.html'
    success_url = reverse_lazy("Web:Ubicaciones")
    action = ACCION_NUEVO
    permission_required=["Web.add_ubicacion"]
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class UbicacionUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = UbicacionForm
    model = Ubicacion
    template_name = 'Web/Catalogos//ubicacion.html'
    success_url = reverse_lazy("Web:Ubicaciones")
    action = ACCION_EDITAR

    permission_required=["Web.change_ubicacion"]
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


class UbicacionDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_ubicacion"]

    def get(self, request, *args, **kwargs):
        id_ubicacion = self.kwargs['pk']
        ubicacion = Ubicacion.objects.get(pk=id_ubicacion)
        ubicacion.changed_by=request.user
        ubicacion.eliminado = True
        ubicacion.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:Ubicaciones',))


class AlmacenesListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/Catalogos/almacenes.html'
    model = Almacen
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_almacen"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AlmacenCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = AlmacenForm
    template_name = 'Web/Catalogos/almacen.html'
    success_url = reverse_lazy("Web:almacenes")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_almacen"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class AlmacenUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = AlmacenForm
    model = Almacen
    template_name = 'Web/Catalogos/almacen.html'
    success_url = reverse_lazy("Web:almacenes")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_almacen"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


class AlmacenDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_almacen"]
    permission_required=["Web.change_almacen"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        Almacen = Almacen.objects.get(pk=id)
        Almacen.changed_by=request.user
        Almacen.eliminado = True
        Almacen.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:almacenes',))


class LugaresListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/Catalogos/lugares.html'
    model = Lugar
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_lugar"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LugarCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = LugarForm
    template_name = 'Web/Catalogos/lugar.html'
    success_url = reverse_lazy("Web:lugares")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_lugar"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class LugarUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = LugarForm
    model = Lugar
    template_name = 'Web/Catalogos/lugar.html'
    success_url = reverse_lazy("Web:lugares")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_lugar"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


class LugarDeleteView(LoginRequiredMixin,ValidateMixin ,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_lugar"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        lugar = Lugar.objects.get(pk=id)
        lugar.changed_by=request.user
        lugar.eliminado = True
        lugar.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:lugares',))


class MarcaRenovacionesListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/Catalogos/marca_renovaciones.html'
    model = MarcaRenova
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_marcarenova"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MarcaRenovacionCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = MarcaRenovaForm
    template_name = 'Web/Catalogos/marca_renovacion.html'
    success_url = reverse_lazy("Web:marca-renovaciones")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_marcarenova"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class MarcaRenovacionUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = MarcaRenovaForm
    model = MarcaRenova
    template_name = 'Web/Catalogos/marca_renovacion.html'
    success_url = reverse_lazy("Web:marca-renovaciones")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_marcarenova"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


class MarcaRenovacionDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_marcarenova"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = MarcaRenova.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:marca-renovaciones',))


class ModeloRenovacionesListView(LoginRequiredMixin, ListView):
    template_name = 'Web/Catalogos/modelo_renovaciones.html'
    model = ModeloRenova
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ModeloRenovacionCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = ModeloRenovaForm
    template_name = 'Web/Catalogos/modelo_renovacion.html'
    success_url = reverse_lazy("Web:modelo-renovaciones")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_marcarenova"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["marca_renova"] =  MarcaRenova.objects.values("id","descripcion","activo","eliminado")
        return context
    

class ModeloRenovacionUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = ModeloRenovaForm
    model = ModeloRenova
    template_name = 'Web/Catalogos/modelo_renovacion.html'
    success_url = reverse_lazy("Web:modelo-renovaciones")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_modelorenova"]
    context_object_name="obj"
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        context["marca_renova"] =  MarcaRenova.objects.values("id","descripcion","activo","eliminado")

        return context


class ModeloRenovacionDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_modelorenova"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = ModeloRenova.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:modelo-renovaciones',))


class AnchoBandaRenovacionesListView(LoginRequiredMixin,ValidateMixin ,ListView):
    template_name = 'Web/Catalogos/ancho_banda_renovaciones.html'
    model = AnchoBandaRenova
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_anchobandarenova"]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False).order_by('-created_at')
        return qs
class AnchoBandaRenovacionCreateView(LoginRequiredMixin, ValidateMixin,CreateView):
    form_class = AnchoBandaRenovaForm
    template_name = 'Web/Catalogos/ancho_banda_renovacion.html'
    success_url = reverse_lazy("Web:ancho-banda-renovaciones")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_anchobandarenova"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_renova'] = MarcaRenova.objects.values("id",'descripcion',"activo","eliminado")
 
        return context
    

class AnchoBandaRenovacionUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = AnchoBandaRenovaForm
    model = AnchoBandaRenova
    template_name = 'Web/Catalogos/ancho_banda_renovacion.html'
    success_url = reverse_lazy("Web:ancho-banda-renovaciones")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_anchobandarenova"]
    context_object_name="obj"
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # import pdb; pdb.set_trace()
        context['marca_renova'] = MarcaRenova.objects.values("id",'descripcion',"activo","eliminado")
        context['update'] = True
        return context


class AnchoBandaRenovacionDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_anchobandarenova"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = AnchoBandaRenova.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:ancho-banda-renovaciones',))


def RenderOption(request):
    id_marca = request.GET.get('id_marca')
    if id_marca!="":
        id_marca = request.GET.get('id_marca')
        modelos = ModeloRenova.objects.filter(marca_renova__pk=id_marca)
        return HttpResponse(json.dumps(list(modelos.values('id','descripcion',"eliminado","activo"))), content_type="application/json")
    else:
        return JsonResponse({"response":"seleccione marca"},safe=False)

def RenderOptionRenova(request):
    id_marca = request.GET.get('id_marca_renova')
    if id_marca!="":
        modelos = AnchoBandaRenova.objects.filter(modelo_renova__pk=id_marca)
        data=[]
        for i in modelos:
            data.append(i.toJSON2())
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({"response":"seleccione marca"},safe=False)

class MarcaLlantasListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/Catalogos/marca_llantas.html'
    model = MarcaLlanta
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_marcallanta"]
    success_url=reverse_lazy("Web:marca-llantas")
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in MarcaLlanta.objects.filter(eliminado=False):
                    data.append(i.toJSON())

            else:
                data["error"]="Ha ocurrido un error"
            return JsonResponse(data,safe=False)

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)


class MarcaLlantaCreateView(LoginRequiredMixin, ValidateMixin,CreateView):
    form_class = MarcaLlantaForm
    template_name = 'Web/Catalogos/marca_llanta.html'
    success_url = reverse_lazy("Web:marca-llantas")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_marcallanta"]
    def get(self,*args, **kwargs):
        form=self.get_form()
        return render(self.request,self.template_name,{"form":form})
    
    
    def post(self, request,*args, **kwargs):      
        try:
            form = self.get_form()

            if form.is_valid():

                instance=form.save(commit=False)
              
                instance.changed_by = self.request.user
                instance.save()
                data = {
                'status': 200
                }
                return JsonResponse(data,safe=False)
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
                return JsonResponse(data)
            

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

        # messages.success(self.request, 'Operación realizada correctamente.')
    
    # def form_invalid(self, form):
    #     messages.warning(self.request, form.errors)
    #     return super().form_invalid(form)


class MarcaLlantaUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = MarcaLlantaForm
    model = MarcaLlanta
    template_name = 'Web/Catalogos/marca_llanta.html'
    success_url = reverse_lazy("Web:marca-llantas")
    action = ACCION_EDITAR
    context_object_name="marcallanta"
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_marcallanta"]

    def dispatch(self,request,*args, **kwargs):
        self.object=self.get_object() 
        return super().dispatch(request,*args,**kwargs)



    def post(self, request,*args, **kwargs):       
        try:
            form = self.get_form()

            if form.is_valid():
                instance=form.save(commit=False)
                if not "activo" in self.request.POST:
                    instance.activo=False
                instance.changed_by = self.request.user
                instance.save()
                data = {
                'status': 200
                }
                return JsonResponse(data,safe=False)
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
                return JsonResponse(data)
            

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

import json
class MarcaLlantaDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_marcallanta"]

    def post(self, request, *args, **kwargs):
        id=self.kwargs["pk"]
        existe = MarcaLlanta.objects.filter(pk=id)
        if existe.exists():
            obj=existe.first()
            obj.changed_by=request.user
            obj.eliminado = True
            obj.activo=False
            obj.save()
            return JsonResponse({"status":200},safe=False)

        else:
            return JsonResponse({"status":500},safe=False)


class ModeloLlantasListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/Catalogos/modelo_llantas.html'
    model = ModeloLlanta
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_modelollanta"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class ModeloLlantaCreateView(LoginRequiredMixin,ValidateMixin ,CreateView):
    form_class = ModeloLlantaForm
    template_name = 'Web/Catalogos/modelo_llanta.html'
    success_url = reverse_lazy("Web:modelo-llantas")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_modelollanta"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_llanta']=MarcaLlanta.objects.values("id","descripcion","activo")
        return context
    

class ModeloLlantaUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = ModeloLlantaForm
    model = ModeloLlanta
    template_name = 'Web/Catalogos/modelo_llanta.html'
    success_url = reverse_lazy("Web:modelo-llantas")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_modelollanta"]
    context_object_name="obj"
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        context['marca_llanta']=MarcaLlanta.objects.values("id","descripcion","activo")

        return context


class ModeloLlantaDeleteView(LoginRequiredMixin,ValidateMixin ,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_modelollanta"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = ModeloLlanta.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:modelo-llantas',))


class MedidaLlantasListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/Catalogos/medida_llantas.html'
    model = MedidaLlanta
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_medidallanta"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(medida__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MedidaLlantaCreateView(LoginRequiredMixin, ValidateMixin,CreateView):
    form_class = MedidaLlantaForm
    template_name = 'Web/Catalogos/medida_llanta.html'
    success_url = reverse_lazy("Web:medida-llantas")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_medidallanta"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_llanta'] = MarcaLlanta.objects.values("id",'descripcion',"activo","eliminado")
 
        return context
    
class MedidaLlantaUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = MedidaLlantaForm
    model = MedidaLlanta
    template_name = 'Web/Catalogos/medida_llanta.html'
    success_url = reverse_lazy("Web:medida-llantas")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_medidallanta"]
    context_object_name="obj"
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_llanta'] = MarcaLlanta.objects.values("id",'descripcion',"activo","eliminado")

        context['update'] = True
        return context


class MedidaLlantaDeleteView(LoginRequiredMixin, ValidateMixin,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_medidallanta"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = MedidaLlanta.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:medida-llantas',))


def RenderOptionLlanta(request,id):
    if id!="":
        modelos = ModeloLlanta.objects.filter(marca_llanta=id)
    
        return HttpResponse(json.dumps(list(modelos.values('id','descripcion',"eliminado","activo"))), content_type="application/json")
    else:
        return JsonResponse({"response":"seleccione marca"},safe=False)

# class EstadoLlantasListView(LoginRequiredMixin,ValidateMixin, ListView):
#     template_name = 'Web/estado_llantas.html'
#     model = EstadoLlanta
#     context_object_name = 'objetos'
#     login_url=reverse_lazy("Web:login")
#     permission_required=["Web.view_estadollanta"]

#     def get_queryset(self):
#         # import pdb; pdb.set_trace();
#         qs = super().get_queryset()
#         qs = qs.filter(eliminado=False)
#         q = self.request.GET.get('q','')
#         qs = qs.filter(descripcion__icontains=q)
#         return qs.order_by('descripcion')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


# class EstadoLlantaCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
#     form_class = EstadoLlantaForm
#     template_name = 'Web/estado_llanta.html'
#     success_url = reverse_lazy("Web:estado-llantas")
#     action = ACCION_NUEVO
#     login_url=reverse_lazy("Web:login")
#     permission_required=["Web.add_estadollanta"]

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.changed_by = self.request.user
#         messages.success(self.request, 'Operación realizada correctamente.')
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.warning(self.request, form.errors)
#         return super().form_invalid(form)


# class EstadoLlantaUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
#     form_class = EstadoLlantaForm
#     model = EstadoLlanta
#     template_name = 'Web/estado_llanta.html'
#     success_url = reverse_lazy("Web:estado-llantas")
#     action = ACCION_EDITAR
#     login_url=reverse_lazy("Web:login")
#     permission_required=["Web.change_estadollanta"]

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.changed_by = self.request.user
#         messages.success(self.request, 'Operación realizada correctamente.')
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.warning(self.request, form.errors)
#         return super().form_invalid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['update'] = True
#         return context


# class EstadoLlantaDeleteView(LoginRequiredMixin, ValidateMixin,View):
#     action = ACCION_EDITAR
#     login_url=reverse_lazy("Web:login")
#     permission_required=["Web.delete_estadollanta"]

#     def get(self, request, *args, **kwargs):
#         id = self.kwargs['pk']
#         obj = EstadoLlanta.objects.get(pk=id)
#         obj.changed_by=request.user
#         obj.eliminado = True
#         obj.save()
#         messages.success(self.request, 'Operación realizada correctamente.')
#         return HttpResponseRedirect(reverse('Web:estado-llantas',))


class TipoServiciosListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/Catalogos/tipo_servicios.html'
    model = TipoServicio
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_tiposervicio"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TipoServicioCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = TipoServicioForm
    template_name = 'Web/Catalogos/tipo_servicio.html'
    success_url = reverse_lazy("Web:tipo-servicios")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_tiposervicio"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class TipoServicioUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = TipoServicioForm
    model = TipoServicio
    template_name = 'Web/Catalogos/tipo_servicio.html'
    success_url = reverse_lazy("Web:tipo-servicios")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_tiposervicio"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


class TipoServicioDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_tiposervicio"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = TipoServicio.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:tipo-servicios',))


class TipoPisosListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/Catalogos/tipo_pisos.html'
    model = TipoPiso
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_tipopiso"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TipoPisoCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = TipoPisoForm
    template_name = 'Web/Catalogos/tipo_piso.html'
    success_url = reverse_lazy("Web:tipo-pisos")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_tipopiso"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class TipoPisoUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = TipoPisoForm
    model = TipoPiso
    template_name = 'Web/Catalogos/tipo_piso.html'
    success_url = reverse_lazy("Web:tipo-pisos")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_tipopiso"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


class TipoPisoDeleteView(LoginRequiredMixin, ValidateMixin,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_tipopiso"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = TipoPiso.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:tipo-pisos',))


class MarcaVehiculosListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/Catalogos/marca_vehiculos.html'
    model = MarcaVehiculo
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_marcavehiculo"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class MarcaVehiculoCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = MarcaVehiculoForm
    template_name = 'Web/Catalogos/marca_vehiculo.html'
    success_url = reverse_lazy("Web:marca-vehiculos")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_marcavehiculo"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class MarcaVehiculoUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = MarcaVehiculoForm
    model = MarcaVehiculo
    template_name = 'Web/Catalogos/marca_vehiculo.html'
    success_url = reverse_lazy("Web:marca-vehiculos")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_marcavehiculo"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


class MarcaVehiculoDeleteView(LoginRequiredMixin, ValidateMixin,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_marcavehiculo"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = MarcaVehiculo.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:marca-vehiculos',))
    
class TipoVehiculosListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/Catalogos/tipo_vehiculos.html'
    model = TipoVehiculo
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_tipovehiculo"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
  
        return qs.order_by('created_at').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
from django.core.files.storage import default_storage

class TipoVehiculoCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = TipoVehiculoForm
    template_name = 'Web/Catalogos/tipo_vehiculo.html'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_tipovehiculo"]
    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.image!="":
            if default_storage.exists(f'vehiculo2/Y/{instance.image}'):
                default_storage.delete(f'vehiculo2/Y/{instance.image}')   
        if instance.image2!="":
            if default_storage.exists(f'vehiculo2/X/{instance.image2}'):
                default_storage.delete(f'vehiculo2/X/{instance.image2}')            
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
import boto3 
class DetalleTipoVehiculo(LoginRequiredMixin,ValidateMixin, ListView):
    model=PosicionesLlantas
    template_name = 'Web/Catalogos/posiciones.html'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_tipovehiculo"]
    context_object_name="obj"
    def post(self,request,*args, **kwargs):
        pos=[]
        for i in range(0,len(self.request.POST)):
            if  i!=0:
                pos.append((self.request.POST.getlist(f'{i}')))
        for i,x in enumerate(self.get_queryset()):
            
            x.posx=pos[i][0]
            x.posy=pos[i][1]
            x.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:tipo-vehiculos',))
    def get_queryset(self):

        return PosicionesLlantas.objects.filter(tipo__id=self.kwargs["pk"]).order_by("posicion")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tipo"] = TipoVehiculo.objects.get(pk=self.kwargs["pk"])
        return context
    
    
class TipoVehiculoUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = TipoVehiculoForm
    model = TipoVehiculo
    template_name = 'Web/Catalogos/tipo_vehiculo.html'
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_tipovehiculo"]
    context_object_name="obj"
    def form_valid(self, form):
        instance = form.save(commit=False)

        if instance.image!="":
            if default_storage.exists(f'vehiculo2/Y/{instance.image}'):
                default_storage.delete(f'vehiculo2/Y/{instance.image}')         
        if instance.image2!="":
            if default_storage.exists(f'vehiculo2/X/{instance.image2}'):
                default_storage.delete(f'vehiculo2/X/{instance.image2}')            
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class TipoVehiculoDeleteView(LoginRequiredMixin, ValidateMixin,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_tipovehiculo"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = TipoVehiculo.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:tipo-vehiculos',))


class ModeloVehiculosListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/Catalogos/modelo_vehiculos.html'
    model = ModeloVehiculo
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_modelovehiculo"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ModeloVehiculoCreateView(LoginRequiredMixin, ValidateMixin,CreateView):
    form_class = ModeloVehiculoForm
    template_name = 'Web/Catalogos/modelo_vehiculo.html'
    success_url = reverse_lazy("Web:modelo-vehiculos")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_modelovehiculo"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_vehiculo']=MarcaVehiculo.objects.values("id","descripcion","activo")
        return context


class ModeloVehiculoUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = ModeloVehiculoForm
    model = ModeloVehiculo
    template_name = 'Web/Catalogos/modelo_vehiculo.html'
    success_url = reverse_lazy("Web:modelo-vehiculos")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_modelovehiculo"]
    context_object_name="obj"
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):

        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        context['marca_vehiculo']=MarcaVehiculo.objects.values("id","descripcion","activo")
        return context


class ModeloVehiculoDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_modelovehiculo"]
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = ModeloVehiculo.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse_lazy('Web:modelo-vehiculos'))

from django.views.decorators.cache import never_cache


import decimal
class CubiertaListView(LoginRequiredMixin,ValidateMixin,TemplateView):
    permission_required=["Web.view_cubiertallanta"]
    template_name="Web/Catalogos/cubiertas_llantas.html"
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request,*args, **kwargs):
        try:
            codigo=self.request.POST["codigo"]
            llanta=CubiertaLlanta.objects.select_related("renovadora","modelo_renova","ancho_banda","llanta").filter(activo=True)
            if codigo:
                llanta=llanta.filter(llanta_id=codigo)
            data=[]
            for i in llanta:
                data.append(i.toJSON2())  
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(reverse("Web:cubierta-llantas"))
    def get_context_data(self, **kwargs):
        context = super(CubiertaListView, self).get_context_data(**kwargs)
        context["llanta"]=Llanta.objects.values("id","codigo","activo","eliminado").filter(eliminado=False,activo=True)
        return context
class CubiertaCreateView(LoginRequiredMixin,ValidateMixin,TemplateView):
    template_name="Web/Catalogos/cubierta.html"
    model=CubiertaLlanta
    permission_required=["Web.add_cubiertallanta"]
    
    def post(self,request,*args, **kwargs):
        try:
            form=CubiertaForm(self.request.POST)
            if form.is_valid():
                llanta=Llanta.objects.get(id=self.request.POST["llanta"])
                instance=CubiertaLlanta()
                instance.llanta=llanta
                instance.changed_by=self.request.user
                instance.nro_ren=self.request.POST["nro_ren"]
                instance.km=self.request.POST["km"]
                instance.alt_inicial=self.request.POST["alt_inicial"]
                instance.alt_final=self.request.POST["alt_final"]
                instance.primer_reen=False
                instance.fech_ren=self.request.POST["fech_ren"]
                instance.renovadora_id=self.request.POST["renovadora"]
                instance.modelo_renova_id=self.request.POST["modelo_renova"]
                instance.ancho_banda_id=self.request.POST["ancho_banda"]
                instance.save()
            
                data={"status":200}
            else:
                data={"status":500,"errors":form.errors}
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(reverse_lazy("Web:cubierta-llantas"))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["llanta"] = Llanta.objects.values("id","codigo","eliminado","activo").order_by("codigo")
        context["renova"] = MarcaRenova.objects.values("id",'descripcion',"activo","eliminado")
        return context
    
class CubiertaEditView(LoginRequiredMixin,ValidateMixin,UpdateView):
    permission_required=["Web.change_cubiertallanta"]

    model=CubiertaLlanta
    template_name="Web/Catalogos/cubierta.html"
    context_object_name="obj"
   
    def dispatch(self,request,*args, **kwargs):

        return super().dispatch(request,*args,**kwargs)

    def get(self,*args, **kwargs):
        renova=MarcaRenova.objects.values("id",'descripcion',"activo","eliminado")
        llanta=Llanta.objects.values("id",'codigo',"activo","eliminado")

        context={"renova":renova,"obj":self.get_object(),"llanta":llanta}
        return render(self.request,self.template_name,context)
    def post(self,request,*args, **kwargs):
        try:
            form=CubiertaForm(self.request.POST,instance=self.get_object())
            if form.is_valid():
                instance=self.get_object()
                instance.llanta.estado="2"
                instance.nro_ren=self.request.POST["nro_ren"]
                instance.km=self.request.POST["km"]
                instance.alt_final=self.request.POST["alt_final"]
                instance.alt_inicial=self.request.POST["alt_inicial"]
                instance.fech_ren=self.request.POST["fech_ren"]
                instance.changed_by=self.request.user
                instance.renovadora_id=self.request.POST["renovadora"]
                instance.modelo_renova_id=self.request.POST["modelo_renova"]
                instance.ancho_banda_id=self.request.POST["ancho_banda"]
                if "activo" in self.request.POST:
                    instance.activo=True
                else:
                    instance.activo=False
                instance.llanta.save()

                instance.save()
                data={"status":200}

            else:
                data={"status":500,"errors":form.errors}
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500},safe=False)
class LlantasListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/Catalogos/llantas.html'
    model = Llanta
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_llanta"]
    success_url=reverse_lazy("Web:inicio")
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
   
    def post(self,request,*args, **kwargs):
        try:
            start_date=self.request.POST["start_date"]
            end_date=self.request.POST["end_date"]
            modelo=self.request.POST["modelo"]
            medida=self.request.POST["medida"]

            marca=self.request.POST["marca"]
            
            search=Llanta.objects.select_related("modelo_llanta","medida_llanta").filter(vehiculo=None)
            if marca:
                search=search.filter(modelo_llanta__marca_llanta_id=marca)
                if modelo:
                    search=search.filter(modelo_llanta__marca_llanta_id=marca,modelo_llanta_id=modelo)
            elif medida!="":
                search=search.filter(medida_llanta=medida)
            elif start_date and end_date:
                search=search.filter(created_at__range=[start_date,end_date])

                if start_date==end_date:     
                    search=search.filter(created_at__contains=start_date)            
            data=[]
            for i in search:
                data.append(i.tabletoJSON())  
            return JsonResponse(data, safe=False)
    
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['medida'] = MedidaLlanta.objects.values("id","medida","profundidad","capas","eliminado","activo")
        context['marca'] = MarcaLlanta.objects.values("id",'descripcion',"activo","eliminado")

        return context
class LlantaCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    template_name = 'Web/Catalogos/llanta2.html'
    success_url = reverse_lazy("Web:llantas")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_llanta"]
    def get(self,*args, **kwargs):
        Llanta=LlantaForm()
        cubierta=CubiertaForm()
        marca_llanta = MarcaLlanta.objects.values("id",'descripcion',"activo","eliminado")
        # modelo_renova = ModeloRenova.objects.values("id",'descripcion',"activo","eliminado")
        # ancho_banda = AnchoBandaRenova.objects.values("id",'descripcion',"activo","eliminado")
        # ubicacion=Ubicacion.objects.values("id",'descripcion',"activo","eliminado")
        # vehiculo=Vehiculo.objects.values("id",'placa',"activo","eliminado")
        medida_llanta=MedidaLlanta.objects.values("id","medida","profundidad","capas","eliminado","activo")
        # modelo_llanta=ModeloLlanta.objects.values("id","marca_llanta","descripcion","activo","eliminado")
        renova=MarcaRenova.objects.values("id",'descripcion',"activo","eliminado")
        context={
            "form":Llanta,
            "form2":cubierta,
            # "ubicacion":ubicacion,
            "marca_llanta":marca_llanta,
            # "modelo_renova":modelo_renova,
            # "ancho_banda":ancho_banda,
            # "vehiculo":vehiculo,
            "medida_llanta":medida_llanta,
            # "modelo_llanta":modelo_llanta,
            "renova":renova,

            "estado":CHOICES_ESTADO_LLANTA
            }
        return render(self.request,self.template_name,context)
     
    
    def post(self,request,*args, **kwargs):
        
        try:
            data = json.loads(self.request.body.decode("utf-8"))
                        
            for i in data:
                instance=Llanta()
                instance.codigo=i["codigo"]
                instance.costo=i["costo"]
                instance.marca_llanta_id=i["marca"]
                instance.modelo_llanta_id=i["modelo"]
                instance.medida_llanta_id=i["medida"]
                instance.estado=i["estado"]
                instance.a_final=i["altura_fin"]
                instance.a_inicial=i["altura_ini"]
                instance.a_promedio=decimal.Decimal(i["altura_fin"])-decimal.Decimal(i["altura_ini"])
                instance.fech_ren=i["fech_ren"]

                instance.changed_by = self.request.user
                instance.save()
                if i["estado"]=="2":
                    for a in i["cubierta"]:
                        
                        instance2=CubiertaLlanta()
                        instance2.llanta=instance
                        instance2.changed_by = self.request.user
                        instance2.km=a["km"]
                        instance2.nro_ren=a["nro_reencauchado"]
                        instance2.fech_ren=a["fech_ren"]
                        instance2.alt_final=a["alt_final"]
                        instance2.alt_inicial=a["alt_inicial"]

                        instance2.primer_reen=True
                        instance2.modelo_renova_id=a["modelo_banda"]["id"]
                        instance2.ancho_banda_id=a["ancho_banda"]["id"]
                        instance2.renovadora_id=a["renovadora"]["id"]
                        instance2.save()
             
           
            return JsonResponse({"status":200,"form":{},"form2":{},"url":reverse_lazy("Web:llanta")})
        
        except Exception as e:
            print(e)
            messages.error(self.request, 'Ha ocurrido un error.')
            return HttpResponseRedirect(self.success_url)
def NeumaticoExists(request,codigo):
    if Llanta.objects.filter(codigo=codigo).exists():
        
        return JsonResponse({"status":300})
    return JsonResponse({"status":200})


def PosicionExists(request):
    if request.method=="GET":
        if Llanta.objects.filter(vehiculo=request.GET["vehiculo"],posicion=request.GET["posicion"]).exists():
            return JsonResponse({"status":300,"mensaje":"El vehpiculo ya tiene un neumático colocado es ensa posición."})
        else:
            data=Vehiculo.objects.get(pk=request.GET["vehiculo"])
            nrollantas=data.tipo_vehiculo.nro_llantas
            nrorepuesto=data.tipo_vehiculo.max_rep
            placa=data.placa
            total=int(nrollantas)+int(nrorepuesto)
            if request.GET["repuesto"]=="true":
                a=""
                for i in range(nrollantas,total):
                    a+=str(i+1)+" "
                if not (int(request.GET["posicion"])<=int(total) and int(request.GET["posicion"])>int(nrollantas)):
                    return JsonResponse({"status":300,"mensaje":f"Este neumático de repuesto solo puede ocupar las posiciones {a}."})

            else:
                if int(request.GET["posicion"]) > total :
                    return JsonResponse({"status":300,"mensaje":f"El vehiculo {placa} no puede tener mas de {total} neumáticos totales."})
                elif int(request.GET["posicion"]) > nrollantas :
                    return JsonResponse({"status":300,"mensaje":f"El vehiculo {placa} solo tiene {nrollantas} neumáticos."})
            return JsonResponse({"status":200})
    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     instance.codigo = instance.code
    #     instance.changed_by = self.request.user
    #     messages.success(self.request, 'Operación realizada correctamente.')
    #     return super().form_valid(form)

    # def form_invalid(self, form):
    #     messages.warning(self.request, form.errors)
    #     return super().form_invalid(form)
    

    


class LlantaUpdateView(LoginRequiredMixin,ValidateMixin,UpdateView):
    model = Llanta
    template_name = 'Web/Catalogos/llanta.html'
    success_url = reverse_lazy("Web:llantas")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_llanta"]



    def dispatch(self,request,*args, **kwargs):        
        return super().dispatch(request,*args,**kwargs)
    def get_reencauches(self):
        data=[]
        try:
            for i in CubiertaLlanta.objects.filter(llanta=self.get_object(),activo=True,primer_reen=True):
                item=i.toJSON()
                data.append(item)
        except:
            pass
        return data
    def get(self,*args, **kwargs):
        form1=LlantaForm(instance=self.get_object())
        # form2=CubiertaForm(instance=cubierta)
        marca_llanta= MarcaLlanta.objects.values("id",'descripcion',"activo","eliminado")
        renova = MarcaRenova.objects.values("id",'descripcion',"activo","eliminado")
        ubicacion=Ubicacion.objects.values("id",'descripcion',"activo","eliminado")
        vehiculo=Vehiculo.objects.values("id",'placa',"activo","eliminado")
        medida_llanta=MedidaLlanta.objects.values("id","medida","profundidad","capas","eliminado","activo")
        context={
           "form":form1,
            "vehiculo":vehiculo,
            # "form2":form2,
            "obj":self.get_object(),
            "marca_llanta":marca_llanta,
            # "modelo_renova":modelo_renova,
            # "ubicacion":ubicacion,
            # "ancho_banda":ancho_banda,
            "medida_llanta":medida_llanta,
            "renova":renova,
            "cubierta":self.get_reencauches()
                }
        return render(self.request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        try:
            # data = json.loads(self.request.body.decode("utf-8"))            
            data=request.POST
            instance=self.get_object()
            instance.codigo=data["codigo"]
            instance.costo=data["costo"]
            instance.marca_llanta_id=data["marca_llanta"]
            instance.modelo_llanta_id=data["modelo_llanta"]
            instance.medida_llanta_id=data["medida_llanta"]
            instance.estado=data["estado"]
            instance.a_final=data["a_final"]
            instance.a_inicial=data["a_inicial"]
            instance.a_promedio=decimal.Decimal(data["a_final"])-decimal.Decimal(data["a_inicial"])
            instance.fech_ren=data["fech_ren"]
            if "activo" in data:
                instance.activo=True
            else:
                instance.activo=False
            instance.changed_by = self.request.user
            instance.save()
            instance2=CubiertaLlanta.objects.filter(llanta=self.get_object())

            if data["estado"]=="2":

                for a in json.loads(data["objeto"]):
                    for i in instance2:
                        if "id" in a:
                            if i.id==a["id"]:
                                i.changed_by = self.request.user
                                i.km=a["km"]
                                i.nro_ren=a["nro_ren"]
                                i.fech_ren=a["fech_ren"]
                                i.alt_final=a["alt_final"]
                                i.alt_inicial=a["alt_inicial"]
                                i.activo=False if a["activo"]==0 else True
                                i.primer_reen=True
                                i.modelo_renova_id=a["modelo_renova"]
                                i.ancho_banda_id=a["ancho_banda"]
                                i.renovadora_id=a["renovadora"]
                                i.save()
                                break
                    else:
                        cubierta=CubiertaLlanta()
                        cubierta.llanta=instance
                        cubierta.changed_by=self.request.user
                        cubierta.nro_ren=a["nro_ren"]
                        cubierta.km=a["km"]
                        cubierta.alt_inicial=a["alt_inicial"]
                        cubierta.alt_final=a["alt_final"]
                        cubierta.fech_ren=a["fech_ren"]
                        cubierta.renovadora_id=a["renovadora"]
                        cubierta.modelo_renova_id=a["modelo_renova"]
                        cubierta.ancho_banda_id=a["ancho_banda"]
                        cubierta.primer_reen=True
                        cubierta.save()
            else:
                for i in instance2:
                    i.activo=False
                    i.save()
                # instance2=CubiertaLlanta.objects.filter(llanta=self.get_object())
                # print(json.loads(data["objeto"]))
                # print(instance2.count())
                # for i in instance2:
                #     print(i.id)
                #     print("---")
                #     for a in json.loads(data["objeto"]):
                #         if i.id==a["id"]:
                #             print(i.nro_ren)
                #             print("***")
                #             i.changed_by = self.request.user
                #             i.km=a["km"]
                #             i.nro_ren=a["nro_ren"]
                #             i.fech_ren=a["fech_ren"]
                #             i.alt_final=a["alt_final"]
                #             i.alt_inicial=a["alt_inicial"]

                #             i.primer_reen=True
                #             i.modelo_renova_id=a["modelo_renova"]
                #             i.ancho_banda_id=a["ancho_banda"]
                #             i.renovadora_id=a["renovadora"]
                #             i.save()
                #             break
                #     else:
                #         active=CubiertaLlanta.objects.get(id=i.id)
                #         active.activo=False
                        # active.save()
                # for a in json.loads(data["objeto"]):
                    
              
            return JsonResponse({"status":200,"url":self.success_url})
            
        except Exception as e:
            print(e)
            messages.error(self.request, 'Ha ocurrido un error.')
            return HttpResponseRedirect(self.success_url)

    # def form_invalid(self, form):
    #     messages.warning(self.request, form.errors)
    #     return super().form_invalid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # import pdb; pdb.set_trace()
    #     id =  self.kwargs['pk']
    #     context['instance'] = Llanta.objects.filter(pk=id).first()
    #     context['update'] = True
    #     return context


class LlantaDeleteView(LoginRequiredMixin, ValidateMixin,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_llanta"]
    
    def post(self, request, *args, **kwargs):
        id_llanta = self.kwargs['pk']
        llanta = Llanta.objects.get(pk=id_llanta)
        llanta.changed_by=request.user
        llanta.eliminado = True
        llanta.save()
        data={"status":200}
        return JsonResponse(data,safe=False)
    
from datetime import date
from datetime import datetime
from time import strptime
class VehiculosListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/Catalogos/vehiculos.html'
    model = Vehiculo
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_vehiculo"]
    success_url=reverse_lazy("Web:inicio")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
     
    
    
    def post(self,request,*args, **kwargs):
        try:
            start_date=self.request.POST["start_date"]
            end_date=self.request.POST["end_date"]
            placa=self.request.POST["placa"]
            modelo=self.request.POST["modelo"]

            marca=self.request.POST["marca"]

            search=Vehiculo.objects.filter(eliminado=False)    
            if marca:
                search=Vehiculo.objects.filter(eliminado=False,modelo_vehiculo__marca_vehiculo_id=marca)

                if modelo:
                    search=Vehiculo.objects.filter(eliminado=False,modelo_vehiculo__marca_vehiculo_id=marca,modelo_vehiculo_id=modelo)
                    
            elif placa:
                search=Vehiculo.objects.filter(placa=placa)
            elif start_date and end_date:
                search=Vehiculo.objects.filter(created_at__range=[start_date,end_date],eliminado=False)
                if start_date==end_date:     
                    search=Vehiculo.objects.filter(created_at__contains=start_date,eliminado=False)

            data=[]
            for i in search:
                item=i.toJSON2()
                data.append(i.toJSON2())
            return JsonResponse(data,safe=False)

           
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['marca'] = MarcaVehiculo.objects.filter().values("id",'descripcion')

        context['placa'] = Vehiculo.objects.filter(eliminado=False).values("placa","id")

        return context


class VehiculoCreateView(LoginRequiredMixin, ValidateMixin,CreateView):
    form_class = VehiculoForm
    template_name = 'Web/Catalogos/vehiculo.html'
    success_url = reverse_lazy("Web:vehiculos")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_vehiculo"]
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_vehiculo'] = MarcaVehiculo.objects.filter().values("id",'descripcion',"activo","eliminado")
        context['ubicacion'] = Lugar.objects.filter().values("id",'descripcion',"activo","eliminado")
        return context
    
class VehiculoUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = VehiculoForm
    model = Vehiculo
    template_name = 'Web/Catalogos/vehiculo.html'
    success_url = reverse_lazy("Web:vehiculos")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_vehiculo"]
    context_object_name="obj"
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.changed_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # import pdb; pdb.set_trace()
        context['marca_vehiculo'] = MarcaVehiculo.objects.filter().values("id",'descripcion',"activo","eliminado")
        context['ubicacion'] = Lugar.objects.filter().values("id",'descripcion',"activo","eliminado")
        context['montado'] = Llanta.objects.filter(vehiculo=self.get_object(),repuesto=False).count()

        context['update'] = True
        return context


class VehiculoDeleteView(LoginRequiredMixin, ValidateMixin,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_vehiculo"]

    def post(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = Vehiculo.objects.get(pk=id)
        obj.changed_by=request.user
        obj.eliminado = True
        obj.save()
        data={"status":200}
        return JsonResponse(data,safe=False)


def RenderOptionVehiculo(request):
    id_marca = request.GET.get('id_marca')
    if id_marca!="":
        id_marca = request.GET.get('id_marca')
        modelos = ModeloVehiculo.objects.filter(marca_vehiculo__pk=id_marca)
        return HttpResponse(json.dumps(list(modelos.values('id','descripcion',"activo","eliminado"))), content_type="application/json")

    else:
        return JsonResponse({"response":"seleccione marca"},safe=False)
class VerVehiculoView(LoginRequiredMixin, ValidateMixin,TemplateView):
    template_name = 'Web/Catalogos/ver_vehiculo.html'
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_vehiculo"]
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    # def get(self,request,*args, **kwargs):
    #     context=Vehiculo.objects.values("placa","id")
    #     return render(self.request,self.template_name,{"drop":context})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        obj = Vehiculo.objects.get(pk=id)
        u=obj.llantas.filter(eliminado=0,activo=True).order_by("posicion")
        posiciones=PosicionesLlantas.objects.filter(tipo_id=obj.tipo_vehiculo.id).order_by("posicion")
    
        # nrollantas=obj.tipo_vehiculo.nro_llantas
        # nrorepuesto=obj.nro_llantas_repuesto
        # pos ,posrep,faltantes ,faltantesrep= [],[],[],[]
        # sum=0
        # nro_llantas = len(u)
        # total=nrollantas+nrorepuesto
        # for i in range(0,nro_llantas):
        #     if u[i].repuesto==True:
        #         posrep.append(u[i].posicion)
           
        
        # for i in range(1,nrollantas+1):
        #     if not i in pos:
        #         faltantes.append(i)
        
  
        # for i in range(nrollantas+1,total+1):
        #     if not i in posrep:
        #         faltantesrep.append(i)    
        
        # data1=[]
        # data2=[]
        # al={}
        # al2={}
        # if len(faltantes)!=0:
            
        #     for i in range(0,len(faltantes)):
        #         al["posicion"]=faltantes[i]
        #         al["id"]=i+nro_llantas
        #         al["repuesto"]=False
        #         data1.append(al)
        #         al={}
        #         sum=sum+1
        # for i in range(0,len(faltantesrep)):
        #     al2["posicion"]=faltantesrep[i]
        #     al2["id"]=i+sum+nro_llantas
        #     al2["repuesto"]=True
        #     data2.append(al2)
        #     al2={}
        context['obj'] =obj
        context["posiciones"]=posiciones
        context["tipo"]=TipoVehiculo.objects.get(pk=obj.tipo_vehiculo.id)
        context["llantas"]=u
        # context["faltantesRe"]=data2
        # context["faltantes"]=data1
        context["ubicaciones"]=Ubicacion.objects.filter(eliminado=0,activo=True).values("id","descripcion")
        return context


class DetalleLlantaView(LoginRequiredMixin,DetailView):
    model = Llanta
    template_name = "Web/Operaciones/detalle_llanta.html"
    context_object_name="obj"
def getLlanta(request):
    if request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        qs = Llanta.objects.get(id=int(post)).toJSON()
        return JsonResponse(qs, content_type='application/json')
def getVehiculo(request):
    if request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        qs = Vehiculo.objects.get(id=post["id"])
        qs_json = serializers.serialize('json', [qs],  use_natural_foreign_keys=True,use_natural_primary_keys=True)
        return HttpResponse(qs_json, content_type='application/json')
def AnchoBandaRenovaSearch(request):
    template_name="Web/Catalogos/buscarrenova.html"
    product=MarcaRenova.objects.filter(eliminado=False,activo=True).values("id","descripcion","activo")
    contexto={"obj":product}
    return render(request,template_name,contexto)
def getTipo(request,id):
    obj=TipoVehiculo.objects.filter(id=id)
    if obj.exists:
        data2=[]
        data2.append(obj.first().toJSON())
        data={"status":200,"response":data2}
    else:
        data={"status":500}
    return JsonResponse(data,safe=False)
def LlantaSearch(request):
    template_name="Web/Catalogos/buscarLlanta.html"
    llantas=Llanta.objects.filter(vehiculo=None,activo=True,eliminado=False)
    contexto={"obj":llantas}
    return render(request,template_name,contexto)
def view_condicion(request):
    template_name="Web/Catalogos/condicion.html"
    return render(request,template_name)

def view_renova(request):
    template_name="Web/Catalagos/reencauchado.html"
    form=CubiertaForm()
    context={"form":form}
    return render(request,template_name,context)
class AgregarLlantaCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = LlantaForm
    template_name = 'Web/add_llanta.html'
    action = ACCION_NUEVO
    vehiculo = None
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_llanta"]

    def get_object(self, pk):
        try:
            return Vehiculo.objects.get(pk=pk)
        except Vehiculo.DoesNotExist:
            raise Http404()

    def dispatch(self, *args, **kwargs):
        id = self.kwargs['pk']
        self.vehiculo = self.get_object(id)
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.codigo = instance.code
        instance.vehiculo = self.vehiculo
        instance.changed_by = self.request.user
        instance.save()
        messages.success(self.request, 'Se agrego la llanta correctamente..')
        return HttpResponseRedirect(reverse('Web:ver-vehiculo', kwargs={'pk':self.vehiculo.pk}))

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehiculo'] = self.vehiculo
        return context
from .constanst import  CHOICES_OBSERVACION,CHOICES_ACCION
from django.db import transaction

class DesmontajeLlantaView(LoginRequiredMixin,ValidateMixin,TemplateView):
    template_name = "Web/Operaciones/desmontaje_llanta.html"
    permission_required=["Web.view_movimientos_historial"]

    def get(self,request,*args, **kwargs):
        context={"obs":CHOICES_OBSERVACION,"obj":request.GET,"estado":CHOICES_ESTADO_LLANTA}
        return render(self.request,self.template_name,context)
    def post(self,request,*args, **kwargs):
        try:
            llanta=Llanta.objects.filter(id=request.POST["llanta"])
            if llanta.exists():
                with transaction.atomic():

                    objeto=llanta.first()
                    objeto.vehiculo=None
                    objeto.posicion=None
                    objeto.estado=request.POST["estado"]
                    objeto.repuesto=False

            
                    objeto.ubicacion_id=request.POST["ubicacion"]
                    objeto.save()
                    historial=Movimientos_Historial()
                    historial.llanta=objeto
                    historial.km=request.POST["kilometros"]
                    historial.estado=request.POST["estado"]
                    historial.obs=request.POST["obs"]
                    if request.POST["repuesto"]=="true":
                        historial.posicion="R"

                    else:
                        historial.posicion=request.POST["posicion"]

                    historial.vehiculo_id=request.POST["vehiculo"]
                    historial.profundidad=request.POST["profundidad"]
                    historial.changed_by=self.request.user
                    historial.ubicacion_id=request.POST["ubicacion"]

                    historial.save()
                    # ins=InpeccionLlantas.objects.get(vehiculo_id=request.POST["vehiculo"])
                    
                    # det=DetalleInspeccion.objects.get(inspeccion=ins,posicion=request.POST["posicion"])
                    # det.delete()
                    response={"status":200}
            else:
                response={"status":500,"message":"Esa llanta no existe."}

            return JsonResponse(response,safe=False)
        except Exception as e:
            print(e)
            messages.error(self.request, 'Ha ocurrido un error.')
            return HttpResponseRedirect(reverse_lazy("Web:inicio"))
class MontajeLlantasView(LoginRequiredMixin,TemplateView):
    template_name = "Web/Operaciones/montaje_llanta.html"
    permission_required=["Web.view_movimientos_historial"]

    def get(self,request,*args, **kwargs):
        llanta=Llanta.objects.filter(vehiculo=None,activo=True,eliminado=False)
        return render(self.request,self.template_name,{"obj":request.GET,"llanta":llanta})
    def post(self,request,*args, **kwargs):
        try:
            llanta=Llanta.objects.filter(id=request.POST["llanta"])
            if llanta.exists():
                with transaction.atomic():
                    if request.POST["repuesto"]=="1":
                        rep=True
                        pos="R"
                    else:
                        rep=False
                        pos=request.POST["posicion"]
                    
                    objeto=llanta.first()
                    objeto.ubicacion_id=1
                    objeto.km=request.POST["kilometros"]
                    objeto.vehiculo_id=request.POST["vehiculo"]
                    objeto.repuesto=rep
                    objeto.posicion=request.POST["posicion"]

                    objeto.save()
                    historial=Movimientos_Historial()
                    historial.llanta=objeto
                    historial.km=request.POST["kilometros"]
                    historial.posicion=pos
                  
                    historial.vehiculo_id=request.POST["vehiculo"]
                    historial.profundidad=request.POST["profundidad"]
                    historial.changed_by=self.request.user
                    historial.ubicacion_id=None
                    historial.save()
                    # ins,p=InpeccionLlantas.objects.get_or_create(vehiculo_id=request.POST["vehiculo"])
                    # detalle=DetalleInspeccion()
                    # detalle.inspeccion=ins
                    # detalle.posicion=request.POST["posicion"]
                    # if request.POST["repuesto"]=="1":
                    #     detalle.repuesto=True
                    # else:
                    #     detalle.repuesto=False
                    # detalle.llanta=objeto
                    # detalle.save()
                    response={"status":200,"id":objeto.id,"codigo":objeto.codigo,"posicion":request.POST["posicion"]}
            else:
                response={"status":500,"message":"Esa llanta no existe."}

            return JsonResponse(response,safe=False)
        except Exception as e:
            print(e)
            messages.error(self.request, 'Ha ocurrido un error.')
            return HttpResponseRedirect(reverse_lazy("Web:inicio"))
class HojaDeMovimientosView(LoginRequiredMixin,ValidateMixin,TemplateView):
    template_name="Web/Operaciones/hoja_movimientos.html"   
    permission_required=["Web.view_movimientos_historial"]

    def post(self,request,*args, **kwargs):
        data,posicion=[],[]
        post = json.loads(request.body.decode("utf-8"))

        if(post["id"]!=""):
            ve=Vehiculo.objects.get(id=post["id"])
            qs = ve.toJSON()
         
            nm = Llanta.objects.filter(vehiculo=post["id"]).order_by("posicion")
            pos=PosicionesLlantas.objects.filter(tipo_id=ve.tipo_vehiculo.id).order_by("posicion")
            for i in nm:
                lala=i.toJSON()
                data.append(lala)   
            for i in pos:
                posicion.append(i.toJSON())
            return JsonResponse({"status":200,"vehiculo":qs,"llantas":data,"pos":posicion},safe=False, content_type='application/json')
        return JsonResponse({"status":303},safe=False, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(HojaDeMovimientosView, self).get_context_data(**kwargs)
        context["placa"]=Vehiculo.objects.values("id","placa").filter(eliminado=False,activo=True)
        context["ubicaciones"]=Ubicacion.objects.filter(eliminado=False,activo=True)
        return context
class InspeccionLlantasView(LoginRequiredMixin,ValidateMixin,TemplateView):
    permission_required=["Web.view_inpeccionllantas"]

    template_name="Web/Operaciones/inspeccion_llantas.html"
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request,*args, **kwargs):
        try:
            post = json.loads(request.body.decode("utf-8"))

            llanta=Llanta.objects.filter(vehiculo_id=post["id"])
            obj,p=InpeccionLlantas.objects.get_or_create(vehiculo_id=post["id"])
            if p:
                for i in llanta:
                    det=DetalleInspeccion()
                    det.inspeccion=obj
                    det.llanta_id=i.id
                    det.save()
            data=[]
            for i in DetalleInspeccion.objects.filter(inspeccion=obj.id).order_by("llanta__posicion"):
                data.append(i.toJSON())
            
        
            
            return JsonResponse({"response":data,"id":obj.id},safe=False)
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)
   
    def get_context_data(self, **kwargs):
        context = super(InspeccionLlantasView, self).get_context_data(**kwargs)
        context["placa"]=Vehiculo.objects.values("id","placa").filter(eliminado=False,activo=True)
        return context
class InsepccionDetalleView(LoginRequiredMixin,ValidateMixin,UpdateView):
    permission_required=["Web.view_inpeccionllantas"]

    model=InpeccionLlantas
    template_name="Web/Operaciones/inspeccion_detalles.html"
    context_object_name="obj"
    form_class=InspeccionForm
   
    def dispatch(self,request,*args, **kwargs):

        return super().dispatch(request,*args,**kwargs)
    def get_details_product(self):
        data=[]
        try:
            for i in DetalleInspeccion.objects.filter(inspeccion=self.get_object().id):
                item=i.toJSON()
               
                data.append(item)
        except:
            pass
        return data
    def get(self,*args, **kwargs):
        detail=DetalleInspeccion.objects.filter(inspeccion=self.get_object()).order_by("llanta__posicion")
        user=Usuario.objects.filter(groups__name="Administrador").select_related("persona")
        det=json.dumps(self.get_details_product())

        context={"det":det,"user":user,"obj":self.get_object(),"form":self.form_class,"detail":detail,"obs":CHOICES_OBSERVACION,"accion":CHOICES_ACCION,"cubierta":CHOICES_CUBIERTA_INSPECCION,"operacion":CHOICES_OPERACION}
        return render(self.request,self.template_name,context)
    def post(self,*args, **kwargs):
        try: 
            with transaction.atomic():
                objeto=json.loads(self.request.POST["objeto"])
                inspeccion=self.get_object()
                inspeccion.fech_ins=datetime.strptime(self.request.POST["fech_ins"], '%Y-%m-%d').date()
                inspeccion.km_act=self.request.POST["km_act"]
                inspeccion.km_ult=self.request.POST["km_ult"]
                inspeccion.fech_km_ant=datetime.strptime(self.request.POST["fech_km_ant"], '%Y-%m-%d').date()
                inspeccion.km_re=self.request.POST["km_re"]
                inspeccion.supervisor_id=self.request.POST["supervisor"]
                inspeccion.tecnico_id=self.request.POST["tecnico"]
                inspeccion.operacion=self.request.POST["operacion"]

                inspeccion.save()
                inspeccion.detalleinspeccion_set.all().delete()

                for i in objeto:
                    data=DetalleInspeccion()
                    data.inspeccion_id=self.get_object().id
                    data.llanta_id=i["llanta"]
                    data.posicion=i["posicion"]
                    data.cubierta=i["cubierta"]
                    data.rem1=i["rem1"]
                    data.rem2=i["rem2"]
                    data.rem3=i["rem3"]
                    data.rem_prom=i["rem_prom"]
                    data.rem_max=i["rem_max"]
                    data.rem_min=i["rem_min"]
                    data.pres_fin=i["pres_fin"]
                    data.pres_ini=i["pres_ini"]
                    data.obs=i["obs"]
                    if i["repuesto"]=="1":
                        data.repuesto=True
                    else:
                        data.repuesto=False
                    data.accion=i["accion"]
                    data.save()
                return JsonResponse({"response":200},safe=False)
     
        except Exception as e:
            messages.error(self.request, 'Ha ocurrido un error.')
            return HttpResponseRedirect(reverse_lazy("Web:inicio"))
def AgregarInspeccion(request):
    template_name="Web/Operaciones/inspeccion-agregar.html"
    context={"obs":CHOICES_OBSERVACION,"accion":CHOICES_ACCION,"cubierta":CHOICES_CUBIERTA_INSPECCION}

    return render(request,template_name,context)
class HistorialLlantas(LoginRequiredMixin,ListView):
    template_name="Web/reportes/historial.html"
    model=Movimientos_Historial
from django.db import IntegrityError, transaction

class AbastecimientoView(LoginRequiredMixin,CreateView):
    template_name="Web/Combustible/abastecimiento.html"
    model=Abastecimiento
    form_class=AbastecimientoForm  
    def dispatch(self, request, *args, **kwargs):
        if request.method =="POST":
            self.data=json.loads(request.POST["objeto"])
            self.placas=[]
            self.vouchers=[]
            self.facturas=[]
            self.contador=0
            self.contador_v=0
            self.contador_f=0
            self.tramo=request.POST["tramo"]

            for k in self.data:
                
                self.modelo=Vehiculo.objects.get(id=k["placa"]["descripcion"])
                self.rend=Rendimiento.objects.filter(tramo=request.POST["tramo_id"],modelo=self.modelo.modelo_vehiculo)
                self.exist_placa=DetalleAbastecimiento.objects.filter(placa=self.modelo)
                self.exist_voucher=DetalleAbastecimiento.objects.filter(voucher=k["voucher"])
                self.exist_factura=DetalleAbastecimiento.objects.filter(factura=k["factura"])

                print( self.exist_placa.order_by("abast__fecha").query)
                if self.exist_placa.exists():
                    self.exist_fecha=self.exist_placa.order_by("abast__fecha").last()
                    if datetime.strptime(request.POST["fecha"], '%Y-%m-%d').date()<= self.exist_fecha.abast.fecha:
                        return JsonResponse({"status":500,"form":{"fecha":["La fecha ingresada es menor o igual a la del último abastecimiento registrado de una de las placas en la tabla."]}})
                if not self.rend.exists():
                    self.contador+=1
                    self.placas.append(self.modelo.placa)
                if self.exist_voucher.exists():
                    self.contador_v+=1
                    self.vouchers.append(k["voucher"])
                if self.exist_factura.exists():
                    self.contador_f+=1
                    self.facturas.append(k["factura"])
            if self.contador>0:
                return JsonResponse({"status":500,"form":{"rendimiento":[f"No se ha configurado un rendimiento para las placas {','.join(self.placas)} y el tramo {self.tramo}."]}})
            if self.contador_v>0:
                return JsonResponse({"status":500,"form":{"voucher":[f"Los voucher {','.join(self.vouchers)} ya se han registrado!."]}})
            if self.contador_f>0:
                return JsonResponse({"status":500,"form":{"factura":[f"Las facturas {','.join(self.facturas)} ya se han registrado!."]}})

        return super().dispatch(request, *args, **kwargs)
        
    def post(self,request,*args, **kwargs):
        try:
            with transaction.atomic():

                form=self.form_class(request.POST)
                if form.is_valid():
                    viaje=Viaje.objects.filter(ruta=request.POST["ruta"],estado=True)
                    if viaje.exists():
                    
                            
                        abast=Abastecimiento()
                        abast.viaje=viaje.get()
                        
                        abast.estacion_id=request.POST["estacion"]
                        abast.fecha=request.POST["fecha"]
                        abast.tipo_id=request.POST["tipo"]
                        abast.tramo=request.POST["tramo"]
                        abast.estado_viaje_id=request.POST["estado_viaje"]
                        abast.producto_id=request.POST["producto"]
                        abast.precio=request.POST["precio"]
                        abast.estado=True
                        abast.changed_by=self.request.user
                        abast.save()
                        for k in self.data:

                            date_time_str = k["hora"]
                            date_time_obj = datetime.strptime(date_time_str, '%H:%M')
                            det_abast=DetalleAbastecimiento()
                            det_abast.abast=abast
                            det_abast.hora=k["hora"]
                            det_abast.placa_id=k["placa"]["descripcion"]
                            det_abast.km=k["km"]
                            det_abast.volumen=float(k["volumen"])
                            det_abast.total=k["total"]
                            det_abast.conductor_id=k["conductor"]
                            det_abast.cargado=k["cargado"]["valor"]
                            modelo_placa=Vehiculo.objects.get(id=k["placa"]["descripcion"])

                            rendimiento=Rendimiento.objects.filter(tramo=request.POST["tramo_id"],modelo=modelo_placa.modelo_vehiculo)
                            if request.POST["tipo"]=="1" and k["cargado"]["id"]!=0:
                               
                                afectacion=AfectacionConsumo.objects.filter(pk=k["cargado"]["id"]).get()

                                det_abast.afectacion=afectacion.afectacion
                                det_abast.gal_obj=float(rendimiento.get().gal_abast)*(1+afectacion.afectacion/100)
                                det_abast.recorrido_obj=rendimiento.get().km

                            elif request.POST["tipo"]=="2" or k["cargado"]["id"]==0:
                                det_abast.recorrido_obj=rendimiento.get().km
                                det_abast.gal_obj=rendimiento.get().gal_abast
                            det_abast.voucher=k["voucher"]
                            det_abast.factura=k["factura"]
                            det_abast.save()
                    else:

                        nuevo_viaje=Viaje()
                        nuevo_viaje.ruta_id=request.POST["ruta"]
                        nuevo_viaje.estado=True
                        nuevo_viaje.changed_by=request.user
                        nuevo_viaje.save()
                        nuevo_abast=Abastecimiento()
                        nuevo_abast.viaje=nuevo_viaje
                        nuevo_abast.estacion_id=request.POST["estacion"]
                        nuevo_abast.fecha=request.POST["fecha"]
                        nuevo_abast.tipo_id=request.POST["tipo"]
                        nuevo_abast.tramo=request.POST["tramo"]
                        nuevo_abast.estado_viaje_id=request.POST["estado_viaje"]
                        nuevo_abast.producto_id=request.POST["producto"]
                        nuevo_abast.precio=request.POST["precio"]
                        nuevo_abast.estado=True
                        nuevo_abast.changed_by=self.request.user
                        nuevo_abast.save()
                        for k in self.data:

                            date_time_str = k["hora"]
                            date_time_obj = datetime.strptime(date_time_str, '%H:%M')
                            nuevo_det_abast=DetalleAbastecimiento()
                            nuevo_det_abast.abast=nuevo_abast
                            nuevo_det_abast.hora=k["hora"]
                            nuevo_det_abast.placa_id=k["placa"]["descripcion"]
                            nuevo_det_abast.km=k["km"]
                            nuevo_det_abast.volumen=float(k["volumen"])
                            nuevo_det_abast.total=k["total"]
                            nuevo_det_abast.conductor_id=k["conductor"]
                            nuevo_det_abast.cargado=k["cargado"]["valor"]
                            modelo_placa=Vehiculo.objects.get(id=k["placa"]["descripcion"])

                            rendimiento=Rendimiento.objects.filter(tramo=request.POST["tramo_id"],modelo=modelo_placa.modelo_vehiculo)
                            if request.POST["tipo"]=="1" and k["cargado"]["id"]!=0:
                              

                                afectacion=AfectacionConsumo.objects.filter(pk=k["cargado"]["id"]).get()

                                nuevo_det_abast.afectacion=afectacion.afectacion
                                nuevo_det_abast.gal_obj=float(rendimiento.get().gal_abast)*(1+afectacion.afectacion/100)
                                nuevo_det_abast.recorrido_obj=rendimiento.get().km
                            elif  request.POST["tipo"]=="2" or k["cargado"]["id"]==0:
                                nuevo_det_abast.recorrido_obj=rendimiento.get().km
                                nuevo_det_abast.gal_obj=rendimiento.get().gal_abast
                            nuevo_det_abast.voucher=k["voucher"]
                            nuevo_det_abast.factura=k["factura"]
                            nuevo_det_abast.save()
                           
                    return JsonResponse({"status":200},safe=False)
                else:
                    return JsonResponse({"status":500,"form":form.errors},safe=False)

        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["placa"] =Vehiculo.objects.values("id","placa","activo","eliminado").filter(activo=True) 
        context["ruta"]=Ruta.objects.values("id","ruta").filter(estado=True)
        context["conductor"]=Conductor.objects.values("id","nombres").filter(estado=True)
        context["tipo"]=TipoAbastecimiento.objects.values("id","descripcion")
        context["estado"]=EstadoViaje.objects.values("id","descripcion")
        context["afectacion"]=AfectacionConsumo.objects.values("id","afectacion","per_carga")

        return context
class RendimientoView(LoginRequiredMixin,CreateView):
    template_name="Web/Combustible/rendimiento.html"
    model=Rendimiento
    form_class=RendimientoForm
    def dispatch(self, request, *args, **kwargs):
        if request.method =="POST":
            self.data=json.loads(request.POST["objeto"])
            for i in self.data:
                rendimiento=Rendimiento.objects.filter(modelo=request.POST["modelo_vehiculo"],tramo__id=i["tramo"])
                if rendimiento.exists():
                    return JsonResponse({"status":500,"form":{"tramo":["Hay un tramo que ya se ingresó para este modelo de vehículo.Revise la tabla!"]}})
        return super().dispatch(request, *args, **kwargs)
    

    def post(self,request,*args, **kwargs):
        try:        
 
            for i in self.data:
                nuevo=Rendimiento()
                nuevo.tramo_id=i["tramo"]
                nuevo.fech_hora=request.POST["fech_hora"]
                nuevo.modelo_id=request.POST["modelo_vehiculo"]
                nuevo.changed_by=request.user
                nuevo.km=int(i["recorrido"])
                nuevo.gal_abast=float(i["galones_abast"])
                nuevo.rend_vacio =float(i["rend_objetivo"])
                nuevo.save()
            return JsonResponse({"status":200},safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_vehiculo'] = MarcaVehiculo.objects.filter().values("id",'descripcion',"activo","eliminado")
        context["ruta"]=Ruta.objects.values("id","ruta").filter(estado=True)
        return context
class RendimientoListView(LoginRequiredMixin,TemplateView):
    model=Rendimiento
    template_name="Web/Combustible/rendimiento.html"
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in Rendimiento.objects.filter(estado=True):
                    data.append(i.toJSON())
            else:
                data["error"]="Ha ocurrido un error"
            return JsonResponse(data,safe=False)

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url) 
class RendimientoEditView(LoginRequiredMixin,UpdateView):
    model=Rendimiento
    template_name="Web/Combustible/rendimiento_editar.html"
    context_object_name="obj"
    form_class=RendimientoForm
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST,instance=self.get_object())
            if form.is_valid():
                self.object=self.get_object()
                self.object.modelo_id=request.POST["modelo"]
                self.object.fech_hora=request.POST["fech_hora"]
                self.object.tramo_id=request.POST["tramo"]
                self.object.km=request.POST["km"]
                self.object.gal_abast=request.POST["gal_abast"]
                self.object.rend_vacio=float(request.POST["km"])/float(request.POST["gal_abast"])
                self.object.save()
                data={"status":200}
            else:
                data={"status":500,"form":form.errors}
            
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["marca_vehiculo"] = MarcaVehiculo.objects.filter().values("id",'descripcion',"activo","eliminado")
        context["ruta"]=Ruta.objects.filter(estado=True)
        return context
    
class FlotaView(LoginRequiredMixin,TemplateView):
    template_name="Web/Combustible/flota.html"
    def post(self,request,*args, **kwargs):
        try:
            Vehiculo.objects.filter(id=request.POST["placa"]).update(empresa=request.POST["empresa"])
            data={"status":200}
           
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["placa"] =Vehiculo.objects.values("id","placa","activo").filter(activo=True,empresa=None) 
        context["empresa"]=Empresa.objects.values("id","nombre")
        return context
    
class FlotaListView(LoginRequiredMixin,TemplateView):
    model=Vehiculo
    template_name="Web/Combustible/flota.html"
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in Vehiculo.objects.filter(activo=True).exclude(empresa=None):
                    data.append(i.toJSON_flota())
            else:
                data["error"]="Ha ocurrido un error"
            return JsonResponse(data,safe=False)

        except Exception as e:
            print(e)
            return JsonResponse({"status":500},safe=False)

class FlotaEditView(LoginRequiredMixin,UpdateView):
    model=Vehiculo
    template_name="Web/Combustible/flota_editar.html"
    context_object_name="obj"
    form_class=ConductoresForm
    def post(self,request,*args, **kwargs):
        try:
            self.object=self.get_object()
            self.object.empresa_id = request.POST["empresa"]
            self.object.save()
            data={"status":200}
            
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context["tip_doc"] = CHOICES_TIPO_DOC2
        context["placa"] =Vehiculo.objects.values("id","placa","activo").filter(activo=True,empresa=None) 
        context["empresa"]=Empresa.objects.values("id","nombre")

        return context
class RutasListView(LoginRequiredMixin,TemplateView):
    model=Ruta
    template_name="Web/Combustible/ruta.html"
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in Ruta.objects.filter(estado=True):
                    data.append(i.toJSON())
            else:
                data["error"]="Ha ocurrido un error"
            return JsonResponse(data,safe=False)

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url) 
class RutaView(LoginRequiredMixin,CreateView):
    model=Ruta
    template_name="Web/Combustible/ruta.html"
    form_class=Rutaform
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST)
            
            if form.is_valid():
                instance=form.save(commit=False)
                instance.changed_by=request.user
                instance.save()
                js=json.loads(request.POST["objeto"])
                print(js)
                tramo_completo=[]
                formato=[]
                ids=[]
                for x,i in enumerate(js):
                    
                    tramo=Tramo()
                    for a in i["descripcion"]:
                        selected=a.split("-")
                        tramo_completo.append(selected[2])  
                        ids.append(selected[0])  
                        formato.append(selected[1])
                    selected_tramo = '-'.join(map(str,tramo_completo)) 
                    selected_ids = '-'.join(map(str,ids)) 
                    selected_type = '-'.join(map(str,  formato))
                    tramo.descripcion=selected_tramo
                    tramo.ruta=instance
                    tramo.changed_by=request.user
                    tramo.formato=selected_type
                    tramo.ids=selected_ids
                    tramo.state=1 if x==0 else 2
                        
                    tramo.save()
                    tramo_completo=[]
                    formato=[]
                    ids=[]

                data={"status":200}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["placa"] =Vehiculo.objects.values("id","placa","activo").filter(activo=True)
        dep=Departamento.objects.values_list("id","descripcion","code","descripcion")
        pro=Provincia.objects.values_list("id","descripcion","code","departamento__descripcion")
        dis=Distrito.objects.values_list("id","descripcion","code","provincia__descripcion")
        context["ubicacion"]=(dep.union(pro,dis).order_by("code","descripcion"))
       
        return context
class RutaEditView(LoginRequiredMixin,TemplateView):
    model=Ruta
    template_name="Web/Combustible/ruta_editar.html"
    def get(self,request,**kwargs):
        data=[]
        objeto={"id":"","descripcion":[]}
        tramos=Tramo.objects.filter(ruta=kwargs["pk"])
       
        for j,i in enumerate(tramos):
            ids_array=i.ids.split("-")
            format_array=i.formato.split("-")
            tramo_array=i.descripcion.split("-")
            
            data_list=[]
            for k in range(len(ids_array)):
                code=ids_array[k]+"-"+format_array[k]+"-"+tramo_array[k]

                data_list.append(code)
            objeto["descripcion"]=data_list
            objeto["id"]=i.pk
            data.append(objeto)
            objeto={"id":"","descripcion":[]}
        dep=Departamento.objects.values_list("id","descripcion","code","descripcion")
        pro=Provincia.objects.values_list("id","descripcion","code","departamento__descripcion")
        dis=Distrito.objects.values_list("id","descripcion","code","provincia__descripcion")
        ubicacion=(dep.union(pro,dis).order_by("code","descripcion"))
        return render(self.request,self.template_name,{"tramo":data,"ruta":kwargs["pk"],"ubicacion2":ubicacion})
    def post(self,request,*args, **kwargs):
        try:
           
            js=json.loads(request.POST["objeto"])
            tramo_completo=[]
            formato=[]
            ids=[]
            for x,i in enumerate(js):
                
                if i["id"]!=0:
                    update=Tramo.objects.get(id=i["id"])
                    update.state=1 if x==0 else 2
                    for a in i["descripcion"]:
                        selected=a.split("-")
                        tramo_completo.append(selected[2])  
                        ids.append(selected[0])  
                        formato.append(selected[1])
                    selected_tramo = '-'.join(map(str,tramo_completo)) 
                    selected_ids = '-'.join(map(str,ids)) 
                    selected_type = '-'.join(map(str,  formato))
                    update.descripcion=selected_tramo
                    update.formato=selected_type
                    update.ids=selected_ids
                    update.state=1 if x==0 else 2
                    update.save()
                    tramo_completo=[]
                    formato=[]
                    ids=[]
                    
                else:
                    create=Tramo()
                    create.ruta_id=kwargs["pk"]
                    for a in i["descripcion"]:
                        selected=a.split("-")
                        tramo_completo.append(selected[2])  
                        ids.append(selected[0])  
                        formato.append(selected[1])
                    selected_tramo = '-'.join(map(str,tramo_completo)) 
                    selected_ids = '-'.join(map(str,ids)) 
                    selected_type = '-'.join(map(str,  formato))
                    create.descripcion=selected_tramo
                    create.formato=selected_type
                    create.ids=selected_ids
                    create.state=1 if x==0 else 2
                    create.changed_by=self.request.user
                    create.save()
                    tramo_completo=[]
                    formato=[]
                    ids=[]
                    
            data={"status":200,"ruta":kwargs["pk"]}
        
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
 
def getVehiculo(request,id): 
    data=Vehiculo.objects.get(id=id)
    return JsonResponse(data.toJSON3())
class EstacionesView(LoginRequiredMixin,CreateView):
    model=Estaciones
    form_class=EstacionesForm
    template_name="Web/Combustible/estaciones.html"
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.changed_by=request.user
                instance.save()
                for i in json.loads(request.POST["producto"]):
                    product=EstacionProducto()
                    product.producto_id=i["producto"]
                    product.precio=i["precio"]
                    product.estacion=instance
                    product.save()
                data={"status":200,"id":instance.id,"descripcion":instance.descripcion}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["producto"] = Producto.objects.filter(estado=True)
        context["eess"]=Estaciones.objects.filter(estado=True)
        context["departamento"]=Departamento.objects.all()
        context["unidad"]=UnidadMedida.objects.filter(estado=True)
        return context
    
class EmpresaCreateView(LoginRequiredMixin,CreateView):
    template_name="Web/Combustible/empresa.html"
    model=Empresa
    form_class=EmpresaForm
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.changed_by=request.user
                instance.save()
                data={"status":200,"id":instance.id,"nombre":instance.nombre}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
class ProductosListView(LoginRequiredMixin,ListView):
    template_name = 'Web/Combustible/estaciones.html'
    model = Producto
    login_url=reverse_lazy("Web:login")
    success_url=reverse_lazy("Web:productos")
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in Producto.objects.filter(estado=True):
                    data.append(i.toJSON())
            else:
                data["error"]="Ha ocurrido un error"
            return JsonResponse(data,safe=False)

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

class ProductoCreateView(LoginRequiredMixin,CreateView):
    template_name="Web/Combustible/producto.html"
    model=Producto
    form_class=ProductoForm
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.changed_by=request.user
                instance.save()
                data={"status":200,"id":instance.id,"descripcion":instance.descripcion}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
class PrecioUpdateView(LoginRequiredMixin,TemplateView):
    template_name="Web/Combustible/precio_lista.html"
    model=EstacionProducto
    context_object_name="obj"
    form_class=EstacionesForm
    def dispatch(self, request, *args, **kwargs):
        self.obj=EstacionProducto.objects.filter(producto_id=kwargs["prod"],estacion_id=kwargs["eess"])

        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        return render(request,self.template_name,{"obj":self.obj.get(),"eess":kwargs["eess"],"prod":kwargs["prod"]})
    def post(self,request,*args, **kwargs):
        try:
            self.obj.update(pre_fech_ini=request.POST["pre_fech_ini"],pre_fech_fin=request.POST["pre_fech_fin"],precio=request.POST["precio_modal"])
            return JsonResponse({"status":200,"precio":self.obj.get().precio},safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
def getAllProducts(request):
    if request.method=="GET":
        p=Producto.objects.filter(estado=True)
        data=[]
        for i in p:
            data.append(i.toJSON())
        return JsonResponse({"status":200,"data":data})
def getProducts(request,id):
    p=EstacionProducto.objects.filter(estacion_id=id)
    if request.method=="GET":
        data=[]
        for i in p:
            data.append(i.toJSON())
        return JsonResponse({"status":200,"data":data})
    elif request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        for i in post:
            if i["id"]!="":
                EstacionProducto.objects.filter(id=i["id"]).update(precio=i["precio"],producto_id=i["producto"]["id"])
            else:
                es=EstacionProducto()
                es.producto_id=i["producto"]["id"]
                es.estacion_id=id
                es.precio=i["precio"]
                es.save()
        return JsonResponse({"status":200})
def getTramos(request,id):

    
    if request.method=="GET":
        data=[]
        p=Tramo.objects.filter(ruta_id=id)

        for i in p:
            data.append(i.cbo_ruta())
        res={"status":200,"data":data}
      
    else:
        res={"status":500}
    return JsonResponse(res)
def getRutas(request):
    p=Ruta.objects.filter(estado=True)
    if request.method=="GET":
        data=[]
        for i in p:
            data.append(i.cbo_ruta())
        res={"status":200,"data":data}
    else:
        res={"status":500}
    return JsonResponse(res)
def getEstaciones(request,tramo):
   
    if tramo!="0":
        tramo=Tramo.objects.get(id=tramo)
        array_formato=tramo.formato.split("-")
        array_ids=tramo.ids.split("-")
        p=Estaciones.objects.filter(Q(ubicacion__provincia__in=array_ids)|Q(ubicacion__provincia__departamento__in=array_ids)|Q(ubicacion__in=array_ids))
        if request.method=="GET":
            data=[]
            for i in p:
                data.append(i.cbo_ruta())
            res={"status":200,"data":data}
        else:
            res={"status":500}
    else:
        res={"status":500}

    return JsonResponse(res,safe=False)

def getVehiculosRuta(request,id):
    qs1=DetalleAbastecimiento.objects.filter(abast__viaje__ruta__id=id,abast__viaje__estado=True).values("placa","abast__tramo").order_by("-abast__fecha").first()
    qs=DetalleAbastecimiento.objects.filter(abast__viaje__ruta__id=id,abast__viaje__estado=True).values("placa").annotate(Count("placa"))
    if qs.exists():

        serialized_q = json.dumps(list(qs), cls=DjangoJSONEncoder)
        data={"data":serialized_q,"status":200,"tramo":qs1["abast__tramo"]}
    else:
        data={"status":500}

    return JsonResponse(data,safe=False)
class EstadoAbastecimientoCreateView(LoginRequiredMixin,CreateView):
    template_name="Web/Combustible/estado.html"
    model=EstadoViaje
    form_class=EstadoViajeForm
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.changed_by=request.user
                instance.save()
                data={"status":200,"id":instance.id,"descripcion":instance.descripcion}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
class TipoAbastecimientoCreateView(LoginRequiredMixin,CreateView):
    template_name="Web/Combustible/tipo.html"
    model=TipoAbastecimiento
    form_class=TipoAbastecimientoForm
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.changed_by=request.user
                instance.save()
                data={"status":200,"id":instance.id,"descripcion":instance.descripcion}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
class UnidadMedidaCreateView(LoginRequiredMixin,CreateView):
    template_name="Web/Combustible/unidad.html"
    model=UnidadMedida
    form_class=UnidadMedidaForm
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.changed_by=request.user
                instance.save()
                data={"status":200,"id":instance.id,"descripcion":instance.descripcion}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})

class ConductoresView(LoginRequiredMixin,CreateView):
    template_name="Web/Combustible/conductores.html"
    model=Conductor
    form_class=ConductoresForm
    # def get(self,request,*args, **kwargs):
    #     context={"tip_doc":CHOICES_TIPO_DOC2}
    #     return render(request,self.template_name,context)
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.changed_by=request.user
                instance.save()
                data={"status":200}
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["aea"] = 123
        return context
    
class ConductorListView(LoginRequiredMixin,TemplateView):
    model=Conductor
    template_name="Web/Combustible/conductores.html"
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in Conductor.objects.filter(estado=True):
                    data.append(i.toJSON())
            else:
                data["error"]="Ha ocurrido un error"
            return JsonResponse(data,safe=False)

        except Exception as e:
            print(e)
            return JsonResponse({"status":500},safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tip_doc"] = CHOICES_TIPO_DOC2
        return context
    
class ConductorEditView(LoginRequiredMixin,UpdateView):
    model=Conductor
    template_name="Web/Combustible/conductor_editar.html"
    context_object_name="obj"
    form_class=ConductoresForm
    def post(self,request,*args, **kwargs):
        try:
            form=self.form_class(request.POST,instance=self.get_object())
            if form.is_valid():
                form.save()
                data={"status":200}
            else:
                data={"status":500,"form":form.errors}
            
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context["tip_doc"] = CHOICES_TIPO_DOC2
        return context
class LiquidacionView(LoginRequiredMixin,TemplateView):
    template_name="Web/Combustible/liquidacion.html"
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            factura=self.request.POST["factura"]
            eess=self.request.POST["eess"]
            start_date=self.request.POST["start_date"]
            end_date=self.request.POST["end_date"]        
            data=[]
            newest = DetalleAbastecimiento.objects.filter(placa=OuterRef('placa'),abast__fecha__lt=OuterRef('abast__fecha')).order_by('-abast__fecha')

            qs=(DetalleAbastecimiento.objects.select_related("abast","placa","conductor","abast__tipo","abast__estacion","abast__producto","abast__estado_viaje").
                                annotate(recorrido=F("km")-Subquery(newest.values('km')[:1])).
                                 order_by("-abast__viaje","-abast__fecha"))
            # if año and factura and eess and mes:
            #     qs=qs.filter(abast__fecha__year=año,abast__fecha__month=mes,factura=factura,abast__estacion__codigo=eess)
            # elif start_date and end_date and factura:
            #     qs=qs.filter(abast__fecha__year=año,abast__fecha__month=mes,factura=fatura)
            # elif start_date and end_date and eess:
            #     qs=qs.filter(abast__fecha__year=año,abast__fecha__month=mes,abast__estacion__codigo=eess)
            # elif mes and factura and eess:
            #     qs=qs.filter(abast__fecha__month=mes,factura=fatura,abast__estacion__codigo=eess)
            # elif año and factura and eess:
            #     qs=qs.filter(abast__fecha__year=año,factura=factura,abast__estacion__codigo=eess)   
            # elif año  and mes:
            #     qs=qs.filter(abast__fecha__year=año,abast__fecha__month=mes)
            # elif año and factura:
            #     qs=qs.filter(abast__fecha__year=año,factura=factura)  
            # elif año and eess:
            #     qs=qs.filter(abast__fecha__year=año,abast__estacion__codigo=eess)
            # elif mes and factura:
            #     qs=qs.filter(abast__fecha__month=mes,factura=factura)
            # elif mes and eess:
            #     qs=qs.filter(abast__fecha__month=mes,abast__estacion__codigo=eess) 
            # elif factura and eess:
            #     qs=qs.filter(factura=factura,abast__estacion__codigo=eess)    
            # elif año:
            #     qs=qs.filter(abast__fecha__year=año)
            # elif mes:
            #     qs=qs.filter(abast__fecha__month=mes) 
            if  start_date and end_date and factura and eess:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,factura=factura,abast__estacion=eess)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],factura=factura,abast__estacion=eess)
            elif factura and eess:
                qs=qs.filter(factura=factura,abast__estacion__codigo=eess)    
            elif start_date and end_date and factura:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,factura=factura)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],factura=factura)
            elif start_date and end_date and eess:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,abast__estacion=eess)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],abast__estacion=eess)
            elif start_date and end_date:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date])

            elif factura:
                qs=qs.filter(factura=factura)
            elif eess:
                qs=qs.filter(abast__estacion=eess)         
            for i in qs:
                item=(i.get_report_liquidacion())
                item["recorrido"]=i.recorrido
                # a=i.abast.tramo.ruta.rendimiento_set.all()
                # for i in a:
                #     item["rend_vacio"]=i.rend_vacio
                #     item["rend_cargado"]=i.rend_cargado
                #     item["rend_prom"]=i.rend_prom
                #     item["rend_km"]=i.km
                data.append(item)
                print(data)
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["eess"] = Estaciones.objects.filter(estado=True)
        return context
from django.db.models import Aggregate, CharField

class GroupConcat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s%(ordering)s%(separator)s)'
    separator = '/'

    def __init__(self, expression, distinct=False, ordering=None, separator='/', **extra):
        super(GroupConcat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            ordering=' ORDER BY %s' % ordering if ordering is not None else '',
            separator=' SEPARATOR "%s"' % separator,
            output_field=CharField(),
            **extra
        )
    
from django.db.models.expressions import RawSQL,Value,ExpressionWrapper
from django.db.models import IntegerField
class RendimientoViajeView(LoginRequiredMixin,TemplateView):
    template_name="Web/Combustible/rendimiento_viaje.html"
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        print("aea")
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        try:
            data=[]
            start_date=self.request.POST["start_date"]
            end_date=self.request.POST["end_date"]     
            placa=request.POST["placa"]
            marca=request.POST["marca"]            
            empresa=request.POST["empresa"]            
            modelo=request.POST["modelo"] 
            km_prev = DetalleAbastecimiento.objects.filter(placa=OuterRef('placa'),abast__viaje=OuterRef('abast__viaje')).order_by('-abast__fecha')

            newest = DetalleAbastecimiento.objects.filter(placa=OuterRef('placa'),abast__fecha__lt=OuterRef('abast__fecha')).order_by('-abast__fecha')

            # newest = Rendimiento.objects.filter(ruta_id=OuterRef('abast__tramo__ruta'))
            qs =(DetalleAbastecimiento.objects.select_related("placa","abast__viaje","abast__tramo").
                 values("placa__modelo_vehiculo__descripcion","placa__placa","placa__modelo_vehiculo__marca_vehiculo__descripcion",
                        "placa__ano","placa__empresa__nombre",
                        "abast__viaje","abast__viaje__fecha_fin").exclude(abast__viaje__fecha_fin=None).
                #  annotate(rend_cargado=Subquery(newest.values('rend_cargado')[:1])). 
                #  annotate(rend_vacio=Subquery(newest.values('rend_vacio')[:1])). 
                #  annotate(rend_prom=Subquery(newest.values('rend_prom')[:1])). 
                #  annotate(rend_km=Subquery(newest.values('km')[:1])). 
         
                 annotate(conductor=Subquery(km_prev.values('conductor__nombres')[:1])). 
                annotate(recorrido_total=Sum(F("km")-Subquery(newest.values('km')[:1]))).
                annotate(last_km=Subquery(km_prev.values('km')[:1])). 

                 annotate(vol_total=Sum("volumen")).
                 annotate(km_total=Sum("km")).
                 annotate(g_obj_total=Sum("gal_obj")).
                 annotate(r_obj_total=Sum("recorrido_obj")).
                 annotate(monto_total=Sum("total")).
                #  annotate(tramo=RawSQL("""select string_agg(a.tramo,'/' ORDER BY d.abast_id) from "Web_detalleabastecimiento" as d inner join "Web_abastecimiento" as a on d.abast_id=a.id where a.viaje_id = "Web_abastecimiento".viaje_id""",())).
                annotate(count=Count("abast"), tramo=GroupConcat('abast__tramo', ordering="abast_id",separator=' / ')).
                 order_by("-abast__viaje","-abast__viaje__fecha_fin"))
            print(qs.query)
            # annotate(km_total=Sum("abastecimiento__detalleabastecimiento__km")).      
            # annotate(end_date=Subquery(newest.values('fecha')[:1])).      
            # annotate(precio=Subquery(newest.values('precio')[:1])))
            if start_date and end_date and placa and marca  and empresa and modelo:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa,placa__modelo_vehiculo=modelo)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa,placa__modelo_vehiculo=modelo)
            elif start_date and end_date and placa and marca and empresa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)
            elif start_date and end_date  and placa and empresa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,placa__empresa=empresa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa,placa__empresa=empresa)
            elif start_date and end_date and placa and marca:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca)
            elif start_date and end_date and placa and marca and modelo:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__modelo_vehiculo=modelo)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__modelo_vehiculo=modelo)
            elif start_date and end_date and marca and modelo:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__modelo_vehiculo=modelo)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa__modelo_vehiculo__marca_vehiculo=marca,placa__modelo_vehiculo=modelo)            
            elif start_date and end_date and placa and marca and empresa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)          
            elif  start_date and end_date  and marca and empresa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)    
            elif placa and marca and empresa and modelo:
                qs=qs.filter(placa__empresa=empresa,placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__modelo_vehiculo=modelo)
            elif placa and marca and empresa:
                qs=qs.filter(placa__empresa=empresa,placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca)
            elif marca and empresa and modelo:
                qs=qs.filter(placa__empresa=empresa,placa__modelo_vehiculo=modelo,placa__modelo_vehiculo__marca_vehiculo=marca)
          
            elif start_date and end_date and placa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa) 
            elif start_date and end_date and marca:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa__modelo_vehiculo__marca_vehiculo=marca)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa__modelo_vehiculo__marca_vehiculo=marca) 
            elif start_date and end_date and empresa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa__empresa=empresa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa__empresa=empresa) 
        
            elif placa and marca:
                qs=qs.filter(placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca)
            elif placa and empresa:
                qs=qs.filter(placa=placa,placa__empresa=empresa)
          
            elif placa and marca and empresa:
                qs=qs.filter(placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)  
            elif placa and marca and modelo:
                qs=qs.filter(placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,placa__modelo_vehiculo=modelo)    
            elif placa and marca and año:
                qs=qs.filter(placa=placa,placa__modelo_vehiculo__marca_vehiculo=marca,abast__fecha__year=año)
          
            elif marca and empresa:
                qs=qs.filter(placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)
            elif marca and empresa:
                qs=qs.filter(placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)   
            elif modelo and empresa:
                qs=qs.filter(placa__modelo_vehiculo=modelo,placa__empresa=empresa)
            elif placa and empresa:
                qs=qs.filter(placa=placa,placa__empresa=empresa)     
            elif modelo and empresa:
                qs=qs.filter(placa__modelo_vehiculo=modelo,placa__empresa=empresa)
                 
                 
  
            elif marca and placa:
                qs=qs.filter(placa__modelo_vehiculo__marca_vehiculo=marca,placa=placa)   
            elif marca and empresa:
                qs=qs.filter(placa__modelo_vehiculo__marca_vehiculo=marca,placa__empresa=empresa)    
            elif marca and modelo:
                qs=qs.filter(placa__modelo_vehiculo__marca_vehiculo=marca,placa__modelo_vehiculo=modelo)    
            elif empresa and placa:
                qs=qs.filter(placa=placa,placa__modelo_vehiculo=modelo)    
            elif empresa and modelo:
                qs=qs.filter(placa__empresa=empresa,placa__modelo_vehiculo=modelo)             
   
            elif start_date and end_date:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date]) 
        
            elif placa:
                qs=qs.filter(placa=placa)
            elif marca:
                qs=qs.filter(placa__modelo_vehiculo__marca_vehiculo=marca)         
            elif empresa:
                qs=qs.filter(placa__empresa=empresa)
            elif modelo:
                qs=qs.filter(placa__modelo_vehiculo=modelo)       
            
            # data = serializers.serialize('json', list(qs), fields=('fileName','id'))
            serialized_q = json.dumps(list(qs), cls=DjangoJSONEncoder)
            # for i in qs:
            #     item=i.get_report_viaje()
            #     item["vol_total"]=i.vol_total
            #     item["km_total"]=i.km_total
            #     item["precio"]=i.precio
            #     item["end_date"]=i.end_date
                              
            #     data.append(item)  
            return JsonResponse(serialized_q,safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status":500})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["placa"] =Vehiculo.objects.values("id","placa","activo").filter(activo=True) 
        context["marca"] =MarcaVehiculo.objects.values("id","descripcion","activo","eliminado")
        context["empresa"]=Empresa.objects.values("id","nombre").filter(estado=True)
        return context

class RendimientoAbastecimientoView(LoginRequiredMixin,TemplateView):
    template_name="Web/Combustible/rendimiento_eess.html"
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            data=[]
       
            start_date=self.request.POST["start_date"]
            end_date=self.request.POST["end_date"]     
            placa=request.POST["placa"]
            ruta=request.POST["ruta"]            
            empresa=request.POST["empresa"]            
            afectacion = AfectacionConsumo.objects.filter(per_carga=OuterRef('cargado'))

            newest = DetalleAbastecimiento.objects.filter(placa=OuterRef('placa'),abast__fecha__lt=OuterRef('abast__fecha')).order_by('-abast__fecha')
            relleno = (DetalleAbastecimiento.objects.filter(placa=OuterRef('placa'),abast__viaje=OuterRef('abast__viaje'),abast__fecha__lt=OuterRef('abast__fecha')).annotate(recorrido=F("km")-Subquery(newest.values('km')[:1])).order_by('-abast__fecha'))
            # qs =(DetalleAbastecimiento.objects.filter(abast__tipo=1).
            #     select_related("abast","abast__tipo","abast__estado_viaje","abast__viaje","placa","conductor").
            #         values("id","km","volumen","gal_obj","total").
            #         annotate(recorrido=F("km")-Subquery(newest.values('km')[:1])).
            #         annotate(relleno=Subquery(relleno.values('km')[:1])).
            #         order_by("-id","placa")) 
            qs =(DetalleAbastecimiento.objects.filter(abast__tipo=1).select_related("abast","abast__tipo","abast__estado_viaje","abast__viaje","placa","conductor").
                    annotate(previous_km=Subquery(newest.values('km')[:1])).

                    annotate(recorrido=Case(
                        When(previous_km=None,then=F("km")),
                        When(previous_km__gte=0,then=F("km")-Subquery(newest.values('km')[:1]))
                    )).
                    # annotate(tramo_relleno=Subquery(relleno.values('abast__tramo')[:1])).
                    annotate(previous_tipo=Subquery(newest.values('abast__tipo')[:1])).
                    annotate(tramo_relleno=Case(
                        When(previous_tipo=2,then=Subquery(newest.values('abast__tramo')[:1])
                    ))).
                    annotate(recorrido_relleno=Case(
                        When(previous_tipo=2,then=Subquery(relleno.values('recorrido')[:1])
                    ))).

                    annotate(volumen_relleno=Case(
                        When(previous_tipo=2,then=Subquery(relleno.values('volumen')[:1])
                    ))).
                    annotate(total_relleno=Case(
                        When(previous_tipo=2,then=Subquery(relleno.values('total')[:1])
                    ))).exclude(previous_km=None).
                    order_by("-abast__viaje","placa","-abast__fecha",))
            print(qs.query)
            if start_date and end_date and placa and ruta and empresa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,abast__tramo=tramo,placa__empresa=empresa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa,abast__tramo=ruta,placa__empresa=empresa)
            
            elif start_date and end_date and placa and ruta:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,abast__tramo=ruta)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa,abast__tramo=ruta)
            elif start_date and end_date and placa and empresa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa,placa__empresa=empresa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa,placa__empresa=empresa)

            elif  start_date and end_date and ruta and empresa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa__empresa=empresa,abast__tramo=ruta)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa__empresa=empresa,abast__tramo=ruta)
          
            elif  start_date and end_date and ruta:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,abast__tramo=ruta)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],abast__tramo=ruta)   
            elif  start_date and end_date and empresa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa__empresa=empresa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa__empresa=empresa)           
            elif  start_date and end_date and placa:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date,placa=placa)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date],placa=placa)
          
            elif ruta and empresa:
                qs=qs.filter(abast__tramo=ruta,placa__empresa=empresa) 
            elif ruta and placa:
                qs=qs.filter(abast__tramo=ruta,placa=placa)        
            elif empresa and placa:
                qs=qs.filter(placa__empresa=empresa,placa=placa) 

            elif start_date and end_date:
                if start_date==end_date:     
                    qs=qs.filter(abast__fecha__contains=start_date)
                else:
                    qs=qs.filter(abast__fecha__range=[start_date,end_date]) 
        
            elif placa:
                qs=qs.filter(placa=placa)
         
            elif empresa:
                qs=qs.filter(placa__empresa=empresa) 
            elif ruta:
                qs=qs.filter(abast__tramo=ruta)
     
            for i in qs:
                item=i.get_report_abast()
                item["recorrido"]=i.recorrido
                item["volumen_relleno"]=i.volumen_relleno
                item["tramo_relleno"]=i.tramo_relleno
                item["total_relleno"]=i.total_relleno
                item["recorrido_relleno"]=i.recorrido_relleno
          
                data.append(item)
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["placa"] =Vehiculo.objects.values("id","placa","activo").filter(activo=True) 
        context["empresa"]=Empresa.objects.values("id","nombre").filter(estado=True)
        context["ruta"]=Abastecimiento.objects.values("tramo").annotate(Count("tramo"))
        context["tipo"]=TipoAbastecimiento.objects.values("id","descripcion")
        return context
class AfectacionListView(LoginRequiredMixin,ListView):
    template_name = 'Web/Combustible/afectaciones.html'
    model = AfectacionConsumo
    login_url=reverse_lazy("Web:login")
    success_url=reverse_lazy("Web:afectaciones")
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in AfectacionConsumo.objects.filter(estado=True):
                    data.append(i.toJSON())

            else:
                data["error"]="Ha ocurrido un error"
            return JsonResponse(data,safe=False)

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)


class AfectacionCreateView(LoginRequiredMixin,CreateView):
    form_class = AfectacionConsumoForm
    template_name = 'Web/Combustible/afectacion.html'
    login_url=reverse_lazy("Web:login")
    def get(self,*args, **kwargs):
        form=self.get_form()
        return render(self.request,self.template_name,{"form":form})
    def post(self, request,*args, **kwargs):      
        try:
            form = self.get_form()

            if form.is_valid():

                instance=form.save(commit=False)
              
                instance.changed_by = self.request.user
                instance.save()
                data = {
                'status': 200
                }
                return JsonResponse(data,safe=False)
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
                return JsonResponse(data)
            

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

class AfectacionUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AfectacionConsumoForm
    model = AfectacionConsumo  
    template_name = 'Web/Combustible/afectacion.html'
    context_object_name="obj"
    login_url=reverse_lazy("Web:login")

    def dispatch(self,request,*args, **kwargs):
        self.object=self.get_object() 
        return super().dispatch(request,*args,**kwargs)



    def post(self, request,*args, **kwargs):       
        try:
            form = self.get_form()

            if form.is_valid():
                print(form)
                instance=form.save(commit=False)
                if not "activo" in self.request.POST:
                    instance.activo=False
                instance.changed_by = self.request.user
                instance.save()
                data = {
                'status': 200
                }
                return JsonResponse(data,safe=False)
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
                return JsonResponse(data)
            

        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

class AfectacionDeleteView(LoginRequiredMixin, View):
    login_url=reverse_lazy("Web:login")

    def post(self, request, *args, **kwargs):
        id=self.kwargs["pk"]
        existe = AfectacionConsumo.objects.filter(pk=id)
        if existe.exists():
            obj=existe.first()
            obj.changed_by=request.user
            obj.estado=False
            obj.save()
            return JsonResponse({"status":200},safe=False)
            
        else:
            return JsonResponse({"status":500},safe=False)

def import_abastecimiento(request):
    if request.method=="POST":
      
        file=request.FILES.get('file', '')
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo cargado no es .xlsx')
        data=import_abastecimento_xlsx(file)
        print(data)
        return JsonResponse(data,safe=False)