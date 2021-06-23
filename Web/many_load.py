
import csv,io,sys
from .models import *
from django.contrib import messages
from textwrap import wrap
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import decimal
from django.db import connection

def importExcel(file):
    try:
        df = pd.read_excel(file, sheet_name='Hoja1')
        for i in df.index:
            print(df["activo"][i])
            eliminado= True if df["eliminado"][i]==True else False
            activo= True if df["activo"][i]==True else False
            print(activo)
            data=TipoVehiculo.objects.create(descripcion=df["descripcion"][i],
            nro_llantas=df["nro_llantas"][i],
            activo=activo,
            created_at=df["created_at"][i],
            eliminado=eliminado ,
            changed_by_id=df["changed_by_id"][i],
            image=df["image"][i],
            image2=df["image2"][i],
            max_rep=df["max_rep"][i]

            )
            
        return True
    except Exception as e:
        
        print(e)
    return False
def importPosi(file):
    try:
        PosicionesLlantas.objects.all().delete()
        cursor = connection.cursor()

        cursor.execute('''TRUNCATE TABLE "Web_posicionesllantas" RESTART IDENTITY''')
        df = pd.read_excel(file, sheet_name='Hoja1')
        for i in df.index:
            tipo=TipoVehiculo.objects.get(id=df["tipo_id"][i])
            repuesto= True if df["repuesto"][i]==True else False

            data=PosicionesLlantas.objects.create(posicion=df["posicion"][i],
            repuesto=repuesto,
            posy=df["posy"][i],
            posx=df["posx"][i],
            tipo=tipo,
       

            )
            
        return True
    except Exception as e:
        
        print(e)
    return False
def importVehi(file):
    try:
        df = pd.read_excel(file, sheet_name='Hoja1')
        for i in df.index:
            def l(v):
                value=v  if  not pd.isna(v) else None 
                return value
            # activo= True if df["activo"][i]==True else False
            # eliminado= True if df["eliminado"][i]==True else False
            modelo_v=ModeloVehiculo.objects.get(id=df["modelo_vehiculo_id"][i])
            ubicacion=Lugar.objects.get(id=df["ubicacionv_id"][i])
            tipo=TipoVehiculo.objects.get(id=df["tipo_vehiculo_id"][i])

            data=Vehiculo.objects.create(ano=df["ano"][i],
            activo=df["activo"][i],
            eliminado= df["eliminado"][i],
            propiedad=df["propiedad"][i],
            placa=df["placa"][i],
            operacion=df["operacion"][i],
            km=np.float64(df["km"][i]).item(),
            nro_ejes=l(df["nro_ejes"][i]),
            obs=df["obs"][i],
            created_at=df["created_at"][i],
            changed_by_id=df["changed_by_id"][i],
            modelo_vehiculo=modelo_v,
            tipo_vehiculo=tipo,
            ubicacionv=ubicacion,
            nro_chasis=l(df["nro_chasis"][i]),
            nro_motor=l(df["nro_motor"][i]),
            
            )
            
        return True
    except Exception as e:
        
        print(e)
    return False
def importMedi(file):
    try:
        df = pd.read_excel(file, sheet_name='Hoja1')
        for i in df.index:
            def l(v):
                value=v  if  not pd.isna(v) else None 
                return value
            # activo= True if df["activo"][i]==True else False
            # eliminado= True if df["eliminado"][i]==True else False
            modelo_l=ModeloLlanta.objects.get(id=df["modelo_llanta_id"][i])
    
            data=MedidaLlanta.objects.create(
            activo=df["activo"][i],
            eliminado= df["eliminado"][i],
            capas=np.float64(df["capas"][i]).item(),
            profundidad=np.float64(df["profundidad"][i]).item(),
            medida=df["medida"][i],

            descripcion=l(df["descripcion"][i]),
            created_at=df["created_at"][i],
            changed_by_id=df["changed_by_id"][i],
            modelo_llanta=modelo_l,
         
            
            )
            
        return True
    except Exception as e:
        
        print(e)
    return False
def importLLan(file):
    try:


        df = pd.read_excel(file, sheet_name='Hoja1')
        for i in df.index:
            print()
            def l(v):
                value=v  if  not pd.isna(v) else None 
                return value
            # activo= True if df["activo"][i]==True else False
            # eliminado= True if df["eliminado"][i]==True else False
            medida=MedidaLlanta.objects.get(id=df["medida_llanta_id"][i]) if  not pd.isna((df['medida_llanta_id'][i])) else None
            modelo_l=ModeloLlanta.objects.get(id=df["modelo_llanta_id"][i]) if not pd.isna((df['modelo_llanta_id'][i])) else None
            ubicacion=Ubicacion.objects.get(id=df["ubicacion_id"][i]) if not pd.isna((df['ubicacion_id'][i]))  else  None
            vehiculo=Vehiculo.objects.get(id=df["vehiculo_id"][i]) if not pd.isna((df['vehiculo_id'][i]))  else  None
            
            print(medida)
            data=Llanta.objects.create(
            activo=df["activo"][i],
            eliminado= df["eliminado"][i],
            codigo=str(df["codigo"][i]),
            posicion=l(df["posicion"][i]),
            
            repuesto= df["repuesto"][i],
            estado= df["estado"][i],
            created_at= df["created_at"][i],
            changed_by_id= df["changed_by_id"][i],
            medida_llanta=medida,
            modelo_llanta=modelo_l,
            ubicacion=ubicacion,
            vehiculo=vehiculo,              
            costo=np.float64(df["costo"][i]).item(),
            a_inicial=np.float64(df["a_inicial"][i]).item(),
            a_final=np.float64(df["a_final"][i]).item(),
            a_promedio=np.float64(df["a_promedio"][i]).item(),

            fech_ren=df["fech_ren"][i],
            
            )
            
        return True
    except Exception as e:
        
        print(e)
    return False
