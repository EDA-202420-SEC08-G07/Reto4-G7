from DataStructures.Graph import edge as eg
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as lt

def new_graph(size = 19, directed = False):
    if directed:
        return {"vertices": mp.new_map(size, 0.5), "information": mp.new_map(size, 0.5), "in_degree":None, "edges": 0, "directed": True, "type": "ADJ_LIST"}
    grafo = {"vertices": mp.new_map(size, 0.5), "information": mp.new_map(size, 0.5),"in_degree":None,"edges": 0, "directed": directed, "type": "ADJ_LIST"}
    return grafo

def insert_vertex(my_graph, key_vertex, info_vertex):
    if key_vertex not in mp.key_set(my_graph["vertices"]):  
        mp.put(my_graph["vertices"], key_vertex, lt.new_list())  
        mp.put(my_graph["information"], key_vertex, info_vertex) 
    return my_graph

def remove_vertex(my_graph, key_vertex):
    if key_vertex in my_graph["vertices"]:
        mp.remove(my_graph["vertices"], key_vertex)
        mp.remove(my_graph["info"], key_vertex)
    return my_graph

def num_vertices(my_graph):
    return mp.size(my_graph["vertices"])

def num_edges(my_graph):
    return my_graph["edges"]

def vertices(my_graph):
    lista_vertices = lt.new_list()
    vertex_llaves = mp.key_set(my_graph["vertices"])  
    for llave_vertice in vertex_llaves['elements']: 
        lt.add_last(lista_vertices, llave_vertice)
    return lista_vertices

def degree(graph, vertex):
    """
    Retorna el grado (número de aristas incidentes) de un vértice en el grafo.
    """
    adj_list = mp.get(graph["vertices"], vertex)
    if adj_list is None:
        return 0  # Si el vértice no tiene adyacencias, retorna 0
    return len(adj_list["elements"])  # Retorna la cantidad de conexiones



def in_degree(my_graph, vertex):
    """
    Devuelve el grado de entrada de un vértice en un grafo dirigido.

    Parameters:
    - my_graph (dict): Representación del grafo con una lista de adyacencia.
    - vertex (str): Vértice del cual calcular el grado de entrada.

    Returns:
    - int: Grado de entrada del vértice.
    - None: Si el vértice no existe en el grafo.
    """
    if not mp.contains(my_graph["vertices"], vertex):
        return None

    if not my_graph["directed"]:
        return degree(my_graph, vertex)

    in_deg = 0

    # Iterar sobre todos los vértices
    vertices = mp.key_set(my_graph["vertices"])
    num_vertices = lt.size(vertices)
    for i in range(num_vertices):
        current_vertex = lt.get_element(vertices, i)
        adj_list = mp.get(my_graph["vertices"], current_vertex)
        
        if adj_list and "elements" in adj_list and isinstance(adj_list["elements"], list):  # Verificar si "elements" es una lista
            for edge in adj_list["elements"]:
                if edge["vertex"] == vertex:  # Compara si el vértice es el que se busca
                    in_deg += 1

    return in_deg

def out_degree(my_graph, key_vertex):
    if key_vertex not in my_graph["vertices"]:
        return 0

    adj_list = mp.get(my_graph["vertices"], key_vertex)
    return lt.size(adj_list)

    
def get_edge(my_graph, vertex_a, vertex_b):
    if mp.contains(my_graph["vertices"], vertex_a):
        adj_list = mp.get(my_graph["vertices"], vertex_a)
        for edge in adj_list:
            if edge["vertex"] == vertex_b:
                return edge
    return None

def contains_vertex(my_graph, vertex):
    return mp.contains(my_graph["vertices"], vertex)

def add_edge(my_graph, vertex_a, vertex_b, weight=0):
    if not mp.contains(my_graph["vertices"], vertex_a) or not mp.contains(my_graph["vertices"], vertex_b):
        return my_graph
    adj_list_a = mp.get(my_graph["vertices"], vertex_a)
    existe = False
    for edge in adj_list_a['elements']:
        if edge.get("vertex") == vertex_b:  
            edge["weight"] = weight
            existe= True
            break
    if not existe:
        lt.add_last(adj_list_a, {"vertex": vertex_b, "weight": weight})
        my_graph["edges"] += 1  
        if not my_graph["directed"]:
            adj_list_b = mp.get(my_graph["vertices"], vertex_b)
            lt.add_last(adj_list_b, {"vertex": vertex_a, "weight": weight})
    return my_graph

def get_vertex_info(my_graph, vertex_key):
    """
    Devuelve la información asociada a un vértice en el grafo.
    
    Parameters:
    my_graph (dict): Grafo donde buscar el vértice.
    vertex_key (str): Clave del vértice (USER_ID).
    
    Returns:
    dict: Información asociada al vértice o None si no existe.
    """
    if mp.contains(my_graph["information"], vertex_key):
        return mp.get(my_graph["information"], vertex_key)
    return None


def adjacents(my_graph, vertex):
    """
    Devuelve una lista de los vértices adyacentes (amigos) de un vértice dado.

    Parameters:
    - my_graph (dict): Grafo representado como lista de adyacencia.
    - vertex (str): Vértice del cual obtener los adyacentes.

    Returns:
    - list: Lista de vértices adyacentes.
    - None: Si el vértice no existe en el grafo.
    """
    if not mp.contains(my_graph["vertices"], vertex):
        return None

    adj_list = mp.get(my_graph["vertices"], vertex)
    adyacentes = lt.new_list()

    # Extraer los vértices adyacentes de la lista de adyacencia
    for edge in adj_list['elements']:
        lt.add_last(adyacentes, edge["vertex"])

    return adyacentes