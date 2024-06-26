# lookup_tables/graph_type_lookup.py
from backend.factories.bar_chart_factory import BarChartFactory
from backend.factories.line_chart_factory import LineChartFactory
from backend.factories.pie_chart_factory import PieChartFactory

GRAPH_TYPE_LOOKUP = {
    "bar_chart": BarChartFactory(),
    "line_chart": LineChartFactory(),
    "pie_chart": PieChartFactory()
}
