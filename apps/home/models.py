from email.policy import default
from random import choices
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone



# Create your models here.

class ZONA(models.Model):
    ZON_ID = models.AutoField(('Id zona'), primary_key=True)
    ZON_NOMBRE = models.CharField(('Nombre zona'), max_length=40, null=True, blank=True)

    class  Meta:
        db_table = "ZONA"

    def __str__(self):
        return self.ZON_NOMBRE
        

class ESTADO(models.Model):
    EST_ID = models.AutoField(('Id estado'), primary_key=True)
    EST_NOMBRE = models.CharField(('Nombre de estado'), max_length=100, null=True, blank=True)

    class Meta:
        db_table = "ESTADO"

    def __str__(self):
        return self.EST_NOMBRE


class TRANSPORTE(models.Model):
    TRA_ID = models.AutoField(('Id transporte'), primary_key=True)
    TRA_NOMBRESERVICIO = models.CharField(('Nombre servicio de transporte'), max_length=40, null=True, blank=True)
    TRA_HORARIO = models.CharField(('Horario del transporte'), max_length=50, null=True, blank=True)
    TRA_VEHICULO = models.CharField(('Vehiculo de transporte'), max_length=50, null=True, blank=True)
    TRA_CONDUCTOR = models.CharField(('Nombre conductor'), max_length=100, null=True, blank=True)
    TRA_VALOR = models.IntegerField(('Valor del transporte'), null=True, blank=True)

    class Meta: 
        db_table = "TRANSPORTE"

    def __str__(self):
        return self.TRA_NOMBRESERVICIO


class TOUR(models.Model):
    TOU_ID = models.AutoField(('Id servicio de tour'), primary_key=True)
    ZON_ID = models.ForeignKey(ZONA, verbose_name="Zona", on_delete=models.PROTECT)
    TOU_NOMBRE = models.CharField(('Nombre de tour'), max_length=100, null=True, blank=True)
    TOU_DESCRIPCION = RichTextField(blank=True,null=True) 
    TOU_VALOR = models.IntegerField(('Valor del tour'), null=True, blank=True)

    class Meta:
        db_table = "TOUR"

    def __str__(self):
        return self.TOU_NOMBRE + ' - ' + str(self.ZON_ID)


class DEPARTAMENTO(models.Model):
    DEP_ID = models.AutoField(('Id departamento'), primary_key=True)
    DEP_NOMBRE = models.CharField(('Nombre de departamento'), max_length=100, null=True, blank=True)
    EST_ID = models.ForeignKey(ESTADO, verbose_name="Estado", on_delete=models.PROTECT)
    DEP_DESCRIPCION = models.CharField(('Descripción de departamento'), max_length=255, null=True, blank=True)
    DEP_CANTIDADHABITACIONES = models.IntegerField(('Cantidad de habitaciones'), null=True, blank=True)
    DEP_CANTIDADCAMAS = models.IntegerField(('Cantidad de camas'), null=True, blank=True)
    DEP_CANTIDADBANOS = models.IntegerField(('Cantidad de baños'), null=True, blank=True)
    DEP_CANTIDADPERSONAS = models.IntegerField(('Cantidad de personas'), null=True, blank=True)
    DEP_DIRECCION = models.CharField(('Direccion departamento'), max_length=100, null=True, blank=True)    
    ZON_ID = models.ForeignKey(ZONA, verbose_name="Zona", on_delete=models.PROTECT)
    DEP_VALOR_DIA = models.IntegerField(('Valor arriendo por dia'), null=True, blank=True)
    DEP_IMAGEN1 = models.ImageField(upload_to='departamentos', null=True)
    DEP_IMAGEN2 = models.ImageField(upload_to='departamentos', null=True)
    DEP_IMAGEN3 = models.ImageField(upload_to='departamentos', null=True)
    TOU_ID1 = models.ForeignKey(TOUR, related_name="Tour_asociado_1", verbose_name="Tour asociado", on_delete=models.PROTECT)
    TOU_ID2 = models.ForeignKey(TOUR, related_name="Tour_asociado_2", verbose_name="Tour 2 asociado", on_delete=models.PROTECT)
    TOU_ID3 = models.ForeignKey(TOUR, related_name="Tour_asociado_3", verbose_name="Tour 3 asociado", on_delete=models.PROTECT)

    DEP_INVENTARIO = RichTextField(blank=True,null=True) 
    DEP_CHECK_LIST = RichTextField(blank=True,null=True) 
    DEP_CHECK_LIST_FECHA = models.DateTimeField(auto_now=True)

    class  Meta:
        db_table = "DEPARTAMENTO"

    def __str__(self):
        return self.DEP_NOMBRE + ' - ' + str(self.ZON_ID)#+ ' - ' + self.DEP_DIRECCION + ' - ' + str(self.ZON_ID)


