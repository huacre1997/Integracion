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
from django.contrib.auth.models import Group, Permission, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from simple_history.models import HistoricalRecords

def _update_filename(instance, filename, path):
	filename_aux = ''
	for c in filename:
		if c in letters:
			filename_aux = filename_aux + c

	return os.path.join(path, filename_aux)


def upload_to(path):
    return partial(_update_filename, path=path)



class TipoServicio(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  null=True, editable=False, related_name='%(class)s_created')
   
   eliminado = models.BooleanField(default=False, editable=False)

   def __str__(self):
      return self.descripcion


class Departamento(models.Model):
	code = models.CharField(max_length=5,null=True,blank=True)
	descripcion = models.CharField(max_length=100)

	def __str__(self):
		return self.descripcion


class Provincia(models.Model):
	departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
	code = models.CharField(max_length=5,null=True,blank=True)
	descripcion = models.CharField(max_length=100)

	def __str__(self):
		return self.descripcion


class Distrito(models.Model):
	provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
	code = models.CharField(max_length=5,null=True,blank=True)
	descripcion = models.CharField(max_length=100)

	def __str__(self):
		return self.descripcion


class Contacto(models.Model):

   first_name = models.CharField(_("Nombres"), max_length=50)
   last_name = models.CharField(_("Apellidos"), max_length=50)
   tel = models.CharField(_("telefono"), max_length=8)
   cel = models.CharField(_("Celular"), max_length=9)
   email = models.EmailField(_("Email"), max_length=100)


class Direccion(models.Model):
   direccion = models.CharField(_("Direccion"), max_length=150)
   referecias = models.CharField(_("Referencias"), max_length=150)
   departa = models.ForeignKey(Departamento, verbose_name=_(
       "departamento"), on_delete=models.PROTECT)
   provincia = models.ForeignKey(Provincia, verbose_name=_(
       "Provincia"), on_delete=models.PROTECT)
   distrito = models.ForeignKey(Distrito, verbose_name=_(
       "Provincia"), on_delete=models.PROTECT)


class Cliente(models.Model):

   tip_doc = models.CharField(choices=CHOICES_TIPO_DOC2, max_length=50)
   nr_doc = models.CharField(_(""), max_length=20)
   contacto = models.ForeignKey(Contacto, verbose_name=_(
       "Contacto"), on_delete=models.PROTECT)
   created_at = models.DateTimeField(
       auto_now_add=True, null=True, editable=False)
   
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  null=True, editable=False, related_name='%(class)s_created')
  
   eliminado = models.BooleanField(default=False, editable=False)


class Proveedor(models.Model):
   ruc = models.CharField(_("ruc"), max_length=11)
   rsocial = models.CharField(_("Razon Social"), max_length=100)
   servicio = models.ForeignKey(TipoServicio, verbose_name=_(
       "Servicio"), on_delete=models.PROTECT)
   contacto = models.ForeignKey(Contacto, verbose_name=_(
       "Contacto"), on_delete=models.PROTECT)
   created_at = models.DateTimeField(
       auto_now_add=True, null=True, editable=False)
   
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  null=True, editable=False, related_name='%(class)s_created')
  
   eliminado = models.BooleanField(default=False, editable=False)


class ProveedorDireccion(models.Model):
   prov = models.ForeignKey(
       Proveedor, on_delete=models.PROTECT, null=True, default=True)
   direc = models.ForeignKey(
       Direccion, on_delete=models.PROTECT, null=True, default=True)
   created_at = models.DateTimeField(
       auto_now_add=True, null=True, editable=False)
   
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  null=True, editable=False, related_name='%(class)s_created')
  
   eliminado = models.BooleanField(default=False, editable=False)


class ClienteDireccion(models.Model):
   cliente = models.ForeignKey(Cliente, verbose_name=_(
       "cliente"), on_delete=models.PROTECT)
   address = models.ForeignKey(Direccion, verbose_name=_(
       "direccion"), on_delete=models.PROTECT)
   created_at = models.DateTimeField(
       auto_now_add=True, null=True, editable=False)
   
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  null=True, editable=False, related_name='%(class)s_created')
  
   eliminado = models.BooleanField(default=False, editable=False)


