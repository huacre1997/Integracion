
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http.response import HttpResponseRedirect
from django.views.generic.base import ContextMixin, TemplateView
from .models import ( Usuario )
from django.contrib import messages
from django.urls import reverse
from Web.constanst import ACCIONES
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginSelectPerfilView(ContextMixin, View):
    @method_decorator(login_required(login_url='/Web/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class LoginView(ContextMixin, View):
    @method_decorator(login_required(login_url='/Web/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    login_url = '/Web/login/'
    opcion = None
    menu = None
    usuario = None

    def dispatch(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        try:
            self.usuario = Usuario.objects.filter(id=self.request.user.id).first()
            print(self.usuario)
        except Exception as identifier:
            return HttpResponseRedirect(reverse('Web:logout'))
        # if not self.have_permist():
        #     return HttpResponseRedirect(reverse('Web:error403'))
        return super().dispatch(request, *args, **kwargs)
    
    def have_permist(self):
        try:
            # import pdb; pdb.set_trace()
            url = self.request.path
            if url in self.permits_users() or self.action in ACCIONES:
                return True
            else:
                return False
        except Exception as e:
            return False


    def permits_users(self):
        try:
            usuario = Usuario.objects.filter(id=self.request.user.id).first()
            perfiles = usuario.perfil.filter(pk=self.request.session['perfil_id']).first().menu.all()
            urls = []
            for p in perfiles:
                urls.append(p.url)
            urls.append('/Web/inicio/')
            return urls
        except Exception as e:
            messages.warning(self.request, str(e))
            return []