from django.db import models
import uuid
from Web.constanst import (CHOICES_APP, APP_GESTION, CHOICES_TIPO_DOC2, 
   CHOICES_SEXO, TIPO_DOC_DNI, ESTADO_1, CHOICES_ESTADOS )  
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

      super(Usuario, self).save(*args, **kwargs)
    

   def toJSON(self):
      item = model_to_dict(self)
      item["created_at"]=self.created_at.strftime('%Y-%m-%d')
      item["groups"]= item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
      item["persona"]=self.persona.toJSON()
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


class ModeloRenova(models.Model):
   marca_renova = models.ForeignKey(MarcaRenova, on_delete=models.PROTECT, related_name="modelos_renova")
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.descripcion


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
        item = model_to_dict(self)
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


class MedidaLlanta(models.Model):
   modelo_llanta = models.ForeignKey(ModeloLlanta, on_delete=models.PROTECT)
   descripcion = models.CharField(max_length=100, null=True, blank=True)
   medida = models.DecimalField(max_digits=10, decimal_places=2)
   profundidad = models.DecimalField(max_digits=10, decimal_places=2)
   capas = models.DecimalField(max_digits=10, decimal_places=2)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return 'Medida {} - {} - {}'.format(str(self.medida), str(self.profundidad), str(self.capas))


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


class Vehiculo(models.Model):
   ano = models.IntegerField(null=True)
   modelo_vehiculo = models.ForeignKey(ModeloVehiculo, on_delete=models.PROTECT)
   tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.PROTECT)
   ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, null=True)
   almacen = models.ForeignKey(Almacen, null=True, on_delete=models.PROTECT)
   propiedad = models.CharField(max_length=50, null=True)
   placa = models.CharField(max_length=50, null=True, blank=True)
   operacion = models.CharField(max_length=100, null=True, blank=True)
   km = models.DecimalField(max_digits=10, decimal_places=2)
   nro_ejes = models.IntegerField(null=True)
   nro_llantas = models.IntegerField(null=True)
   nro_llantas_repuesto = models.IntegerField(null=True)
   obs = models.TextField(null=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.placa


class Llanta(models.Model):
   modelo_llanta = models.ForeignKey(ModeloLlanta, on_delete=models.PROTECT)
   vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name="llantas", null=True)
   codigo = models.CharField(max_length=100, null=True, blank=True)
   medida_llanta = models.ForeignKey(MedidaLlanta, on_delete=models.PROTECT)
   ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
   almacen = models.ForeignKey(Almacen, null=True, on_delete=models.PROTECT)
   costo = models.DecimalField(max_digits=10, decimal_places=2)
   km = models.DecimalField(max_digits=10, decimal_places=2)
   estado = models.ForeignKey(EstadoLlanta, on_delete=models.PROTECT, null=True)
   obs = models.TextField(null=True)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   modified_at = models.DateTimeField(auto_now=True)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
   eliminado=models.BooleanField(default=False,editable=False)

   def __str__(self):
      return self.codigo
   
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