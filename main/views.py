from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import requests


from .mixins import (

	RedirectParams,
	APIMixin
)

'''
Basic view for selecting query
'''
def index(request):

	if request.method == "POST":
		cat = request.POST.get("cat", None)
		if cat:
			return RedirectParams(url = 'main:results', params = {"cat": cat})

	return render(request, 'main/index.html', {})



'''
Basic view for displaying results
'''
def results(request):
	cat = request.GET.get("cat", None)

	if cat:
		results = APIMixin(cat=cat).get_data()
		print (results)

		if results:
			context = {
				"results": results,
				"cat": cat,
			}

			return render(request, 'main/results.html', context)
	return redirect(reverse('main:home'))





def neows_data(request):
    api_key = settings.NASA_API_KEY
    endpoint = 'https://api.nasa.gov/neo/rest/v1/feed'

    # Parámetros de ejemplo, ajusta según tus necesidades
    params = {
        'start_date': '2023-10-27',
        'end_date': '2023-10-28',
        'api_key': api_key,
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Error al obtener datos de la API NeoWS'}, status=500)


##========================================================##

def login_view(request):
    if request.method == 'POST':
        # Procesar el formulario
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')
        
        # Aquí puedes realizar la lógica de autenticación o cualquier otro procesamiento necesario
        # Por ejemplo, puedes verificar las credenciales del usuario en tu base de datos

        # Si las credenciales son correctas, puedes redirigir al usuario a una página de bienvenida
        return HttpResponse(f'Bienvenido, {nombre} {apellidos}.')
    
        # Autenticar al usuario
        user = authenticate(request, email=email, password=contrasena)

        if user is not None:
            # El usuario se autenticó con éxito
            login(request, user)  # Iniciar sesión en Django
            return redirect('pagina_de_bienvenida')  # Redirigir a una página de bienvenida
        else:
            # Las credenciales son incorrectas, puedes mostrar un mensaje de error
            return render(request, 'login.html', {'error_message': 'Credenciales incorrectas'})

