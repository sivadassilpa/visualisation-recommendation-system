from typing import List, Tuple, Optional, Any, Dict


def responseParser(
    columnNames: List[Tuple[str]], columnValues: Optional[List[Any]]
) -> Optional[Dict[str, Any]]:
    if not columnValues:
        return None

    # Extract column names from the description tuples
    column_names = [desc[0] for desc in columnNames]

    # Create a dictionary using zip for better readability
    result = dict(zip(column_names, columnValues))

    return result
