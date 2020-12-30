import queryparser.revoke as revoke

def execute(query,user):
    try:
        revoke.parse(query,user)
        return None
    except Exception as e:
        print(e)
        return None