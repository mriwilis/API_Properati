# https://127.0.0.1:3030/api/BARRIO/INMUEBLE/TIPO
from bs4 import BeautifulSoup
import requests
import unicodedata


localidad = "palermo"
inmueble = "departamento"


def pagina(num):
    url = "https://www.properati.com.ar/s/palermo/departamento/alquiler?page=" + str(num)
    response = requests.get(url)
    response.encoding = "utf-8"
    html = response.text
    dom = BeautifulSoup(html, features = "html.parser")
    fin = dom.find( attrs = { 'class' : 'StyledPagerButton-sq1exe-0 cFkGqv pager-next' } )
    return fin, dom

row=1
lista_propiedades=[]
num=1
fin, dom = pagina(num)


while fin != None:
    
    anuncios = dom.find_all( attrs = { 'class' : 'StyledCard-n9541a-1 jWSYcc' } )
    
    for anuncio in anuncios:
        row=row
        titulo = anuncio.find( attrs = { 'class' : 'StyledTitle-n9541a-4 bwJAej' } )
        precio = anuncio.find( attrs = { 'class' : 'StyledPrice-sc-1wixp9h-0 bZCCaW' } )
        expensas = anuncio.find( attrs = { 'class' : 'StyledMaintenanceFees-n9541a-6 cRsmn' } )
        detalles = anuncio.find( attrs = { 'class' : 'StyledInfoIcons-n9541a-9 fgcFIO' } )
        inmobiliaria = anuncio.find( attrs = { 'class' : 'seller-name' } )
        url = 'https://www.properati.com.ar/' + anuncio.find( attrs = { 'class' : 'StyledCardInfo-n9541a-2 ctwAhK' } ).a['href']
        
        if titulo: titulo = titulo.get_text()
        if precio: precio= precio.get_text()
        if expensas: expensas = unicodedata.normalize("NFKD", expensas.get_text()) 
        if inmobiliaria: imobiliaria = inmobiliaria.get_text()
        if detalles:
            spans = detalles.find_all('span')
            for span in spans:
                txt = span.get_text()
                if (txt.find('m²')>=0): m2 = txt
                if (txt.find('ambiente')>=0): ambientes = txt
                if (txt.find('baño')>=0): banios = txt
    
        dicc_propiedad = {'id':row,
                          'titulo':titulo,
                          'precio':precio,
                          'expensas':expensas,
                          'inmobiliaria':inmobiliaria,
                          'detalles':detalles,
                          'link':url}
        
        lista_propiedades.append(dicc_propiedad)
        row = row + 1
    
    num = num + 1
    
    fin , dom = pagina(num)
    
    
        


