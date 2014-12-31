#!/usr/bin/env python

from db_tseeker import dbclient
from schema_tseeker import User, Query
import argparse

# set up for parsing command line arguments
parser = argparse.ArgumentParser(description='Add items to the tweeter-seeker database for workers to fill out.')

parser.add_argument('type', choices=['user','query'], help="The type of item(s) to be added.")
# TODO: add geo objects (i.e. all tweets within x km of a place)
parser.add_argument('items', help="A single item or list of items; queries or users as specified in the earlier arguments.")
parser.add_argument('-v', '--verbose', action="store_true", help="Increase output verbosity.")
parser.add_argument('--dbhost', default="localhost", help="Specify database address. Defaults to localhost.")
parser.add_argument('--dbport', type=int, default=27017, help="Specify database port. Defaults to 27017.")

# now do the actual parsing
args = parser.parse_args()

# connect the db
db = dbclient(args.dbhost, args.dbport)
if not db:
    print("Unable to connect to database at " + args.dbhost + ":" + args.dbport)
    sys.exit(0)

def addUsers(users):
    # recieves array of Twitter user handles (may not be valid)
    toInsert = []
    rejected = []
    for user in users:
        # check if exists
        # TODO this is very slow, but will do for now
        exists = db.findOne('users', {"username":user}, {"username":1})
        if exists == None:
            toInsert.append(User(user)) # turn the username into a valid object for insertion, and queue it up
        else:
            print("User " + user + " is not unique.")
            rejected.append(user)
    # bulk insert whatever is unique
    db.insert('users', toInsert)
    return rejected # in case we want to print a failure message

def addQueries(queries):
    # recieves array of Twitter queries (may not be valid)
    toInsert = []
    rejected = []
    for query in queries:
        # check if exists
        # TODO this is very slow, but will do for now
        exists = db.findOne('queries', {"query":query}, {"query":1})
        if exists == None:
            toInsert.append(Query(query)) # turn the username into a valid object for insertion, and queue it up
        else:
            print("Query " + query + " is not unique.")
            rejected.append(query)
    # bulk insert whatever is unique
    db.insert('queries', toInsert)
    return rejected # in case we want to print a failure message

# items comes in as a comma separated list, may have leading/trailing spaces
items = [x.strip() for x in args.items.split(",")]

if args.type == 'user':
    addUsers(items)
elif args.type == 'query':
    addQueries(items)
else:
    # the arg parser should catch this, but just in case
    print("Unrecognized item type: " + args.items)
    sys.exit(0)

