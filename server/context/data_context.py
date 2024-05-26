class DataContext:
    def __init__(self, objective, dataType, patterns, comparisons, colorPreferences, usage):
        self.objective = objective
        self.dataType = dataType
        self.patterns = patterns
        self.comparisons = comparisons
        self.colorPreferences = colorPreferences
        self.usage = usage

    def to_dict(self):
        return {
            "objective": self.objective,
            "dataType": self.dataType,
            "patterns": self.patterns,
            "comparisons": self.comparisons,
            "colorPreferences": self.colorPreferences,
            "usage": self.usage
        }
