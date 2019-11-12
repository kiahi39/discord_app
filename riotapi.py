import os
import urllib.request as urllib2
import urllib.parse
import json
from datetime import datetime

def getSummoner(sumname):
    SUMMONER_V4 = "https://jp1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    rak = os.environ.get('RIOT_API_KEY')
    s1 = "null"
    try:
        str1 = urllib.parse.quote(sumname)
        s1 = urllib2.urlopen(SUMMONER_V4 + str1 + '?api_key=' + rak)
        summ = json.loads(s1.read().decode('utf-8'))
    finally:
        s1.close()
        if s1 != "null":
            return summ
        else:
            return "null"

def getAccountID(sumname):
    summ = getSummoner(sumname)
    ACCOUNT_ID = summ["accountId"]
    return ACCOUNT_ID

def getSummLevel(sumname):
    summ = getSummoner(sumname)
    sl = summ["summonerLevel"]
    return sl

def getLastMatch(accountId):

    MATCHLISTS_V4 = "https://jp1.api.riotgames.com/lol/match/v4/matchlists/by-account/"
    rak = os.environ.get('RIOT_API_KEY')
    try:
        #クエリendIndex=1で1試合取得。最大100試合(endIndex=100)
        s1 = urllib2.urlopen(MATCHLISTS_V4 + accountId + "?endIndex=1&api_key=" + rak)
        json_matchlists = json.loads(s1.read().decode('utf-8'))
        lastmatch = json_matchlists['matches'][0]
        lastmatchId = lastmatch['gameId']
        #timestamp = (lastmatch['timestamp'])
        #lastmatchDate = datetime.fromtimestamp(timestamp)
        #print(lastmatchDate)
    finally:
        s1.close()
        return lastmatchId

def getParticipant(summoner_name, matchId):

    MATCH_V4 = "https://jp1.api.riotgames.com/lol/match/v4/matches/"
    rak = os.environ.get('RIOT_API_KEY')
    try:
        s1 = urllib2.urlopen(MATCH_V4 + str(matchId) + "?api_key=" + rak)
        json_match = json.loads(s1.read().decode('utf-8'))

        for par in json_match['participantIdentities']:
            if par['player']['summonerName'] == summoner_name:
                pId = par['participantId']
                break

        stats = json_match['participants'][pId-1]
        print(stats['visionWardsBoughtInGame'])
    finally:
        s1.close()
        return stats

def getChampionName(championId):
    URL = "https://ddragon.leagueoflegends.com/cdn/9.15.1/data/ja_JP/champion.json"
    try:
        s1 = urllib2.urlopen(URL)
        json_file = json.loads(s1.read().decode('utf-8'))
        cName = "NotFound."
        for champData in json_file['data'].values():
            if champData['key'] == str(championId):
                cName = champData['id']
    finally:
        s1.close()
        return cName

def getSquareChampion(championId):
    cName = getChampionName(championId)
    URL="http://ddragon.leagueoflegends.com/cdn/9.15.1/img/champion/{0}.png".format(cName)
    return URL


#aId = getAccountID("39cm")
#getLastMatchParticipant(summonerName = "39cm", accountId=aId)
#print(getSquareChampion(championId=1))