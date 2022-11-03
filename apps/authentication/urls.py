from django.urls import path
from .views import login_view, home_admin, home_funcionario, registroFuncionario, listar_usuario , modificar_usuario, eliminar_usuario
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # #URL que redirige a la página de inicio de sesión
    path('accounts/login/', login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    #URL que redirige a la página del administrador
    path("home/admin/", home_admin, name="home_admin"),

    #URL que redirige a la página del funcionario
    path("home/funcionario/", home_funcionario, name="home_funcionario"),


    path('registroFuncionario/', registroFuncionario, name="registroFuncionario"),
    path('listar_usuario/', listar_usuario, name="listar_usuario"),
    path('modificar_usuario/<id>/', modificar_usuario, name="modificar_usuario"),
    path('eliminar_usuario/<id>/', eliminar_usuario, name="eliminar_usuario"),

]
 