class Persona(models.Model):
   uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
   tip_doc = models.IntegerField(
       choices=CHOICES_TIPO_DOC2, default=TIPO_DOC_DNI)
   nro_doc = models.CharField(max_length=15)
   nom = models.CharField(max_length=100)
   apep = models.CharField(max_length=100)
   apem = models.CharField(max_length=100, null=True, blank=True)
   fech_nac = models.DateField(null=True, blank=True)
   fech_inicio = models.DateField(null=True, blank=True)
   fech_fin = models.DateField(null=True, blank=True)

   sexo = models.IntegerField(choices=CHOICES_SEXO, blank=True, null=True)
   departamento = models.ForeignKey(
       Departamento, on_delete=models.PROTECT, null=True, blank=True)
   provincia = models.ForeignKey(
       Provincia, on_delete=models.PROTECT, null=True, blank=True)
   distrito = models.ForeignKey(
       Distrito, on_delete=models.PROTECT, null=True, blank=True)
   direccion = models.CharField(max_length=100, null=True, blank=True)
   referencia = models.CharField(max_length=300, null=True, blank=True)
   celular = models.CharField(max_length=9, null=True, blank=True)
   telefono = models.CharField(max_length=9, null=True, blank=True)
   correo = models.CharField(max_length=50, null=True, blank=True)
   area = models.CharField(max_length=50, null=True, blank=True)
   cargo = models.CharField(max_length=50, null=True, blank=True)

   foto_nueva = models.FileField(upload_to=upload_to(
       'fotos/'), null=True, blank=True)
   created_at = models.DateTimeField(
       auto_now_add=True, null=True, editable=False)
   
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  null=True, editable=False, related_name='%(class)s_created')

   eliminado = models.BooleanField(default=False, editable=False)
   history = HistoricalRecords(table_name='Web_Historial_Persona',user_model=settings.AUTH_USER_MODEL)

   @property
   def _history_user(self):
        return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
        self.changed_by = value  
   class Meta:
      ordering = ["-created_at"]

   def get_image(self):
        if self.foto_nueva:
            return '{}{}'.format(settings.MEDIA_URL, self.foto_nueva)
        return '{}{}'.format(settings.STATIC_URL, "img/img_avatar1.png")

   def __str__(self):
      return self.apep + ' ' + self.apem + ' ' + self.nom

   def toJSON(self):
      item = model_to_dict(self)
      item["foto_nueva"] = self.get_image()
      return item



  
class Usuario(AbstractUser):
   persona = models.OneToOneField(Persona, on_delete=models.CASCADE,null=True,blank=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_Usuario',user_model=settings.AUTH_USER_MODEL)

   @property
   def _history_user(self):
        return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
        self.changed_by = value  
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
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_Ubicacion',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value    
   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["eliminado","changed_by"])
      return item
class Almacen(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   
   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["eliminado","changed_by"])
      return item

class Lugar(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   
   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["eliminado","changed_by"])
      return item
class MarcaRenova(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_MarcaRenova',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value  
   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["eliminado","changed_by"])
      return item

class ModeloRenova(models.Model):
   marca_renova = models.ForeignKey(MarcaRenova, on_delete=models.PROTECT, related_name="modelos_renova")
   descripcion = models.CharField(max_length=100)
   profundidad = models.DecimalField(max_digits=10, decimal_places=2)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_ModeloRenova',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value  
   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["eliminado","changed_by"])
      item["marca_renova"]=self.marca_renova.toJSON()
      return item

class AnchoBandaRenova(models.Model):
   modelo_renova = models.ForeignKey(ModeloRenova, on_delete=models.PROTECT)
   descripcion = models.CharField(max_length=100)
   ancho_banda = models.DecimalField(max_digits=10, decimal_places=2)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_AnchoBandaRenova',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value  
   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["eliminado","changed_by"])
      item["modelo_renova"]=self.modelo_renova.toJSON()
      return item
   def toJSON2(self):
      item = model_to_dict(self,exclude=["changed_by","modelo_renova"])
      item["ancho_banda"]=format(self.ancho_banda, '.2f')

      return item
class MarcaLlanta(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_MarcaLlanta',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value  
   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["eliminado","changed_by"])
      return item
