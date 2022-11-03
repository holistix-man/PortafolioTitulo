from email import message
from lib2to3.pygram import pattern_symbols
from typing import List
from django.shortcuts import get_object_or_404, render, redirect
from django import template
from django import forms
from django.contrib.auth.models import User
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView, View, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from datetime import datetime
from .models import *
from .forms import *
from .functions import comprobar_disponibilidad, render_to_pdf
from django.db.models import Count, F, Value
from datetime import datetime



# Create your views here.

######################## VISTAS CRUD DEPARTAMENTO ############################

class ADDONE_DEPARTAMENTO(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    try:
        model = DEPARTAMENTO
        form_class = formDEPARTAMENTO
        template_name = 'home/admin/dep_addone.html'
        success_url = reverse_lazy('dep_listall')
        success_message = "Departamento agregado correctamente"

    except Exception as e:
        message=f"Error al agregar departamento"

class DEPARTAMENTO_LISTALL(LoginRequiredMixin, ListView):
    model = DEPARTAMENTO
    template_name = 'home/admin/dep_listall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DEPARTAMENTO_UPDATE(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DEPARTAMENTO
    form_class = formDEPARTAMENTO
    template_name = 'home/admin/dep_addone.html'
    success_url = reverse_lazy('dep_listall')
    success_message = "Información de departamento actualizada correctamente"

def ELIMINAR_DEPARTAMENTO(request, id):
    depto = get_object_or_404(DEPARTAMENTO, DEP_ID=id)

    if depto.EST_ID.EST_NOMBRE == 'Reservado':
        messages.error(request, 'No se puede eliminar un departamento reservado.')

    else:
        depto.delete()
        messages.success(request, "Departamento eliminado correctamente")

    return redirect(to="dep_listall")


###########################  VISTAS INVENTARIO DEPTO  #############################

class INVENTARIO_MODIFY(SuccessMessageMixin, UpdateView):
    model = DEPARTAMENTO
    form_class = formINVENTARIO_ADDONE
    template_name = 'home/admin/inv_addone.html'
    success_url = reverse_lazy('inv_listall')
    success_message = "Inventario modificado correctamente"

class INVENTARIO_LISTALL(ListView):
    model = DEPARTAMENTO
    template_name = 'home/admin/inv_listall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


######################## VISTAS CRUD TOUR ############################

class TOUR_ADDONE(SuccessMessageMixin, CreateView):
    model = TOUR
    form_class = formTOUR
    template_name = 'home/admin/tou_addone.html'
    success_url = reverse_lazy('tou_listall')
    success_message = "Tour agregado correctamente"

class TOUR_LISTALL(ListView):
    model = TOUR
    template_name = 'home/admin/tou_listall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TOUR_UPDATE(SuccessMessageMixin, UpdateView):
    model = TOUR
    form_class = formTOUR
    template_name = 'home/admin/tou_addone.html'
    success_url = reverse_lazy('tou_listall')
    success_message = "Información de tour actualizada correctamente" 

def ELIMINAR_TOUR(request, id):
    tour = get_object_or_404(TOUR, TOU_ID=id)
    tour.delete()
    messages.success(request, "Tour eliminado correctamente")
    return redirect(to="tou_listall")


######################## VISTAS CRUD TRANSPORTE ############################

class TRANSPORTE_ADDONE(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TRANSPORTE
    form_class = formTRANSPORTE
    template_name = 'home/admin/tra_addone.html'
    success_url = reverse_lazy('tra_listall')
    success_message = "Transporte agregado correctamente"

class TRANSPORTE_LISTALL(ListView):
    model = TRANSPORTE
    template_name = 'home/admin/tra_listall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TRANPORTE_UPDATE(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TRANSPORTE
    form_class = formTRANSPORTE
    template_name = 'home/admin/tra_addone.html'
    success_url = reverse_lazy('tra_listall')
    success_message = "Transporte actualizado correctamente"

def TRANSPORTE_DELETE(request, id):
    transporte = get_object_or_404(TRANSPORTE, TRA_ID=id)
    transporte.delete()
    messages.success(request, "Transporte eliminado correctamente")
    return redirect(to="tra_listall")



######################## vistas HOME_PRINCIPAL ########################

#Listado de DEPARTAMENTOS cliente
class DepartamentoListView(ListView):
    model = DEPARTAMENTO
    template_name = 'home/cliente/dep_list.html'

#Detalle de DEPARTAMENTO + Crear RESERVA
class DepartamentoDetailView(View):
    def get(self,request,*args, **kwargs):
        id = self.kwargs.get('DEP_ID', None)
        form = formRESERVA()
        depto_list = DEPARTAMENTO.objects.filter(DEP_ID=id)

        if len(depto_list)>0:
            depto = depto_list[0]
            context = {
                'depto_id': depto,
                'form':form,
            }
            return render(request,'home/cliente/dep_detail.html', context)

        else:
            messages.error(request, "ERROR. El departamento ingresado no existe.")
            return redirect(to='DepartamentoList')

    def post(self,request,*args, **kwargs):
        id = self.kwargs.get('DEP_ID', None)
        depto_list = DEPARTAMENTO.objects.filter(DEP_ID=id)
        form = formRESERVA(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        dias_reserva = data['fecha_salida']-data['fecha_ingreso']

        disponibilidad_deptos =[]

        for departamento in depto_list:
            if comprobar_disponibilidad(departamento, data['fecha_ingreso'], data['fecha_salida']):
                disponibilidad_deptos.append(departamento)
            
        if len(disponibilidad_deptos)>0:
            departamento = disponibilidad_deptos[0]
            reserva = RESERVA.objects.create(
                RES_USER = self.request.user,
                RES_DEPARTAMENTO = departamento,
                RES_FECHA_INGRESO = data['fecha_ingreso'],
                RES_FECHA_SALIDA = data['fecha_salida'],
                RES_CANTIDAD_DIAS = dias_reserva.days,
                RES_ASISTENTES = data['asistentes'],
                RES_DESEA_TOUR_1 = data['tour1'],
                RES_DESEA_TOUR_2 = data['tour2'],
                RES_DESEA_TOUR_3 = data['tour3'],
                RES_TRANSPORTE = TRANSPORTE.objects.get(TRA_ID=data['transporte']),
                RES_VALOR_DEPARTAMENTO = (departamento.DEP_VALOR_DIA*dias_reserva.days),
                RES_VALOR_SERVICIOS_EXTRA = 0,
            )

            reserva.save()
            messages.success(request, "Reserva realizada correctamente")
            return redirect(to='ReservaList')

        else:
            messages.error(request, "ERROR. El departamento se encuentra reservado para esa fecha. Por favor pruebe con otra.")
            return redirect('DepartamentoDetailView', DEP_ID=id)

#Listado de RESERVAS (Cliente/Funcionario)
class ReservaListView(ListView):
    model = RESERVA
    template_name = 'home/funcionario/res_list.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            reserva_list = RESERVA.objects.all()
            return reserva_list

        else:
            reserva_list = RESERVA.objects.filter(RES_USER=self.request.user)
            return reserva_list

#Detalle de RESERVA
class ReservaDetailView(DetailView):
    model = RESERVA
    template_name = 'home/cliente/res_detail.html'

#Cancelar/eliminar RESERVA
def CANCELAR_RESERVA(request, id):
    reserva = get_object_or_404(RESERVA, RES_ID=id)
    reserva.delete()
    messages.success(request, "Reserva cancelada.")
    return redirect(to='ReservaList')



###############        vistas FUNCIONARIO            ####################


class CHECKLIST_ADDONE(SuccessMessageMixin, UpdateView):
    model = DEPARTAMENTO
    form_class = formCHECKLIST
    template_name = 'home/funcionario/clist_addone.html'
    success_url = reverse_lazy('checklist_list')
    success_message = "CheckList guardado correctamente"

class CHECKLIST_LISTALL(ListView):
    model = DEPARTAMENTO
    template_name = 'home/funcionario/clist_listall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CHECK_IN(SuccessMessageMixin, UpdateView):
    model = RESERVA
    form_class = formCHECK_IN
    template_name = 'home/funcionario/checkin.html'
    success_url = reverse_lazy('ReservaList')
    success_message = "CHECK IN ingresado correctamente"

class CHECK_OUT(SuccessMessageMixin, UpdateView):
    model = RESERVA
    form_class = formCHECK_OUT
    template_name = 'home/funcionario/checkout.html'
    success_url = reverse_lazy('ReservaList')
    success_message = "Check Out ingresado correctamente"

class PAGO_ADDONE(SuccessMessageMixin, CreateView):
    model = PAGO
    form_class = formPAGO
    template_name = 'home/admin/pago_addone.html'
    success_url = reverse_lazy('pago_listall')
    success_message = "Pago ingresado correctamente"

class PAGO_LISTALL(ListView):
    model = PAGO
    template_name = 'home/admin/pago_listall.html'


############  estadisticas #################

#class estadisticas_pagos(View):

    
def estadisticas_pago(request):
    n_total_pagos = PAGO.objects.all().count()        
   # v_total_pagado = PAGO.objects.get(PAG_ID=1)

    pagos_debito = PAGO.objects.filter(PAG_METODO_PAGO="DEBITO").count()
    pagos_credito = PAGO.objects.filter(PAG_METODO_PAGO="CREDITO").count()
    pagos_transferencia = PAGO.objects.filter(PAG_METODO_PAGO="TRANSFERENCIA").count()
    pagos_efectivo = PAGO.objects.filter(PAG_METODO_PAGO="EFECTIVO").count()


    data = {
        'n_total_pagos': n_total_pagos,
        #'v_total_pagado': v_total_pagado,
        'pagos_debito': pagos_debito,
        'pagos_credito': pagos_credito,
        'pagos_transferencia': pagos_transferencia,
        'pagos_efectivo': pagos_efectivo,
    }

    return render(request,'home/admin/estadisticas_pagos.html', data)


def estadisticas_reservas(request):
    n_total_reservas = RESERVA.objects.all().count()
    n_reservas_norte = RESERVA.objects.all().filter(RES_DEPARTAMENTO='1').count() | RESERVA.objects.all().filter(RES_DEPARTAMENTO='3').count() | RESERVA.objects.all().filter(RES_DEPARTAMENTO='10').count() | RESERVA.objects.all().filter(RES_DEPARTAMENTO='11').count()
    n_reservas_centro = RESERVA.objects.all().filter(RES_DEPARTAMENTO='4').count() | RESERVA.objects.all().filter(RES_DEPARTAMENTO='5').count() | RESERVA.objects.all().filter(RES_DEPARTAMENTO='6').count()
    n_reservas_sur = RESERVA.objects.all().filter(RES_DEPARTAMENTO='21').count() | RESERVA.objects.all().filter(RES_DEPARTAMENTO='22').count() | RESERVA.objects.all().filter(RES_DEPARTAMENTO='23').count()


    reservas = RESERVA.objects.all()

    reservas_norte = RESERVA.objects.all().filter(RES_DEPARTAMENTO='1') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='3') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='10') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='11')
    reservas_centro = RESERVA.objects.all().filter(RES_DEPARTAMENTO='4') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='5') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='6')
    reservas_sur = RESERVA.objects.all().filter(RES_DEPARTAMENTO='21') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='22') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='23')

    dinero_zona_norte = 0
    dinero_zona_centro = 0
    dinero_zona_sur = 0

    for r_norte in reservas_norte:
        dinero_zona_norte += r_norte.VALOR_FINAL_RESERVA
        
    for r_centro in reservas_centro:
        dinero_zona_centro += r_centro.VALOR_FINAL_RESERVA

    for r_sur in reservas_sur:
        dinero_zona_sur += r_sur.VALOR_FINAL_RESERVA

    departamentos = DEPARTAMENTO.objects.all()

    r_depto_1 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='1')
    r_depto_2 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='3')
    r_depto_3 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='4')
    r_depto_4 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='5')
    r_depto_5 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='6')
    r_depto_6 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='8')
    r_depto_7 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='9')
    r_depto_8 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='10')
    r_depto_9 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='11')
    r_depto_10 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='20')

    nr_depto_1 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='1').count()
    nr_depto_2 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='3').count()
    nr_depto_3 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='4').count()
    nr_depto_4 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='5').count()
    nr_depto_5 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='6').count()
    nr_depto_6 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='8').count()
    nr_depto_7 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='9').count()
    nr_depto_8 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='10').count()
    nr_depto_9 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='11').count()
    nr_depto_10 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='20').count()

    dinero_d1 = 0
    dinero_d2 = 0
    dinero_d3 = 0
    dinero_d4 = 0
    dinero_d5 = 0
    dinero_d6 = 0
    dinero_d7 = 0
    dinero_d8 = 0
    dinero_d9 = 0
    dinero_d10 = 0


    for d1 in r_depto_1:
        dinero_d1 += d1.VALOR_FINAL_RESERVA

    for d2 in r_depto_2:
        dinero_d2 += d2.VALOR_FINAL_RESERVA
    
    for d3 in r_depto_3:
        dinero_d3 += d3.VALOR_FINAL_RESERVA

    for d4 in r_depto_4:
        dinero_d4 += d4.VALOR_FINAL_RESERVA

    for d5 in r_depto_5:
        dinero_d5 += d5.VALOR_FINAL_RESERVA

    for d6 in r_depto_6:
        dinero_d6 += d6.VALOR_FINAL_RESERVA

    for d7 in r_depto_7:
        dinero_d7 += d7.VALOR_FINAL_RESERVA
    
    for d8 in r_depto_8:
        dinero_d8 += d8.VALOR_FINAL_RESERVA
    
    for d9 in r_depto_9:
        dinero_d9 += d9.VALOR_FINAL_RESERVA
    
    for d10 in r_depto_10:
        dinero_d10 += d10.VALOR_FINAL_RESERVA


    n_total_pagos = PAGO.objects.all().count()        
    # v_total_pagado = PAGO.objects.get(PAG_ID=1)

    pagos_debito = PAGO.objects.filter(PAG_METODO_PAGO="DEBITO").count()
    pagos_credito = PAGO.objects.filter(PAG_METODO_PAGO="CREDITO").count()
    pagos_transferencia = PAGO.objects.filter(PAG_METODO_PAGO="TRANSFERENCIA").count()
    pagos_efectivo = PAGO.objects.filter(PAG_METODO_PAGO="EFECTIVO").count()


        

    data = {

        'n_total_reservas': n_total_reservas,
        
        'reservas_norte': reservas_norte,
        'n_reservas_norte': n_reservas_norte,
        'dinero_zona_norte': dinero_zona_norte,

        'reservas_centro': reservas_centro,
        'n_reservas_centro': n_reservas_centro,
        'dinero_zona_centro': dinero_zona_centro,

        'reservas_sur': reservas_sur,
        'n_reservas_sur': n_reservas_sur,
        'dinero_zona_sur': dinero_zona_sur,
        
        'r_depto_1': r_depto_1,
        'r_depto_2': r_depto_2,
        'r_depto_3': r_depto_3,
        'r_depto_4': r_depto_4,
        'r_depto_5': r_depto_5,
        'r_depto_6': r_depto_6,
        'r_depto_7': r_depto_7,
        'r_depto_8': r_depto_8,
        'r_depto_9': r_depto_9,
        'r_depto_10': r_depto_10,

        'nr_depto_1': nr_depto_1,
        'nr_depto_2': nr_depto_2,
        'nr_depto_3': nr_depto_3,
        'nr_depto_4': nr_depto_4,
        'nr_depto_5': nr_depto_5,
        'nr_depto_6': nr_depto_6,
        'nr_depto_7': nr_depto_7,
        'nr_depto_8': nr_depto_8,
        'nr_depto_9': nr_depto_9,
        'nr_depto_10': nr_depto_10,


        'dinero_d1': dinero_d1,
        'dinero_d2': dinero_d2,
        'dinero_d3': dinero_d3,
        'dinero_d4': dinero_d4,
        'dinero_d5': dinero_d5,
        'dinero_d6': dinero_d6,
        'dinero_d7': dinero_d7,
        'dinero_d8': dinero_d8,
        'dinero_d9': dinero_d9,
        'dinero_d10': dinero_d10,


        'n_total_pagos': n_total_pagos,
        #'v_total_pagado': v_total_pagado,
        'pagos_debito': pagos_debito,
        'pagos_credito': pagos_credito,
        'pagos_transferencia': pagos_transferencia,
        'pagos_efectivo': pagos_efectivo,
        
    }

    return render(request, 'home/admin/estadisticas_reservas.html', data)


