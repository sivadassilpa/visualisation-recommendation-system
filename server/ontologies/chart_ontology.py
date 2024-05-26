from ontologies.ontology import Ontology

class BarChartOntology(Ontology):
    def define(self):
        return "BarChart Ontology Defined"
    
    def get_attributes(self):
        return {
            "x_axis": "Category",
            "y_axis": "Values",
            "color": "Category",
            "orientation": ["vertical", "horizontal"]
        }

class LineChartOntology(Ontology):
    def define(self):
        return "LineChart Ontology Defined"
    
    def get_attributes(self):
        return {
            "x_axis": "Time",
            "y_axis": "Values",
            "color": "Category",
            "line_style": ["solid", "dashed", "dotted"]
        }

class PieChartOntology(Ontology):
    def define(self):
        return "PieChart Ontology Defined"
    
    def get_attributes(self):
        return {
            "slices": "Category",
            "values": "Values",
            "color": "Category"
        }