class RESERVA(models.Model):
    RES_ID = models.AutoField(('ID Reserva'), primary_key=True)
    RES_USER = models.ForeignKey(User, on_delete=models.CASCADE)
    RES_DEPARTAMENTO = models.ForeignKey(DEPARTAMENTO, on_delete=models.CASCADE)
    
    RES_FECHA_INGRESO = models.DateField(('Fecha de ingreso'),null=True, blank=True)
    RES_FECHA_SALIDA = models.DateField(('Fecha de salida'),null=True, blank=True)
    RES_CANTIDAD_DIAS = models.IntegerField(('Cantidad de dias'),null=True, blank=True)
    
    RES_ASISTENTES = models.TextField(('Asistentes'),null=True, blank=True, help_text="Ingrese nombre y rut de los asistentes a la reserva")
    
    RES_DESEA_TOUR_1 = models.BooleanField(('Desea tour 1'),default=False)
    RES_DESEA_TOUR_2 = models.BooleanField(('Desea tour 2'),default=False)
    RES_DESEA_TOUR_3 = models.BooleanField(('Desea tour 3'),default=False)

    RES_TRANSPORTE = models.ForeignKey(TRANSPORTE, on_delete=models.DO_NOTHING)

    RES_VALOR_DEPARTAMENTO = models.IntegerField(('Valor del departamento'),null=True, blank=True)
    RES_VALOR_SERVICIOS_EXTRA = models.IntegerField(('Valor de servicios extra'), null=True, blank=True, default=0)
    #RES_VALOR_TOTAL = models.IntegerField(('Valor total de la reserva'), null=True,blank=True)

    RES_CHECK_IN = models.BooleanField(('Check In'), default=False)
    RES_VALIDA_CLIENTE = models.BooleanField(('Cliente válido'), default=False)
    RES_CLIST_IN = RichTextField(blank=True,null=True) 
    RES_DEPOSITO_GARANTIA = models.IntegerField(('Deposito de garantía'), null=True, blank=True, default=0)

    RES_CHECK_OUT = models.BooleanField(('Check Out'), default=False)
    RES_CLIST_OUT =  RichTextField(blank=True,null=True) 

    RES_VALOR_MULTAS = models.IntegerField(('Valor multas'), null=True, blank=True, default=0)
    #RES_VALOR_FINAL_RESERVA = models.IntegerField(('Valor final de reserva'), null=True, blank=True)


    class Meta:
        db_table = "RESERVA"
    
    def __str__(self):
        return f"Reserva '{self.RES_DEPARTAMENTO}' efectuada por '{self.RES_USER}', entre {self.RES_FECHA_INGRESO} - {self.RES_FECHA_SALIDA}"

    def _valor_reserva(self):
        return self.RES_VALOR_DEPARTAMENTO + self.RES_VALOR_SERVICIOS_EXTRA

    VALOR_RESERVA = property(_valor_reserva)

    def _valor_final_reserva(self):
        return self.VALOR_RESERVA + self.RES_VALOR_MULTAS

    VALOR_FINAL_RESERVA = property(_valor_final_reserva)



class PAGO(models.Model):
    PAG_ID = models.AutoField(('ID Pago'), primary_key=True)
    PAG_CANTIDAD_PAGADA = models.IntegerField(('Cantidad pagada'), null=True, blank=True)
    
    METODO_PAGO_CHOICES = (
        ("DEBITO", "Débito"),
        ("CREDITO", "Crédito"),
        ("TRANSFERENCIA", "Transferencia"),
        ("EFECTIVO", "Efectivo"),
    )

    PAG_METODO_PAGO = models.CharField(choices= METODO_PAGO_CHOICES, max_length=100, null=True, blank=True)
    PAG_FECHA_INGRESO = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "PAGO"

    def __str__(self):
        return f"Registro de pago por ${self.PAG_CANTIDAD_PAGADA} ingresado el {self.PAG_FECHA_INGRESO}"

    def _valor_total_pagos(self):

        valor_total_pago = 0

        for pago in PAGO.objects.all():
            valor_total_pago += pago.PAG_CANTIDAD_PAGADA

        return valor_total_pago



    VALOR_TOTAL_PAGOS = property(_valor_total_pagos)
     
    