tweeter-seeker
==============

Creating databases of Tweets and Twitter users for all of your Twitter analysis needs.

Provide tweeter-seeker with one or more valid Twitter queries and a MongoDB server, and it will provide you with a pseudo-graph database of Tweets about those topics (as complete as Twitter's rate limiting will allow) and the authors who wrote them, complete with all the data you need for whatever analysis you have in mind.

## Installation

To install, run `./setup`

Alternately, just install [PyMongo](http://api.mongodb.org/python/current/) and [Twython](http://twython.readthedocs.org/en/latest/) in whatever way you prefer.

## FAQ

###### Q: Why MongoDB?
A: Two reasons: 1) It's easy, and 2) It's easy. I wanted this project off the ground as quickly as possible and as easy to use as possible, so while a graph database like Neo4j would be more appropriate, it takes more setup and effort to get working. That and I avoid touching Java whenever possible. However, the code is structured such that setting up a new database should be fairly easy to do - it's possible the switch will be made in the future.

###### Q: Why do I have to run so many things just to make this work?
A: Distribution and flexibility. The general idea is that each of the worker programs could be run from different places, at different times, doing different things, all contributing to one central database, allowing flexibility in gathering and analysis of the data. It also means that if you don't care about, say, who follows who - only Tweets - it's easy to not end up with that data... but still easy to change your mind later by running that worker to backfill what you *do* have.

###### Q: Does this violate Twitter's terms of service?
A: I've read them pretty closely, and - as long as you only authenticate with one application token - I'm fairly certain it does not. That said, I'm not a lawyer. If you work for Twitter or otherwise think this violates their ToS, [let me know](mailto:dakota.w.nelson@gmail.com).
