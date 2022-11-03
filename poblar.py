
from asyncio.windows_events import NULL
from datetime import datetime
import os
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE","core.settings")
import django, random as ran 
from random import random

django.setup()
from apps.home.models import * 

def poblar():
    zonanorte_id = 100
    zonanorte_nombre ="ZONA NORTE"
    
    zonacentro_id = 200
    zonacentro_nombre = "ZONA CENTRO"

    zonasur_id = 300
    zonasur_nombre = "ZONA SUR"

    zonanorte = ZONA.objects.get_or_create(ZON_ID=zonanorte_id, ZON_NOMBRE=zonanorte_nombre)[0]
    zonacentro = ZONA.objects.get_or_create(ZON_ID=zonacentro_id, ZON_NOMBRE=zonacentro_nombre)[0]
    zonasur = ZONA.objects.get_or_create(ZON_ID=zonasur_id, ZON_NOMBRE=zonasur_nombre)[0]

    zonanorte.save()
    zonacentro.save()
    zonasur.save()

    estado_disp_id = 100
    estado_disp_nombre = "DISPONIBLE"
    estado_res_id = 200
    estado_res_nombre = "RESERVADO"
    estado_mant_id = 300
    estado_mant_nombre = "MANTENCION" 

    estado_disp = ESTADO.objects.get_or_create(EST_ID=estado_disp_id, EST_NOMBRE=estado_disp_nombre)[0]
    estado_res = ESTADO.objects.get_or_create(EST_ID=estado_res_id, EST_NOMBRE=estado_res_nombre)[0]
    estado_mant = ESTADO.objects.get_or_create(EST_ID=estado_mant_id, EST_NOMBRE=estado_mant_nombre)[0]

    estado_disp.save()
    estado_mant.save()
    estado_res.save()

    trans_ida_id = 100
    trans_ida_nombre = "Desde aeropuerto a residencia"
    trans_ida_horario = "09:00 AM"
    trans_ida_vehiculo = "Mazda CX-3"
    trans_ida_conductor = "Felipe Zuñiga"
    trans_ida_valor = 50000

    trans_vuelta_id = 200
    trans_vuelta_nombre = "Desde residencia a aeropuerto"
    trans_vuelta_horario = "11:00 AM"
    trans_vuelta_vehiculo = "Mazda CX-3"
    trans_vuelta_conductor = "Felipe Zuñiga"
    trans_vuelta_valor = 50000

    trans_ambos_id = 300
    trans_ambos_nombre = "Ambos (ida y vuelta)"
    trans_ambos_horario = "09:00 AM llegada - 11:00 AM ida"
    trans_ambos_conductor = "Felipe Zuñiga"
    trans_ambos_vehiculo = "Mazda CX-3"
    trans_ambos_valor = 100000

    trans_ninguno_id = 400
    trans_ninguno_nombre = "Sin transporte"
    trans_ninguno_horario = "No aplica"
    trans_ninguno_vehiculo = "No aplica"
    trans_ninguno_conductor="No aplica"
    trans_ninguno_valor = 0

    trans_ida = TRANSPORTE.objects.get_or_create(TRA_ID = trans_ida_id, TRA_NOMBRESERVICIO=trans_ida_nombre,TRA_HORARIO=trans_ida_horario, TRA_VEHICULO = trans_ida_vehiculo,TRA_CONDUCTOR=trans_ida_conductor,TRA_VALOR = trans_ida_valor)[0]
    
    trans_vuelta = TRANSPORTE.objects.get_or_create(TRA_ID = trans_vuelta_id,TRA_NOMBRESERVICIO=trans_vuelta_nombre,TRA_HORARIO=trans_vuelta_horario,TRA_VEHICULO = trans_vuelta_vehiculo,TRA_CONDUCTOR=trans_vuelta_conductor,TRA_VALOR = trans_vuelta_valor)[0]

    trans_ambos = TRANSPORTE.objects.get_or_create(TRA_ID = trans_ambos_id, TRA_NOMBRESERVICIO=trans_ambos_nombre,TRA_HORARIO=trans_ambos_horario,TRA_VEHICULO = trans_ambos_vehiculo,TRA_CONDUCTOR=trans_ambos_conductor,TRA_VALOR = trans_ambos_valor)[0]

    trans_ninguno = TRANSPORTE.objects.get_or_create(TRA_ID = trans_ninguno_id,TRA_NOMBRESERVICIO=trans_ninguno_nombre,TRA_HORARIO=trans_ninguno_horario,TRA_VEHICULO = trans_ninguno_vehiculo,TRA_CONDUCTOR=trans_ninguno_conductor,TRA_VALOR = trans_ninguno_valor)[0]

    trans_ida.save()
    trans_vuelta.save()
    trans_ambos.save()
    trans_ninguno.save()

    tour_norte1_id = 101
    tour_norte1_nombre = "VALLE DE LA LUNA | San Pedro de Atacama"
    tour_norte1_desc = "En este paseo de medio día, nos vamos a visitar el lado oeste de San Pedro de Atacama, El valle de la luna. En este lugar único, podremos visitar la llamada cordillera de sal, mirador la piedra del coyote, donde esperaremos la puesta del sol."
    tour_norte1_valor = 80000


    tour_norte2_id = 102
    tour_norte2_nombre = "SALAR DE TARA | San Pedro de Atacama"
    tour_norte2_desc = "Pasaremos un día completo entre la Cordillera de los Andes recorriendo el altiplano. Comenzamos nuestra ruta frente al volcán Licancabur, para seguir en el altiplano hasta encontrarnos con los monjes de la Pacana, para posteriormente llegar al salar de Tara con sus hermosas catedrales. Aquí disfrutaremos de nuestro almuerzo con una vista privilegiada de este hermoso lugar. Se requiere previa aclimatación a la altura."
    tour_norte2_valor = 50000

    
    tour_norte3_id = 103
    tour_norte3_nombre = "GEYSER DEL TATIO | San Pedro de Atacama"
    tour_norte3_desc = "Muy temprano nos vamos a visitar este campo geométrico. Aquí, nos esperan temperaturas muy bajas antes de los primeros rayos de sol. Un buen lugar donde podremos disfrutar un hermoso espectáculo natural. Manifestaciones geométricas y fumarolas de gran altura, disfrutando, si lo desea, de un agradable baño termal. Conoceremos además, parte de la cultura atacameña visitando pequeños pueblos de la zona. Se requiere previa aclimatación a la altura."
    tour_norte3_valor = 60000

    tour_centro1_id = 201
    tour_centro1_nombre = "ISLA NEGRA Y VIÑA VERAMONTE"
    tour_centro1_desc = "En este tour viajaremos a la costa chilena y conoceremos la casa del poeta Pablo Neruda en Isla Negra y recorreremos la Viña Veramonte para degustar una exquisita selección de vinos."
    tour_centro1_valor = 80000

    tour_centro2_id = 202
    tour_centro2_nombre = "Tour Cajón del Maipo (Embalse el Yeso)"
    tour_centro2_desc = "Valoramos el tiempo de las personas y su estadia en Santiago, por lo que invertimos el tiempo en lo que realmente es importante en este tour como lo es la naturaleza que ofrece el embalse."
    tour_centro2_valor = 40000

    tour_centro3_id = 203
    tour_centro3_nombre = "Santiago como un local: tour privado personalizado"
    tour_centro3_desc = "Descubra la capital de Chile a través de los ojos de un local en este tour a pie de Lokafy a medida. Omita la típica visita guiada y, en su lugar, conéctese con un local de Santiago que le mostrará la ciudad como un amigo y le presentará los vecindarios que conoce y ama."
    tour_centro3_valor = 60000

    tour_sur1_id = 301
    tour_sur1_nombre = "Puerto Varas, Chiloé y Saltos del Petrohué"
    tour_sur1_desc = "Visita Puerto Varas y su maravilloso Lago Llanquihue. También cruzaremos por ferry a la mágica Isla de Chiloé con sus mágicos atractivos y deliciosos mariscos.Además una bella excursión a los Saltos de Petrohué y Volcán Osorno."
    tour_sur1_valor = 150000

    tour_sur2_id = 302
    tour_sur2_nombre = "PARQUE NACIONAL VILLARRICA - PUCÓN"
    tour_sur2_desc = "Asómbrate con las espectaculares vistas que te regalará el volcán Villarrica dese 1.250 metros de altura, con el volcán Llaima y los lagos de la zona como telón de fondo."
    tour_sur2_valor = 60000

    tour_sur3_id = 303
    tour_sur3_nombre = "PARQUE NACIONAL HUERQUEHUE - PUCÓN"
    tour_sur3_desc = "Ven a conocer el Parque Nacional Huerquehue en una excursión full day que te permitirá conocer los mejores paisajes de bosques de araucarias, cascadas, lagos y lagunas de la Región de La Araucanía."
    tour_sur3_valor = 70000



    tour_norte1 = TOUR.objects.get_or_create(   TOU_ID = tour_norte1_id,
                                                ZON_ID = ZONA.objects.get(ZON_ID=300),
                                                TOU_NOMBRE = tour_norte1_nombre,
                                                TOU_DESCRIPCION = tour_norte1_desc,
                                                TOU_VALOR = tour_norte1_valor)[0]

    tour_norte2 = TOUR.objects.get_or_create(   TOU_ID = tour_norte2_id,
                                                ZON_ID = ZONA.objects.get(ZON_ID=300),
                                                TOU_NOMBRE = tour_norte2_nombre,
                                                TOU_DESCRIPCION = tour_norte2_desc,
                                                TOU_VALOR = tour_norte2_valor)[0]


    tour_norte3 = TOUR.objects.get_or_create(   TOU_ID = tour_norte3_id,
                                                ZON_ID = ZONA.objects.get(ZON_ID=300),
                                                TOU_NOMBRE = tour_norte3_nombre,
                                                TOU_DESCRIPCION = tour_norte3_desc,
                                                TOU_VALOR = tour_norte3_valor)[0]

    tour_centro1 = TOUR.objects.get_or_create(   TOU_ID = tour_centro1_id,
                                                ZON_ID = ZONA.objects.get(ZON_ID=200),
                                                TOU_NOMBRE = tour_centro1_nombre,
                                                TOU_DESCRIPCION = tour_centro1_desc,
                                                TOU_VALOR = tour_centro1_valor)[0]
    
    tour_centro2 = TOUR.objects.get_or_create(   TOU_ID = tour_centro2_id,
                                                ZON_ID = ZONA.objects.get(ZON_ID=200),
                                                TOU_NOMBRE = tour_centro2_nombre,
                                                TOU_DESCRIPCION = tour_centro2_desc,
                                                TOU_VALOR = tour_centro2_valor)[0]

    tour_centro3 = TOUR.objects.get_or_create(   TOU_ID = tour_centro3_id,
                                                ZON_ID = ZONA.objects.get(ZON_ID=200),
                                                TOU_NOMBRE = tour_centro3_nombre,
                                                TOU_DESCRIPCION = tour_centro3_desc,
                                                TOU_VALOR = tour_centro3_valor)[0]

    tour_sur1 = TOUR.objects.get_or_create( TOU_ID = tour_sur1_id,
                                            ZON_ID = ZONA.objects.get(ZON_ID=100),
                                            TOU_NOMBRE = tour_sur1_nombre,
                                            TOU_DESCRIPCION = tour_sur1_desc,
                                            TOU_VALOR = tour_sur1_valor)[0]

    tour_sur2 = TOUR.objects.get_or_create( TOU_ID = tour_sur2_id,
                                            ZON_ID = ZONA.objects.get(ZON_ID=100),
                                            TOU_NOMBRE = tour_sur2_nombre,
                                            TOU_DESCRIPCION = tour_sur2_desc,
                                            TOU_VALOR = tour_sur2_valor)[0]

    tour_sur3 = TOUR.objects.get_or_create( TOU_ID = tour_sur3_id,
                                            ZON_ID = ZONA.objects.get(ZON_ID=100),
                                            TOU_NOMBRE = tour_sur3_nombre,
                                            TOU_DESCRIPCION = tour_sur3_desc,
                                            TOU_VALOR = tour_sur3_valor)[0]


    tour_norte1.save()
    tour_norte2.save()
    tour_norte3.save()

    tour_centro1.save()
    tour_centro2.save()
    tour_centro3.save()

    tour_sur1.save()
    tour_sur2.save()
    tour_sur3.save()

    depto1_id = 101
    depto1_nombre = "Departamento en Coquimbo"
    #depto1_estado = 
    depto1_desc = "Departamento ubicado en la IV región de Coquimbo, en el Norte Chico de Chile. Cuenta con una vista al mar que maravilla a todos los huespedes que se hospedan en este departamento."
    depto1_habitaciones = 2
    depto1_camas = 3
    depto1_banos = 1
    depto1_personas = 4
    depto1_direccion = "Las praderas 3563, Coquimbo"
    # depto1_zona = 
    depto1_valor = 80000
    depto1_img1 = "https://pics.nuroa.com/departamento_en_venta_en_la_marina_6690024655489100602.jpg"
    depto1_img2 = "https://media-cdn.tripadvisor.com/media/vr-splice-j/04/5f/43/d1.jpg"
    #depto1_img3 = "https://cf.chilepropiedades.cl/imagenes/publicacion/venta-usada/departamento/coquimbo/0/50c574d43a27439589c0f5745c4220e3.jpeg"
    # depto1_tour1 = 
    # depto1_tour2 =
    # depto1_tour3 =
    depto1_inv = "Este departamento cuenta con servicios de televición HD, WiFi, estacionamiento, piscina, gimnacio."
    depto1_clist = ""
    #depto1_fecha = datetime.today()

    depto1 = DEPARTAMENTO.objects.get_or_create(DEP_ID = depto1_id,
                                                DEP_NOMBRE = depto1_nombre,
                                                EST_ID = ESTADO.objects.get(EST_ID=100),
                                                DEP_DESCRIPCION = depto1_desc,
                                                DEP_CANTIDADHABITACIONES = depto1_habitaciones,
                                                DEP_CANTIDADCAMAS = depto1_camas,
                                                DEP_CANTIDADBANOS = depto1_banos,
                                                DEP_CANTIDADPERSONAS = depto1_personas,
                                                DEP_DIRECCION = depto1_direccion,
                                                ZON_ID = ZONA.objects.get(ZON_ID=100),
                                                DEP_VALOR_DIA = depto1_valor,
                                                DEP_IMAGEN1 = depto1_img1,
                                                DEP_IMAGEN2 = depto1_img2,
                                                #DEP_IMAGEN3 = depto1_img3,
                                                TOU_ID1 = TOUR.objects.get(TOU_ID=101),
                                                TOU_ID2 = TOUR.objects.get(TOU_ID=102),
                                                TOU_ID3 = TOUR.objects.get(TOU_ID=103),
                                                DEP_INVENTARIO = depto1_inv,
                                                DEP_CHECK_LIST = depto1_clist)[0]

    depto1.save()

if __name__ =='__main__':
    print("CREACION DE DATOS")

    poblar()



