# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login 
from django.http import HttpResponse

def user_login(request): 
    if request.method == 'POST': 
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        user = authenticate(request, username=username, password=password) 
        if user is not None: 
            login(request, user) 
            return redirect('home') # Redirige a la página principal u otra página 
        else: 
            return HttpResponse('Nombre de usuario o contraseña incorrectos') 
    return render(request, 'login.html')

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    #Filtra las imágenes según el término de búsqueda ingresado por el usuario. Si no se ingresa un término, devuelve todas las imágenes de la API.
    search_msg = request.POST.get('query', '')

    if (search_msg != ''):
        images = services.getAllImages(search_msg)
        favourite_list = services.getAllFavourites(request)
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services.saveFavourite(request)  # Llama a la capa de servicio para guardar el favorito.
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services.deleteFavourite(request)  # Llama a la capa de servicio para eliminar el favorito.
    return redirect('home')

@login_required
def exit(request):
    logout(request)
    return redirect('index-page')