import os
import urllib.request as urllib2
import json

def getAccountID(sumname):
    SUMMONER_V4 = "https://jp1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    rak = os.environ.get('RIOT_API_KEY')
    try:
        s1 = urllib2.urlopen(SUMMONER_V4 + str(sumname) + '?api_key=' + rak)
        summ = json.loads(s1.read().decode('utf-8'))
        ACCOUNT_ID = summ["accountId"]
    finally:
        s1.close()
        return ACCOUNT_ID

def getWards(summonerName, accountId):

    MATCHLISTS_V4 = "https://jp1.api.riotgames.com/lol/match/v4/matchlists/by-account/"
    rak = os.environ.get('RIOT_API_KEY')
    try:
        s1 = urllib2.urlopen(MATCHLISTS_V4 + accountId + "?endIndex=1&api_key=" + rak)
        json_matchlists = json.loads(s1.read().decode('utf-8'))
        lastmatchId = json_matchlists['matches'][0]['gameId']
    finally:
        s1.close()

    MATCH_V4 = "https://jp1.api.riotgames.com/lol/match/v4/matches/"
    rak = os.environ.get('RIOT_API_KEY')
    try:
        s1 = urllib2.urlopen(MATCH_V4 + str(lastmatchId) + "?api_key=" + rak)
        json_match = json.loads(s1.read().decode('utf-8'))

        for par in json_match['participantIdentities']:
            if par['player']['summonerName'] == summonerName:
                pId = par['participantId']
                break

        ward = json_match['participants'][pId-1]['stats']['visionWardsBoughtInGame']
        print(ward)
    finally:
        s1.close()
        return ward

#aId = getAccountID("39cm")
#getWards(summonerName = "39cm", accountId=aId)