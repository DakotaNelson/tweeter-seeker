import datetime

# note: these are functions and not classes, because they shouldn't need any member functions - just put data in, get a valid dict out. Classes are overkill (for now).

def User(username, userObject=None):
    return {'_id': username, 'user': userObject, 'added': datetime.datetime.utcnow()}

def Query(query, added=datetime.datetime.utcnow()):
    return {'query': query, 'added': added, 'last_used': datetime.datetime.utcnow()}

def Tweet(tweet, userid, queryid, added=datetime.datetime.utcnow()):
    return {'_id': tweet.id, 'tweet':tweet, 'added':added}
