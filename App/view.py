"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

ufosfile = 'UFOS-utf8-small.csv'
cont = None


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def printPrimeros3(lista):
    i=1
    while i<=3:
        avistamiento = lt.getElement(lista,i)
        print(str(i)+". Fecha y Hora: " + avistamiento['datetime'] + " , Ciudad: " + avistamiento['city'] +' , Pais: ' + avistamiento['country'] + 
                                ' , Duración en segundos: ' + avistamiento['duration (seconds)'] + ' , Forma del objeto: ' +  avistamiento['shape'])
        i+=1
    print('...')

def printUltimos3(lista):
    size=lt.size(lista)
    i=size-2
    while i<=size:
        avistamiento = lt.getElement(lista,i)
        print(str(i)+". Fecha y Hora: " + avistamiento['datetime'] + " , Ciudad: " + avistamiento['city'] +' , Pais: ' + avistamiento['country'] + 
                                ' , Duración en segundos: ' + avistamiento['duration (seconds)'] + ' , Forma del objeto: ' +  avistamiento['shape'])
        i+=1


def printMenu():
    print("\nBienvenido")
    print("1- Inicializar")
    print("2- Cargar información en el catálogo")
    print("3- Contar los avistamientos en una ciudad")
    print("4- Contar los avistamientos por duración")
    print("5- Contar avistamientos por Hora/Minutos del día")
    print("6- Contar los avistamientos en un rango de fechas")
    print("7- Contar los avistamientos de una Zona Geográfica")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('\nSeleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de avistamientos ....")
        controller.loadData(cont, ufosfile)
        print('Avistamientos cargados: ' + str(controller.ufosSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))

        print(cont['ciudades'])

    elif int(inputs[0]) == 3:
        ciudad=input('\nIngrese la ciudad: ')
        total = controller.req1(cont,ciudad)
        print('\nHay '+str(lt.size(total)) + ' avistamientos en la ciudad de: '+ciudad)
        print('Los primeros 3 y ultimos 3 avistamientos en '+ciudad +' son: ')
        printPrimeros3(total)
        printUltimos3(total)

    else:
        sys.exit(0)
sys.exit(0)
