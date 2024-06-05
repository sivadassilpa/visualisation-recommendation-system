from backend.factories.visualization_factory import VisualizationFactory
from backend.ontologies.chart_ontology import LineChartOntology

class LineChartFactory(VisualizationFactory):
    def create_visualization(self):
        return LineChartOntology()
