from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import json
import requests

def RedirectParams(**kwargs):
    """
    Función para redirigir a una URL con parámetros.

    Args:
        kwargs (dict): Un diccionario con las siguientes claves:
            - 'url': La URL a la que redirigir.
            - 'params' (opcional): Parámetros a agregar a la URL.

    Returns:
        HttpResponseRedirect: Una respuesta de redirección con parámetros si se especifican.
    """
    url = kwargs.get("url")
    params = kwargs.get("params")
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string
    return response

class APIMixin:
    """
    Clase que interactúa con la API de la NASA para obtener datos de diferentes categorías.
    """
    def __init__(self, *args, **kwargs):
        self.cat = kwargs.get("cat")

    def get_data(self):
        """
        Obtiene datos de la API de la NASA según la categoría especificada.

        Returns:
            dict or None: Un diccionario con información de imagen y texto relacionado con la categoría
            seleccionada. None si la solicitud a la API no tiene éxito.
        """
        cat_dict = {
            'apod': f'planetary/apod?api_key={settings.API_KEY}',
            'mars': f'mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={settings.API_KEY}',
            'epic': f'EPIC/api/natural/images?api_key={settings.API_KEY}',
            'neows': f'neo/rest/v1/neo/3542519?api_key={settings.API_KEY}' 
        }
        
        url = f'https://api.nasa.gov/{cat_dict[self.cat]}'
        r = requests.get(url)
        
        if r.status_code == 200:
            if self.cat == "mars":
                return { 
                    "image": r.json()['photos'][0]["img_src"],
                    "text": "Image data gathered by NASA's Curiosity, Opportunity, and Spirit rovers on Mars."
                }
            elif self.cat == "apod":
                return {
                    "image": r.json()["url"],
                    "text": r.json()["explanation"]
                }
            elif self.cat == "neows":  # Agregado para NEOWS
                return {
                    "image": r.json()["7DQyFMpvwpHcjjGOZwGnbde1gcXTBJSoFMRCIO9k"],  # Ajusta esto al formato real de la respuesta de NEOWS
                    "text": "Descripción de un objeto cercano a la Tierra."  # Ajusta esto al formato real de la respuesta de NEOWS
                }
            else:
                image_id = r.json()[0]["image"]
                date = r.json()[0]["2023-10-28"].split(" ")[0].split("-")
                new_url = f'https://api.nasa.gov/EPIC/archive/natural/{date[0]}/{date[1]}/{date[2]}/png/{image_id}.png?api_key={settings.API_KEY}'
                return {
                    "image": new_url,
                    "text": "Imagery collected by DSCOVR's Earth Polychromatic Imaging Camera (EPIC) instrument.Uniquely positioned at the Earth-Sun Lagrange point, EPIC provides full disc imagery of the Earth and captures unique perspectives of certain astronomical events such as lunar transits using a 2048x2048 pixel CCD detector coupled to a 30-cm aperture Cassegrain telescope."
                }
        return  None