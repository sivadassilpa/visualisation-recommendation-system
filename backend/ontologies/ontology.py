class Ontology:
    def define(self):
        pass

    def get_common_vega_spec(self):
        return {
            "$schema": "https://vega.github.io/schema/vega/v5.json",
            "width": 300,
            "height": 200,
            "padding": 5,
            "title": self.get_chart_title(),
        }

    def get_chart_title(self):
        """
        Generate the chart title in the format: "Chart Name: Column1 vs Column2 vs Column3"
        """
        chart_name = self.chartType
        column_names = " vs ".join(self.data.columns)
        return f"{chart_name}: {column_names}"
