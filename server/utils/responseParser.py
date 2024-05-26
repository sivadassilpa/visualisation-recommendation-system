def responseParser(columnNames, columnValues):
    if(columnValues):
        column_names = [desc[0] for desc in columnNames]
        result = {column_names[i]: columnValues[i] for i in range(len(column_names))}
    else:
        result = None
    
    return result