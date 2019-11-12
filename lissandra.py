import discord
import datetime
import random
from discord.ext import commands
from discord.utils import find

import os
import psycopg2
import hashlib

import urllib.request as urllib2
import json

#import jaconv

import riotapi
import database as db

client = commands.Bot(command_prefix='liss.')
#client = discord.Client()
pretime_dict = {}
reply_channel_name = "lissandra"
text = []
logintime_dict = {}
PATCH = "9.15"

#login
@client.command()
async def login(ctx, *_sname):
    map_result = map(str, _sname)
    sname = ' '.join(map_result)
    summoner = riotapi.getSummoner(sname)
    userName = ctx.message.author.name

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT summoner_name FROM LissWard WHERE discord_id = %s;', (str(ctx.message.author.id), ))
            sn = "null"
            for summoner_name in cur:
                sn = summoner_name[0]
            if sn != summoner["name"]:
                cur.execute('DELETE FROM LissWard WHERE discord_id = %s;', (str(ctx.message.author.id), ))
                cur.execute('INSERT INTO LissWard (discord_id, summoner_name) VALUES (%s, %s)', (ctx.message.author.id, summoner['name']))
                loginText = "登録しました."
            else:
                loginText = "ログイン済みです."
        conn.commit()
    embed = discord.Embed(color=0x30DADD)
    embed.set_author(name=userName, icon_url=ctx.message.author.avatar_url_as(size=32))
    embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/{0}.1/img/profileicon/{1}.png".format(PATCH, summoner['profileIconId']))
    embed.add_field(
        name="サモナーネーム："+summoner['name']+"　"+ loginText,
        value="サモナーレベル："+ str(summoner['summonerLevel']),
    )
    await ctx.send(embed=embed)
        
#getwards
@client.command()
async def ward(ctx):
    discordId = str(ctx.message.author.id)
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT summoner_name FROM LissWard WHERE discord_id=%s;', (str(discordId), ))
            for sn in cur:
                sname = sn[0]
            aId = riotapi.getAccountID(sname)
            if(aId == "null"):
                await ctx.send("RiotAPIキーの有効期限が切れています。更新して！@39cmさん！")
            lastMatchId = riotapi.getLastMatch(accountId = aId)
            par = riotapi.getParticipant(summoner_name=sname, matchId=lastMatchId)
            wards = par['stats']['visionWardsBoughtInGame']
            #wards = jaconv.h2z(str(wards),digit=True)
            k = str(par['stats']['kills'])
            d = str(par['stats']['deaths'])
            a = str(par['stats']['assists'])
            wintext = ""
            doubletext = ""
            if par['stats']['win']:
                wintext = "勝ったのですね！"
                double = 2
                doubletext = "２倍の"
            else:
                double = 1
                wintext = "負けたのですね."
            cur.execute('SELECT last_match_id FROM LissWard WHERE discord_id=%s;', (str(discordId), ))
            for last_match_id in cur:
                if(last_match_id[0] != str(lastMatchId)):
                    cur.execute('UPDATE LissWard Set last_match_id=%s WHERE discord_id=%s;', (str(lastMatchId), str(discordId)))
                    cur.execute('UPDATE LissWard Set wards = wards+%s WHERE discord_id=%s;', (int(wards)*double, str(discordId)))
                    wardText = "コントロールワードを"+doubletext+" "+ str(wards*double) +"個 受領しました ."
                else:
                    wardText = "コントロールワードを"+doubletext+" "+ str(wards*double) +"個 既に受領済みです ."
                cur.execute('SELECT wards FROM LissWard WHERE discord_id=%s;', (str(discordId), ))
                for w in cur:
                    totalWard = w
        conn.commit()
    embed = discord.Embed(color=0x30DADD)
    embed.set_author(name=sname +"　KDA："+k+"/"+d+"/"+a, icon_url=riotapi.getSquareChampion(par['championId']))
    embed.add_field(
        name=wintext +"　/　"+ wardText,
        value="累計 ： %s 個" % totalWard
    )
    await ctx.send(embed=embed)

#sumlevel
@client.command()
async def level(ctx, name):
    sl = riotapi.getSummLevel(name)
    await ctx.send(str(name)+"のサモナーレベルは,"+str(sl)+"です.")

#a369852 
@client.command()
async def a369852(ctx, name, time):
    pretime_dict[str(name)] = datetime.datetime.now() - datetime.timedelta(seconds = int(time))
    await ctx.send("はーい.")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT content FROM LissText')
            for row in cur:
                text.append(row[0])

