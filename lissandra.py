

import discord
import datetime
import random
from discord.ext import commands
from discord.utils import find

bot = commands.Bot(command_prefix='$')

client = discord.Client()
pretime_dict = {}

reply_channel_name = "lissandra"


@commands.command()
async def test(ctx, arg):
    await ctx.send(arg)

bot.add_command(test)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


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

        text = [
            "%sは%sの間 氷漬けにされていました.",
            "%sは%s間ずっと狂ったようにモンスターを狩り続けていました.",
            "%sは%sの時間を有意義に過ごしました.",
            "%sは%s間の記憶がないようです.",
            "%sは%s前まで元気でした.",
            "%sは右クリックを夢中で押していただけなのに%sが経過していました.",
            "%sは睡眠時間を%s失いました.",
            "%sは%s なにも食べていません.",
            "%sが静かになるまで%sかかりました.",
            "%sは%sも勉強してえらい.",
            "%sが%sずっと部屋から出てきません.",
            
        ]

        reply_text = random.choice(text) % (member.name, str_td)

        embed = discord.Embed(color=0x30DADD)
        embed.set_author(name=member.name, icon_url=member.avatar_url_as(size=32))
        embed.add_field(
            name=reply_text,
            value=before.channel.name + "　|　" + before.channel.category.name, 
            inline=False
        )


        if duration_time >= datetime.timedelta(0, 60):
            await reply_channel.send(embed=embed)


@client.event
async def on_message(message):
    #help
    if message.content.startswith("liss.help"):
        embed = discord.Embed(color=0x30DADD)
        embed.add_field(name="liss.help", value="コマンドリスト")
        embed.add_field(name="liss.time", value="経過時間")
        embed.add_field(name="ども", value="あいさつ")
        await message.channel.send(embed=embed)
    #あいさつ
    if message.content.startswith("ども"):
        if client.user != message.author:
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


client.run("token")
