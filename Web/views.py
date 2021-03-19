#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import FormView, CreateView, ListView, UpdateView,DetailView
from django.views.generic import FormView
from django.contrib.auth.models import Group,Permission
from .forms import (UserGroupForm,UserPasswordResetForm,LoginForm, PersonaForm, UsuarioForm,
    UbicacionForm, MarcaRenovaForm, ModeloRenovaForm, AnchoBandaRenovaForm,InspeccionForm, 
    MarcaLlantaForm ,ModeloLlantaForm, MedidaLlantaForm, AlmacenForm, LugarForm,
    TipoPisoForm, TipoServicioForm, MarcaVehiculoForm, ModeloVehiculoForm, LlantaForm, VehiculoForm,TipoVehiculoForm,CubiertaForm)
from django.http.response import HttpResponseRedirect
from django.contrib import messages, auth
from .common import LoginView, LoginSelectPerfilView
from django.urls import reverse
from .models import *
from django.db import transaction	
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import Http404
from Web.constanst import ACCION_NUEVO, ACCION_EDITAR, ACCION_ELIMINAR
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator

from .mixins import ValidateMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
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
    permission_required=["auth.view_seguridad"]

class OperacionesView(LoginRequiredMixin,ValidateMixin,TemplateView):
    template_name="Web/Operaciones/operaciones_base.html"
    permission_required=["auth.view_procesos"]

class ReportesView(LoginRequiredMixin,TemplateView):
    template_name="Web/Reportes/reportes_base.html"
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
            print("aeaaaaa")
            auth.login(self.request, user)
            messages.success(self.request,f"Bienvenido {self.request.user}",extra_tags="login")

            return redirect(self.success_url)
        else:
            auth.logout(self.request)    
            messages.error(self.request, 'El usuario o la clave es incorrecto.')
            print("aea")
            return redirect(reverse_lazy("Web:login"))            
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'El usuario o la clave es incorrecto.')
        return super().form_invalid(form)

class HomePageView(LoginView, TemplateView):
    template_name = "Web/base.html"
  
class Error403(TemplateView):
    template_name = 'Web/403.html'


class LogoutView(LoginSelectPerfilView, View):
    template_name = 'Web/logout.html'

    def get(self, request):
        auth.logout(request)
        return render(request, self.template_name)



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
                    form.instance.modified_by = self.request.user

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
                form.instance.created_by = self.request.user
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
                print("if")
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
        print(request.POST)
        try:
            form = self.get_form()

            if form.is_valid(): 
           
                form.created_by = self.request.user
          
                
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
                instance.modified_by = self.request.user
                
                instance.save()    

                persona=Persona.objects.filter(id=self.object.persona.id)
                if persona.exists():
                    data=persona.first()
                    data.nom=self.request.POST["name"]
                    data.apep=self.request.POST["apep"]
                    data.apem=self.request.POST["apem"]
                    data.modified_by=self.request.user
                    
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
            data.modified_by=request.user
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
            data.modified_by=request.user

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
        instance.created_by = self.request.user
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
        instance.modified_by = self.request.user
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
        ubicacion.modified_by=request.user
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
        instance.created_by = self.request.user
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
        instance.modified_by = self.request.user
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
        Almacen.modified_by=request.user
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
        instance.created_by = self.request.user
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
        instance.modified_by = self.request.user
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
        lugar.modified_by=request.user
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
        instance.created_by = self.request.user
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
        instance.modified_by = self.request.user
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
        obj.modified_by=request.user
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
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["marca_renova"] =  MarcaRenova.objects.all().values("id","descripcion","activo","eliminado")
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
        instance.modified_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        context["marca_renova"] =  MarcaRenova.objects.all().values("id","descripcion","activo","eliminado")

        return context


class ModeloRenovacionDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_modelorenova"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = ModeloRenova.objects.get(pk=id)
        obj.modified_by=request.user
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
        print(qs)
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
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_renova'] = MarcaRenova.objects.all().values("id",'descripcion',"activo","eliminado")
 
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
        instance.modified_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # import pdb; pdb.set_trace()
        context['marca_renova'] = MarcaRenova.objects.all().values("id",'descripcion',"activo","eliminado")
        context['update'] = True
        return context


class AnchoBandaRenovacionDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_anchobandarenova"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = AnchoBandaRenova.objects.get(pk=id)
        obj.modified_by=request.user
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
        print(request.POST) 
        try:
            form = self.get_form()

            if form.is_valid():

                instance=form.save(commit=False)
              
                instance.created_by = self.request.user
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
            print(self.request.POST)
            form = self.get_form()

            if form.is_valid():
                print(form)
                instance=form.save(commit=False)
                if not "activo" in self.request.POST:
                    print("aeaaaa")
                    instance.activo=False
                instance.modified_by = self.request.user
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
            print(obj)
            obj.modified_by=request.user
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
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_llanta']=MarcaLlanta.objects.all().values("id","descripcion","activo")
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
        instance.modified_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        context['marca_llanta']=MarcaLlanta.objects.all().values("id","descripcion","activo")

        return context


class ModeloLlantaDeleteView(LoginRequiredMixin,ValidateMixin ,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_modelollanta"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = ModeloLlanta.objects.get(pk=id)
        obj.modified_by=request.user
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
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_llanta'] = MarcaLlanta.objects.all().values("id",'descripcion',"activo","eliminado")
 
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
        instance.modified_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_llanta'] = MarcaLlanta.objects.all().values("id",'descripcion',"activo","eliminado")

        context['update'] = True
        return context


class MedidaLlantaDeleteView(LoginRequiredMixin, ValidateMixin,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_medidallanta"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = MedidaLlanta.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:medida-llantas',))


def RenderOptionLlanta(request):
    id_marca = request.GET.get('id_marca')
    if id_marca!="":
        modelos = ModeloLlanta.objects.filter(marca_llanta=id_marca)
    
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
#         instance.created_by = self.request.user
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
#         instance.modified_by = self.request.user
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
#         obj.modified_by=request.user
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
        instance.created_by = self.request.user
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
        instance.modified_by = self.request.user
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
        obj.modified_by=request.user
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
        instance.created_by = self.request.user
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
        instance.modified_by = self.request.user
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
        obj.modified_by=request.user
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
        instance.created_by = self.request.user
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
        instance.modified_by = self.request.user
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
        obj.modified_by=request.user
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
        instance.created_by = self.request.user
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
            print(i)
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
        print(instance.image)

        if instance.image!="":
            if default_storage.exists(f'vehiculo2/Y/{instance.image}'):
                default_storage.delete(f'vehiculo2/Y/{instance.image}')         
        if instance.image2!="":
            if default_storage.exists(f'vehiculo2/X/{instance.image2}'):
                default_storage.delete(f'vehiculo2/X/{instance.image2}')            
        instance.modified_by = self.request.user
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
        obj.modified_by=request.user
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
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca_vehiculo']=MarcaVehiculo.objects.all().values("id","descripcion","activo")
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
        instance.modified_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form)

        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        context['marca_vehiculo']=MarcaVehiculo.objects.all().values("id","descripcion","activo")
        return context


class ModeloVehiculoDeleteView(LoginRequiredMixin,ValidateMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_modelovehiculo"]
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = ModeloVehiculo.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse_lazy('Web:modelo-vehiculos'))

from django.views.decorators.cache import never_cache

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

            search=Llanta.objects.filter(eliminado=False).order_by("-created_at") 
            response=search 
            if marca:
                response=search.filter(modelo_llanta__marca_llanta_id=marca)

                if modelo:

                    response=search.filter(modelo_llanta__marca_llanta_id=marca,modelo_llanta_id=modelo)
            elif medida!="":
                response=search.filter(medida_llanta=medida)

            elif start_date and end_date:
                response=search.filter(created_at__range=[start_date,end_date])

                if start_date==end_date:     
                    response=search.filter(created_at__contains=start_date)            
            data=[]
            for i in response:
                data.append(i.toJSON())  
                 
            return JsonResponse(data, safe=False)
 
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)
    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        
        qs = qs.filter(eliminado=False,activo=True)
      
        # modelo = self.request.GET.get('modelo','')
        # costo = self.request.GET.get('costo','')
        # fi = self.request.GET.get('fecha_inicio')
        # ff =self.request.GET.get('fecha_fin')
        
        # if modelo:
        #     qs = qs.filter(modelo_llanta__pk=modelo)
        # if costo:
        #     qs = qs.filter(costo__icontains=costo)
        
        # if fi:
        #     fi=datetime.strptime(fi, '%Y-%m-%d').date()
        #     ff=datetime.strptime(ff, '%Y-%m-%d').date()
        #     ff = ff + timedelta(days=1)
        #     qs = qs.filter(created_at__range=(fi,ff))
        
        return qs.order_by('created_at').reverse()

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['medida'] = MedidaLlanta.objects.all()
        context['marca'] = MarcaLlanta.objects.all().values("id",'descripcion')

        return context


class LlantaCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    template_name = 'Web/Catalogos/llanta.html'
    success_url = reverse_lazy("Web:llantas")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_llanta"]
    def get(self,*args, **kwargs):
        Llanta=LlantaForm()
        cubierta=CubiertaForm()
        marca_llanta = MarcaLlanta.objects.all().values("id",'descripcion',"activo","eliminado")
        modelo_renova = ModeloRenova.objects.all().values("id",'descripcion',"activo","eliminado")
        ancho_banda = AnchoBandaRenova.objects.all().values("id",'descripcion',"activo","eliminado")
        ubicacion=Ubicacion.objects.all().values("id",'descripcion',"activo","eliminado")
        vehiculo=Vehiculo.objects.all().values("id",'placa',"activo","eliminado")
        medida_llanta=MedidaLlanta.objects.all().values("id","medida","profundidad","capas","eliminado","activo")

        context={
            "form":Llanta,
            "form2":cubierta,
            "ubicacion":ubicacion,
            "marca_llanta":marca_llanta,
            "modelo_renova":modelo_renova,
            "ancho_banda":ancho_banda,
            "vehiculo":vehiculo,
            "medida_llanta":medida_llanta

            }
        return render(self.request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        try:
            form1=LlantaForm(request.POST)

            form2=CubiertaForm(request.POST)

            if form1.is_valid() and form2.is_valid():
                instance2=CubiertaLlanta()
                instance2.created_by = self.request.user
                instance2.km=self.request.POST["km"]
                instance2.costo=self.request.POST["costo"]
                instance2.fech_ren=self.request.POST["fech_ren"]
                instance2.nro_ren=self.request.POST["nro_ren"]
                instance2.a_final=self.request.POST["a_final"]
                instance2.a_inicial=self.request.POST["a_inicial"]
                instance2.a_promedio=self.request.POST["a_promedio"]
                instance2.modelo_renova_id=self.request.POST["modelo_renova"]
                instance2.ancho_banda_id=self.request.POST["ancho_banda"]
                instance2.renovadora_id=self.request.POST["renovadora"]
                instance2.categoria=self.request.POST["categoria"]
                instance2.save()
                instance=form1.save(commit=False)
                instance.cubierta=instance2
                if "repuesto" in request.POST:
                    instance.repuesto=True
                else:
                    instance.repuesto=False
                if "activo" in request.POST:
                    instance.activo=True
                else:
                    instance.activo=False
                instance.created_by = self.request.user
                instance.save()
                if self.request.POST["ubicacion"]=="":
                    obj,p=InpeccionLlantas.objects.get_or_create(vehiculo_id=self.request.POST["vehiculo"])
                    
                    det=DetalleInspeccion()
                    if "repuesto" in request.POST:
                        det.repuesto=True
                    else:
                        det.repuesto=False
                    det.inspeccion=obj
                    det.llanta_id=instance.id
                    det.posicion=self.request.POST["posicion"]
                    det.save()
                return JsonResponse({"status":200,"form":{},"form2":{},"url":reverse_lazy("Web:llanta")})
            else:
                data = {
                    "form":form1.errors,
                    "form2":form2.errors,
                    'status': 500,
                    }
                return JsonResponse(data)
        except Exception as e:
            print(e)
            messages.error(self.request, 'Ha ocurrido un error.')
            return HttpResponseRedirect(self.success_url)

    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     instance.codigo = instance.code
    #     instance.created_by = self.request.user
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
    
    # def form_valid(self, form):
    #     # import pdb; pdb.set_trace()
    #     instance = form.save(commit=False)
    #     instance.modified_by = self.request.user
    #     messages.success(self.request, 'Operación realizada correctamente.')
    #     return super().form_valid(form)

    def dispatch(self,request,*args, **kwargs):        
        return super().dispatch(request,*args,**kwargs)


    def get(self,*args, **kwargs):
        cubierta=CubiertaLlanta.objects.filter(id=self.get_object().cubierta.id).first()
        form1=LlantaForm(instance=self.get_object())
        form2=CubiertaForm(instance=cubierta)
        marca_llanta= MarcaLlanta.objects.all().values("id",'descripcion',"activo","eliminado")
        modelo_renova = ModeloRenova.objects.all().values("id",'descripcion',"activo","eliminado")
        ancho_banda = AnchoBandaRenova.objects.all().values("id",'descripcion',"activo","eliminado")
        ubicacion=Ubicacion.objects.all().values("id",'descripcion',"activo","eliminado")
        vehiculo=Vehiculo.objects.all().values("id",'placa',"activo","eliminado")
        medida_llanta=MedidaLlanta.objects.all().values("id","medida","profundidad","capas","eliminado","activo")

        context={
           "form":form1,
            "vehiculo":vehiculo,
            "form2":form2,
            "cubierta":cubierta,
            "obj":self.get_object(),
            "marca_llanta":marca_llanta,
            "modelo_renova":modelo_renova,
            "ubicacion":ubicacion,
            "ancho_banda":ancho_banda,
            "medida_llanta":medida_llanta
                }
        return render(self.request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        try:
            form2=CubiertaForm(request.POST)
            form1=LlantaForm(request.POST,instance=self.get_object())
            
            if form1.is_valid() and form2.is_valid():
                if self.get_object().cubierta:
                    instance2=CubiertaLlanta.objects.filter(id=self.get_object().cubierta.id).first()

                    instance2.modified_by = self.request.user
                    instance2.km=self.request.POST["km"]
                    instance2.costo=self.request.POST["costo"]
                    instance2.fech_ren=self.request.POST["fech_ren"]
                    instance2.nro_ren=self.request.POST["nro_ren"]
                    instance2.a_final=self.request.POST["a_final"]
                    instance2.a_inicial=self.request.POST["a_inicial"]
                    instance2.a_promedio=self.request.POST["a_promedio"]

                    instance2.modelo_renova_id=self.request.POST["modelo_renova"]

                    instance2.ancho_banda_id=self.request.POST["ancho_banda"]

                    instance2.renovadora_id=self.request.POST["renovadora"]

                    instance2.categoria=self.request.POST["categoria"]
    
                    instance2.save()
               
                instance=self.get_object()
                instance.codigo=self.request.POST["codigo"]
                instance.vehiculo_id=self.request.POST["vehiculo"]
                

                instance.medida_llanta_id=self.request.POST["medida_llanta"]
                instance.modelo_llanta_id=self.request.POST["modelo_llanta"]
                instance.marca_llanta_id=self.request.POST["marca_llanta"]
                if "repuesto" in request.POST:
                    instance.repuesto=True
                    
                else:
                    instance.repuesto=False
                if "activo" in request.POST:
                    instance.activo=True
                    instance.ubicacion_id=self.request.POST["ubicacion"]
                    instance.estado=self.request.POST["estado"]
                    if self.request.POST["posicion"]!="":
                        instance.posicion=self.request.POST["posicion"]
                    else:
                        instance.posicion=None

                else:
                    instance.activo=False

                    instance.vehiculo=None
                    instance.posicion=None
                    
                    instance.repuesto=False

            
                    instance.ubicacion_id=3
              

                if self.get_object().cubierta:
                    instance.cubierta=instance2
                instance.modified_by = self.request.user
                instance.save()
                return JsonResponse({"status":200,"url":self.success_url})
            else:
                data = {
                    "form":form1.errors,
                    "form2":form2.errors,
                    'status': 500,
                    }
                return JsonResponse(data,safe=False)
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
        llanta.modified_by=request.user
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
        instance.created_by = self.request.user
        
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
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
        instance.modified_by = self.request.user
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
        print(id)
        obj = Vehiculo.objects.get(pk=id)
        obj.modified_by=request.user
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
        posiciones=PosicionesLlantas.objects.filter(tipo_id=obj.tipo_vehiculo.id)

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
        print(qs)
        return JsonResponse(qs, content_type='application/json')
def getVehiculo(request):
    if request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        print(post)
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
        instance.created_by = self.request.user
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
    permission_required=["Web.view_historialllantas"]

    def get(self,request,*args, **kwargs):
        context={"obs":CHOICES_OBSERVACION,"obj":request.GET,"estado":CHOICES_ESTADO_LLANTA}
        return render(self.request,self.template_name,context)
    def post(self,request,*args, **kwargs):
        print(request.POST)
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
                    historial=HistorialLLantas()
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
                    historial.created_by=self.request.user
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
    permission_required=["Web.view_historialllantas"]

    def get(self,request,*args, **kwargs):
        print(request.GET)
        return render(self.request,self.template_name,{"obj":request.GET})
    def post(self,request,*args, **kwargs):
        print(request.POST)
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

                    objeto.vehiculo_id=request.POST["vehiculo"]
                    objeto.repuesto=rep
                    objeto.posicion=request.POST["posicion"]

                    objeto.save()
                    historial=HistorialLLantas()
                    historial.llanta=objeto
                    historial.km=request.POST["kilometros"]
                    historial.posicion=pos
                  
                    historial.vehiculo_id=request.POST["vehiculo"]
                    historial.profundidad=request.POST["profundidad"]
                    historial.created_by=self.request.user
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
    permission_required=["Web.view_historialllantas"]

    def post(self,request,*args, **kwargs):
        data,posicion=[],[]
        post = json.loads(request.body.decode("utf-8"))

        if(post["id"]!=""):
            ve=Vehiculo.objects.get(id=post["id"])
            qs = ve.toJSON()
         
            nm = Llanta.objects.filter(vehiculo=post["id"]).order_by("posicion")
            pos=PosicionesLlantas.objects.filter(tipo_id=ve.tipo_vehiculo.id)
            for i in nm:
                lala=i.toJSON()
                data.append(lala)   
            for i in pos:
                posicion.append(i.toJSON())
            return JsonResponse({"status":200,"vehiculo":qs,"llantas":data,"pos":posicion},safe=False, content_type='application/json')
        return JsonResponse({"status":303},safe=False, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(HojaDeMovimientosView, self).get_context_data(**kwargs)
        context["placa"]=Vehiculo.objects.all().values("id","placa").filter(eliminado=False,activo=True)
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
                print("Entro al p ")
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
        context["placa"]=Vehiculo.objects.all().values("id","placa").filter(eliminado=False,activo=True)
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
class HistorialLlantas(ListView,LoginRequiredMixin):
    template_name="Web/reportes/historial.html"
    model=HistorialLLantas