#通話時間計測 : 通話開始時間を保持しておく仕組み
@client.event
async def on_voice_state_update(member, before, after):
    if(before.channel is None):
        pretime_dict[member.name] = datetime.datetime.now()
        #db.insert('INSERT INTO LissText (id, content) VALUES (%s, %s)', (member.id))
    elif(after.channel is None):
        duration_time = cal_timedelta(pretime_dict[member.name])
        pretime_dict.pop(member.name)
        str_td = timedelta_to_HM(duration_time)
        
        reply_channel = [channel for channel in before.channel.guild.channels if channel.name == reply_channel_name][0]
        reply_text = random.choice(text).format(member.name, str_td)
        embed = discord.Embed(color=0x30DADD)
        embed.set_author(name=member.name, icon_url=member.avatar_url_as(size=32))
        embed.add_field(
            name=reply_text,
            value=before.channel.name + "　|　" + before.channel.category.name, 
            inline=False
        )
        #if duration_time >= datetime.timedelta(0, 60):
        await reply_channel.send(embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #help
    if message.content.startswith("liss.help"):
        embed = discord.Embed(color=0x30DADD)
        embed.add_field(name="liss.help", value="コマンドリスト")
        embed.add_field(name="liss.time", value="経過時間")
        embed.add_field(name="ども", value="あいさつ")
        embed.add_field(name="liss.code", value="ソースコード")
        embed.add_field(name="liss.addtext (文章)", value="テキストを追加")
        embed.add_field(name="liss.textlist", value="テキストのリスト")
        embed.add_field(name="liss.deltext", value="テキストの削除（IDを指定）")
        embed.add_field(name="liss.login (サモナーネーム)", value="サモナーネームを登録")
        embed.add_field(name="liss.ward", value="リサンドラにワードをあげる")
        await message.channel.send(embed=embed)
    #あいさつ
    if message.content.startswith("ども"):
        m = "ハロー、" + message.author.name + "！"
        await message.channel.send(m)
    #経過時間 liss.time
    if message.content == "liss.time":
        if message.author.name in pretime_dict:
            duration_time = cal_timedelta(pretime_dict[message.author.name])
            str_td = timedelta_to_HM(duration_time, contain_seconds=True)
            
            reply_text = "： "+ str_td +" 経過."
        else:
            reply_text = "は通話中ではありません."
        embed = discord.Embed(color=0x30DADD)
        embed.set_author(
            name=message.author.name + reply_text, 
            icon_url=message.author.avatar_url_as(size=64)
        )
        await message.channel.send(embed=embed)
    #liss.code
    if message.content.startswith("liss.code"):
        m = "プログラムリサンドラのプログラムはこちら.\n"
        m += "https://github.com/kiahi39/discord_app/blob/master/lissandra.py"
        await message.channel.send(m)
    #liss.addtext 
    if message.content.startswith("liss.addtext "):
        m = message.content
        m = m.replace("liss.addtext ", "")
        if ("{0}"in m) and ("{1}"in m):
            id0 = hash4(datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S'))
            db.insert('INSERT INTO LissText (id, content) VALUES (%s, %s)', (id0, m))
            text.append(m)
            await message.channel.send("テキストを追加.id: "+ id0 +"「"+ m +"」")
        else:
            await message.channel.send("{0}と{1}が含まれていません.")

    #liss.textlist
    if message.content.startswith("liss.textlist"):
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM LissText')
                for row in cur:
                    await message.channel.send(row)
    #liss.deltext
    if message.content.startswith("liss.deltext "):
        m = message.content
        m = m.replace("liss.deltext ", "")
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT content FROM LissText WHERE id = %s;', (m, ))
                for row in cur:
                    text.remove(row[0])
                cur.execute('DELETE FROM LissText WHERE id = %s;', (m, )) 
        await message.channel.send("削除 ID:"+m)
    await client.process_commands(message)
    
def cal_timedelta(pretime):
    return datetime.datetime.now() - pretime

def timedelta_to_HM(timedelta, contain_seconds=False):
    sec = timedelta.total_seconds()
    hour = sec // 3600
    minute = sec%3600 // 60
    
    a = ""
    b = str(int(minute)) + "分"
    c = ""
    if hour > 0:
        a = str(int(hour)) + "時間"
    if contain_seconds:
        second = sec%3600 % 60
        c = str(int(second)) + "秒"
    return (a+b+c)

def hash4(dat):
    hs = hashlib.md5(dat.encode()).hexdigest()
    hs = hs[:4]
    return hs

client.run("NjA2ODkzODc4MDA3ODI0NDIx.XU4-gw.PkjTqJ-KcrPo_5cBgo1kYfO_WQk")