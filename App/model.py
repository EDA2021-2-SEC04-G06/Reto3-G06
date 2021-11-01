"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as sm
from DISClib.ADT import orderedmap as om
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newAnalyzer():
    analyzer = {'ufos': None,
                'ciudades':None,
                'dateIndex': None,
                'formatoHHMM': None
                }

    analyzer['ufos'] = lt.newList('SINGLE_LINKED', compareDates)
    analyzer['ciudades'] = om.newMap(omaptype='RBT', 
                                        comparefunction=compareLenCiudad)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['formatoHHMM'] = om.newMap(omaptype='BST', comparefunction=compareHHMM)
    return analyzer

# Funciones para agregar informacion al catalogo




def addUfo(analyzer, ufo):
    lt.addLast(analyzer['ufos'], ufo)
    updateDateIndex(analyzer['dateIndex'], ufo)
    updateCiudades(analyzer['ciudades'],ufo)
    updateformatoHHMM(analyzer['formatoHHMM'],ufo)
    return analyzer

def updateformatoHHMM(map, ufo):
    fecha = ufo['datetime']
    horaMinutosufo=(fecha[11:16])
    hora=horaMinutosufo[:2]
    minutos=horaMinutosufo[3:5]
    horayMinutos=int(str(hora)+str(minutos))
    entry = om.get(map,horayMinutos)
    if entry is None:
        datentry=newFormatEntry(ufo)
        lt.addLast(datentry['UFOS'],ufo)
        om.put(map,horayMinutos,datentry)
    else:
        datentry=me.getValue(entry)
        lt.addLast(datentry['UFOS'],ufo)
    return map

def newFormatEntry(ufo):
    entry = {'UFOS': None}
    entry['UFOS'] = lt.newList(datastructure='ARRAY_LIST')
    return entry

def updateCiudades(map, ufo):
    ciudades = ufo['city']
    lenCiudad = len(ciudades)
    entry = om.get(map, lenCiudad)
    if entry is None:
        datentry = newCityEntry2(ufo)
        om.put(map, lenCiudad, datentry)
    else:
        datentry = me.getValue(entry)
    addCity(datentry, ufo)
    return map

def addCity(dataentry, ufo):
    map=dataentry['cities']
    ciudadentry = mp.get(map, ufo['city'])
    if (ciudadentry is None):
        entry = newCiudadEntry(ufo['city'], ufo)
        lt.addLast(entry['UFOS'],ufo)
        mp.put(map, ufo['city'],entry)
    else:
        entry = me.getValue(ciudadentry)
        lt.addLast(entry['UFOS'], ufo)
    return dataentry

def newCityEntry2(ufo):
    entry = {'cities': None} 
    entry['cities']= mp.newMap(maptype='PROBING',
                                        comparefunction=compareMapCity)
    return entry

def newCiudadEntry(citiesgroup, ufo):
    ciudadEntry = {'UFOS':None}
    ciudadEntry['UFOS']=lt.newList('ARRAY_LIST')
    return ciudadEntry


def updateDateIndex(map, ufo):
    occurreddate = ufo['datetime']
    ufodate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, ufodate.date())
    if entry is None:
        datentry = newDataEntry(ufo)
        om.put(map, ufodate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, ufo)
    return map

def addDateIndex(dateEntry, ufo):
    lst = dateEntry['lstUfos']
    lt.addLast(lst, ufo)
    CityIndex = dateEntry['ufoIndex']
    Cityentry = mp.get(CityIndex, ufo['city'])
    if (Cityentry is None):
        entry = newCityEntry(ufo['city'], ufo)
        lt.addLast(entry['lstCities'], ufo)
        mp.put(CityIndex, ufo['city'], entry)
    else:
        entry = me.getValue(Cityentry)
        lt.addLast(entry['lstCities'], ufo)
    return dateEntry


