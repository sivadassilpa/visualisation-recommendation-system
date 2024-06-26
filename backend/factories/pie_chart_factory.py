from backend.factories.visualization_factory import VisualizationFactory
from backend.ontologies.chart_ontology import PieChartOntology

class PieChartFactory(VisualizationFactory):
    def create_visualization(self):
        return PieChartOntology()