class ModeloLlanta(models.Model):
   marca_llanta = models.ForeignKey(MarcaLlanta, on_delete=models.PROTECT, related_name="modelos")
   descripcion = models.CharField(max_length=100)

   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_ModeloLlanta',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value  
   def __str__(self):
      return self.descripcion
   def toJSON(self):
      item = model_to_dict(self,exclude=["changed_by","activo","created_at","eliminado"])
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
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_MedidaLlanta',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value  
   def __str__(self):
      if self.capas:
         return 'Medida {} - {} - {}'.format(str(self.medida), str(format(self.profundidad, '.2f')), str(format(self.capas, '.2f')))
      else:
         return 'Medida {} - {} '.format(str(self.medida), str(format(self.profundidad, '.2f')))   
   def toJSON(self):
      item = model_to_dict(self,exclude=["changed_by"])
      item["modelo_llanta"]= self.modelo_llanta.toJSON()
      item["descripcion"]='Medida {} - {} - {}'.format(str(self.medida), str(self.profundidad), str(self.capas))
      return item
      

# class EstadoLlanta(models.Model):
#    descripcion = models.CharField(max_length=100)
#    activo = models.BooleanField(default=True)
#    created_at = models.DateTimeField(auto_now_add=True, null=True)
# #    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
# #    eliminado=models.BooleanField(default=False,editable=False)
   
#    def __str__(self):
#       return self.descripcion
#    def toJSON(self):
#       item = model_to_dict(self,exclude=["changed_by"])
#       return item
        

class TipoPiso(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   
   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["changed_by"])
      return item
        


class MarcaVehiculo(models.Model):
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(Usuario,on_delete=models.PROTECT)
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_MarcaVehiculo',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value  
   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["changed_by",])
      return item

class ModeloVehiculo(models.Model):
   marca_vehiculo = models.ForeignKey(MarcaVehiculo, on_delete=models.PROTECT, related_name="modelos")
   descripcion = models.CharField(max_length=100)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_ModeloVehiculo',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
        self.changed_by = value  
   def __str__(self):
      return self.descripcion

   def toJSON(self):
      item = model_to_dict(self,exclude=["changed_by",])
      item["marca-vehiculo"]=self.marca_vehiculo.toJSON()
      return item
from django.urls import reverse
class TipoVehiculo(models.Model):
   descripcion = models.CharField(max_length=100)
   image=models.ImageField(upload_to="vehiculo2/Y/",null=True,blank=True)
   image2=models.ImageField(upload_to="vehiculo2/X",null=True,blank=True)
   nro_llantas=models.IntegerField()
   max_rep=models.IntegerField(default=0)
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_TipoVehiculo',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value  
   def __str__(self):
      return self.descripcion+"-"+str(self.nro_llantas)+" llantas"
   def get_image(self):
      if self.image:
         return '{}{}'.format(settings.MEDIA_URL, self.image)
   def get_image2(self):
      if self.image2:
         return '{}{}'.format(settings.MEDIA_URL, self.image2)
   def toJSON(self):
      item = model_to_dict(self,exclude=["changed_by",])
      item["image"]=self.get_image()
      item["image2"]=self.get_image2()
      return item
   def get_absolute_url(self):
      return reverse('Web:posiciones', kwargs={'pk': self.pk})

class PosicionesLlantas(models.Model):
   tipo=models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE,null=True,blank=True)
   posicion=models.IntegerField(null=True,blank=True)
   posx=models.CharField(max_length=15,default="0")
   posy=models.CharField(max_length=15,default="0")
   repuesto=models.BooleanField(default=False)
   def toJSON(self):
      item = model_to_dict(self,exclude=["tipo",])
      return item

@receiver(post_save, sender=TipoVehiculo)
def save_tipo(sender, instance, **kwargs):

   m=PosicionesLlantas.objects.filter(tipo__id=instance.id)
   if not m.exists():
      for i in range(1,instance.nro_llantas+instance.max_rep+1):
         data=PosicionesLlantas()
         if i>instance.nro_llantas:
            data.repuesto=True
         data.tipo=instance
         data.posicion=i
         data.save()
   else:
      faltantes=instance.nro_llantas+instance.max_rep-len(m)
      if faltantes<0:
         for i in m:
            i.repuesto=False
            i.save()
         for i in m:
            if i.posicion>instance.nro_llantas+instance.max_rep:
               i.delete()
            elif i.posicion>instance.nro_llantas:
               i.repuesto=True
               i.save()           
      else:   
         for i in range(1,faltantes+1):  
            data=PosicionesLlantas()
            data.repuesto=False
            data.tipo=instance
            data.posicion=len(m)+i
            data.save()
         for a in PosicionesLlantas.objects.filter(tipo__id=instance.id):
            if a.posicion>instance.nro_llantas:
               a.repuesto=True
            else:
               a.repuesto=False
            a.save()
