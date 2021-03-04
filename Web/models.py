from django.db import models
import uuid
from Web.constanst import *
from functools import partial
from .functions import letters
import uuid
import os
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from django.contrib.auth.models import Group,Permission
from django.conf import settings
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

def _update_filename(instance, filename, path):
	filename_aux=''
	for c in filename:
		if c in letters:
			filename_aux = filename_aux + c

	return os.path.join(path, filename_aux)


def upload_to(path):
    return partial(_update_filename, path=path)


class Empresa(models.Model):
   uuid_empresa=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
   nombre = models.CharField(max_length=200, null=True)
   direccion = models.CharField(max_length=200, null=True)
   telefono = models.CharField(max_length=20, null=True)
   email = models.CharField(max_length=100, null=True)
   banco = models.CharField(max_length=100, null=True)
   banco_abr = models.CharField(max_length=100, null=True)
   cta_corriente = models.CharField(max_length=100, null=True)
   cci = models.CharField(max_length=100, null=True)
   
   def __unicode__(self):
      return self.nombre



class TipoServicio(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   
   def __str__(self):
      return self.descripcion

class Departamento(models.Model):
	code = models.CharField(max_length=5)
	descripcion = models.CharField(max_length=100)

	def __str__(self):
		return self.descripcion

class Provincia(models.Model):
	departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
	code = models.CharField(max_length=5)
	descripcion = models.CharField(max_length=100)

	def __str__(self):
		return self.descripcion

class Distrito(models.Model):
	provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
	code = models.CharField(max_length=5)
	descripcion = models.CharField(max_length=100)

	def __str__(self):
		return self.descripcion
class Contacto(models.Model):
   
   first_name=models.CharField(_("Nombres"), max_length=50)
   last_name=models.CharField(_("Apellidos"), max_length=50)
   tel=models.CharField(_("telefono"), max_length=8)
   cel=models.CharField(_("Celular"), max_length=9)
   email=models.EmailField(_("Email"), max_length=100)
   
class Direccion(models.Model):
   direccion=models.CharField(_("Direccion"), max_length=150)
   referecias=models.CharField(_("Referencias"), max_length=150)
   departa=models.ForeignKey(Departamento, verbose_name=_("departamento"), on_delete=models.PROTECT)
   provincia=models.ForeignKey(Provincia, verbose_name=_("Provincia"), on_delete=models.PROTECT)
   distrito=models.ForeignKey(Distrito, verbose_name=_("Provincia"), on_delete=models.PROTECT)

   

class Cliente(models.Model):
   
   tip_doc=models.CharField(choices=CHOICES_TIPO_DOC2, max_length=50)
   nr_doc=models.CharField(_(""), max_length=20)
   contacto=models.ForeignKey(Contacto, verbose_name=_("Contacto"), on_delete=models.PROTECT)
   created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
   modified_at = models.DateTimeField(auto_now=True, editable=False)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
class Proveedor(models.Model):
   ruc=models.CharField(_("ruc"), max_length=11)
   rsocial=models.CharField(_("Razon Social"), max_length=100)
   servicio=models.ForeignKey(TipoServicio, verbose_name=_("Servicio"), on_delete=models.PROTECT)
   contacto=models.ForeignKey(Contacto, verbose_name=_("Contacto"), on_delete=models.PROTECT)
   created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
   modified_at = models.DateTimeField(auto_now=True, editable=False)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
class ProveedorDireccion(models.Model):
   prov=models.ForeignKey(Proveedor, on_delete=models.PROTECT,null=True,default=True)
   direc=models.ForeignKey(Direccion,on_delete=models.PROTECT,null=True,default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
   modified_at = models.DateTimeField(auto_now=True, editable=False)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
class ClienteDireccion(models.Model):
   cliente=models.ForeignKey(Cliente, verbose_name=_("cliente"), on_delete=models.PROTECT)
   direc=models.ForeignKey(Direccion, verbose_name=_("direccion"), on_delete=models.PROTECT)
   created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
   modified_at = models.DateTimeField(auto_now=True, editable=False)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
class Persona(models.Model):
   uuid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
   tip_doc = models.IntegerField(choices=CHOICES_TIPO_DOC2, default=TIPO_DOC_DNI)
   nro_doc=models.CharField(max_length=15)
   nom=models.CharField(max_length=100)
   apep=models.CharField(max_length=100)
   apem=models.CharField(max_length=100, null=True, blank=True)
   fech_nac=models.DateField(null=True,blank=True)
   fech_inicio=models.DateField(null=True,blank=True)
   fech_fin=models.DateField(null=True,blank=True)

   sexo=models.IntegerField(choices=CHOICES_SEXO, blank=True, null=True)
   departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, null=True, blank=True)
   provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, null=True, blank=True)
   distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT, null=True, blank=True)
   direccion = models.CharField(max_length=100, null=True, blank=True)
   referencia = models.CharField(max_length=300, null=True, blank=True)
   celular = models.CharField(max_length=9, null=True, blank=True)
   telefono = models.CharField(max_length=9, null=True, blank=True)
   correo = models.CharField(max_length=50, null=True, blank=True)
   area=models.CharField( max_length=50,null=True,blank=True)
   cargo=models.CharField( max_length=50,null=True,blank=True)

   foto_nueva = models.FileField(upload_to = upload_to('documentos/fotos/'), null=True, blank=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
   modified_at = models.DateTimeField(auto_now=True, editable=False)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   class Meta:
      ordering =["-created_at"]
   def get_image(self):
        if self.foto_nueva:
            return '{}{}'.format(settings.MEDIA_URL,self.foto_nueva)
        return '{}{}'.format(settings.STATIC_URL,"img/img_avatar1.png")
   def __str__(self):
      return self.apep + ' '  + self.apem + ' ' + self.nom
   def toJSON(self):
      item = model_to_dict(self)
      item["foto_nueva"]=self.get_image()
      return item
class Usuario(AbstractUser):
   persona = models.OneToOneField(Persona, on_delete=models.CASCADE,null=True,blank=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   def save(self, *args, **kwargs):
      if self.persona:
         self.email=self.persona.correo
      # if self.groups:
      #    if("Administrador" in [i.name for i in self.groups.all()]):
      #       self.is_staff=True
      super(Usuario, self).save(*args, **kwargs)
    

   def toJSON(self):
      item = model_to_dict(self)
      item["created_at"]=self.created_at.strftime('%Y-%m-%d')
      item["groups"]= item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
      item["persona"]=self.persona.toJSON()
      return item
   def toJSON2(self):
      item = model_to_dict(self,exclude=["groups","created_at"])
      item["persona"]=self.persona.nom+" "+self.persona.apep+" "+self.persona.apem
      return item

@receiver(post_save, sender=Usuario)
def update_user(sender, instance, **kwargs):
   if instance.persona:

      if instance.is_active:
         instance.persona.eliminado=False
      else:
         instance.persona.eliminado=True
      instance.persona.save()

class Ubicacion(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   
   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","modified_at","eliminado","created_by","modified_at"])
      return item
class Almacen(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   
   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","modified_at","eliminado","created_by","modified_at"])
      return item

class Lugar(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   
   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","modified_at","eliminado","created_by","modified_at"])
      return item
class MarcaRenova(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","modified_at","eliminado","created_by","modified_at"])
      return item

class ModeloRenova(models.Model):
   marca_renova = models.ForeignKey(MarcaRenova, on_delete=models.PROTECT, related_name="modelos_renova")
   descripcion = models.CharField(max_length=100)
   profundidad = models.DecimalField(max_digits=10, decimal_places=2)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","modified_at","eliminado","created_by","modified_at"])
      item["marca_renova"]=self.marca_renova.toJSON()
      return item

class AnchoBandaRenova(models.Model):
   modelo_renova = models.ForeignKey(ModeloRenova, on_delete=models.PROTECT)
   descripcion = models.CharField(max_length=100)
   ancho_banda = models.DecimalField(max_digits=10, decimal_places=2)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","modified_at","eliminado","created_by","modified_at"])
      item["modelo_renova"]=self.modelo_renova.toJSON()
      return item

class MarcaLlanta(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["activo","modified_by","eliminado","created_by","modified_at"])
      return item
class ModeloLlanta(models.Model):
   marca_llanta = models.ForeignKey(MarcaLlanta, on_delete=models.PROTECT, related_name="modelos")
   descripcion = models.CharField(max_length=100)

   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["created_by","modified_by"])
      item=self.marca_llanta.toJSON()
      return item
      

class MedidaLlanta(models.Model):
   modelo_llanta = models.ForeignKey(ModeloLlanta, on_delete=models.PROTECT)
   descripcion = models.CharField(max_length=100, null=True, blank=True)
   medida = models.CharField(max_length=50)
   profundidad = models.DecimalField(max_digits=10, decimal_places=2)
   capas = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return 'Medida {} - {} - {}'.format(str(self.medida), str(self.profundidad), str(self.capas))
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","created_by"])
      item["modelo_llanta"]= self.modelo_llanta.toJSON()
      item["descripcion"]='Medida {} - {} - {}'.format(str(self.medida), str(self.profundidad), str(self.capas))
      return item
      

class EstadoLlanta(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   
   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","created_by"])
      return item
        

class TipoPiso(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   
   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","created_by"])
      return item
        


class MarcaVehiculo(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["created_by","modified_by"])
      return item

class ModeloVehiculo(models.Model):
   marca_vehiculo = models.ForeignKey(MarcaVehiculo, on_delete=models.PROTECT, related_name="modelos")
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["created_by","modified_by"])
      item["marca-vehiculo"]=self.marca_vehiculo.toJSON()
      return item
class TipoVehiculo(models.Model):
   descripcion = models.CharField(max_length=100)
   croquis = models.FileField(upload_to = 'documentos/croquis_vehiculo/')
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.descripcion
   def get_image(self):
        if self.croquis:
            return '{}{}'.format(settings.MEDIA_URL,self.croquis)
   def toJSON(self):
      item = model_to_dict(self,exclude=["created_by","modified_by"])

      item["croquis"]=self.get_image()


      return item

class Vehiculo(models.Model):
   class Operacion(models.TextChoices):
        COMBUSTIBLE = "1", _('COMBUSTIBLE')
        MINERALES = "2", _('MINERALES')
   ano = models.IntegerField(null=True)
   modelo_vehiculo = models.ForeignKey(ModeloVehiculo, on_delete=models.PROTECT)
   tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.PROTECT)
   ubicacion = models.CharField( max_length=50,null=False,blank=True)
   almacen = models.ForeignKey(Almacen, null=True, on_delete=models.PROTECT)
   propiedad = models.CharField(max_length=50, null=True)
   placa = models.CharField(max_length=50, null=True, blank=True)
   operacion = models.CharField(max_length=2,choices=Operacion.choices, null=True, blank=True)
   km = models.DecimalField(max_digits=10, decimal_places=2)
   nro_ejes = models.IntegerField(null=True)
   nro_llantas = models.IntegerField(null=True)
   nro_llantas_repuesto = models.IntegerField(null=True)
   obs = models.TextField(null=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   activo=models.BooleanField(default=True)

   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.placa
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","almacen"])
      item["created_by"]=self.created_by.toJSON2()

      item["created_at"]=self.created_at.strftime('%Y-%m-%d')
      item["modelo_vehiculo"]=self.modelo_vehiculo.toJSON()
      item["tipo_vehiculo"]=self.tipo_vehiculo.toJSON()

      return item
class Renovadora(models.Model):
   nombre=models.CharField(max_length=100,null=True,blank=True)
   diseño=models.CharField(max_length=100, null=True,blank=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   def __str__(self):
      return self.nombre
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_by","created_by"])
      return item
        
class  CubiertaLlanta(models.Model):
   class TipoCubierta(models.TextChoices):
        NUEVO = "1", _('Nuevo')
        REENCAUCHADO = "2", _('Reencauchado')
   nro_ren=models.CharField(max_length=2,null=True,blank=True,default=None)      
   categoria=models.CharField(max_length=10, default=TipoCubierta.NUEVO,choices=TipoCubierta.choices)
   costo = models.DecimalField(max_digits=10, decimal_places=2)
   km = models.DecimalField(max_digits=10, decimal_places=2)
   a_final = models.DecimalField(max_digits=10, decimal_places=2)
   a_inicial=models.DecimalField(max_digits=10, decimal_places=2)
   a_promedio=models.DecimalField(max_digits=10, decimal_places=2)
   fech_ren=models.DateField()
   modelo_renova=models.ForeignKey(ModeloRenova, on_delete=models.PROTECT,blank=True,null=True,default=None)
   ancho_banda=models.ForeignKey(AnchoBandaRenova, on_delete=models.CASCADE,blank=True,null=True,default=None)
   renovadora=models.ForeignKey(Renovadora,on_delete=models.CASCADE,blank=True,null=True,default=None)
   
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   def toJSON(self):
      item = model_to_dict(self,exclude=["eliminado","modelo_renova","ancho_banda","eliminado","renovadora","created_by","modified_by"])
      item["costo"]=self.costo
      item["km"]=self.km
      return item
class Llanta(models.Model):

   marca_llanta = models.ForeignKey(MarcaLlanta, on_delete=models.PROTECT,null=True)

   modelo_llanta = models.ForeignKey(ModeloLlanta, on_delete=models.PROTECT,null=True)
   medida_llanta = models.ForeignKey(MedidaLlanta, on_delete=models.PROTECT)
   # ubicacion = models.CharField(max_length=50, choices=CHOICES_UBICACION_LLANTA,null=True,blank=True)
   cubierta=models.ForeignKey(CubiertaLlanta, verbose_name=_("Cubierta"), on_delete=models.PROTECT,null=True,blank=True)
   ubicacion = models.ForeignKey(Ubicacion,on_delete=models.PROTECT,null=True,blank=True)

   vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name="llantas", null=True,blank=True,default=None)
   
   codigo = models.CharField(max_length=100, null=True, blank=True)
   posicion=models.IntegerField(blank=True,null=True,default=None)
   repuesto=models.BooleanField(default=False)

   almacen = models.ForeignKey(Almacen, null=True, on_delete=models.PROTECT,blank=True)
   estado = models.ForeignKey(EstadoLlanta, on_delete=models.PROTECT, null=True)
   
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   def __str__(self):
      return self.codigo
   def toJSON(self):
      item = model_to_dict(self,exclude=["almacen","estado","eliminado","activo","modified_at","eliminado","created_by","modified_by"])
      item["marca_llanta"]=self.marca_llanta.descripcion
      item["modelo_llanta"]=self.modelo_llanta.descripcion
      item["medida"]='Medida {} - {} - {}'.format(str(self.medida_llanta.medida), str(format(self.medida_llanta.profundidad, '.2f')), str(format(self.medida_llanta.capas, '.2f')))
      item["km"]=format(self.cubierta.km, '.2f')
      item["costo"]=format(self.cubierta.costo, '.2f')
      
      item["created_at"]=self.created_at.strftime('%Y-%m-%d')  
      if self.vehiculo: 
         item["vehiculo"]=self.vehiculo.placa
      return item
   def toJSON2(self):
      item = model_to_dict(self,exclude=["almacen","marca_llanta","medida_llanta","activo","modelo_llanta","cubierta","vehiculo","ubicacion"])
    
      return item
   @property
   def code(self):
      # import pdb; pdb.set_trace()
      ano = str(datetime.today().year)[2:4]
      ultimo = Llanta.objects.all().last()
      if ultimo:
         aux = ultimo.pk
      else:
         aux = 0
      codigo = '{}{}'.format(ano, str((aux + 1)).zfill(6))
      return codigo
class HistorialLLantas(models.Model):
  
   llanta=models.ForeignKey(Llanta,on_delete=models.PROTECT,blank=True,null=True)
   km=models.CharField( max_length=20,blank=True,null=True)
   profundidad=models.CharField(max_length=20,blank=True,null=True)
   vehiculo=models.ForeignKey(Vehiculo, verbose_name=_("Vehículo"), on_delete=models.PROTECT,blank=True,null=True)
   posicion=models.CharField(max_length=5,blank=True,null=True)
   estado=models.ForeignKey(EstadoLlanta,on_delete=models.PROTECT,blank=True,null=True)
   obs=models.CharField(max_length=50,choices=CHOICES_OBSERVACION,blank=True,null=True)
   ubicacion=models.ForeignKey(Ubicacion,on_delete=models.PROTECT,blank=True,null=True)
   activo = models.BooleanField(default=True)
   eliminado=models.BooleanField(default=False,editable=False)

   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   
   
class InpeccionLlantas(models.Model):
     
   vehiculo=models.ForeignKey(Vehiculo,on_delete=models.PROTECT,null=True,blank=True)
   fech_ins=models.DateField(blank=True,null=True)
   km_act=models.CharField(max_length=50,blank=True,null=True)
   km_ult=models.CharField(max_length=50,blank=True,null=True)
   km_re=models.CharField(max_length=50,blank=True,null=True)
   operacion=models.CharField(choices=CHOICES_OPERACION, max_length=50,blank=True,null=True)
   supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_supervisor')
   tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_tecnico')

   fech_km_ant=models.DateField(blank=True,null=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
import decimal
class DetalleInspeccion(models.Model):
  
   inspeccion=models.ForeignKey(InpeccionLlantas, verbose_name=_(""), on_delete=models.PROTECT,blank=True,null=True)
   llanta=models.ForeignKey(Llanta, verbose_name=_("Llanta"), on_delete=models.PROTECT,null=True,blank=True)
   posicion=models.CharField(_("Posicion"), max_length=5,blank=True,null=True)
   cubierta=models.CharField(choices=CHOICES_CUBIERTA_INSPECCION  ,max_length=10,blank=True,null=True)
   rem1=models.IntegerField(blank=True,null=True,default=0)
   rem2=models.IntegerField(blank=True,null=True,default=0)
   rem3=models.IntegerField(blank=True,null=True,default=0)
   rem_prom= models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True,default=0.00)
   rem_max=models.CharField(_("Presión inicial"), max_length=10,blank=True,null=True)
   rem_min=models.CharField(_("Presión inicial"), max_length=10,blank=True,null=True)
   pres_ini=models.CharField(_("Presión inicial"), max_length=10,blank=True,null=True)
   pres_fin=models.CharField(_("Presión final"), max_length=10,blank=True,null=True)
   obs=models.CharField(_("Observación"), choices=CHOICES_OBSERVACION,max_length=50)
   accion=models.CharField(_("Acción"),choices=CHOICES_ACCION,max_length=50)
   repuesto=models.BooleanField(blank=True,null=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)
   def toJSON(self):
      item = model_to_dict(self,exclude=["modified_at","created_by","modified_by","inspeccion"])
      item["codigo"]=self.llanta.codigo
      item["rem_prom"]=format(self.rem_prom,".2f")
      return item
   
   
@receiver(post_save, sender=DetalleInspeccion)
def detalle_inspeccion(sender,instance,**kwargs):
   print(sender)
   print()
   ex=Llanta.objects.filter(pk=instance.llanta.id).first()
   if ex:
      print("if")
      ex.ubicacion_id=None
      ex.vehiculo=instance.inspeccion.vehiculo
      ex.posicion=instance.posicion
      ex.repuesto=instance.repuesto
      ex.save()
   else:
      print("else")
