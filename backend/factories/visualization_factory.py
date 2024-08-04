from backend.ontologies.chart_ontology import (
    BarChartOntology,
    LineChartOntology,
    PieChartOntology,
    ScatterPlotOntology,
    HeatmapOntology,
    WordCloudOntology,
)
from abc import ABC, abstractmethod


class ChartFactory:
    @staticmethod
    def get_chart_ontology(chart_type, selectedData, selectedColumns):
        if chart_type == "Bar Chart":
            return BarChartOntology(selectedData, chart_type, selectedColumns)
        elif chart_type == "Line Chart":
            return LineChartOntology(selectedData, chart_type, selectedColumns)
        elif chart_type == "Pie Chart":
            return PieChartOntology(selectedData, chart_type, selectedColumns)
        elif chart_type == "Scatter Plot":
            return ScatterPlotOntology(selectedData, chart_type, selectedColumns)
        elif chart_type == "Heatmap":
            return HeatmapOntology(selectedData, chart_type, selectedColumns)
        elif chart_type == "Word Cloud":
            return WordCloudOntology(selectedData, chart_type, selectedColumns)
        # Add other chart types here
        else:
            return LineChartOntology(selectedData, chart_type, selectedColumns)
            # raise ValueError(f"Unknown chart type: {chart_type}")


class VisualizationFactory:
    @abstractmethod
    def create_visualization(self):
        pass
