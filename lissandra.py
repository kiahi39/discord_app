import discord
import datetime
import random
from discord.ext import commands
from discord.utils import find

import os
import psycopg2
import hashlib

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

client = commands.Bot(command_prefix='$')

#client = discord.Client()
pretime_dict = {}

reply_channel_name = "lissandra"

text = []


@commands.command()
async def test(ctx, arg):
    await ctx.send(arg)

client.add_command(test)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT content FROM LissText')
            for row in cur:
                print(row)
                text.append(row[0])


@client.event
async def on_voice_state_update(member, before, after):

    if(before.channel is None):
        pretime_dict[member.name] = datetime.datetime.now()
    elif(after.channel is None):
        duration_time = cal_timedelta(pretime_dict[member.name])
        pretime_dict.pop(member.name)
        str_td = timedelta_to_HM(duration_time)
        

        reply_channel = [
            channel for channel in before.channel.guild.channels if channel.name == reply_channel_name][0]

        '''
        text = [
            "{0}は{1}の間 氷漬けにされていました.",
            "{0}は{1}間ずっと狂ったようにモンスターを狩り続けていました.",
            "{0}は{1}の時間を有意義に過ごしました.",
            "{0}は{1}間の記憶がないようです.",
            "{0}は{1}前まで元気でした.",
            "{0}は右クリックを夢中で押していただけなのに{1}が経過していました.",
            "{0}は睡眠時間を{1}失いました.",
            "{0}は{1} なにも食べていません.",
            "{0}が静かになるまで{1}かかりました.",
            "{0}は{1}も勉強してえらい.",
            "{0}が{1}ずっと部屋から出てきません.",
            
        ]
        '''

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
        embed.add_field(name="例「liss.addtext {0}が{1}通話.」", value="テキストを追加.")
        embed.add_field(name="liss.textlist", value="テキストのリスト")
        embed.add_field(name="liss.deltext", value="テキストの削除（IDを指定）")
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
            with get_connection() as conn:
                with conn.cursor() as cur:
                    id0 = hash4(datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S'))
                    cur.execute('INSERT INTO LissText (id, content) VALUES (%s, %s)', (id0, m))
                    text.append(m)
                conn.commit()
            await message.channel.send("テキストを追加.id: "+ id0 +"「"+ m +"」")
        else:
            await message.channel.send("{0}と{1}が含まれていません.")

    #liss.textlist
    if message.content.startswith("liss.textlist"):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM LissText')
                for row in cur:
                    await message.channel.send(row)
    #liss.deltext
    if message.content.startswith("liss.deltext "):
        m = message.content
        m = m.replace("liss.deltext ", "")
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT content FROM LissText WHERE id = %s;', (m, ))
                for row in cur:
                    text.remove(row[0])
                cur.execute('DELETE FROM LissText WHERE id = %s;', (m, )) 
        await message.channel.send("削除 ID:"+m)
    await client.process_commands(message)


def cal_timedelta(pretime):
    return datetime.datetime.now() - pretime

def timedelta_to_HM(td, contain_seconds=False):
    sec = td.total_seconds()
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


client.run("token")
