import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        anni = self._model.get_years()
        for a in anni:
            self._view._ddYear1.options.append(ft.dropdown.Option(a))
            self._view._ddYear2.options.append(ft.dropdown.Option(a))
        self._view.update_page()



    def handleBuildGraph(self, e):
        anno1 = self._view._ddYear1.value
        anno2 = self._view._ddYear2.value
        if anno1 is None or anno2 is None:
            self._view._txtGraphDetails.controls.append(ft.Text("Selezionare un anno di inizio e fine range"))
            self._view.update_page()
            return
        if anno2 < anno1:
            self._view._txtGraphDetails.controls.append(ft.Text("Anno fine range deve essere > di anno inizio range"))
            self._view.update_page()
            return
        self._model.buildGraph(anno1, anno2)
        nodi, archi = self._model.getGraphDetails()
        self._view._txtGraphDetails.controls.append(ft.Text(f"Grafo creato con {nodi} nodi e {archi} archi"))
        self._view.update_page()

    def handlePrintDetails(self, e):
        nodiComponente = self._model.getMaxComponente()
        self._view._txtGraphDetails.controls.append(ft.Text("Di seguito i nodi della massima componente connessa: "))
        for n,p in nodiComponente:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{n} -- {p}"))
        self._view.update_page()


    def handleCercaDreamChampionship(self, e):
        try:
            k = int(self._view._txtInSoglia.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserire un intero per la soglia"))
            self._view.update_page()
            return

        try:
            m = int(self._view._txtInNumDiEdizioni.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserire un intero per il num di edizioni"))
            self._view.update_page()
            return
        indiceMax = self._model.getMaxIndice(k, m)
        self._view._txt_result.controls.append(ft.Text(f"l'indice di imprevedibilità max è: {indiceMax}"))
        self._view.update_page()


