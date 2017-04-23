"""
This script will pull all players from MongoDB, partition them into pitcher
and hitter pools, sort those pools by player ability, and then have teams draft
the players. 
"""

from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.tweetball
playerColl = db.players
teamColl = db.teams

# First, build an aggregation pipeline for pulling the players from mongoDB

# These lists will be summed in the query for overall ability in batting and pitching
batOverall = ['$ratings.contact', '$ratings.power', '$ratings.discipline']
pitOverall = ['$ratings.stuff', '$ratings.control', '$ratings.composure']

# overallDiff subtracts pitOverall from batOverall to get a list sorted by 
# how much better players are at batting than pitching. This will be good
# for partitioning the player pool into batters and pitchers 

overallDiff = { '$subtract' : [ { '$add' : batOverall }, { '$add' : pitOverall } ] }

# aggPipeline uses overallDiff to make a query projecting player IDs and overall
# batting/pitching differences 

aggPipeline = [{'$project' : { '_id' : 1, 'ratings' : 1, 'overallDiff' : overallDiff }}]

# Finally, make a list of all the player documents returned 

allPlayersPool = list(playerColl.aggregate(aggPipeline))

# Sort the list by overallDiff descending

allPlayersPool.sort(key = lambda x: x['overallDiff'], reverse = True)

# Tweetball will be 34 teams with 25 man rosters. For simplicity, each team
# will carry 12 pitchers and 13 batters. So we need 408 pitchers and 
# 442 batters out of a total 850 players. Hitters are pulled from the front
# of the sorted pool, pitchers from the back

pitcherPool = []
batterPool = []

for i in range(0,442):
	
	batterPool.append(allPlayersPool.pop(0))
	
for i in range(0,408):

	pitcherPool.append(allPlayersPool.pop())

# Sort the pools. The best players will be at the end of the list, which
# is fine since we'll use pop() to draft

batKey = lambda x : x['ratings']['contact'] + x['ratings']['power'] + x['ratings']['discipline']
pitchKey = lambda x : x['ratings']['stuff'] + x['ratings']['control'] + x['ratings']['composure']

batterPool.sort(key = batKey)
pitcherPool.sort(key = pitchKey)