def newDataEntry(ufo):
    entry = {'ufoIndex': None, 'lstUfos': None}
    entry['ufoIndex'] = mp.newMap(numelements=30,
                                  maptype='PROBING',
                                  comparefunction=compareCities)
    entry['lstUfos'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newCityEntry(cities, ufo):
    cityentry = {'city': None, 'lstCities': None}
    cityentry['city'] = cities
    cityentry['lstCities'] = lt.newList('ARRAY_LIST', compareCities)
    return cityentry

# Funciones para creacion de datos

# Funciones de consulta


def ufosSize(analyzer):
    return lt.size(analyzer['ufos'])


def indexHeight(analyzer):
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    return om.size(analyzer['dateIndex'])

def req1(analyzer,ciudad):
    mapaCiudades=(om.get(analyzer['ciudades'],len(ciudad)))['value']['cities']
    listaCiudad=(mp.get(mapaCiudades,ciudad))['value']['UFOS']
    sortedList=sm.sort(listaCiudad,compareDatesReq1)
    return sortedList

def req3(analyzer, hora_inicial, hora_final):
    horaI=hora_inicial[:2]
    minutosI=hora_inicial[3:5]
    horayMinutosI=int(str(horaI)+str(minutosI))
    horaF=hora_final[:2]
    minutosF=hora_final[3:5]
    horayMinutosF=int(str(horaF)+str(minutosF))
    listaEnLista=om.values(analyzer['formatoHHMM'],horayMinutosI, horayMinutosF)
    lista=None
    lista=lt.newList(datastructure='ARRAY_LIST')
    for i in lt.iterator(listaEnLista):
        for j in lt.iterator(i['UFOS']):
            lt.addLast(lista,j)
    sortedList=sm.sort(lista, compareDatesHHMM)
    return sortedList

# Funciones utilizadas para comparar elementos dentro de una lista


def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareLenCiudad(ciudad1, ciudad2):
    if (ciudad1 == ciudad2):
        return 0
    elif (ciudad1 > ciudad2):
        return 1
    else:
        return -1

def compareHHMM(fecha1, fecha2):
    if fecha1 > fecha2:
        return 1
    elif fecha1 < fecha2:
        return -1
    else:
        return 0

def compareMapCity(city1, city2):
    city = me.getKey(city2)
    if city1 == city:
        return 0
    elif city1 > city:
        return 1
    else:
        return -1
    

def compareCities(city1, city2):
    city = me.getKey(city2)
    if (city1 == city):
        return 0
    elif (city1 > city):
        return 1
    else:
        return -1

# Funciones de ordenamiento

def compareDatesReq1(ufo1, ufo2):
    fechaUFO1=ufo1['datetime']
    fechaUFO2=ufo2['datetime']
    if len(fechaUFO1) != 19:
        fechaUFO1=str(datetime.today())
    if len(fechaUFO2) != 19:
        fechaUFO2=str(datetime.today())
    anho_ufo1 = float(fechaUFO1[:4])
    mes_ufo1 = float(fechaUFO1[5:7])
    dia_ufo1 = float(fechaUFO1[8:10])
    hora_ufo1=float(fechaUFO1[11:13])
    minutos_ufo1=float(fechaUFO1[14:16])
    segundos_ufo1=float(fechaUFO1[17:19])
    anho_ufo2 = float(fechaUFO2[:4])
    mes_ufo2 = float(fechaUFO2[5:7])
    dia_ufo2 = float(fechaUFO2[8:10])
    hora_ufo2=float(fechaUFO2[11:13])
    minutos_ufo2=float(fechaUFO2[14:16])
    segundos_ufo2=float(fechaUFO2[17:19])
    if fechaUFO1 == fechaUFO2:
        return 0
    elif anho_ufo1 < anho_ufo2:
        return 1
    elif anho_ufo1 > anho_ufo2:
        return 0
    elif anho_ufo1 == anho_ufo2:
        if mes_ufo1 < mes_ufo2:
            return 1
        elif mes_ufo1 > mes_ufo2:
            return 0
        elif mes_ufo1 == mes_ufo2:
            if dia_ufo1 < dia_ufo2:
                return 1
            elif dia_ufo1 > dia_ufo2:
                return 0
            elif dia_ufo1 == dia_ufo2:
                if hora_ufo1 < hora_ufo2:
                    return 1
                elif hora_ufo1 > hora_ufo2:
                    return 0
                elif hora_ufo1 == hora_ufo2:
                    if minutos_ufo1 < minutos_ufo2:
                        return 1
                    elif minutos_ufo1 > minutos_ufo2:
                        return 0
                    elif minutos_ufo1 == minutos_ufo2:
                        if segundos_ufo1 < segundos_ufo2:
                            return 1
                        elif segundos_ufo1 > segundos_ufo2:
                            return 0

def compareDatesHHMM(ufo1, ufo2):
    fechaUFO1=ufo1['datetime']
    fechaUFO2=ufo2['datetime']
    anho_ufo1 = float(fechaUFO1[:4])
    mes_ufo1 = float(fechaUFO1[5:7])
    dia_ufo1 = float(fechaUFO1[8:10])
    hora_ufo1=float(fechaUFO1[11:13])
    minutos_ufo1=float(fechaUFO1[14:16])
    segundos_ufo1=float(fechaUFO1[17:19])
    anho_ufo2 = float(fechaUFO2[:4])
    mes_ufo2 = float(fechaUFO2[5:7])
    dia_ufo2 = float(fechaUFO2[8:10])
    hora_ufo2=float(fechaUFO2[11:13])
    minutos_ufo2=float(fechaUFO2[14:16])
    segundos_ufo2=float(fechaUFO2[17:19])
    if hora_ufo1 < hora_ufo2:
        return 1
    elif hora_ufo1 > hora_ufo2:
        return 0
    elif hora_ufo1 == hora_ufo2:
        if minutos_ufo1 < minutos_ufo2:
            return 1
        elif minutos_ufo1 > minutos_ufo2:
            return 0
        elif minutos_ufo1 == minutos_ufo2:
            if anho_ufo1 < anho_ufo2:
                return 1
            elif anho_ufo1 > anho_ufo2:
                return 0
            elif anho_ufo1 == anho_ufo2:
                if mes_ufo1 < mes_ufo2:
                    return 1
                elif mes_ufo1 > mes_ufo2:
                    return 0
                elif mes_ufo1 == mes_ufo2:
                    if dia_ufo1 < dia_ufo2:
                        return 1
                    elif dia_ufo1 > dia_ufo2:
                        return 0
                    elif dia_ufo1 == dia_ufo2:
                        return 0