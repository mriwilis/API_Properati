# https://127.0.0.1:3030/api/BARRIO/INMUEBLE/TIPO
from bs4 import BeautifulSoup
import requests
import unicodedata
from flask import Flask, json, request

def pagina(num,localidad,inmueble,tipo):
    link = "https://www.properati.com.ar/s/" + localidad + "/" + inmueble +"/" + tipo + "?page="
    url = link + str(num)
    response = requests.get(url)
    response.encoding = "utf-8"
    html = response.text
    dom = BeautifulSoup(html, features = "html.parser")
    fin = dom.find( attrs = { 'class' : 'StyledPagerButton-sq1exe-0 cFkGqv pager-next' } )
    return fin, dom


app = Flask(__name__)

@app.route("/<localidad>/<inmueble>/<tipo>")
def scrapeo(localidad,inmueble,tipo):
    row=1
    lista_propiedades=[]
    num=1
    
    fin,dom = pagina(num,localidad,inmueble,tipo)
    
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
            if inmobiliaria: inmobiliaria = inmobiliaria.get_text()
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
                              'm2':m2,
                              'baños':banios,
                              'inmobiliaria':inmobiliaria,
                              'link':url}

            
            lista_propiedades.append(dicc_propiedad)
            row = row + 1
    
        num = num + 1
        
        fin , dom = pagina(num,localidad,inmueble,tipo)
    
    json_propiedades = json.dumps(lista_propiedades)
    
    response = app.response_class(response=json_propiedades, status=200, mimetype = "application/json")
    
    return response
    
app.run( port = 3030, host = '0.0.0.0' )