class Empresa(models.Model):

   nombre = models.CharField(max_length=200, null=True)
   direccion = models.CharField(max_length=200, null=True)
   telefono = models.CharField(max_length=20, null=True)
   email = models.CharField(max_length=100, null=True)
   banco = models.CharField(max_length=100, null=True)
   banco_abr = models.CharField(max_length=100, null=True)
   cta_corriente = models.CharField(max_length=100, null=True)
   cci = models.CharField(max_length=100, null=True)
   estado=models.BooleanField(default=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Empresa',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
   def __unicode__(self):
      return self.nombre
class Vehiculo(models.Model):

   ano = models.IntegerField(null=True)
   modelo_vehiculo = models.ForeignKey(ModeloVehiculo, on_delete=models.PROTECT)
   tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.PROTECT)
   ubicacionv = models.ForeignKey(Lugar, verbose_name="Lugar", on_delete=models.PROTECT, null=True, blank=True)
   propiedad = models.CharField(max_length=50, null=True)
   placa = models.CharField(max_length=20, null=True, blank=True)
   operacion = models.CharField(max_length=50, null=True, blank=True)
   km = models.DecimalField(max_digits=10, decimal_places=2)
   nro_ejes = models.IntegerField(null=True)
   nro_motor = models.CharField(max_length=50,null=True,blank=True)
   nro_chasis = models.CharField(max_length=50,null=True,blank=True)

   obs = models.TextField(null=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   activo=models.BooleanField(default=True)
   empresa=models.ForeignKey(Empresa, verbose_name=_(""), on_delete=models.CASCADE,null=True,blank=True)
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_Vehiculo',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by
   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value  
   def __str__(self):
      return self.placa
   def toJSON(self):
      item = model_to_dict(self,exclude=[])
      item["changed_by"]=self.changed_by.toJSON2()

      item["created_at"]=self.created_at.strftime('%Y-%m-%d')
      item["modelo_vehiculo"]=self.modelo_vehiculo.toJSON()
      item["tipo_vehiculo"]=self.tipo_vehiculo.toJSON()

      return item
   def toJSON2(self):
      item = model_to_dict(self,exclude=["obs","nro_ejes","estado","propiedad","operacion","almacen","modelo_vehiculo","tipo_vehiculo","changed_by","ubicacionv"])
      item["marca"]=self.modelo_vehiculo.marca_vehiculo.descripcion
      item["modelo"]=self.modelo_vehiculo.descripcion
      item["nro_llantas"]=self.tipo_vehiculo.nro_llantas
      item["created_at"]=self.created_at.strftime('%Y-%m-%d')

      return item
     
   def toJSON3(self):
      item = model_to_dict(self,fields=["nro_chasis","ano","placa"])
      item["marca"]=self.modelo_vehiculo.marca_vehiculo.descripcion
      item["modelo"]=self.modelo_vehiculo.descripcion
      item["tipo"]=self.tipo_vehiculo.descripcion
      if self.empresa!=None:
         item["empresa"]=self.empresa.nombre
      return item
   def toJSON_flota(self):
      item = model_to_dict(self,fields=["placa","empresa","id"])
      if self.empresa:
         item["empresa"]=self.empresa.nombre
      return item
class Llanta(models.Model):


   modelo_llanta = models.ForeignKey(ModeloLlanta, on_delete=models.PROTECT,null=True)
   medida_llanta = models.ForeignKey(MedidaLlanta, on_delete=models.PROTECT)
   # ubicacion = models.CharField(max_length=50, choices=CHOICES_UBICACION_LLANTA,null=True,blank=True)
   ubicacion = models.ForeignKey(Ubicacion,on_delete=models.PROTECT,null=True,blank=True)
   vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name="llantas", null=True,blank=True)
   km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   codigo = models.CharField(max_length=100, null=True, blank=True)
   posicion=models.IntegerField(blank=True,null=True,default=None)
   repuesto=models.BooleanField(default=False)
   estado = models.CharField(max_length=9,choices=CHOICES_ESTADO_LLANTA)
   costo = models.DecimalField(max_digits=10, decimal_places=2)
   a_final = models.DecimalField(max_digits=10, decimal_places=2)
   a_inicial=models.DecimalField(max_digits=10, decimal_places=2)
   a_promedio=models.DecimalField(max_digits=10, decimal_places=2)
   fech_ren=models.DateField()
   activo = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   history = HistoricalRecords(table_name='Web_Historial_Llanta',user_model=Usuario)

   def __str__(self):
      return self.codigo
   def toJSON(self):
      item = model_to_dict(self,exclude=["a_inicial","a_final","a_promedio","fech_ren","ubicacion","estado","eliminado","changed_by",])
      if self.medida_llanta.capas:
         item["medida"]='Medida {} - {} - {}'.format(str(self.medida_llanta.medida), str(format(self.medida_llanta.profundidad, '.2f')), str(format(self.medida_llanta.capas, '.2f')))
      else:
         item["medida"]='Medida {} - {} '.format(str(self.medida_llanta.medida), str(format(self.medida_llanta.profundidad, '.2f')))
      # item["km"]=format(self.cubierta.km, '.2f')
      item["costo"]=format(self.costo, '.2f')
      item["modelo_llanta"]=self.modelo_llanta.descripcion
      item["marca_llanta"]=self.modelo_llanta.marca_llanta.descripcion
      # if self.ubicacion: 
      #    item["ubicacion"]=self.ubicacion.descripcion 
      item["created_at"]=self.created_at.strftime('%Y-%m-%d')  
      # if self.vehiculo: 
      #    item["vehiculo"]=self.vehiculo.placa
      return item
   def tabletoJSON(self):
      item = model_to_dict(self,exclude=["modelo_llanta","medida_llanta","ubicacion","posicion","vehiculo","repuesto","cubierta","eliminado","eliminado","changed_by",])
      item["modelo_llanta"]=self.modelo_llanta.descripcion
      item["marca_llanta"]=self.modelo_llanta.marca_llanta.descripcion
      if self.medida_llanta.capas:
         item["medida"]='Medida {} - {} - {}'.format(str(self.medida_llanta.medida), str(format(self.medida_llanta.profundidad, '.2f')), str(format(self.medida_llanta.capas, '.2f')))
      else:
         item["medida"]='Medida {} - {} '.format(str(self.medida_llanta.medida), str(format(self.medida_llanta.profundidad, '.2f')))
    
      # item["km"]=format(self.cubierta.km, '.2f')
      item["costo"]=format(self.costo, '.2f')
      item["created_at"]=self.created_at.strftime('%Y-%m-%d')  
    

      return item

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
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
   
   
class  CubiertaLlanta(models.Model):
   
   llanta=models.ForeignKey(Llanta, verbose_name=_("Llanta"), on_delete=models.PROTECT,null=True,blank=True)
    
   nro_ren=models.CharField(max_length=2,null=True,blank=True,default=None)      
   primer_reen=models.BooleanField(default=False)
   km = models.DecimalField(max_digits=10, decimal_places=2)
   fech_ren=models.DateField(null=True,blank=False)
   modelo_renova=models.ForeignKey(ModeloRenova, on_delete=models.PROTECT,blank=True,null=True,default=None)
   ancho_banda=models.ForeignKey(AnchoBandaRenova, on_delete=models.PROTECT,blank=True,null=True,default=None)
   renovadora=models.ForeignKey(MarcaRenova,on_delete=models.PROTECT,blank=True,null=True,default=None)
   alt_inicial= models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
   alt_final= models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)

   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   activo=models.BooleanField(default=True)
   history = HistoricalRecords(table_name='Web_Historial_CubiertaLlanta',user_model=Usuario)

   def toJSON(self):
      item = model_to_dict(self,exclude=["primer_reen","llanta","eliminado","eliminado","changed_by","activo"])
      item["km"]=format(self.km, '.2f')
      item["alt_inicial"]=format(self.alt_inicial, '.2f')
      item["alt_final"]=format(self.alt_final, '.2f')      
      item["fech_ren"]=self.fech_ren.strftime('%Y-%m-%d')  

      item["renovadora"]=self.renovadora.id
      item["descripcion"]=self.renovadora.descripcion

      item["modelo_renova"]=self.modelo_renova.id
      item["ancho_banda"]=self.ancho_banda.id
      item["activo"]=1 if self.activo else 0
      return item
   def toJSON2(self):
      item = model_to_dict(self,exclude=["primer_reen","llanta","eliminado","eliminado","changed_by","activo"])
      item["km"]=format(self.km, '.2f')
      item["alt_inicial"]=format(self.alt_inicial, '.2f')
      item["alt_final"]=format(self.alt_final, '.2f')

      item["fech_ren"]=self.fech_ren.strftime('%Y-%m-%d')  
      item["renovadora"]=self.renovadora.descripcion
      item["modelo_renova"]=self.modelo_renova.descripcion
      item["ancho_banda"]=self.ancho_banda.descripcion
      item["llanta"]=self.llanta.codigo
      return item 
   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
