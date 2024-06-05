from backend.factories.visualization_factory import VisualizationFactory
from backend.ontologies.chart_ontology import BarChartOntology

class BarChartFactory(VisualizationFactory):
    def create_visualization(self):
        return BarChartOntology()
