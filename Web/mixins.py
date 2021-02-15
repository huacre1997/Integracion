from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import Permission,Group
import string
class ValidateMixin(object):
    permission_required=""
    url_redirect=None
    def get_perms(self):

        if isinstance(self.permission_required,str): 
           
            return (self.permission_required).split()

        else:
            return self.permission_required
    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy("Web:login")
        return self.url_redirect
    
    def dispatch(self, request, *args, **kwargs):
        if len(self.get_perms())==1:
            if self.get_perms()[0] in self.request.user.get_group_permissions():
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request,"No tienes permisos para ese módulo")
                return redirect(self.get_url_redirect())
            
        else:
            if set(self.request.user.get_group_permissions())==set(self.get_perms()):
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request,"No tienes permisos para ese módulo")
                return redirect(self.get_url_redirect())

class AdminPermission(object):
    permission_required:""
    url_redirect=None
    
    def get_perms(self):
        # x=[(x.codename) for x in Permission.objects.all()]
        # y=list(self.request.user.get_group_permissions())
        data=[]
        group= self.request.user.groups.all().values("name")
        for i in group:
            data.append(i["name"])
        return data
    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy("Web:login")
        return self.url_redirect
    
    def dispatch(self, request, *args, **kwargs):
        if "Administrador" in (self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request,"No tienes permisos para ese módulo")
        return redirect(self.get_url_redirect())
    
