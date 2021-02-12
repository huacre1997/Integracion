from Web.models import *
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django import template
from django.contrib import auth
from django.contrib.auth import logout
import time
import os
from Web.constanst import APP_GESTION
from django.shortcuts import redirect
from django.contrib import messages

register = template.Library()


@register.simple_tag
def MenuUsuario(request):
    # import pdb; pdb.set_trace()
    try:
        usuario = Usuario.objects.get(user=request.user)
        menus=usuario.perfil.all()[0].menu.all()
        urls=[id.pk for id in menus] 
        template = 'web/menu/tree_cats.html'        
        folders = Menu.objects.filter(parent = None, aplication=APP_GESTION).order_by('orden')
        context = {
            'folders': folders,
            'urls': urls,
            'perfil': request.session.get('perfil_id')
        }
        rendered = render_to_string(template, context)
        return rendered
    except Exception as e:
        print(e)
        messages.error(request, str(e))
        #return HttpResponse('<script>location.href = "/Web/logout/";</script>')


@register.filter(name="has_group")
def has_group(usuario,grupo):
    return usuario.groups.filter(name__exact=grupo).exists()

@register.simple_tag
def UsuarioPerfil(request):
    try:
        idUsuario = request.user.id
        idPerfil = Usuario.objects.get(usuario_id=idUsuario)
        #idPerfil = request.session['id_perfil']
        #perfil = Perfil.objects.get(id_perfil = idPerfil.pk)
        return idPerfil.perfil
    except:
        return redirect('Web/logout/')


@register.filter()
@register.simple_tag
def InMenu(perfil, id):
    #import ipdb; ipdb.set_trace()
    p = perfil.filter(id_perfil=id)
    return p


@register.simple_tag
def relative_url(urlencode):
    url = ''
    for d in urlencode.items():
        if d[0] != 'page':
            url=url + u'&{}={}'.format(d[0],d[1])
    return url


# @register.simple_tag
# def number_page(number, page, pages):
#     return number + ((page - 1) * pages)