from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as lt


def dfs_path(my_graph, start_vertex, end_vertex, visited=None, path=None):
    """
    Busca un camino entre dos nodos utilizando DFS.
    
    Parameters:
    my_graph (dict): Grafo donde realizar la búsqueda.
    start_vertex (str): Nodo de inicio.
    end_vertex (str): Nodo destino.
    visited (set): Conjunto de nodos visitados.
    path (list): Lista para construir el camino actual.

    Returns:
    list: Camino encontrado o None si no existe camino.
    """
    if visited is None:
        visited = set()  # Conjunto para almacenar nodos visitados
    if path is None:
        path = []  # Lista para almacenar el camino actual

    visited.add(start_vertex)
    path.append(start_vertex)

    if start_vertex == end_vertex:
        return path  # Se encontró el camino

    # Obtener los vecinos del nodo actual
    adj_list = mp.get(my_graph["vertices"], start_vertex)
    if adj_list:
        for edge in adj_list["elements"]:
            neighbor = edge["vertex"]
            if neighbor not in visited:
                result = dfs_path(my_graph, neighbor, end_vertex, visited, path)
                if result:
                    return result

    path.pop()  # Retroceder si no hay camino desde aquí
    return None  # No se encontró camino desde este nodo

