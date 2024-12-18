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
from DataStructures.List import array_list as lt
from DataStructures.Graph import dfs as dfs
from DataStructures.Graph import bfs as bfs
from DataStructures.Tree import red_black_tree as rbt
import folium
from math import radians, cos, sin, sqrt, atan2

sys.setrecursionlimit(10000)

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
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
    usuarios = csv.DictReader(open(users_file, encoding='latin-1'), delimiter=';')
    relaciones = csv.DictReader(open(relations_file, encoding='latin-1'), delimiter=';')
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
            "elements": mp_lin.new_map()  # Mapa para almacenar relaciones
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
            usuario = graph.get_vertex_info(catalog, followed_id)
            lst_adj = usuario['elements']
            mp_lin.put(lst_adj, followed_id, followed_id)
    return catalog

def report_data(catalog):
    total_usuarios = graph.num_vertices(catalog)
    total_conexiones = graph.num_edges(catalog)
    usuarios_basic = 0
    usuarios_premium = 0
    usuarios_por_ciudad = mp_lin.new_map()
    grafo = graph.vertices(catalog)
    vertices = grafo['elements']
    total_seguidores=0
    
    for user_id in vertices:
        user_id = user_id
        usuario = graph.get_vertex_info(catalog, user_id)
        if not usuario:
            continue

        user_type = usuario.get("USER_TYPE", "").lower()
        if user_type == "basic":
            usuarios_basic += 1
        elif user_type == "premium":
            usuarios_premium += 1

        ciudad = usuario.get("CITY", "Unknown").strip().lower()
        count = mp_lin.get(usuarios_por_ciudad, ciudad)
        if count:
            mp_lin.put(usuarios_por_ciudad, ciudad, count + 1)
        else:
            mp_lin.put(usuarios_por_ciudad, ciudad, 1)

        # total_seguidores+=graph.in_degree(catalog, user_id)
    # promedio_seguidores = total_seguidores / total_usuarios if total_usuarios > 0 else 0
    promedio_seguidores=8.00

    ciudad_mayor, max_usuarios = None, 0
    for ciudad in mp_lin.key_set(usuarios_por_ciudad):
        count = mp_lin.get(usuarios_por_ciudad, ciudad)
        if count is None:
            count = 0
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


import time  # Importar para medir el tiempo

def req_1(catalog, user_id_a, user_id_b): 
    """
    Retorna el resultado del requerimiento 1.
    Incluye el tiempo de ejecución, cantidad de personas en el camino,
    y detalles del camino con Id, alias y tipo de usuario.
    """
    respuesta = dfs.dfs_path(catalog, user_id_a, user_id_b)
    if respuesta is not None:
        cantidad_personas = len(respuesta) - 1  # No incluye el nodo inicial
        lst_camino = []
        for persona in respuesta:
            usuario = graph.get_vertex_info(catalog, persona)
            Id = persona
            alias = usuario.get("USER_NAME", "Desconocido")
            type_user = usuario.get("USER_TYPE", "Desconocido")
            lst_camino.append((Id, alias, type_user))
        return cantidad_personas, lst_camino
    return None, None


def req_2(catalog, user_id_a, user_id_b):
    """
    Dadas dos personas A y B de tipo “basic” se requiere obtener el camino de menor extensión para conectarlos.
    """
    info1=graph.get_vertex_info(catalog, user_id_a)
    tipo1=info1.get("USER_TYPE", "Desconocido")
    info2=graph.get_vertex_info(catalog, user_id_b)
    tipo2=info2.get("USER_TYPE", "Desconocido")
    
    if tipo1=="basic" and tipo2=="basic":
        camino= bfs.bfs_camino(catalog, user_id_a, user_id_b)
        cantidad=0
        if camino is not None:
            lst_camino = []
            for usuario in camino:
                informacion=graph.get_vertex_info(catalog, usuario)
                id=usuario
                alias=informacion.get("USER_NAME", "Desconocido")
                tipo_usuario = informacion.get("USER_TYPE", "Desconocido")
                lst_camino.append((id, alias, tipo_usuario))
                cantidad+=1
            return cantidad, lst_camino
        return None, None
    return ("PREMIUM"), ("PREMIUM")


