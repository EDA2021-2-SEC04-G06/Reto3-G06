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
from DISClib.Algorithms.Sorting import shellsort as sa
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
                'dateIndex': None
                }

    analyzer['ufos'] = lt.newList('SINGLE_LINKED', compareDates)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo


def addUfo(analyzer, ufo):
    lt.addLast(analyzer['ufos'], ufo)
    updateDateIndex(analyzer['dateIndex'], ufo)
    return analyzer


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
    cityentry['lstCities'] = lt.newList('SINGLELINKED', compareCities)
    return cityentry

# Funciones para creacion de datos

# Funciones de consulta


def ufosSize(analyzer):
    return lt.size(analyzer['ufos'])


def indexHeight(analyzer):
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    return om.size(analyzer['dateIndex'])

# Funciones utilizadas para comparar elementos dentro de una lista


def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
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
