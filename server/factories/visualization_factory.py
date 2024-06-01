from ontologies.chart_ontology import BarChartOntology, LineChartOntology
from abc import ABC, abstractmethod


class ChartFactory:
    @staticmethod
    def get_chart_ontology(chart_type):
        if chart_type == "Bar Chart":
            return BarChartOntology()
        elif chart_type == "Line Chart":
            return LineChartOntology()
        # Add other chart types here
        else:
            raise ValueError(f"Unknown chart type: {chart_type}")


class VisualizationFactory:
    @abstractmethod
    def create_visualization(self):
        pass
