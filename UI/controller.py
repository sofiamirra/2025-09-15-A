import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _fillDDYears(self):
        years = self._model.getAllYears()
        yearsDD = []
        for year in years:
            yearsDD.append(ft.dropdown.Option(year))
        self._view._ddAnno1.options = yearsDD
        self._view._ddAnno2.options = yearsDD
        self._view.update_page()

    def handleCreaGrafo(self,e):
        """Recupera gli anni dal DropDown"""
        year1 = self._view._ddAnno1.value
        year2 = self._view._ddAnno2.value
        self._model.buildGraph(year1, year2)
        self._view.txt_result.controls.clear() # pulisco prima di stampare qualsiasi cosa
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="red"))

        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {nEdges}"))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view.txt_result.controls.clear() # pulisco prima di stampare qualsiasi cosa
        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore: ", color="red"))
        top_archi = self._model.getTop3Archi()
        for arco in top_archi:
            # Metodo di stampa definito in __str__ di arco
            self._view.txt_result.controls.append(ft.Text(str(arco)))

        nComp,  bComp, nodes = self._model.getComponentiConnesseDetails()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nComp} componenti connesse", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({len(nodes)} nodi): ", color="red"))
        for node in nodes:
            self._view.txt_result.controls.append(ft.Text(f"{node.driverRef} ({node.driverId}) -- DoB: {node.dob}"))

        self._view.txt_result.controls.append(ft.Text(f"Componente connessa in ordine decrescente: ", color="red"))
        for node in nodes:
            grado = self._model._graph.degree(node)
            self._view.txt_result.controls.append(ft.Text(f"{node.driverRef} ({node.driverId}) -- DoB: {node.dob} (grado={grado})"))
        self._view.update_page()

    def handleCerca(self, e):
        pass

