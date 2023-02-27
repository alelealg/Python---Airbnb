import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

URL = 'https://www.airbnb.mx/s/Tzintzuntzan/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=Tzintzuntzan&place_id=ChIJUcqmhhu9LYQRZZLknhAcQSs&source=structured_search_input_header&search_type=autocomplete_click'
sopa = BeautifulSoup(requests.get(URL).text, 'lxml')
catalogodf = []
URL2 = sopa.find('a', class_ = "_1c5c8zn")['href'].strip()
contador = 0
urlnum = 20

while contador <= 10:
    if contador == 0:
        url = URL
    elif contador == 1:
        url = URL2
    else:
        # Replace the specific part of the string based on pattern
        urlnum += 20
        urlcon = 'items_offset=' + str(urlnum)
        url = re.sub('items_offset=[0-9]*', str(urlcon), URL2)

    contador += 1

    sopa_urls = BeautifulSoup(requests.get(URL).text, 'lxml')
    lista = sopa_urls.find('div', class_='_fhph4u')
    for casa in lista:
        nombre = casa.find('div', class_='_10l1pmgh').get_text().strip()
        if casa.find('span', class_='_10fy1f8') is None:
            calificacion = ''
        else:
            calificacion = casa.find('span', class_='_10fy1f8').get_text().strip()
        try:
            cant_evaluaciones = casa.find('span', class_='_krjbj')[1].get_text().strip()
        except:
            cant_evaluaciones = ''  # Indicate that the extraction failed -> can indicate no reviews or a mistake in scraping
        descripcion = casa.find('div', class_='_1tanv1h').get_text().strip()
        info = casa.find('div', class_='_kqh46o').get_text().strip()
        # huespedes
        huespedes = info[:info.index(' ') + len(' ')].replace(' ', '')
        # Baños
        sub_str = ' baño'
        banos = info[(info.index(sub_str) - 3) : info.index(sub_str) + len(sub_str)].replace(' ', '').replace('·', '').replace('baño', '')
        precio_final = casa.find('span', class_='_1p7iugi').get_text().strip().replace('Precio:$', '').replace(' MXN', '')
        catalogodf.append([nombre, calificacion, cant_evaluaciones, descripcion, huespedes, banos, precio_final])


catalogodf = pd.DataFrame(catalogodf, columns=['Nombre', 'Calificación promedio', 'Cantidad de evaluaciones',
                                                    'Descripción', 'Huéspedes', 'Baños', 'Precio_final'])
print(catalogodf)
print()

print(catalogodf['Cantidad de evaluaciones'])