class generar_reporte(View):
    def get(self,request,*args,**kwargs):
        template_name = 'home/admin/reporte.html'

        fecha = datetime.today().strftime('%d-%m-%Y')

        reservas = RESERVA.objects.all()

        reservas_norte = RESERVA.objects.all().filter(RES_DEPARTAMENTO='1') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='3') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='10') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='11')
        reservas_centro = RESERVA.objects.all().filter(RES_DEPARTAMENTO='4') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='5') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='6')
        reservas_sur = RESERVA.objects.all().filter(RES_DEPARTAMENTO='21') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='22') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='23')


        ganancias = 0
        ganancias_norte = 0
        ganancias_centro = 0
        ganancias_sur = 0

        for ganancias_t in reservas:
            ganancias += ganancias_t.VALOR_FINAL_RESERVA

        for ganancias_n in reservas_norte:
            ganancias_norte += ganancias_n.VALOR_FINAL_RESERVA

        for ganancias_c in reservas_centro:
            ganancias_centro += ganancias_c.VALOR_FINAL_RESERVA

        for ganancias_s in reservas_sur:
            ganancias_sur += ganancias_s.VALOR_FINAL_RESERVA

        data = {
            'fecha': fecha,
            'count': reservas.count(),
            'reservas': reservas,
            'count_reservas_norte': reservas_norte.count(),
            'count_reservas_centro': reservas_centro.count(),
            'count_reservas_sur': reservas_sur.count(),
            'reservas_norte': reservas_norte,
            'reservas_centro': reservas_centro,
            'reservas_sur': reservas_sur,


            'ganancias': ganancias,
            'ganancias_norte': ganancias_norte,
            'ganancias_centro': ganancias_centro,
            'ganancias_sur': ganancias_sur,
        }
        pdf = render_to_pdf(template_name,data)

        #print(fecha)
        return HttpResponse(pdf,content_type='application/pdf')


