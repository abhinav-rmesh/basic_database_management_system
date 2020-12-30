import queryparser.grant as grant

def execute(query,user):
    try:
        grant.parse(query,user)
        return None
    except Exception as e:
        print(e)
        return None