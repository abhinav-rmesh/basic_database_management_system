def parse(query):
    query = query.upper()
    query = query.replace(";","")

    parts = query.split(" ")

    if len(parts)!=2:
        raise Exception("Invalid 'Use' query structure")

    return parts[1]