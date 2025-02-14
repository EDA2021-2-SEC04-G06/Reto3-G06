﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos


def loadData(analyzer, ufosfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    ufosfile = cf.data_dir + ufosfile
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    for ufo in input_file:
        model.addUfo(analyzer, ufo)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def ufosSize(analyzer):
    return model.ufosSize(analyzer)


def indexHeight(analyzer):
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    return model.indexSize(analyzer)


def req1(analyzer, ciudad):
    return model.req1(analyzer, ciudad)


def req2(analyzer, segundos_min, segundos_max):
    return model.req2(analyzer, segundos_min, segundos_max)


def req3(analyzer, hora_inicial, hora_final):
    return model.req3(analyzer, hora_inicial, hora_final)


def req4(analyzer, fecha_inicial, fecha_final):
    return model.req4(analyzer, fecha_inicial, fecha_final)


def req5(analyzer, longitud_min, longitud_max, latitud_min, latitud_max):
    return model.req5(analyzer, longitud_min, longitud_max, latitud_min, latitud_max)
