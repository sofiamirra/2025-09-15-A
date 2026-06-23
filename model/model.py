import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._drivers = []
        self._idMapDrivers = {}
        self._lista_archi = []

    def getAllYears(self):
            return DAO.getAllYears()

    def buildGraph(self, y1, y2):
        self._graph.clear()
        self._idMapDrivers = {}
        nodes = DAO.getAllNodes(y1, y2)
        self._graph.add_nodes_from(nodes)
        for d in nodes:
            # la chiave deve sempre corrispondere all'attributo chiave primaria
            self._idMapDrivers[d.driverId] = d
        allEdges = DAO.getAllEdges(y1, y2, self._idMapDrivers)
        for e in allEdges:
            self._graph.add_edge(e.d1, e.d2, weight=e.peso)
            self._lista_archi.append(e)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop3Archi(self):
        """Restituisce i 3 archi con peso maggiore in ordine decrescente"""
        self._lista_archi.sort(key=lambda x: x.peso, reverse=True)
        return self._lista_archi[:3]

    def getComponentiConnesseDetails(self):
        # Conta quante "isole separate" ci sono nel grafo (A -- B -- C), (D -- F)
        componenti = list(nx.connected_components(self._graph)) # restituisce tutte le componenti, ogni componente è un insieme di nodi

        # Prende la componente con più nodi
        largest = max(componenti, key=len)
        nodi_ordinati = sorted(largest, key=lambda n: self._graph.degree(n), reverse=True)

        return len(componenti), largest, nodi_ordinati

