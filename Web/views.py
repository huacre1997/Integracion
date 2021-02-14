#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.urls import reverse_lazy

from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import FormView, CreateView, ListView, UpdateView
from django.views.generic import FormView
from django.contrib.auth.models import Group,Permission
from .forms import (UserGroupForm,LoginForm, PersonaForm, UsuarioForm,
    UbicacionForm, MarcaRenovaForm, ModeloRenovaForm, AnchoBandaRenovaForm, 
    MarcaLlantaForm ,ModeloLlantaForm, MedidaLlantaForm, AlmacenForm, LugarForm, EstadoLlantaForm,
    TipoPisoForm, TipoServicioForm, MarcaVehiculoForm, ModeloVehiculoForm, LlantaForm, VehiculoForm)
from django.http.response import HttpResponseRedirect
from django.contrib import messages, auth
from .common import LoginView, LoginSelectPerfilView
from django.urls import reverse
from .models import (Persona, Usuario, Ubicacion, MarcaRenova, ModeloRenova, AnchoBandaRenova,
    MarcaLlanta, ModeloLlanta, MedidaLlanta, Almacen, Lugar, EstadoLlanta, TipoServicio, TipoPiso, 
    MarcaVehiculo, ModeloVehiculo, Vehiculo, Llanta,Provincia,Distrito)
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
        print(post)
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
        print(username)
        print(password)
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            print("if")
            auth.login(self.request, user)
            messages.success(self.request,f"Bienvenido {self.request.user}",extra_tags="login")

            return redirect(self.success_url)
        else:
            print("else")
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



class PerfilesTemplateView(LoginRequiredMixin,AdminPermission ,TemplateView):
    template_name = "Web/perfiles.html"
    context_object_name = 'perfiles'
    login_url=reverse_lazy("Web:login")
    def post(self, request, *args, **kwargs):
        #import pdb; pdb.set_trace()
        try:
            #persona = Persona.objects.get(id_usuario=self.request.user)
            # request.session['perfil_id'] = int(request.POST['perfil'])
            return HttpResponseRedirect("/Web/inicio")            
        except Exception as e:
            messages.error(request, str(e))
            return HttpResponseRedirect("/Web/login")            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #import ipdb; ipdb.set_trace()
        # usuario = Usuario.objects.filter(user=self.request.user).first()
        context['perfiles'] = Group.objects.all()
        # context['perfiles'] = usuario.perfil.all()
        #context['url_foto'] = settings.URL_FOTO
        return context
