from operator import attrgetter
from django import forms
from django.contrib.auth.models import *
from django.contrib.auth.forms import UserCreationForm
from .models import *



class formDEPARTAMENTO(forms.ModelForm):
    
    class Meta:
        model = DEPARTAMENTO
        fields = ['DEP_NOMBRE', 'EST_ID','DEP_DESCRIPCION','DEP_CANTIDADHABITACIONES','DEP_CANTIDADCAMAS', 
                'DEP_CANTIDADBANOS','DEP_CANTIDADPERSONAS','DEP_DIRECCION','ZON_ID','DEP_VALOR_DIA',
                'DEP_IMAGEN1','DEP_IMAGEN2', 'DEP_IMAGEN3','TOU_ID1','TOU_ID2','TOU_ID3']

        labels = '__all__'

        widgets = {
            'DEP_NOMBRE': forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
            'EST_ID': forms.Select(),            
            'DEP_DESCRIPCION': forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'DEP_CANTIDADHABITACIONES': forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
            'DEP_CANTIDADCAMAS': forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
            'DEP_CANTIDADBANOS': forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'DEP_CANTIDADPERSONAS': forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'DEP_DIRECCION': forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
            'ZON_ID': forms.Select(),
            'DEP_VALOR_DIA': forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
            'TOU_ID1': forms.Select(),
            'TOU_ID2': forms.Select(),
            'TOU_ID3': forms.Select()
        }


class formTOUR(forms.ModelForm):

    class Meta:
        model = TOUR
        fields = ['ZON_ID','TOU_NOMBRE','TOU_DESCRIPCION','TOU_VALOR']
        labels = '__all__'
        widgets = {
            'ZON_ID': forms.Select(),
            'TOU_NOMBRE': forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'TOU_DESCRIPCION': forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'TOU_VALOR': forms.TextInput(attrs={'class':'form-control', 'type':'number'})
        }


class formTRANSPORTE(forms.ModelForm):

    class Meta:
        model = TRANSPORTE
        fields = ['TRA_NOMBRESERVICIO', 'TRA_HORARIO','TRA_VEHICULO','TRA_CONDUCTOR','TRA_VALOR']
        labels = '__all__'
        widgets = {
            'TRA_NOMBRESERVICIO': forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'TRA_HORARIO': forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'TRA_VEHICULO': forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'TRA_CONDUCTOR': forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'TRA_VALOR': forms.TextInput(attrs={'class':'form-control','type':'number'})
        }    


class formINVENTARIO_ADDONE(forms.ModelForm):
    class Meta:
        model = DEPARTAMENTO
        fields = ['DEP_INVENTARIO']
        labels = '__all__'
        widgets = {
            'DEP_INVENTARIO': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese el inventario del departamento'})
        }


class formCHECKLIST(forms.ModelForm):
    class Meta:
        model = DEPARTAMENTO
        fields = ['DEP_CHECK_LIST']
        labels = '__all__'
        widgets = {
            'DEP_CHECK_LIST': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese el inventario del departamento'}),
        }


class formCHECK_IN(forms.ModelForm):
    class Meta:
        model = RESERVA
        fields = ['RES_CHECK_IN','RES_VALIDA_CLIENTE','RES_CLIST_IN','RES_DEPOSITO_GARANTIA']
        labels = '__all__'
        widgets = {
            'RES_CHECK_IN': forms.CheckboxInput(attrs={'type':'checkbox'}),
            'RES_VALIDA_CLIENTE':forms.CheckboxInput(attrs={'type':'checkbox','required':'required'}),
            'RES_CLIST_IN': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese el inventario y estado con el que se entrega el departamento'}),
            'RES_DEPOSITO_GARANTIA': forms.TextInput(attrs={'class':'form-control', 'type':'number'})
        }

class formCHECK_OUT(forms.ModelForm):
    class Meta:
        model = RESERVA
        fields = ['RES_CHECK_OUT','RES_CLIST_OUT', 'RES_CLIST_IN','RES_VALOR_MULTAS']
        labels = '__all__'
        widgets = {
            'RES_CHECK_OUT':forms.CheckboxInput(attrs={'type':'checkbox'}),
            'RES_CLIST_OUT':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Compara el check list ingresado en el check in del departamento'}),
            'RES_CLIST_IN': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese el inventario y estado con el que se entrega el departamento'}),
            'RES_VALOR_MULTAS': forms.TextInput(attrs={'class':'form-control', 'type':'number'})
        }


class formRESERVA(forms.Form):
    fecha_ingreso= forms.DateField(required=True)
    fecha_salida= forms.DateField(required=True)
    asistentes= forms.CharField(widget=forms.Textarea)
    tour1 = forms.CharField(widget=forms.CheckboxInput)
    tour2 = forms.CharField(widget=forms.CheckboxInput)
    tour3 = forms.CharField(widget=forms.CheckboxInput)
    OPCIONES_TRANSPORTE = ((400,'Sin transporte'),(100,'Aeropuerto a residencia'), (200, 'Residencia a aeropuerto'),(300, 'Ambos (ida y vuelta)'))

    transporte = forms.ChoiceField(choices=OPCIONES_TRANSPORTE)
        

class formPAGO(forms.ModelForm):
    class Meta:
        model = PAGO
        fields = ['PAG_CANTIDAD_PAGADA','PAG_METODO_PAGO']
        labels = '__all__'
        widgets = {
            'PAG_CANTIDAD_PAGADA':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'PAG_METODO_PAGO': forms.Select()
        }