from django.shortcuts import redirect
from django.urls import reverse

def login_required(function):

    def wrapper(request, *args, **kwargs):
        if 'user_data' not in request.session:
            return redirect(reverse("my_index"))
        resp = function(request, *args, **kwargs)
        return resp
    
    return wrapper

#def saludar(nombre, apellido, inicio=0, fin=3):
def saludar(*args, **kwargs):
    nombre = args[0]
    apellido = args[1]
    inicio = kwargs['inicio']
    fin = kwargs['fin']
    

    for i in range(inicio, fin):
        print(f"Hola {nombre} {apellido}")
        
        
#saludar("juan", "perez", fin=10, inicio=2)