from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
import requests
import webbrowser

URL = 'https://listado.mercadolibre.com.ar/'

def obtener_productos_finales(productos:list): 
    productos.sort(key = lambda x: float(x["precio"].replace(".","")))
    productos_finales = [productos[i] for i in range(0,12)]
    return productos_finales

def abrir_link(url):
    webbrowser.open(url)

def crear_cards(productos_list):
    lista_productos = obtener_productos_finales(productos_list)

    for i in range(len(lista_productos)):
        producto = Frame(contenedor_productos, bg="gray") 
        producto.grid(row=i // 4, column=i % 4, padx=1, pady=5)

        marca = Label(producto, text=lista_productos[i]["marca"],width=30,bg="yellow")
        marca.pack(pady=1, padx=2)

        descripcion = Label(producto, text=lista_productos[i]["descripcion"], anchor="center", wraplength=200, width=30, height=5)
        descripcion.pack(pady=5)

        precio = Label(producto, text=lista_productos[i]["precio"])
        precio.pack(pady=2)

        def ver_detalle(link=productos_list[i]["link"]):
            abrir_link(link)

        detalles = Button(producto, text="detalle", command=ver_detalle)
        detalles.pack(pady=2)

def obtener_array_productos(peticion):
    soup = BeautifulSoup(peticion.text, features='html.parser')

    box = soup.find_all('li', class_="ui-search-layout__item")

    productos_list= []

    for i in range(0,len(box)):
        producto = {
         "marca": "Desconocido" if type(box[i].find('span', class_="poly-component__brand")) == type(None) else box[i].find('span', class_="poly-component__brand").get_text(),
            "descripcion": box[i].find('h2', class_="poly-box").get_text(),
            "precio": box[i].find('span', class_="andes-money-amount__fraction").get_text(),
            "link": box[i].find_all('a')[0]["href"]
        }
        productos_list.append(producto)

    return productos_list

def texto_input() :
    texto =  buscador.get()
    return texto

def iniciar_busqueda():
    texto = texto_input().lower()

    peticion = requests.get(f"{URL}{texto}")

    try:
        productos_list = obtener_array_productos(peticion)
        crear_cards(productos_list)

    except IndexError:
        messagebox.showwarning(title="Advertencia", message="No hay resultados encontrados, vuelva a intentarlo")

Ventana = Tk()

Ventana.title("Mercadito humilde")
Ventana.geometry("900x750")
Ventana.resizable(0,0)
Ventana.config(bg="lightblue")

nombre_app = Label(Ventana, text="Listado de productos",bg="yellow",height=2, font=15)
nombre_app.pack(fill=BOTH)

buscador = Entry(Ventana, font='Helvetica 10')
buscador.pack()

boton = Button(Ventana, text="buscar", command=iniciar_busqueda, width=10, height=1)
boton.pack()

contenedor_productos = Frame(Ventana)
contenedor_productos.pack(fill=BOTH, pady=10, padx=5)

Ventana.mainloop()
