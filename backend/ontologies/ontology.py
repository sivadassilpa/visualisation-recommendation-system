class Ontology:
    def define(self):
        pass

    def get_common_vega_spec(self):
        return {
            "$schema": "https://vega.github.io/schema/vega/v5.json",
            "width": 400,
            "height": 200,
            "padding": 5,
            "axes": [
                {"orient": "bottom", "scale": "xscale"},
                {"orient": "left", "scale": "yscale"},
            ],
        }
