from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login 
from .forms import LoginForm, CustomerUserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


########################################################################################################################
########                                                                                                        ########
########   EN ESTE ARCHIVO SE ENCUENTRAN TODAS LAS VISTAS CORRESPONDIENTES A LA AUTENTICACIÓN EN EL SISTEMA     ########
########                                                                                                        ########
########   Vistas para iniciar sesion y registrarse. Además se encuentra la distincion y redirección            ########                                                                         ########
########   a la página correspondiente según el tipo de usuario que se loguea                                   ########
########                                                                                                        ########
########################################################################################################################


#Vista que carga la página principal (HOME) del administrador del sistema
def home_admin(request):

    #Al ser el HOME del ADMINISTRADOR, para controlar quien accede a la URL "home_admin", se agregan validaciones para reconocer
    # al tipo de usuario que está intentando acceder
    
    #En caso de ser ADMINISTRADOR, se redirige correctamente y muestra el home del admin
    if request.user.is_superuser:
        return render(request, 'home/admin/home_admin.html')

    #Si un FUNCIONARIO quiere acceder al home del admin, mostrará un mensaje de error de permisos y redirige a home funcionario
    elif request.user.is_staff:
        messages.warning(request, 'No tiene permisos para acceder a home de administrador. Se muestra home correspondiente')
        success_url = reverse_lazy('home_funcionario')
        return redirect(success_url)
    
    #Si un usuario COMÚN quiere acceder al home del admin, mostrará un mensaje de error de permisos y redirige a home principal
    else:
        messages.warning(request, 'No tiene permisos para acceder a home de administrador. Se muestra home correspondiente')
        return redirect("/")
        
#Vista que carga la página principal (HOME) de los funcionarios del sistema
def home_funcionario(request):

    #En el caso de que un usuario que no sea funcionario intente acceder al home del funcionario, será redirigido al home principal
    if not request.user.is_staff:
        messages.warning(request, 'No tiene permisos para acceder a home de funcionario. Se muestra home correspondiente')
        return redirect("/")
        
    else:
        return render(request, 'home/funcionario/home_funcionario.html')

# #Vista encargada del inicio de sesión en el sistema
def login_view(request):

    form = LoginForm(request.POST or None)
    msg = None

    #Si la acción efectuada (request) es del tipo POST, entra a validar el formulario 
    if request.method == "POST":

        if form.is_valid():
            #Si el formulario es válido, extrae los datos ingresados(usuario y contraseña)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            #Se intentará iniciar sesion con los datos obtenidos 
            try:
                #usuario en minusculas
                username = username.lower()
                user = authenticate(username=username, password=password)
                login(request, user)

                #Si el usuario es administrador, redirigirá al home de administrador
                if user.is_superuser:
                    success_url = reverse_lazy('home_admin')
                    return redirect(success_url)

                #Si el usuario es funcionario, redirigirá al home de funcionario
                elif user.is_staff:
                    success_url = reverse_lazy('home_funcionario')
                    return redirect(success_url)

                #Si es un usuario común, se redigirá al home principal
                else:
                    return redirect("/")

            #En caso de no iniciar sesión con usuario en minusculas, cae en la excepcion y se intenta denuevo
            except Exception as e:
                try:
                    #Usuario en mayusculas 
                    username = username.upper()
                    user = authenticate(username=username, password=password)
                    login(request, user)

                    if user.is_superuser:
                        success_url = reverse_lazy('home_admin')
                        return redirect(success_url)

                    elif user.is_staff:
                        success_url = reverse_lazy('home_funcionario')
                        return redirect(success_url)
                        
                    else:
                        return redirect("/")
                    
                #En caso de que no se inicie sesión, se alerta de que los datos no son validos, debido a que el sistema no los valida
                except Exception as e:
                    messages.info(request,'Usuario o contraseña no validos!')
        else:
            msg = 'Error validando el formulario'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def registroFuncionario(request):
    data = {
        'form': CustomerUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomerUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Funcionario agregado correctamente")
            return redirect(to="listar_usuario")
        data["form"] = formulario
    return render(request, "accounts/registroFuncionario.html" , data)




def listar_usuario(request):
    users = User.objects.all()
    data = {
        'user' : users
    }
    return render(request, 'accounts/listar.html',data )

def modificar_usuario(request,id):
    user = get_object_or_404(User, id=id)
    data = {
        'form': CustomerUserCreationForm(instance=user)
    }
    if request.method == 'POST':
        formulario = CustomerUserCreationForm(data=request.POST, instance=user, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Usuario actualizado correctamente")
            return redirect(to="listar_usuario")
        data["form"] = formulario
    return render(request, 'accounts/modificar.html',data)

def eliminar_usuario(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, "Usuario eliminado correctamente")
    return redirect(to="listar_usuario")