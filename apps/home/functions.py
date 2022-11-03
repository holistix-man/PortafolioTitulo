from ast import Bytes
import datetime
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import *

def comprobar_disponibilidad(departamento, fecha_ingreso, fecha_salida):
    lista_disponibilidad =[]
    reserva_list = RESERVA.objects.filter(RES_DEPARTAMENTO=departamento)
    for reserva in reserva_list:
        if reserva.RES_FECHA_INGRESO > fecha_salida or reserva.RES_FECHA_SALIDA < fecha_ingreso:
            lista_disponibilidad.append(True)
        else:
            lista_disponibilidad.append(False)

    return all(lista_disponibilidad)


def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None
