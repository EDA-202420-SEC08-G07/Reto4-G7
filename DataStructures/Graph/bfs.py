from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as lt

def bfs_camino(mi_grafo, inicio, destino):
    """
    Busca un camino entre dos nodos utilizando BFS (Búsqueda en Amplitud).

    Parameters:
    mi_grafo (dict): Grafo donde realizar la búsqueda.
    inicio (str): Nodo de inicio.
    destino (str): Nodo destino.

    Returns:
    list: Camino encontrado o None si no existe camino.
    """
    visitados = set()  # Conjunto para almacenar nodos visitados
    cola = [[inicio]]  # Lista para simular una cola, cada elemento es un camino

    while cola:
        # Sacar el primer camino de la cola
        camino = cola.pop(0)  # Simula un dequeue
        nodo_actual = camino[-1]  # Último nodo en el camino actual

        # Si encontramos el nodo destino, devolver el camino
        if nodo_actual == destino:
            return camino

        # Marcar el nodo como visitado
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)

            # Obtener los vecinos del nodo actual
            lista_adyacentes = mp.get(mi_grafo["vertices"], nodo_actual)
            if lista_adyacentes:
                for arista in lista_adyacentes["elements"]:
                    vecino = arista["vertex"]
                    if vecino not in visitados:
                        # Crear un nuevo camino y agregarlo a la cola
                        nuevo_camino = camino + [vecino]
                        cola.append(nuevo_camino)

    return None  # Si no se encuentra camino