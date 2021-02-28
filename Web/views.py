#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page

from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import FormView, CreateView, ListView, UpdateView,DetailView
from django.views.generic import FormView
from django.contrib.auth.models import Group,Permission
from .forms import (UserGroupForm,UserPasswordResetForm,LoginForm, PersonaForm, UsuarioForm,
    UbicacionForm, MarcaRenovaForm, ModeloRenovaForm, AnchoBandaRenovaForm, 
    MarcaLlantaForm ,ModeloLlantaForm, MedidaLlantaForm, AlmacenForm, LugarForm, EstadoLlantaForm,
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

from .mixins import ValidateMixin,AdminPermission
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
        messages.error(self.request, str(form.errors))
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
    template_name = "Web/perfiles.html"
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
    template_name = 'Web/perfil.html'
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
                data={"stat":200,"url":self.success_url}
            else:
                data = {
                "form":form.errors,
                'stat': 500,
                }
            return JsonResponse(data,safe=False)
        

        except Exception as e:
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)
  


class PerfilUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = UserGroupForm
    model = Group
    template_name = "Web/perfil.html"
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
              
                return JsonResponse({"stat":200,"url":self.success_url})
            else:
                return JsonResponse({"stat":500,"form":form.errors})

        except Exception as e:
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

class PersonaListView(LoginRequiredMixin,ValidateMixin,ListView):
    template_name = 'Web/personas.html'
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
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)
   