def importCub(file):
    try:
        df = pd.read_excel(file, sheet_name='Hoja1')
        for i in df.index:
            def l(v):
                value=v  if  not pd.isna(v) else None 
                return value
            # activo= True if df["activo"][i]==True else False
            # eliminado= True if df["eliminado"][i]==True else False
            anchobanda=AnchoBandaRenova.objects.get(id=df["ancho_banda_id"][i]) if  not pd.isna((df['ancho_banda_id'][i])) else None
            modelorenova=ModeloRenova.objects.get(id=df["modelo_renova_id"][i]) if not pd.isna((df['modelo_renova_id'][i])) else None
            renovadora=MarcaRenova.objects.get(id=df["renovadora_id"][i]) if not pd.isna((df['renovadora_id'][i]))  else  None
            llanta=Llanta.objects.get(id=df["llanta_id"][i]) if not pd.isna((df['llanta_id'][i]))  else  None
            
            data=CubiertaLlanta.objects.create(
            activo=df["activo"][i],
            eliminado= df["eliminado"][i],
            primer_reen= df["primer_reen"][i],
            nro_ren=df["nro_ren"][i],
            km=np.float64(df["km"][i]).item(),
            created_at= df["created_at"][i],            
            changed_by_id= df["changed_by_id"][i],
            ancho_banda=anchobanda,
            modelo_renova=modelorenova,
            renovadora=renovadora,
            llanta=llanta,              
            alt_final=np.float64(df["alt_final"][i]).item(),
            alt_inicial=np.float64(df["alt_inicial"][i]).item(),

            fech_ren=df["fech_ren"][i],      
            )
            
        return True
    except Exception as e:
        
        print(e)
    return False
def updateLlantas(file):
    try:
        df = pd.read_excel(file, sheet_name='Hoja1')
        for i in df.index:
            print()
            def l(v):
                value=v  if  not pd.isna(v) else None 
                return value
            # activo= True if df["activo"][i]==True else False
            # eliminado= True if df["eliminado"][i]==True else False
            medida=MedidaLlanta.objects.get(id=df["medida_llanta_id"][i]) if  not pd.isna((df['medida_llanta_id'][i])) else None
            modelo_l=ModeloLlanta.objects.get(id=df["modelo_llanta_id"][i]) if not pd.isna((df['modelo_llanta_id'][i])) else None
            ubicacion=Ubicacion.objects.get(id=df["ubicacion_id"][i]) if not pd.isna((df['ubicacion_id'][i]))  else  None
            vehiculo=Vehiculo.objects.get(id=df["vehiculo_id"][i]) if not pd.isna((df['vehiculo_id'][i]))  else  None
            
            data=Llanta.objects.update_or_create(codigo=str(df["codigo"][i]),defaults={
            "activo":df["activo"][i],
            "eliminado": df["eliminado"][i],
            "codigo":str(df["codigo"][i]),
            "posicion":l(df["posicion"][i]),
            
            "repuesto": df["repuesto"][i],
            "estado": df["estado"][i],
            "created_at": df["created_at"][i],
            "changed_by_id": df["changed_by_id"][i],
            "medida_llanta":medida,
            "modelo_llanta":modelo_l,
            "ubicacion":ubicacion,
            "vehiculo":vehiculo,              
            "costo":np.float64(df["costo"][i]).item(),
            "a_inicial":np.float64(df["a_inicial"][i]).item(),
            "a_final":np.float64(df["a_final"][i]).item(),
            "a_promedio":np.float64(df["a_promedio"][i]).item(),

            "fech_ren":df["fech_ren"][i],
            
         })
            
        return True
    except Exception as e:
        
        print(e)
    return False
def import_abastecimento_xlsx(file):
    try:
        df = pd.read_excel(file, sheet_name='Hoja1')
        data=[]
        objeto={"placa":"","precio":"","producto":"","total":"","factura":"","voucher":"","volumen":""}
        for i in df.index:
            def l(v):
                value=v  if  not pd.isna(v) else None 
                return value
            
            objeto["placa"]=df["placa"][i]
            objeto["producto"]=df["producto"][i]
            objeto["factura"]=df["factura"][i]
            objeto["voucher"]=df["voucher"][i]
            objeto["precio"]='{0:.2f}'.format(np.float64(df["precio"][i]).item()),
            objeto["total"]='{0:.2f}'.format(np.float64(df["total"][i]).item()),
            objeto["volumen"]='{0:.2f}'.format(np.float64(df["volumen"][i]).item()),
            data.append(objeto)
            objeto={"placa":"","precio":"","producto":"","total":"","factura":"","volumen":""}

            
        return data
    except Exception as e:
        data=[]
        print(e)
    return data