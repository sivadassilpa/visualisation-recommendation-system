from ontologies.ontology import Ontology


class BarChartOntology(Ontology):
    def define(self):
        vega_spec = self.get_common_vega_spec()
        vega_spec.update(
            {
                "data": [
                    {
                        "name": "table",
                        "values": [
                            {"category": "A", "amount": 28},
                            {"category": "B", "amount": 55},
                            {"category": "C", "amount": 43},
                            {"category": "D", "amount": 91},
                            {"category": "E", "amount": 81},
                            {"category": "F", "amount": 53},
                            {"category": "G", "amount": 19},
                            {"category": "H", "amount": 87},
                        ],
                    },
                ],
                "signals": [
                    {
                        "name": "tooltip",
                        "value": {},
                        "on": [
                            {"events": "rect:mouseover", "update": "datum"},
                            {"events": "rect:mouseout", "update": "{}"},
                        ],
                    },
                ],
                "scales": [
                    {
                        "name": "xscale",
                        "type": "band",
                        "domain": {"data": "table", "field": "category"},
                        "range": "width",
                        "padding": 0.05,
                        "round": True,
                    },
                    {
                        "name": "yscale",
                        "domain": {"data": "table", "field": "amount"},
                        "nice": True,
                        "range": "height",
                    },
                ],
                "marks": [
                    {
                        "type": "rect",
                        "from": {"data": "table"},
                        "encode": {
                            "enter": {
                                "x": {"scale": "xscale", "field": "category"},
                                "width": {"scale": "xscale", "band": 1},
                                "y": {"scale": "yscale", "field": "amount"},
                                "y2": {"scale": "yscale", "value": 0},
                            },
                            "update": {
                                "fill": {"value": "steelblue"},
                            },
                            "hover": {
                                "fill": {"value": "red"},
                            },
                        },
                    },
                    {
                        "type": "text",
                        "encode": {
                            "enter": {
                                "align": {"value": "center"},
                                "baseline": {"value": "bottom"},
                                "fill": {"value": "#333"},
                            },
                            "update": {
                                "x": {
                                    "scale": "xscale",
                                    "signal": "tooltip.category",
                                    "band": 0.5,
                                },
                                "y": {
                                    "scale": "yscale",
                                    "signal": "tooltip.amount",
                                    "offset": -2,
                                },
                                "text": {"signal": "tooltip.amount"},
                                "fillOpacity": [
                                    {"test": "isNaN(tooltip.amount)", "value": 0},
                                    {"value": 1},
                                ],
                            },
                        },
                    },
                ],
            }
        )
        return vega_spec


class LineChartOntology(Ontology):
    def define(self):
        vega_spec = self.get_common_vega_spec()
        vega_spec.update(
            {
                "data": [
                    {
                        "name": "table",
                        "values": [
                            {"x": 0, "y": 28, "c": 0},
                            {"x": 0, "y": 20, "c": 1},
                            {"x": 1, "y": 43, "c": 0},
                            {"x": 1, "y": 35, "c": 1},
                            {"x": 2, "y": 81, "c": 0},
                            {"x": 2, "y": 10, "c": 1},
                            {"x": 3, "y": 19, "c": 0},
                            {"x": 3, "y": 15, "c": 1},
                            {"x": 4, "y": 52, "c": 0},
                            {"x": 4, "y": 48, "c": 1},
                            {"x": 5, "y": 24, "c": 0},
                            {"x": 5, "y": 28, "c": 1},
                            {"x": 6, "y": 87, "c": 0},
                            {"x": 6, "y": 66, "c": 1},
                            {"x": 7, "y": 17, "c": 0},
                            {"x": 7, "y": 27, "c": 1},
                            {"x": 8, "y": 68, "c": 0},
                            {"x": 8, "y": 16, "c": 1},
                            {"x": 9, "y": 49, "c": 0},
                            {"x": 9, "y": 25, "c": 1},
                        ],
                    }
                ],
                "scales": [
                    {
                        "name": "x",
                        "type": "point",
                        "range": "width",
                        "domain": {"data": "table", "field": "x"},
                    },
                    {
                        "name": "y",
                        "type": "linear",
                        "range": "height",
                        "nice": True,
                        "zero": True,
                        "domain": {"data": "table", "field": "y"},
                    },
                    {
                        "name": "color",
                        "type": "ordinal",
                        "range": "category",
                        "domain": {"data": "table", "field": "c"},
                    },
                ],
                "signals": [
                    {
                        "name": "interpolate",
                        "value": "linear",
                        "bind": {
                            "input": "select",
                            "options": [
                                "basis",
                                "cardinal",
                                "catmull-rom",
                                "linear",
                                "monotone",
                                "natural",
                                "step",
                                "step-after",
                                "step-before",
                            ],
                        },
                    },
                ],
                "axes": [
                    {"orient": "bottom", "scale": "x"},
                    {"orient": "left", "scale": "y"},
                ],
                "marks": [
                    {
                        "type": "group",
                        "from": {
                            "facet": {"name": "series", "data": "table", "groupby": "c"}
                        },
                        "marks": [
                            {
                                "type": "line",
                                "from": {"data": "series"},
                                "encode": {
                                    "enter": {
                                        "x": {"scale": "x", "field": "x"},
                                        "y": {"scale": "y", "field": "y"},
                                        "stroke": {"scale": "color", "field": "c"},
                                        "strokeWidth": {"value": 2},
                                    },
                                    "update": {
                                        "interpolate": {"signal": "interpolate"},
                                        "strokeOpacity": {"value": 1},
                                    },
                                    "hover": {"strokeOpacity": {"value": 0.5}},
                                },
                            }
                        ],
                    }
                ],
            }
        )
        return vega_spec

    def get_attributes(self):
        return {
            "x_axis": "Time",
            "y_axis": "Values",
            "color": "Category",
            "line_style": ["solid", "dashed", "dotted"],
        }


class PieChartOntology(Ontology):
    def define(self):
        return "PieChart Ontology Defined"

    def get_attributes(self):
        return {"slices": "Category", "values": "Values", "color": "Category"}