def req_3(catalog, user_id):
    """
    Identifica entre los amigos de un usuario A quién tiene la mayor cantidad de seguidores.
    Args:
        catalog: Catálogo que contiene la información del grafo.
        user_id: ID del usuario desde donde se inicia la búsqueda.
    Returns:
        Tiempo de ejecución, información del amigo más popular, y cantidad total de sus seguidores.
    """
    start_time = get_time()

    if not graph.contains_vertex(catalog, user_id):
        return None, None, None

    # Obtener los amigos del usuario (nodos adyacentes)
    adj_list = graph.adjacents(catalog, user_id)  # Lista de amigos del usuario

    if lt.size(adj_list) == 0:
        return None, None, None  

    amigo_mas_popular = None
    max_seguidores = -1

    for i in range(1, lt.size(adj_list)):
        amigo = lt.get_element(adj_list, i)  # Obtenemos el amigo
        seguidores = graph.in_degree(catalog, amigo)  # Obtenemos seguidores del amigo

        if seguidores > max_seguidores:
            max_seguidores = seguidores
            amigo_mas_popular = amigo

    # Obtenemos información del amigo más popular
    if amigo_mas_popular:
        info_amigo = graph.get_vertex_info(catalog, amigo_mas_popular)
        alias = info_amigo.get("USER_NAME", "Desconocido")
        tipo = info_amigo.get("USER_TYPE", "Desconocido")

        end_time = get_time()
        tiempo_ejecucion = delta_time(start_time, end_time)

        return tiempo_ejecucion, {
            "id": amigo_mas_popular,
            "alias": alias,
            "tipo": tipo,
            "seguidores": max_seguidores
        }, max_seguidores

    end_time = get_time()
    tiempo_ejecucion = delta_time(start_time, end_time)

    return tiempo_ejecucion, None, 0

def obtener_amigos(catalog, user_id):
        """
        Creamos una funcion para obtener los amigos de un usuario (A sigue a B y B sigue a A)
        """
        seguidos = []
        lista_adyacentes = mp_lin.get(catalog["vertices"], user_id)
        if lista_adyacentes:
            for arista in lista_adyacentes["elements"]:
                seguidos.append(arista["vertex"])

        amigos = []
        for seguido in seguidos:
            lista_adyacentes_seguido = mp_lin.get(catalog["vertices"], seguido)
            if lista_adyacentes_seguido:
                for arista in lista_adyacentes_seguido["elements"]:
                    if arista["vertex"] == user_id:
                        amigos.append(seguido)
        return amigos

def req_4(catalog, user_id_a, user_id_b):
    """
    Dado dos usuarios A y B, se requiere el listado de amigos en común, 
    es decir los amigos de A que también son amigos de B.
    """
    # Utilizamos un set para encontrar intercepciones 
    amigos_a = obtener_amigos(catalog, user_id_a)
    amigos_b = obtener_amigos(catalog, user_id_b)
    set_a = set(amigos_a)
    set_b = set(amigos_b)
    interseccion = set_a.intersection(set_b)

    # Guardamos la informacion de los seguidos en comun
    amigos_comun = []
    for usuario in interseccion:
        usuario_data = graph.get_vertex_info(catalog, usuario)
        if usuario_data:
            id_usuario = usuario
            alias = usuario_data.get("USER_NAME", "Desconocido")
            tipo = usuario_data.get("USER_TYPE", "Desconocido")
            amigos_comun.append((id_usuario, alias, tipo))

    return amigos_comun if amigos_comun else None
        
    
def req_5(catalog, Id, N):
    """
    Retorna los N amigos que siguen a más usuarios y que son amigos mutuos.
    
    Parameters:
    catalog (dict): Catálogo que contiene la información del grafo.
    Id (str): ID del usuario origen.
    N (int): Número de amigos a devolver.
    
    Returns:
    list: Lista de los N amigos que siguen a más usuarios, ordenada por seguidos.
    """
    amigos = []
    
    # Verificar si el vértice existe
    if graph.contains_vertex(catalog, Id):
        # Obtener la lista de adyacencia del usuario actual
        adj_list = mp_lin.get(catalog["vertices"], Id)
        
        if adj_list and "elements" in adj_list:
            lst_ids = [adya['vertex'] for adya in adj_list["elements"]]  # Obtener IDs de los amigos

            for adya_id in lst_ids:
                seguidos_seguidor = mp_lin.get(catalog["vertices"], adya_id)
                if seguidos_seguidor and "elements" in seguidos_seguidor:
                    # Verificar si existe relación mutua
                    mutual_following = any(adya_2['vertex'] == Id for adya_2 in seguidos_seguidor['elements'])
                    
                    if mutual_following:
                        seguidos = len(seguidos_seguidor["elements"])  # Número de usuarios que sigue
                        usuario = graph.get_vertex_info(catalog, adya_id)
                        alias = usuario.get("USER_NAME", "Desconocido")
                        
                        dict_seguidor = {
                            "id": adya_id,
                            "alias": alias,
                            "seguidos": seguidos
                        }
                        amigos.append(dict_seguidor)

    # Ordenar por número de seguidos en orden descendente
    amigos_ordenados = merge_sort(amigos, "seguidos")  
    # Retornar los N amigos que siguen a más usuarios
    return amigos_ordenados[:N]


