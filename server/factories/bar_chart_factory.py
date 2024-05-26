from factories.visualization_factory import VisualizationFactory
from ontologies.chart_ontology import BarChartOntology

class BarChartFactory(VisualizationFactory):
    def create_visualization(self):
        return BarChartOntology()
