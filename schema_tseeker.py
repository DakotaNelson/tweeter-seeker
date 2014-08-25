import datetime

# note: these are functions and not classes, because they shouldn't need any member functions - just put data in, get a valid dict out. Classes are overkill (for now).

def User(username, userObject=None):
    return {'username': username, 'data': userObject, 'modified': datetime.datetime.utcnow()}

def Query(query):
    return {'query': query, 'added': datetime.datetime.utcnow()}