class graficos(TemplateView):
    template_name = 'home/admin/graficos.html'

    def get_grafico_zona(self):
        data = []
        try:
            reservas_norte = RESERVA.objects.all().filter(RES_DEPARTAMENTO='1') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='3') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='10') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='11')
            reservas_centro = RESERVA.objects.all().filter(RES_DEPARTAMENTO='4') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='5') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='6')
            reservas_sur = RESERVA.objects.all().filter(RES_DEPARTAMENTO='21') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='22') | RESERVA.objects.all().filter(RES_DEPARTAMENTO='23')
        
            data.append(reservas_norte.count())
            data.append(reservas_centro.count())
            data.append(reservas_sur.count())

        except:
            pass
        return data

    def get_grafico_departamento(self):
        data=[]
        try:
            r_depto_1 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='1')
            r_depto_2 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='3')
            r_depto_3 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='4')
            r_depto_4 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='5')
            r_depto_5 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='6')
            r_depto_6 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='8')
            r_depto_7 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='9')
            r_depto_8 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='10')
            r_depto_9 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='11')
            r_depto_10 = RESERVA.objects.all().filter(RES_DEPARTAMENTO='20')

            data.append(r_depto_1.count())
            data.append(r_depto_2.count())
            data.append(r_depto_3.count())
            data.append(r_depto_4.count())
            data.append(r_depto_5.count())
            data.append(r_depto_6.count())
            data.append(r_depto_7.count())
            data.append(r_depto_8.count())
            data.append(r_depto_9.count())
            data.append(r_depto_10.count())

        except:
            pass

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grafico_zona'] = self.get_grafico_zona()
        context['grafico_departamento'] = self.get_grafico_departamento()
        return context


