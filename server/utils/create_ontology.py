from factories.bar_chart_factory import BarChartFactory
from factories.line_chart_factory import LineChartFactory
from factories.pie_chart_factory import PieChartFactory
from lookup_tables.graph_type_lookup import GRAPH_TYPE_LOOKUP
def create_ontology(graph_type):
    factory = GRAPH_TYPE_LOOKUP.get(graph_type)
    if factory:
        ontology = factory.create_visualization()
        return {
            "definition": ontology.define(),
            "attributes": ontology.get_attributes()
        }
    else:
        return {"error": "Unknown graph type"}

# Example usage
def test():
    graph_types = ["bar_chart", "line_chart", "pie_chart", "unknown_chart"]
    
    for graph_type in graph_types:
        result = create_ontology(graph_type)
        print(f"Graph Type: {graph_type}")
        print(f"Result: {result}")
        print()