class PersonaUpdateView(LoginRequiredMixin,ValidateMixin,UpdateView):
    model = Persona
    template_name="Web/persona.html"
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
                    'stat': 'ok',
                   }
                    return JsonResponse(data)
                else:
                    data = {
                    "error":form.errors,
                    'stat': False,
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
    template_name = 'Web/persona.html'
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
                    'status': 200,
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
    template_name = 'Web/list_usuarios.html'
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
    template_name = 'Web/usuario.html'
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
    template_name = 'Web/usuarioEdit.html'
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
    template_name = 'Web/usuarioChangePassword.html'
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
    template_name = 'Web/ubicaciones.html'
    model = Ubicacion
    paginate_by = 10
    context_object_name = 'ubicaciones'
    permission_required=["Web.view_ubicacion"]
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
        context['pages'] = self.paginate_by
        return context


class UbicacionCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = UbicacionForm
    template_name = 'Web/ubicacion.html'
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
    template_name = 'Web/ubicacion.html'
    success_url = reverse_lazy("Web:lugares")
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
    template_name = 'Web/almacenes.html'
    model = Almacen
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context


class AlmacenCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = AlmacenForm
    template_name = 'Web/almacen.html'
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
    template_name = 'Web/almacen.html'
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
    template_name = 'Web/lugares.html'
    model = Lugar
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context


class LugarCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = LugarForm
    template_name = 'Web/lugar.html'
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
    template_name = 'Web/lugar.html'
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
        Lugar = Lugar.objects.get(pk=id)
        Lugar.modified_by=request.user
        Lugar.eliminado = True
        Lugar.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:lugares',))


class MarcaRenovacionesListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/marca_renovaciones.html'
    model = MarcaRenova
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context


class MarcaRenovacionCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = MarcaRenovaForm
    template_name = 'Web/marca_renovacion.html'
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
    template_name = 'Web/marca_renovacion.html'
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
    template_name = 'Web/modelo_renovaciones.html'
    model = ModeloRenova
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context


class ModeloRenovacionCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = ModeloRenovaForm
    template_name = 'Web/modelo_renovacion.html'
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


class ModeloRenovacionUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = ModeloRenovaForm
    model = ModeloRenova
    template_name = 'Web/modelo_renovacion.html'
    success_url = reverse_lazy("Web:modelo-renovaciones")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_modelorenova"]

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
    template_name = 'Web/ancho_banda_renovaciones.html'
    model = AnchoBandaRenova
    paginate_by = 10
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_anchobandarenova"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.paginate_by
        return context


class AnchoBandaRenovacionCreateView(LoginRequiredMixin, ValidateMixin,CreateView):
    form_class = AnchoBandaRenovaForm
    template_name = 'Web/ancho_banda_renovacion.html'
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


class AnchoBandaRenovacionUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = AnchoBandaRenovaForm
    model = AnchoBandaRenova
    template_name = 'Web/ancho_banda_renovacion.html'
    success_url = reverse_lazy("Web:ancho-banda-renovaciones")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_anchobandarenova"]

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
        idancho =  self.kwargs['pk']
        context['instance'] = AnchoBandaRenova.objects.filter(pk=idancho).first()
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
    modelos = ModeloRenova.objects.filter(eliminado=False, marca_renova__pk=id_marca)
    return HttpResponse(json.dumps(list(modelos.values('id','descripcion'))), content_type="application/json")


class MarcaLlantasListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/marca_llantas.html'
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
                for i in MarcaLlanta.objects.filter(activo=True).order_by("created_at").reverse():
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
    template_name = 'Web/marca_llanta.html'
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
    template_name = 'Web/marca_llanta.html'
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
    template_name = 'Web/modelo_llantas.html'
    model = ModeloLlanta
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context


class ModeloLlantaCreateView(LoginRequiredMixin,ValidateMixin ,CreateView):
    form_class = ModeloLlantaForm
    template_name = 'Web/modelo_llanta.html'
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


class ModeloLlantaUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = ModeloLlantaForm
    model = ModeloLlanta
    template_name = 'Web/modelo_llanta.html'
    success_url = reverse_lazy("Web:modelo-llantas")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_modelollanta"]

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
    template_name = 'Web/medida_llantas.html'
    model = MedidaLlanta
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context


class MedidaLlantaCreateView(LoginRequiredMixin, ValidateMixin,CreateView):
    form_class = MedidaLlantaForm
    template_name = 'Web/medida_llanta.html'
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


class MedidaLlantaUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = MedidaLlantaForm
    model = MedidaLlanta
    template_name = 'Web/medida_llanta.html'
    success_url = reverse_lazy("Web:medida-llantas")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_medidallanta"]

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
        id =  self.kwargs['pk']
        context['instance'] = MedidaLlanta.objects.filter(pk=id).first()
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
    print(id_marca  )
    modelos = ModeloLlanta.objects.filter(eliminado=False, marca_llanta=id_marca)
    return HttpResponse(json.dumps(list(modelos.values('id','descripcion'))), content_type="application/json")


class EstadoLlantasListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/estado_llantas.html'
    model = EstadoLlanta
    paginate_by = 10
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_estadollanta"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.paginate_by
        return context


class EstadoLlantaCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = EstadoLlantaForm
    template_name = 'Web/estado_llanta.html'
    success_url = reverse_lazy("Web:estado-llantas")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_estadollanta"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class EstadoLlantaUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = EstadoLlantaForm
    model = EstadoLlanta
    template_name = 'Web/estado_llanta.html'
    success_url = reverse_lazy("Web:estado-llantas")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_estadollanta"]

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


class EstadoLlantaDeleteView(LoginRequiredMixin, ValidateMixin,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_estadollanta"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = EstadoLlanta.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:estado-llantas',))


class TipoServiciosListView(LoginRequiredMixin,ValidateMixin, ListView):
    template_name = 'Web/tipo_servicios.html'
    model = TipoServicio
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context


class TipoServicioCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = TipoServicioForm
    template_name = 'Web/tipo_servicio.html'
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
    template_name = 'Web/tipo_servicio.html'
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
    template_name = 'Web/tipo_pisos.html'
    model = TipoPiso
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context


class TipoPisoCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = TipoPisoForm
    template_name = 'Web/tipo_piso.html'
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
    template_name = 'Web/tipo_piso.html'
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
    template_name = 'Web/marca_vehiculos.html'
    model = MarcaVehiculo
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context




class MarcaVehiculoCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = MarcaVehiculoForm
    template_name = 'Web/marca_vehiculo.html'
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
    template_name = 'Web/marca_vehiculo.html'
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
    template_name = 'Web/tipo_vehiculos.html'
    model = TipoVehiculo
    paginate_by = 10
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_tipovehiculo"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        q = self.request.GET.get('q','')
        qs = qs.filter(descripcion__icontains=q)
        return qs.order_by('descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.paginate_by
        return context
class TipoVehiculoCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    form_class = TipoVehiculoForm
    template_name = 'Web/tipo_vehiculo.html'
    success_url = reverse_lazy("Web:tipo-vehiculos")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_tipovehiculo"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)
class TipoVehiculoUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = TipoVehiculoForm
    model = TipoVehiculo
    template_name = 'Web/tipo_vehiculo.html'
    success_url = reverse_lazy("Web:tipo-vehiculos")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_tipovehiculo"]

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
    template_name = 'Web/modelo_vehiculos.html'
    model = ModeloVehiculo
    paginate_by = 10
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
        context['pages'] = self.paginate_by
        return context


class ModeloVehiculoCreateView(LoginRequiredMixin, ValidateMixin,CreateView):
    form_class = ModeloVehiculoForm
    template_name = 'Web/modelo_vehiculo.html'
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


class ModeloVehiculoUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    form_class = ModeloVehiculoForm
    model = ModeloVehiculo
    template_name = 'Web/modelo_vehiculo.html'
    success_url = reverse_lazy("Web:modelo-vehiculos")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_modelovehiculo"]

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
    template_name = 'Web/llantas.html'
    model = Llanta
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_llanta"]
    success_url=reverse_lazy("Web:inicio")
    @method_decorator(csrf_exempt)
    # @method_decorator(never_cache)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
   
    def post(self,request,*args, **kwargs):
        try:
            action=request.POST["action"]
            print("if")
            if action=="searchData":
                print(action)
                data=[]
                for i in Llanta.objects.filter(activo=True,eliminado=False).order_by("created_at").reverse():
                    data.append(i.toJSON())
              

            else:
               
                data["error"]="Ha ocurrido un error"
            dump = json.dumps(data)
            return HttpResponse(dump, content_type='application/json')
 
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

    # def get_context_data(self, **kwargs):
    #     # import pdb; pdb.set_trace()
    #     context = super().get_context_data(**kwargs)
    #     # context['pages'] = self.paginate_by
    #     context['marcas'] = MarcaLlanta.objects.filter(eliminado=False,activo=True).order_by('descripcion')
    #     return context


class LlantaCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    template_name = 'Web/llanta.html'
    success_url = reverse_lazy("Web:llantas")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.add_llanta"]
    def get(self,*args, **kwargs):
        Llanta=LlantaForm()
        cubierta=CubiertaForm()
        context={"form":Llanta,"form2":cubierta}
        return render(self.request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        print(request.POST)
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

                instance.created_by = self.request.user
                instance.save()
                return JsonResponse({"status":200,"url":reverse_lazy("Web:llanta")})
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
    template_name = 'Web/llanta.html'
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
        self.object=self.get_object() 
        
        return super().dispatch(request,*args,**kwargs)


    def get(self,*args, **kwargs):
        cubierta=CubiertaLlanta.objects.filter(id=self.object.cubierta.id).first()
        print(self.object.ubicacion)
        form1=LlantaForm(instance=self.object)
        form2=CubiertaForm(instance=cubierta)
        print(cubierta.categoria)
        context={"form":form1,"form2":form2,"cubierta":cubierta,"obj":self.get_object()}
        return render(self.request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        print(self.request.POST)
        try:
            form2=CubiertaForm(request.POST)

            form1=LlantaForm(request.POST,instance=self.object)
            if form1.is_valid() and form2.is_valid():
                instance2=CubiertaLlanta.objects.filter(id=self.object.cubierta.id).first()
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
                if self.request.POST["vehiculo"]!="":
                    instance.vehiculo_id=self.request.POST["vehiculo"]
                else:
                    instance.vehiculo_id=None
                instance.medida_llanta_id=self.request.POST["medida_llanta"]
                instance.modelo_llanta_id=self.request.POST["modelo_llanta"]
                instance.marca_llanta_id=self.request.POST["marca_llanta"]
                if "repuesto" in request.POST:
                    instance.repuesto=True
                else:
                    instance.repuesto=False
                
                if self.request.POST["posicion"]=="":
                    instance.posicion=None
                else:
                    instance.posicion=self.request.POST["posicion"]
                instance.ubicacion_id=self.request.POST["ubicacion"]
                instance.estado_id=self.request.POST["estado"]

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
        try:
            id = self.kwargs['pk']
            obj = Llanta.objects.get(pk=id)
            obj.modified_by=request.user
            obj.eliminado = True
            obj.save()
            data={"response":200}
            
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            messages.error(self.request, 'Ha ocurrido un error.')
            return HttpResponseRedirect(reverse_lazy("Web:inicio"))
class VehiculosListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/vehiculos.html'
    model = Vehiculo
    paginate_by = 10
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.view_vehiculo"]

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        modelo = self.request.GET.get('modelo','')
        placa = self.request.GET.get('placa','')
        fi = self.request.GET.get('fecha_inicio')
        ff =self.request.GET.get('fecha_fin')
        
        if modelo:
            qs = qs.filter(modelo_vehiculo__pk=modelo)
        if placa:
            qs = qs.filter(placa__icontains=placa)
        
        if fi:
            fi=datetime.strptime(fi, '%Y-%m-%d').date()
            ff=datetime.strptime(ff, '%Y-%m-%d').date()
            ff = ff + timedelta(days=1)
            qs = qs.filter(created_at__range=(fi,ff))
        
        return qs.order_by('-pk')

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['pages'] = self.paginate_by
        context['marcas'] = MarcaVehiculo.objects.filter(eliminado=False).order_by('descripcion')
        return context


class VehiculoCreateView(LoginRequiredMixin, ValidateMixin,CreateView):
    form_class = VehiculoForm
    template_name = 'Web/vehiculo.html'
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
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class VehiculoUpdateView(LoginRequiredMixin, ValidateMixin,UpdateView):
    form_class = VehiculoForm
    model = Vehiculo
    template_name = 'Web/vehiculo.html'
    success_url = reverse_lazy("Web:vehiculos")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.change_vehiculo"]

    def form_valid(self, form):
        # import pdb; pdb.set_trace()
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
        id =  self.kwargs['pk']
        context['instance'] = Vehiculo.objects.filter(pk=id).first()
        context['update'] = True
        return context


class VehiculoDeleteView(LoginRequiredMixin, ValidateMixin,View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    permission_required=["Web.delete_vehiculo"]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = Vehiculo.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:vehiculos',))


def RenderOptionVehiculo(request):
    id_marca = request.GET.get('id_marca')
    modelos = ModeloVehiculo.objects.filter(eliminado=False, marca_vehiculo__pk=id_marca)
    return HttpResponse(json.dumps(list(modelos.values('id','descripcion'))), content_type="application/json")


class VerVehiculoView(LoginRequiredMixin, ValidateMixin,TemplateView):
    template_name = 'Web/ver_vehiculo.html'
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
        context['obj'] =obj
        context["vehiculo"]=obj.llantas.filter(eliminado=0,activo=True).order_by("posicion")
        context["ubicaciones"]=Ubicacion.objects.filter(eliminado=0,activo=True).values("id","descripcion")

        return context
# @login_required(login_url="/login/")
from django.core import serializers
from django.http import HttpResponse

class DetalleLlantaView(LoginRequiredMixin,DetailView):
    model = Llanta
    template_name = "Web/detalle_llanta.html"
    context_object_name="obj"
def getLlanta(request):
    if request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        print(f'El id es {post}')
        qs = Llanta.objects.get(id=int(post)).toJSON()
        return JsonResponse(qs, content_type='application/json')
def getVehiculo(request):
    if request.method=="POST":
        post = json.loads(request.body.decode("utf-8"))
        print(post)
        qs = Vehiculo.objects.get(id=post["id"])
        qs_json = serializers.serialize('json', [qs],  use_natural_foreign_keys=True,use_natural_primary_keys=True)
        return HttpResponse(qs_json, content_type='application/json')
def AnchoBandaRenovaSearch(request):
    template_name="Web/buscarrenova.html"
    product=Renovadora.objects.all()

    contexto={"obj":product}
    return render(request,template_name,contexto)
def view_condicion(request):
    template_name="Web/condicion.html"
    return render(request,template_name)

def view_renova(request):
    template_name="Web/reencauchado.html"
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

class DesmontajeLlantaView(LoginRequiredMixin,TemplateView):
    template_name = "Web/desmontaje_llanta.html"
    def get(self,request,*args, **kwargs):
        estado=EstadoLlanta.objects.all().values("id","descripcion")
        print(f'el get esta en {request.GET}')
        context={"condicion":estado,"obs":CHOICES_OBSERVACION,"obj":request.GET}
        return render(self.request,self.template_name,context)
    def post(self,request,*args, **kwargs):
        # print(request.POST)
        try:
            llanta=Llanta.objects.filter(id=request.POST["llanta"])
            if llanta.exists():
                with transaction.atomic():

                    objeto=llanta.first()
                    objeto.vehiculo=None
                    objeto.posicion=None
                    objeto.estado_id=request.POST["estado"]

                    objeto.ubicacion_id=request.POST["ubicacion"]
                    objeto.save()
                    historial=HistorialLLantas()
                    historial.llanta=objeto
                    historial.km=request.POST["kilometros"]
                    historial.estado_id=request.POST["estado"]
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
                    response={"status":200}
            else:
                response={"status":500,"message":"Esa llanta no existe."}

            return JsonResponse(response,safe=False)
        except Exception as e:
            print(e)
            messages.error(self.request, 'Ha ocurrido un error.')
            return HttpResponseRedirect(reverse_lazy("Web:inicio"))
class HojaDeMovimientosView(LoginRequiredMixin,TemplateView):
    template_name="Web/hoja_movimientos.html"   

    def post(self,request,*args, **kwargs):
        data=[]
        post = json.loads(request.body.decode("utf-8"))
        qs = Vehiculo.objects.get(id=post["id"]).toJSON()
        nm = Llanta.objects.filter(vehiculo=post["id"]).order_by("posicion")
        for i in nm:
           data.append(i.toJSON2())
        return JsonResponse({"vehiculo":qs,"llantas":data},safe=False, content_type='application/json')
    def get_context_data(self, **kwargs):
        context = super(HojaDeMovimientosView, self).get_context_data(**kwargs)
        context["placa"]=Vehiculo.objects.all().values("id","placa")
        context["ubicaciones"]=Ubicacion.objects.filter(eliminado=False,activo=True)
        return context
class InspeccionLlantasView(LoginRequiredMixin,TemplateView):
    template_name="Web/inspeccion_llantas.html"
