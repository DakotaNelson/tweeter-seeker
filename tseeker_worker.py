#!/usr/bin/env python

from db_tseeker import dbclient
from schema_tseeker import User, Query, Tweet
import argparse
import signal
import time
import datetime
from twython import Twython
from multiprocessing import Process, Queue

""" subprocess to harvest Tweets based on queries """
def getQueries(poisonPill):
    while poisonPill.empty():
        try:
            # find the query that hasn't been touched the longest
            query = db.findGreatest('queries', 'last_used')[0]
            # TODO findandModify in order to 'lock' a query to avoid two workers duplicating efforet
            db.update('queries', {'_id':query['_id']}, {'$set':{'last_used':datetime.datetime.utcnow()}})
            query = query['query'] # get the actual query string, not the other stuff (age, id, etc.)
            if args.verbose:
                print("Searching for query: " + query)
            results = twitter.search(q=query, count=3)
            for status in results['statuses']:
                # although Twitter wants us to use id instead of screen name (as screen name is unique but *can* change), keying from screen name helps notice changes in screen name as well as allowing us to add 'empty' user objects to be filled by workers
                user = User(status['user']['screen_name'], status['user'])
                status.pop('user', None)
                # if the user doesn't exist, insert it
                #db.insert("users", user
                print(user)
                # then insert the status, with references to the query and user objects
                tweet = Tweet(status, user['_id'], query['_id'])
                db.insert("tweets", tweet)
                print(status)
                # maybe something useful in the metadata?
                print(status['search_metadata']
            time.sleep(2) # so we don't hit the rate limit
            # TODO time how long the process takes and adjust this intelligently
        except IndexError:
            print("No queries in database to harvest Tweets for!")
            time.sleeep(30)
    return

""" subprocess to harvest users"""
def getUsers(poisonPill):
    return

""" subprocess to harvest all of a user's Tweets"""
def getTimelines(poisonPill):
    return

""" kills subprocesses with a poison pill """
def dieGracefully(signal, frame):
    killQueue.put(True)
    return

# set up for parsing command line arguments
parser = argparse.ArgumentParser(description='Start a worker to fill out your tweeter-seeker database. If instructed to harvest Tweets, the worker will find Tweets that match the queries in the database. If instructed to harvest users, the worker will harvest Twitter user objects for the Tweets currently in the database. If instructed to harvest timelines, the worker will harvest all the Tweets of each author in the database.')

#parser.add_argument('type', choices=['tweets','users','timelines'], help="The Twitter entity this worker should harvest.")
parser.add_argument('--tweets', action="store_true", help="Harvest Tweets for the queries in the database.")
parser.add_argument('--users', action="store_true", help="Harvest users for all the Tweets in the database.")
parser.add_argument('--timelines', action="store_true", help="Harvest the Tweets of all the users in the database.")
parser.add_argument('-v', '--verbose', action="store_true", help="Increase output verbosity.")
parser.add_argument('--dbhost', default="localhost", help="Specify database address. Defaults to localhost.")
parser.add_argument('--dbport', type=int, default=27017, help="Specify database port. Defaults to 27017.")
parser.add_argument('apikey', help="Twitter API key.")
parser.add_argument('apisecret', help="Twitter API secret.")

# now do the actual parsing
args = parser.parse_args()

if not (args.tweets or args.users or args.timelines):
    print("Nothing to harvest! Please specify one or more objects to harvest: tweets, users, or timelines.")
    sys.exit(0)

# connect the db
db = dbclient(args.dbhost, args.dbport)
if not db:
    print("Unable to connect to database at " + args.dbhost + ":" + args.dbport)
    sys.exit(0)

# do the OAuth dance
twitter = Twython(args.apikey, args.apisecret, oauth_version=2)
TOKEN = twitter.obtain_access_token()
twitter = Twython(args.apikey, access_token=TOKEN)

### And... begin! ###

processes = []
killQueue = Queue()

signal.signal(signal.SIGINT, dieGracefully)

if args.tweets:
    queryProcess = Process(target=getQueries, args=(killQueue,))
    processes.append(queryProcess)

if args.users:
    userProcess = Process(target=getUsers, args=(killQueue,))
    processes.append(userProcess)

if args.timelines:
    timelineProcess = Process(target=getTimelines, args=(killQueue,))
    processes.append(timelineProcess)

for process in processes:
    process.start()

# keep running until we're killed
signal.pause()
