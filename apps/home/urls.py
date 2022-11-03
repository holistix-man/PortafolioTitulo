from django.urls import path, re_path
from apps.home import views
from django.contrib.auth.views import login_required
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    ##########################        DEPARTAMENTO         ########################
    #Crear DEPARTAMENTO
    path('dep_addone', views.ADDONE_DEPARTAMENTO.as_view(), name='dep_addone'),
    #Listar DEPARTAMENTOS
    path('dep_listall', views.DEPARTAMENTO_LISTALL.as_view(), name='dep_listall'),
    #Modificar DEPARTAMENTO
    path('dep_update/<int:pk>', views.DEPARTAMENTO_UPDATE.as_view(), name='dep_update'),
    #Eliminar DEPARTAMENTO
    path('eliminar_departamento/<id>/', views.ELIMINAR_DEPARTAMENTO, name="eliminar_departamento"),


    ##########################       INVENTARIO        #############################

    path('inv_addone/<int:pk>', views.INVENTARIO_MODIFY.as_view(), name='inv_addone'),

    path('inv_listall', views.INVENTARIO_LISTALL.as_view(), name='inv_listall'),


    ###########################         TOUR          #############################
    #Crear TOUR
    path('tou_addone', views.TOUR_ADDONE.as_view(), name='tou_addone'),
    #Listar TOUR
    path('tou_listall', views.TOUR_LISTALL.as_view(), name='tou_listall'),
    #Actualizar TOUR
    path('tou_update/<int:pk>', views.TOUR_UPDATE.as_view(), name='tou_update'),
    #Eliminar TOUR
    path('eliminar_tour/<id>/', views.ELIMINAR_TOUR, name='eliminar_tour'),


    ########################         TRANSPORTE          ##########################
    #Crear TRANSPORTE
    path('tra_addone', views.TRANSPORTE_ADDONE.as_view(), name='tra_addone'),
    #Listar TRANSPORTES
    path('tra_listall', views.TRANSPORTE_LISTALL.as_view(), name='tra_listall'),
    #Editar TRANSPORTE
    path('tra_update/<int:pk>', views.TRANPORTE_UPDATE.as_view(), name='tra_update'),
    #Eliminar TRANSPORTE
    path('eliminar_transporte/<id>/', views.TRANSPORTE_DELETE, name='eliminar_transporte'),


    #########################       HOME_PRINCIPAL         ########################

    #Listar DEPARTAMENTOS
    path('departamentos/', views.DepartamentoListView.as_view(),name='DepartamentoList'),

    #Detalle  DEPARTAMENTO
    path('detalleDepartamento/<DEP_ID>', views.DepartamentoDetailView.as_view(), name='DepartamentoDetailView'),

    #Listar RESERVAS
    path('reservas/', views.ReservaListView.as_view(), name='ReservaList'),

    #Detalle RESERVA
    path('detalleReserva/<int:pk>', views.ReservaDetailView.as_view(), name='detalleReserva'),

    #Cancelar RESERVA
    path('cancelarReserva/<id>/', views.CANCELAR_RESERVA, name='cancelarReserva'),


    ################# url FUNCIONARIO #####################
    path('checklist/<int:pk>', views.CHECKLIST_ADDONE.as_view(), name='checklist'),

    path('checklist_list', views.CHECKLIST_LISTALL.as_view(), name='checklist_list'),

    #ingresar CHECK IN 
    path('checkin/<int:pk>/', views.CHECK_IN.as_view(), name='checkin'),

    #ingresar CHECK OUT
    path('checkout/<int:pk>/', views.CHECK_OUT.as_view(), name='checkout'),


    #################### url ADMINISTRADOR ##################
    
    #registrar PAGO
    path('pago_addone', views.PAGO_ADDONE.as_view(), name='pago_addone'),

    #listar PAGOs
    path('pago_listall', views.PAGO_LISTALL.as_view(), name='pago_listall'),

    #estadisiticas
    path('estadisticas_pagos', views.estadisticas_pago, name='estadisticas_pagos'),

    path('estadisticas_reservas', views.estadisticas_reservas, name='estadisticas_reservas'),

    path('generar_reporte/', views.generar_reporte.as_view(), name='generar_reporte'),

    path('graficos', views.graficos.as_view(), name='graficos'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)