

import discord
import datetime
import random
from discord.ext import commands

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
        duration_time = datetime.datetime.now() - pretime_dict[member.name]
        str_td = timedelta_to_HM(duration_time)
        #duration_time_adjust = int(duration_time.total_seconds()) * -1

        reply_channel = [
            channel for channel in before.channel.guild.channels if channel.name == reply_channel_name][0]
        #reply_text = member.name + "　が　"+ before.channel.name + "　から抜けました。　通話時間：" + str(duration_time_adjust) +"秒"

        text = [
            "%sは%sの間 氷漬けにされていました.",
            "%sは%s間ずっと狂ったようにモンスターを狩り続けていました.",
            "%sは%sの時間を有意義に過ごしました.",
            "%sは%s間の記憶がないようです.",
            "%sは%s前まで元気でした.",
            "%sによると %s間を返してください.とのこと.",
            "%sは右クリックを夢中で押していただけなのに%sが経過していました.",
        ]

        reply_text = random.choice(text) % (member.name, str_td)

        embed = discord.Embed(color=0x30DADD)
        embed.set_author(name=member.name, icon_url=member.avatar_url_as(size=32))
        embed.add_field(
            name=reply_text,
            #value="connected : " + str(duration_time_adjust) +" second."
            value=before.channel.name + "　|　" + before.channel.category.name
        )

        await reply_channel.send(embed=embed)


@client.event
async def on_message(message):
    # 「おはよう」で始まるか調べる
    if message.content.startswith("ども"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージを書きます
            m = "どもです" + message.author.name + "さん！"
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await message.channel.send(m)
    if message.content == "リサさん、いまどれぐらい？":
        if 'message.author.name' in pretime_dict:
            duration_time = datetime.datetime.now() - pretime_dict[message.author.name]
            await message.channel.send(duration_time)
        await message.channel.send("わかりません.")


def timedelta_to_HM(td):
    sec = td.total_seconds()
    hour = sec // 3600
    minute = sec%3600 // 60
    a = ""
    b = str(int(minute)) + "分"
    if hour > 0:
        a = str(int(hour)) + "時間"
    return (a+b)


client.run("NjA2ODkzODc4MDA3ODI0NDIx.XUc67w.99WZO8T81KgBzUOKbgRi4Q9QZUk")