class PerfilCreateView(LoginRequiredMixin, CreateView):
    model=Group
    form_class = UserGroupForm
    template_name = 'Web/perfil.html'
    success_url = reverse_lazy("Web:Perfiles") 
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        print("if")

        instance = form.save(commit=False)
        
        messages.success(self.request, 'Perfil guardado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)     


class PerfilUpdateView(LoginRequiredMixin, AdminPermission,UpdateView):
    form_class = UserGroupForm
    model = Group
    template_name = "Web/perfil.html"
    context_object_name="perfil"
    success_url = reverse_lazy("Web:Perfiles")
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update(instance={
    #         'perfiles': self.object
    #     })
    #     return kwargs
        
    def form_valid(self, form):
        instance = form.save(commit=False)
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context




class ListUsuariosListView(LoginRequiredMixin, ValidateMixin,ListView):
    template_name = 'Web/list_usuarios.html'
    model = Usuario
    context_object_name = 'usuarios'
    permission_required=["Web.view_usuario"]
    login_url=reverse_lazy("Web:login")

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
                    data.append(i.toJSON())
                
            else:
                data["error"]="Ha ocurrido un error"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)
    # def get_queryset(self):
    #     # import pdb; pdb.set_trace();
    #     qs = super().get_queryset()
    #     qs = qs.filter(eliminado=False)
    #     q = self.request.GET.get('q', None)
    #     print(q)
    #     if q:
    #         if q.isdigit():
    #             qs = qs.filter(Q(persona__nro_doc__icontains=q))
    #         else:
    #             terms = q.split(" ")
    #             search = [
    #                 (Q(persona__nom__icontains=word) | 
    #                 Q(persona__apep__icontains=word) | 
    #                 Q(persona__apem__icontains=word)
    #             ) for word in terms]
    #             qs = qs.filter(*search)
    #     return qs
class PersonaListView(LoginRequiredMixin,ListView):
    template_name = 'Web/personas.html'
    model = Persona
    login_url=reverse_lazy("Web:login")

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in Persona.objects.all():
                    data.append(i.toJSON())
            else:
                data["error"]="Ha ocurrido un error"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)
   
class PersonaUpdateView(LoginRequiredMixin,UpdateView):
    model = Persona
    template_name="Web/persona.html"

    context_object_name = "persona" 
    form_class = PersonaForm
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
            print(e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["provincia"] = Provincia.objects.filter(departamento=self.object.departamento)
        context["distrito"] = Distrito.objects.filter(provincia=self.object.provincia)
 
        return context
    
class PersonaCreateView(LoginRequiredMixin,CreateView):
    model=Persona
    template_name = 'Web/persona.html'
    form_class=PersonaForm
    login_url=reverse_lazy("Web:login")
    action = ACCION_NUEVO
    
    def post(self,request,*args, **kwargs):
        data={}
        print(request.POST)
        try:
            action=request.POST["action"]
            if action=="add":
                form = self.get_form()
                if form.is_valid():     
                    form.save()    
                    print("if form valid create")
                    data = {  }
                    return JsonResponse(data)
                else:
                    data = {
                    "error":form.errors,
                    'stat': False,
                    }
                    return JsonResponse(data)
            else:
                print("else")
                data["error"]="Nose ha ingresado nadas"
                return HttpResponse("error")
        except Exception as e:
            print(e)

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model=Usuario
    template_name = 'Web/usuario.html'
    success_url = reverse_lazy("Web:Usuarios")
    action = ACCION_NUEVO
    form_class=UsuarioForm
    login_url=reverse_lazy("Web:login")

    def post(self,request,*args, **kwargs):
        data={}
        print(request.POST)
        try:
            action=request.POST["action"]
            if action=="add":
                form = self.get_form()
                if form.is_valid():   
                    self.object.groups.clear()
                    self.object.groups.add(form.cleaned_data["groups"])  
                    form.save()    
                    print("if form valid create")
                    data = {  }
                    return JsonResponse(data)
                else:
                    data = {
                    "error":form.errors,
                    'stat': False,
                    }
                    messages.success(self.request, 'Se ha guardado correctamente.')

                    return JsonResponse(data)
            else:
                print("else")
                data["error"]="Nose ha ingresado nadas"

                return HttpResponse("error")
        except Exception as e:
            print(e)     

    # def form_invalid(self, form):
    #     messages.warning(self.request, form.errors)
    #     return super().form_invalid(form)

    # def get_context_data(self, **kwargs):
    #     if 'formUsuario' not in kwargs:
    #         kwargs['formUsuario'] = UsuarioForm()
    #     if 'formPersona' not in kwargs:
    #         kwargs['formPersona'] = PersonaForm()
    #     return kwargs

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    login_url=reverse_lazy("Web:login")

    model = Usuario
    template_name = 'Web/usuario.html'
    context_object_name="usuario"
    form_class=UsuarioForm
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
                    self.object.groups.clear()
                    self.object.groups.set(form.cleaned_data["groups"])  
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
            print(e)

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
    success_url = '/Web/Ubicaciones/'
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
    success_url = '/Web/Ubicaciones/'
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


class UbicacionDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
   
    def get(self, request, *args, **kwargs):
        id_ubicacion = self.kwargs['pk']
        ubicacion = Ubicacion.objects.get(pk=id_ubicacion)
        ubicacion.modified_by=request.user
        ubicacion.eliminado = True
        ubicacion.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:Ubicaciones',))


class AlmacenesListView(LoginRequiredMixin, ListView):
    template_name = 'Web/almacenes.html'
    model = Almacen
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


class AlmacenCreateView(LoginRequiredMixin, CreateView):
    form_class = AlmacenForm
    template_name = 'Web/almacen.html'
    success_url = '/Web/almacenes/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class AlmacenUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AlmacenForm
    model = Almacen
    template_name = 'Web/almacen.html'
    success_url = '/Web/almacenes/'
    action = ACCION_EDITAR
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


class AlmacenDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        Almacen = Almacen.objects.get(pk=id)
        Almacen.modified_by=request.user
        Almacen.eliminado = True
        Almacen.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:almacenes',))


class LugaresListView(LoginRequiredMixin, ListView):
    template_name = 'Web/lugares.html'
    model = Lugar
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


class LugarCreateView(LoginRequiredMixin, CreateView):
    form_class = LugarForm
    template_name = 'Web/lugar.html'
    success_url = reverse_lazy("Web:Lugares")
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class LugarUpdateView(LoginRequiredMixin, UpdateView):
    form_class = LugarForm
    model = Lugar
    template_name = 'Web/lugar.html'
    success_url = '/Web/lugares/'
    action = ACCION_EDITAR
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


class LugarDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
   
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        Lugar = Lugar.objects.get(pk=id)
        Lugar.modified_by=request.user
        Lugar.eliminado = True
        Lugar.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:lugares',))


class MarcaRenovacionesListView(LoginRequiredMixin, ListView):
    template_name = 'Web/marca_renovaciones.html'
    model = MarcaRenova
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


class MarcaRenovacionCreateView(LoginRequiredMixin, CreateView):
    form_class = MarcaRenovaForm
    template_name = 'Web/marca_renovacion.html'
    success_url = '/Web/marca-renovaciones/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class MarcaRenovacionUpdateView(LoginRequiredMixin, UpdateView):
    form_class = MarcaRenovaForm
    model = MarcaRenova
    template_name = 'Web/marca_renovacion.html'
    success_url = '/Web/marca-renovaciones/'
    action = ACCION_EDITAR
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


class MarcaRenovacionDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
   
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


class ModeloRenovacionCreateView(LoginRequiredMixin, CreateView):
    form_class = ModeloRenovaForm
    template_name = 'Web/modelo_renovacion.html'
    success_url = '/Web/modelo-renovaciones/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class ModeloRenovacionUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ModeloRenovaForm
    model = ModeloRenova
    template_name = 'Web/modelo_renovacion.html'
    success_url = '/Web/modelo-renovaciones/'
    action = ACCION_EDITAR
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


class ModeloRenovacionDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = ModeloRenova.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:modelo-renovaciones',))


class AnchoBandaRenovacionesListView(LoginRequiredMixin, ListView):
    template_name = 'Web/ancho_banda_renovaciones.html'
    model = AnchoBandaRenova
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


class AnchoBandaRenovacionCreateView(LoginRequiredMixin, CreateView):
    form_class = AnchoBandaRenovaForm
    template_name = 'Web/ancho_banda_renovacion.html'
    success_url = '/Web/ancho-banda-renovaciones/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class AnchoBandaRenovacionUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AnchoBandaRenovaForm
    model = AnchoBandaRenova
    template_name = 'Web/ancho_banda_renovacion.html'
    success_url = '/Web/ancho-banda-renovaciones/'
    action = ACCION_EDITAR
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
        # import pdb; pdb.set_trace()
        idancho =  self.kwargs['pk']
        context['instance'] = AnchoBandaRenova.objects.filter(pk=idancho).first()
        context['update'] = True
        return context


class AnchoBandaRenovacionDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
   
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


class MarcaLlantasListView(LoginRequiredMixin, ListView):
    template_name = 'Web/marca_llantas.html'
    model = MarcaLlanta
    login_url=reverse_lazy("Web:login")

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
 
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in MarcaLlanta.objects.filter(activo=True):
                    data.append(i.toJSON())
            else:
                data["error"]="Ha ocurrido un error"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)
   

class MarcaLlantaCreateView(LoginRequiredMixin, CreateView):
    form_class = MarcaLlantaForm
    template_name = 'Web/marca_llanta.html'
    success_url = '/Web/marca-llantas/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class MarcaLlantaUpdateView(LoginRequiredMixin, UpdateView):
    form_class = MarcaLlantaForm
    model = MarcaLlanta
    template_name = 'Web/marca_llanta.html'
    success_url = '/Web/marca-llantas/'
    action = ACCION_EDITAR
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

import json
class MarcaLlantaDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
   
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


class ModeloLlantasListView(LoginRequiredMixin, ListView):
    template_name = 'Web/modelo_llantas.html'
    model = ModeloLlanta
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


class ModeloLlantaCreateView(LoginRequiredMixin, CreateView):
    form_class = ModeloLlantaForm
    template_name = 'Web/modelo_llanta.html'
    success_url = '/Web/modelo-llantas/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class ModeloLlantaUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ModeloLlantaForm
    model = ModeloLlanta
    template_name = 'Web/modelo_llanta.html'
    success_url = '/Web/modelo-llantas/'
    action = ACCION_EDITAR
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


class ModeloLlantaDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = ModeloLlanta.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:modelo-llantas',))


class MedidaLlantasListView(LoginRequiredMixin, ListView):
    template_name = 'Web/medida_llantas.html'
    model = MedidaLlanta
    paginate_by = 10
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")

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


class MedidaLlantaCreateView(LoginRequiredMixin, CreateView):
    form_class = MedidaLlantaForm
    template_name = 'Web/medida_llanta.html'
    success_url = '/Web/medida-llantas/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class MedidaLlantaUpdateView(LoginRequiredMixin, UpdateView):
    form_class = MedidaLlantaForm
    model = MedidaLlanta
    template_name = 'Web/medida_llanta.html'
    success_url = '/Web/medida-llantas/'
    action = ACCION_EDITAR
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
        # import pdb; pdb.set_trace()
        id =  self.kwargs['pk']
        context['instance'] = MedidaLlanta.objects.filter(pk=id).first()
        context['update'] = True
        return context


class MedidaLlantaDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    
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
    modelos = ModeloLlanta.objects.filter(eliminado=False, marca_llanta__pk=id_marca)
    return HttpResponse(json.dumps(list(modelos.values('id','descripcion'))), content_type="application/json")


class EstadoLlantasListView(LoginRequiredMixin, ListView):
    template_name = 'Web/estado_llantas.html'
    model = EstadoLlanta
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


class EstadoLlantaCreateView(LoginRequiredMixin, CreateView):
    form_class = EstadoLlantaForm
    template_name = 'Web/estado_llanta.html'
    success_url = '/Web/estado-llantas/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class EstadoLlantaUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EstadoLlantaForm
    model = EstadoLlanta
    template_name = 'Web/estado_llanta.html'
    success_url = '/Web/estado-llantas/'
    action = ACCION_EDITAR
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


class EstadoLlantaDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = EstadoLlanta.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:estado-llantas',))


class TipoServiciosListView(LoginRequiredMixin, ListView):
    template_name = 'Web/tipo_servicios.html'
    model = TipoServicio
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


class TipoServicioCreateView(LoginRequiredMixin, CreateView):
    form_class = TipoServicioForm
    template_name = 'Web/tipo_servicio.html'
    success_url = '/Web/tipo-servicios/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class TipoServicioUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TipoServicioForm
    model = TipoServicio
    template_name = 'Web/tipo_servicio.html'
    success_url = '/Web/tipo-servicios/'
    action = ACCION_EDITAR
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


class TipoServicioDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
   
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = TipoServicio.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:tipo-servicios',))


class TipoPisosListView(LoginRequiredMixin, ListView):
    template_name = 'Web/tipo_pisos.html'
    model = TipoPiso
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


class TipoPisoCreateView(LoginRequiredMixin, CreateView):
    form_class = TipoPisoForm
    template_name = 'Web/tipo_piso.html'
    success_url = '/Web/tipo-pisos/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class TipoPisoUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TipoPisoForm
    model = TipoPiso
    template_name = 'Web/tipo_piso.html'
    success_url = '/Web/tipo-pisos/'
    action = ACCION_EDITAR
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


class TipoPisoDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
   
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = TipoPiso.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:tipo-pisos',))


class MarcaVehiculosListView(LoginRequiredMixin, ListView):
    template_name = 'Web/marca_vehiculos.html'
    model = MarcaVehiculo
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


class MarcaVehiculoCreateView(LoginRequiredMixin, CreateView):
    form_class = MarcaVehiculoForm
    template_name = 'Web/marca_vehiculo.html'
    success_url = '/Web/marca-vehiculos/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class MarcaVehiculoUpdateView(LoginRequiredMixin, UpdateView):
    form_class = MarcaVehiculoForm
    model = MarcaVehiculo
    template_name = 'Web/marca_vehiculo.html'
    success_url = '/Web/marca-vehiculos/'
    action = ACCION_EDITAR
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


class MarcaVehiculoDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = MarcaVehiculo.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:marca-vehiculos',))


class ModeloVehiculosListView(LoginRequiredMixin, ListView):
    template_name = 'Web/modelo_vehiculos.html'
    model = ModeloVehiculo
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


class ModeloVehiculoCreateView(LoginRequiredMixin, CreateView):
    form_class = ModeloVehiculoForm
    template_name = 'Web/modelo_vehiculo.html'
    success_url = '/Web/modelo-vehiculos/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class ModeloVehiculoUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ModeloVehiculoForm
    model = ModeloVehiculo
    template_name = 'Web/modelo_vehiculo.html'
    success_url = '/Web/modelo-vehiculos/'
    action = ACCION_EDITAR
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


class ModeloVehiculoDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = ModeloVehiculo.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:modelo-vehiculos',))


class LlantasListView(LoginRequiredMixin, ListView):
    template_name = 'Web/llantas.html'
    model = Llanta
    paginate_by = 10
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")

    def get_queryset(self):
        # import pdb; pdb.set_trace();
        qs = super().get_queryset()
        qs = qs.filter(eliminado=False)
        modelo = self.request.GET.get('modelo','')
        costo = self.request.GET.get('costo','')
        fi = self.request.GET.get('fecha_inicio')
        ff =self.request.GET.get('fecha_fin')
        
        if modelo:
            qs = qs.filter(modelo_llanta__pk=modelo)
        if costo:
            qs = qs.filter(costo__icontains=costo)
        
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
        context['marcas'] = MarcaLlanta.objects.filter(eliminado=False).order_by('descripcion')
        return context


class LlantaCreateView(LoginRequiredMixin, CreateView):
    form_class = LlantaForm
    template_name = 'Web/llanta.html'
    success_url = '/Web/llantas/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.codigo = instance.code
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class LlantaUpdateView(LoginRequiredMixin, UpdateView):
    form_class = LlantaForm
    model = Llanta
    template_name = 'Web/llanta.html'
    success_url = '/Web/llantas/'
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")

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
        context['instance'] = Llanta.objects.filter(pk=id).first()
        context['update'] = True
        return context


class LlantaDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        obj = Llanta.objects.get(pk=id)
        obj.modified_by=request.user
        obj.eliminado = True
        obj.save()
        messages.success(self.request, 'Operación realizada correctamente.')
        return HttpResponseRedirect(reverse('Web:llantas',))


class VehiculosListView(LoginRequiredMixin, ListView):
    template_name = 'Web/vehiculos.html'
    model = Vehiculo
    paginate_by = 10
    context_object_name = 'objetos'
    login_url=reverse_lazy("Web:login")

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


class VehiculoCreateView(LoginRequiredMixin, CreateView):
    form_class = VehiculoForm
    template_name = 'Web/vehiculo.html'
    success_url = '/Web/vehiculos/'
    action = ACCION_NUEVO
    login_url=reverse_lazy("Web:login")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        messages.success(self.request, 'Operación realizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return super().form_invalid(form)


class VehiculoUpdateView(LoginRequiredMixin, UpdateView):
    form_class = VehiculoForm
    model = Vehiculo
    template_name = 'Web/vehiculo.html'
    success_url = '/Web/vehiculos/'
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")

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


class VehiculoDeleteView(LoginRequiredMixin, View):
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")
    
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


class VerVehiculoView(LoginRequiredMixin, TemplateView):
    template_name = 'Web/ver_vehiculo.html'
    action = ACCION_EDITAR
    login_url=reverse_lazy("Web:login")

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        obj = Vehiculo.objects.get(pk=id)
        context['obj'] = obj
        return context


class AgregarLlantaCreateView(LoginRequiredMixin, CreateView):
    form_class = LlantaForm
    template_name = 'Web/add_llanta.html'
    action = ACCION_NUEVO
    vehiculo = None
    login_url=reverse_lazy("Web:login")

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
