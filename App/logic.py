import time
import sys
import os
import json
import csv
from DataStructures.Graph import add_list_graph as graph
from DataStructures.Graph import edge as graph_edge
from DataStructures.Map import map_entry as mp_entry
from DataStructures.Map import map_functions as mp_fun
from DataStructures.Map import map_linear_probing as mp_lin

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = graph.new_graph(10000, True)
    return catalog


# Funciones para la carga de datos
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

def load_data(catalog, data_dir, filename, filename_relations):
    """
    Carga los datos de usuarios y relaciones, y los organiza en un grafo dirigido.
    """
    users_file = data_dir + filename
    relations_file = data_dir + filename_relations
    usuarios = csv.DictReader(open(users_file, encoding='utf-8'))
    relaciones = csv.DictReader(open(relations_file, encoding='utf-8'))
    for usuario in usuarios:
        Id = usuario.get("USER_ID", "Unknown")
        nodo_usuario = {
            "Id": Id,
            "USER_NAME": usuario.get("USER_NAME", "Unknown"),
            "USER_TYPE": usuario.get("USER_TYPE", "Unknown"),
            "AGE": usuario.get("AGE", "Unknown"),
            "JOIN_DATE": usuario.get("JOIN_DATE", "Unknown"),
            "PHOTO": usuario.get("PHOTO", "Unknown"),
            "HOBBIES": usuario.get("HOBBIES", "Unknown"),
            "CITY": usuario.get("CITY", "Unknown"),
            "LATITUDE": usuario.get("LATITUDE", "Unknown"),
            "LONGITUDE": usuario.get("LONGITUDE", "Unknown"),
            "SEGUIDOS": mp_lin.new_map()  # Mapa para almacenar relaciones
        }
        graph.insert_vertex(catalog, Id, nodo_usuario)  # Inserta el nodo en el grafo

    # Agregar relaciones entre nodos
    for relacion in relaciones:
        follower_id = relacion.get("FOLLOWER_ID", "Unknown")
        followed_id = relacion.get("FOLLOWED_ID", "Unknown")
        start_date = relacion.get("START_DATE", "Unknown")

        if graph.contains_vertex(catalog, follower_id) and graph.contains_vertex(catalog, followed_id):
            # Añadir la relación con el peso de fecha
            graph.add_edge(catalog, follower_id, followed_id, start_date)

            # Almacenar la relación en el mapa RELATIONS del nodo seguidor
            nodo_seguidor = mp_lin.get(catalog, follower_id)
            if nodo_seguidor:
                mp_fun.put(nodo_seguidor["SEGUIDOS"], followed_id, start_date)
    return None

def report_data(catalog):
    """
    Reporta la información sobre la red social.
    """
    total_usuarios = graph.num_vertices(catalog)
    total_conexiones = graph.num_edges(catalog)
    usuarios_basic = 0
    usuarios_premium = 0
    usuarios_por_ciudad = mp_lin.new_map()
    
    for user_id in graph.vertices(catalog):
        usuario = mp_fun.get(catalog, user_id)
        user_type = usuario["USER_TYPE"].lower()
        if user_type == "basic":
            usuarios_basic += 1
        elif user_type == "premium":
            usuarios_premium += 1

        ciudad = usuario["CITY"]
        if ciudad:
            if mp_fun.contains(usuarios_por_ciudad, ciudad):
                count = mp_fun.get(usuarios_por_ciudad, ciudad)
                mp_fun.put(usuarios_por_ciudad, ciudad, count + 1)
            else:
                mp_fun.put(usuarios_por_ciudad, ciudad, 1)

    total_seguidores = sum([graph.in_degree(catalog, user_id) for user_id in graph.vertices(catalog)])
    promedio_seguidores = total_seguidores / total_usuarios if total_usuarios > 0 else 0

    ciudad_mayor, max_usuarios = None, 0
    for ciudad in mp_fun.key_set(usuarios_por_ciudad):
        count = mp_fun.get(usuarios_por_ciudad, ciudad)
        if count > max_usuarios:
            max_usuarios = count
            ciudad_mayor = ciudad
    return total_usuarios, total_conexiones, usuarios_basic, usuarios_premium, promedio_seguidores, ciudad_mayor, max_usuarios


# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