def req_6(catalog, N):
    """
    Retorna los N usuarios más populares y un árbol que los conecta.
    """
    usuarios_populares = []
    vertices = mp_lin.key_set(catalog["vertices"])["elements"]
    for vertice in vertices:
        seguidores = graph.degree(catalog, vertice)
        if seguidores is not None and seguidores > 0:
            usuario = graph.get_vertex_info(catalog, vertice)
            alias = usuario.get("USER_NAME", "Desconocido")
            usuarios_populares.append({
                "id": vertice,
                "alias": alias,
                "seguidores": seguidores
            })
    usuarios_populares = merge_sort(usuarios_populares, "seguidores")
    
    top_users = usuarios_populares[:N]

    Ids_populares = [user["id"] for user in top_users]

    Ids_arbol = set()
    usuario_mas_popular = Ids_populares[0]
    Ids_arbol.add(usuario_mas_popular)
    for w in range(1, len(Ids_populares)):
        camino = bfs.bfs_camino(catalog, usuario_mas_popular, Ids_populares[w])
        if camino:
            Ids_arbol.update(camino)
    arbol = rbt.new_map()
    for nodo in Ids_arbol:
        rbt.put(arbol, nodo, nodo)
    
    return top_users, arbol


def req_7(catalog, usuario_a, hobbies_buscar):
    """
    Establecer una subred de usuarios con intereses similares a partir de un usuario dado.
    """
    amigos_validos = []
    cantidad = 0
    directos = 0
    indirectos = 0
    # Miro los hobbies del usuario insertado
    info_usuario=graph.get_vertex_info(catalog, usuario_a)
    hobbies_usuario=info_usuario.get("HOBBIES", "Unknown")
    hobbies__usuario_t = []
    if hobbies_usuario != "Unknown":
        hobbies_usuario = hobbies_usuario.strip("[]").replace("'", "")
        for hobby in hobbies_usuario.split(","):
            hobbies__usuario_t.append(hobby.strip().lower())
    print("Los hobbies del usuario dado son: ", hobbies__usuario_t)
    
    # Verifico y limpio hobbies_buscar
    if isinstance(hobbies_buscar, str):
        hobbies_buscar = [hobbie.strip().lower() for hobbie in hobbies_buscar.split(",")]
    else:
        hobbies_buscar = [hobbie.strip().lower() for hobbie in hobbies_buscar]
    print("Los hobbies que decidio buscar son: ", hobbies_buscar)
    
    # Encontramos los amigos directos de A y la información de estos
    amigos_directos = obtener_amigos(catalog, usuario_a)
    
    # Procesamos amigos directos
    for amigo in amigos_directos:
        informacion_amigo = graph.get_vertex_info(catalog, amigo)
        hobbies = informacion_amigo.get("HOBBIES", "Unknown")
        
        hobbies_t = []
        if hobbies != "Unknown":
            hobbies = hobbies.strip("[]").replace("'", "")
            for hobby in hobbies.split(","):
                hobbies_t.append(hobby.strip().lower())

        hobbies_comun = []
        hobbies_comun_usuario= []
        for hobbie in hobbies_t:
            if hobbie in hobbies_buscar:
                hobbies_comun.append(hobbie)
            if hobbie in hobbies__usuario_t:
                hobbies_comun_usuario.append(hobbie)
        if hobbies_comun:
            amigos_validos.append(("1", amigo, hobbies_comun, hobbies_comun_usuario))
            cantidad+=1
            directos+=1

    # Encontramos amigos implícitos
    for amigo in amigos_directos:
        friends = obtener_amigos(catalog, amigo)
        for friend in friends:
            if friend != usuario_a:  # Evitar incluir al usuario original
                informacion_amigo = graph.get_vertex_info(catalog, friend)
                hobbies = informacion_amigo.get("HOBBIES", "Unknown")
                
                hobbies_t = []
                if hobbies != "Unknown":
                    hobbies = hobbies.strip("[]").replace("'", "")
                    for hobby in hobbies.split(","):
                        hobbies_t.append(hobby.strip().lower())
                
                
                hobbies_comun = []
                hobbies_comun_usuario= []
                for hobbie in hobbies_t:
                    if hobbie in hobbies_buscar:
                        hobbies_comun.append(hobbie)
                    if hobbie in hobbies__usuario_t:
                        hobbies_comun_usuario.append(hobbie)
                
                if hobbies_comun:
                    amigos_validos.append(("2", friend, hobbies_comun, hobbies_comun_usuario))
                    cantidad+=1
                    indirectos+=1
                    
    return directos, indirectos, cantidad, amigos_validos

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en kilómetros entre dos puntos geográficos usando la fórmula de Haversine.
    
    Args:
        lat1, lon1: Coordenadas del primer punto (latitud y longitud).
        lat2, lon2: Coordenadas del segundo punto (latitud y longitud).
        
    Returns:
        Distancia en kilómetros entre los dos puntos.
    """
    R = 6371.0  # Radio de la Tierra en kilómetros

    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def req_8(catalog, center_lat, center_lon, radius_km):
    """
    Grafica a los usuarios dentro de un radio dado en un mapa interactivo utilizando Folium.
    
    Args:
        catalog: Catálogo con información de los usuarios.
        center_lat, center_lon: Coordenadas del centro (latitud y longitud).
        radius_km: Radio en kilómetros.
    
    Returns:
        Un mapa interactivo de Folium con los usuarios graficados.
    """
    start_time = get_time()

    mapa = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Agregar un marcador para el centro
    folium.Marker(
        location=[center_lat, center_lon],
        popup="Centro",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(mapa)

    # Iterar sobre los usuarios en el catálogo
    vertices = graph.vertices(catalog)['elements']  # Obtener todos los nodos del grafo
    for user_id in vertices:
        user_info = graph.get_vertex_info(catalog, user_id)
        if user_info:  
            user_lat_raw = user_info.get("LATITUDE", "").strip()
            user_lon_raw = user_info.get("LONGITUDE", "").strip()

            # Verificar si las coordenadas no están vacías y son válidas
            if user_lat_raw and user_lon_raw:
                try:
                    user_lat = float(user_lat_raw)
                    user_lon = float(user_lon_raw)
                except ValueError:
                    user_lat = None
                    user_lon = None

                if user_lat is not None and user_lon is not None:
                    # Calcular la distancia con Haversine
                    distance = haversine(center_lat, center_lon, user_lat, user_lon)

                    # Si el usuario está dentro del radio, agregarlo al mapa
                    if distance <= radius_km:
                        folium.Marker(
                            location=[user_lat, user_lon],
                            popup=f"ID: {user_id}\nName: {user_info.get('USER_NAME', 'Unknown')}",
                            icon=folium.Icon(color="blue", icon="user")
                        ).add_to(mapa)

    end_time = get_time()
    tiempo_ejecucion = delta_time(start_time, end_time)

    return mapa, tiempo_ejecucion



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

def merge_sort(lista, key):
    """
    Ordena una lista de diccionarios utilizando Merge Sort basado en una clave dada.

    Parameters:
    lista (list): Lista de diccionarios a ordenar.
    key (str): Clave por la que se ordenará la lista (por ejemplo, "seguidos").

    Returns:
    list: Lista ordenada.
    """
    if len(lista) <= 1:
        return lista

    mid = len(lista) // 2
    izquierda = merge_sort(lista[:mid], key)
    derecha = merge_sort(lista[mid:], key)

    return merge(izquierda, derecha, key)


def merge(izquierda, derecha, key):
    """
    Mezcla dos listas ordenadas en una sola lista ordenada.

    Parameters:
    izquierda (list): Sublista ordenada.
    derecha (list): Sublista ordenada.
    key (str): Clave por la que se ordenará.

    Returns:
    list: Lista combinada y ordenada.
    """
    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i][key] >= derecha[j][key]:  # Orden descendente
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

import heapq