class Movimientos_Historial(models.Model):
  
   llanta=models.ForeignKey(Llanta,on_delete=models.PROTECT,blank=True,null=True)
   km=models.CharField( max_length=20,blank=True,null=True)
   profundidad=models.CharField(max_length=20,blank=True,null=True)
   vehiculo=models.ForeignKey(Vehiculo, verbose_name=_("Vehículo"), on_delete=models.PROTECT,blank=True,null=True)
   posicion=models.CharField(max_length=5,blank=True,null=True)
   estado=models.CharField(max_length=2,choices=CHOICES_ESTADO_LLANTA)
   obs=models.CharField(max_length=100,choices=CHOICES_OBSERVACION,blank=True,null=True)
   ubicacion=models.ForeignKey(Ubicacion,on_delete=models.PROTECT,blank=True,null=True)
   activo = models.BooleanField(default=True)
   eliminado=models.BooleanField(default=False,editable=False)
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   
   
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
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
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
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
   eliminado=models.BooleanField(default=False,editable=False)
   def toJSON(self):
      item = model_to_dict(self,exclude=["changed_by","inspeccion"])
      item["codigo"]=self.llanta.codigo
      item["rem_prom"]=format(self.rem_prom,".2f")
      return item
   
   
@receiver(post_save, sender=DetalleInspeccion)
def detalle_inspeccion(sender,instance,**kwargs):
   ex=Llanta.objects.filter(pk=instance.llanta.id).first()
   if ex:
      ex.ubicacion_id=None
      ex.vehiculo=instance.inspeccion.vehiculo
      ex.posicion=instance.posicion
      ex.repuesto=instance.repuesto
      ex.save()
   
