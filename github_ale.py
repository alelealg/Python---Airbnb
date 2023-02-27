import requests
from bs4 import BeautifulSoup
import pandas as pd


# OBTENER SOPA
def sopa(url):
    result = requests.get(url)
    content = result.content
    return BeautifulSoup(content, features="lxml")

# OBTENER LISTA DE PROPIEDADES
def lista(url):
    propiedades = url.findAll("div", {"class": "_8ssblpx"})
    resultado = []
    for propiedad in propiedades:
        resultado.append(propiedad)
    return propiedad

# SCRAPPEAR DATOS
def abnb_ale(url):
    listap = lista(url)
    catalogodf = []
    for casa in listap:
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
        banos = info
        precio_final = casa.find('span', class_='_1p7iugi').get_text().strip().replace('Precio:$', '').replace(' MXN', '')
        catalogodf.append([nombre, calificacion, cant_evaluaciones, descripcion, huespedes, banos, precio_final])

    catalogodf = pd.DataFrame(catalogodf, columns=['Nombre', 'Calificación promedio', 'Cantidad de evaluaciones',
                                                   'Descripción', 'Huéspedes', 'Baños', 'Precio_final'])
    return catalogodf


# OBTENER LINKS PAGINA SIGUIENTE
def findNextPage(url):
    ''' Finds the next page with listings if it exists '''
    try:
        nextpage = "https://airbnb.com" + url.find("li", {"class": "_i66xk8d"}).find("a")["href"]
    except:
        nextpage = "no next page"
    return nextpage


def getPages(url):
    ''' This function returns all the links to the pages containing
    listings for one particular city '''
    result = []
    while url != "no next page":
        page = sopa(url)
        result = result + [page]
        url = findNextPage(page)
    return result


def extractPages(url):
    ''' This function outputs a dataframe that contains all information of a particular
    city. It thus contains information of multiple listings coming from multiple pages.'''
    pages = getPages(url)
    # Do for the first element to initialize the dataframe
    df = abnb_ale(pages[0])
    # Loop over all other elements of the dataframe
    for pagenumber in range(1, len(pages)):
        df = df.append(abnb_ale(pages[pagenumber]))
    return df


# SCRAPER

def scraper(url):
    df = extractPages(url)
    return df

ale = scraper('https://www.airbnb.mx/s/Tzintzuntzan/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&query=Tzintzuntzan&place_id=ChIJUcqmhhu9LYQRZZLknhAcQSs')


print(ale.head())
print(ale['Baños'])