import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.maxIndice = 0
        self.graph = None
        self.idmap = {}

    def get_years(self):
        return DAO.get_years()

    def buildGraph(self, anno1, anno2):
        self.graph = nx.Graph()

        allNodes = DAO.getAllCircuits()
        for n in allNodes:
            self.idmap[n.circuitId] = n
        self.graph.add_nodes_from(allNodes)
        for n in allNodes:
            for a in range(int(anno1)+1, int(anno2)):
                valori = DAO.get_valori(n, a)
                if len(valori) > 0:
                    n.diz[a] = valori
        allArchi = DAO.getAllArchi(anno1, anno2)
        for c1,c2,p in allArchi:
            self.graph.add_edge(self.idmap[c1], self.idmap[c2], weight = p)


    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getMaxComponente(self):
        componenti = list(nx.connected_components(self.graph))
        componenteCorretta = []
        for c in componenti:
            if len(list(c)) > len(componenteCorretta):
                componenteCorretta = c
        self.cc = componenteCorretta
        nodiConPesi = []
        for n in componenteCorretta:
            pesoMin = None
            for vicino in nx.neighbors(self.graph, n):
                if pesoMin is None or self.graph[vicino][n]['weight'] < pesoMin:
                    pesoMin = self.graph[vicino][n]['weight']
            nodiConPesi.append((n, pesoMin))
        nodiConPesi.sort(key=lambda x:x[1], reverse=True)
        return nodiConPesi

    def getMaxIndice(self, k, m):
        self.ricorsione([], k, m)
        return self.maxIndice

    def ricorsione(self, parziale, k, m):
        if len(parziale) == k:
            if self.calcolaIndice(parziale) > self.maxIndice:
                self.maxIndice = self.calcolaIndice(parziale)
        else:
            for n in self.cc:
                if self.condizione(parziale, n, m):
                    parziale.append(n)
                    self.ricorsione(parziale, k, m)
                    parziale.pop()

    def calcolaIndice(self, parziale):
        indiceTot = 0
        for n in parziale:
            indiceTot += self.calcolaIndiceN(n)
        return indiceTot

    def calcolaIndiceN(self, n):
        np = 0
        npTot = 0
        for key in n.diz.keys():
            for v in n.diz[key]:
                if v.t is not None:
                    np += 1
                npTot += 1
        return 1 - np/npTot

    def condizione(self, parziale, n, m):
        if n in parziale:
            return False
        if len(n.diz.keys()) >= m:
            return True
        return False