class Conductor(models.Model):
   tip_doc = models.IntegerField(
       choices=CHOICES_TIPO_DOC2, default=TIPO_DOC_DNI)
   doc=models.CharField(max_length=20)
   nombres=models.CharField(max_length=100)
   estado=models.BooleanField(default=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Conductores',user_model=Usuario)

   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
   def toJSON(self):
      item= model_to_dict(self,exclude=["changed_by"])
      return item
      
class Ruta(models.Model):
   ruta = models.CharField(max_length=255)
   estado=models.BooleanField(default=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Ruta',user_model=Usuario)  
   def __str__(self):
      return self.ruta
   @property
   def _history_user(self):
      return self.changed_by
   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
   def cbo_ruta(self):
      item=model_to_dict(self,fields=["id","ruta"])
      return item
   def toJSON(self):
      item=model_to_dict(self,exclude=["changed_by"])
      return item 

class Estaciones(models.Model):
   codigo = models.CharField(max_length=20)
   descripcion = models.CharField(max_length=100)
   red=models.CharField(max_length=100)
   ubicacion=models.ForeignKey(Distrito, on_delete=models.CASCADE,null=True)
   direccion = models.CharField(max_length=200)
   contacto=models.CharField(max_length=100)
   estado=models.BooleanField(default=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Estaciones',user_model=Usuario)
   def cbo_ruta(self):
      item=model_to_dict(self,exclude=["changed_by","red","ubicacion","ruta","estado","direccion"])
      return item
   def __str__(self):
      return self.codigo
   @property
   def _history_user(self):
      return self.changed_by


   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
class Tramo(models.Model):
   descripcion=models.CharField(max_length=255)
   formato=models.CharField(max_length=50,null=True)
   ids=models.CharField(max_length=50,null=True)
   ruta=models.ForeignKey(Ruta,on_delete=models.CASCADE,null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Tramo',user_model=Usuario)  
   @property
   def _history_user(self):
      return self.changed_by
   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
   def cbo_ruta(self):
      item=model_to_dict(self,exclude=["changed_by"])
      item["ruta"]=self.ruta.ruta
      return item    
   def toJSON(self):
      item=model_to_dict(self,exclude=["changed_by"])
      return item  

@receiver(post_save, sender=Tramo)
def Tramo_Ruta(sender,instance,**kwargs):
   if instance.state==0:
      pass
   elif instance.state==1:
      instance.ruta.ruta=instance.descripcion
   else:
      instance.ruta.ruta=instance.ruta.ruta+"/"+instance.descripcion
   instance.ruta.save()
   

class Rendimiento(models.Model):
   fech_hora = models.DateTimeField()
   modelo=models.ForeignKey(ModeloVehiculo,on_delete=models.PROTECT)
   tramo=models.ForeignKey(Tramo,on_delete=models.PROTECT)
   rend_vacio=models.DecimalField(max_digits=10, decimal_places=2)
   km=models.IntegerField()
   gal_abast=models.DecimalField(max_digits=10, decimal_places=2)
   estado=models.BooleanField(default=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Rendimiento',user_model=Usuario)
   @property
   def _history_user(self):
      return self.changed_by
   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
   
   def toJSON(self):
      item=model_to_dict(self,exclude=["changed_by"])
      item["tramo"]=self.tramo.descripcion
      item["gal_abast"]=format(self.gal_abast,".2f")
      item["rend_vacio"]=format(self.rend_vacio,".2f")
      item["modelo"]=self.modelo.descripcion
      item["marca"]=self.modelo.marca_vehiculo.descripcion

      return item
class TipoAbastecimiento(models.Model):
   descripcion = models.CharField(max_length=100)
class EstadoViaje(models.Model):
   descripcion = models.CharField(max_length=100)
class UnidadMedida(models.Model):
   descripcion=models.CharField(max_length=100)
   abrev=models.CharField(max_length=50)
   estado=models.BooleanField(default=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Unidad',user_model=Usuario)
   def __str__(self):
      return f'{self.descripcion}({self.abrev})'
   def toJSON(self):
      item=model_to_dict(self,exclude=["changed_by"])
      return item
   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
class Producto(models.Model):
   descripcion = models.CharField(max_length=100)
   unidad=models.ForeignKey(UnidadMedida,on_delete=models.CASCADE)
   estado=models.BooleanField(default=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Productos',user_model=Usuario)
   def __str__(self):
      return f'{self.descripcion}({self.unidad})'
   def toJSON(self):
      item=model_to_dict(self,exclude=["changed_by"])
      item["unidad"]=self.unidad.toJSON()
      return item
   @property
   def _history_user(self):
      return self.changed_by

   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
class EstacionProducto(models.Model):
   producto=models.ForeignKey(Producto, on_delete=models.CASCADE,null=True)
   estacion=models.ForeignKey(Estaciones,on_delete=models.CASCADE,null=True)
   precio=models.DecimalField( max_digits=10, decimal_places=2)
   fecha=models.DateTimeField(auto_now_add=True)
   pre_fech_fin=models.DateField(null=True)
   pre_fech_ini=models.DateField(null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
   history = HistoricalRecords(table_name='Web_Historial_EstacionProductos',user_model=Usuario)
   def toJSON(self):
      item = model_to_dict(self,exclude=["changed_by","inspeccion","estacion"])
      item["producto"]=self.producto.toJSON()
      return item
   @property
   def _history_user(self):
      return self.changed_by
   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value 
class Viaje(models.Model):
   ruta=models.ForeignKey(Ruta,on_delete=models.CASCADE,null=True)
   estado=models.BooleanField(default=True)
   fecha_fin=models.DateField(null=True)
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Viaje',user_model=Usuario)
   
   def toJSON(self):
      item =model_to_dict(self)

      return item
   @property
   def _history_user(self):
      return self.changed_by
   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
class Abastecimiento(models.Model):
   fecha=models.DateField()
   precio=models.DecimalField(max_digits=10, decimal_places=2)
   tipo=models.ForeignKey(TipoAbastecimiento, on_delete=models.CASCADE,null=True)
   estado_viaje=models.ForeignKey(EstadoViaje, on_delete=models.CASCADE,null=True)
   estacion=models.ForeignKey(Estaciones, on_delete=models.CASCADE,null=True)
   tramo=models.CharField(max_length=150,null=True)
   producto=models.ForeignKey(Producto, on_delete=models.CASCADE,null=True)   
   viaje=models.ForeignKey(Viaje,on_delete=models.CASCADE)
   estado=models.BooleanField(default=True)

   
   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
   history = HistoricalRecords(table_name='Web_Historial_Abastecimiento',user_model=Usuario)
 
   @property
   def _history_user(self):
      return self.changed_by
   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
   def toJSON(self):
         item=model_to_dict(self,exclude=["changed_by","producto"])
         item["viaje"]=self.viaje.toJSON()
         item["tipo"]=self.tipo.descripcion
         item["estacion"]=self.estacion.descripcion
         item["precio"]=format(self.precio, '.2f')      
         item["fecha"]=self.fecha.strftime('%Y-%m-%d')  
         return item  
   def toJSON2(self):
         item=model_to_dict(self,exclude=["changed_by","producto","viaje","tramo"])
         item["tipo"]=self.tipo.descripcion
         item["estacion"]=self.estacion.descripcion
         item["precio"]=format(self.precio, '.2f')      
         item["fecha"]=self.fecha.strftime('%Y-%m-%d')  
         return item
@receiver(post_save, sender=Abastecimiento)
def fin_viaje(sender,instance,**kwargs):
   if instance.estado_viaje_id=="2":
      instance.viaje.estado=False
      instance.viaje.fecha_fin=instance.fecha
      instance.viaje.save()

class DetalleAbastecimiento(models.Model):
   abast=models.ForeignKey(Abastecimiento,on_delete=models.CASCADE)
   hora=models.TimeField(null=True)
   placa=models.ForeignKey(Vehiculo,on_delete=models.CASCADE)
   km=models.IntegerField()
   volumen=models.DecimalField( max_digits=10, decimal_places=2,null=True)
   gal_obj=models.DecimalField( max_digits=10, decimal_places=2,null=True)
   recorrido_obj=models.IntegerField()
   total=models.DecimalField( max_digits=10, decimal_places=2,null=True)
   conductor=models.ForeignKey(Conductor, on_delete=models.PROTECT)
   cargado=models.DecimalField(max_digits=10, decimal_places=2)
   voucher=models.CharField(max_length=50)
   factura=models.CharField( max_length=50)
   afectacion=models.IntegerField(null=True)
   def get_report_liquidacion(self):
      item=model_to_dict(self)
      item["volumen"]=format(self.volumen, '.2f')      
      item["cargado"]=format(self.cargado, '.2f')      
      item["abast"]=self.abast.toJSON2()
      item["placa"]=self.placa.toJSON3()
      item["conductor"]=self.conductor.nombres
      return item  
   def get_report_abast(self):
      item=model_to_dict(self)
      item["volumen"]=format(self.volumen, '.2f')      
      item["cargado"]=format(self.cargado, '.2f')      
      item["abast"]=self.abast.toJSON()
      item["placa"]=self.placa.toJSON3()
      item["conductor"]=self.conductor.nombres
      return item
   def get_report_viaje(self):
      item=model_to_dict(self)
      return item
      
class AfectacionConsumo(models.Model):
   per_carga=models.IntegerField()
   afectacion=models.IntegerField()
   estado=models.BooleanField()


   changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
   history = HistoricalRecords(table_name='Web_Historial_AfectacionConsumo',user_model=Usuario)
 
   @property
   def _history_user(self):
      return self.changed_by
   @_history_user.setter
   def _history_user(self, value):
      self.changed_by = value
   def toJSON(self):
      item=model_to_dict(self)
      return item