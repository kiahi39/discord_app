import urllib.request as urllib2

s = "test."
try:
    s = urllib2.urlopen("https://jp1.api.riotgames.com/lol/summoner/v4/summoners/by-name/sdadwawdaada")
finally:
    print(s)