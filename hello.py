import discord
import datetime
import random

client = discord.Client()
pretime_dict = {}

client = discord.Client()

@client.event
async def on_voice_state_update(member, before, after):
    
    if(before.channel is None):
        pretime_dict[after.channel.name] = datetime.datetime.now()
    elif(after.channel is None):
        duration_time = pretime_dict[before.channel.name] - datetime.datetime.now()
        duration_time_adjust = int(duration_time.total_seconds()) * -1

        reply_channel_name = "lissandra"
        reply_channel = [channel for channel in before.channel.guild.channels if channel.name == reply_channel_name][0]
        #reply_text = member.name + "　が　"+ before.channel.name + "　から抜けました。　通話時間：" + str(duration_time_adjust) +"秒"

        text = [
            "%sは%s秒の間 氷漬けにされていました.",
            "%sは%s秒間ずっと狂ったようにモンスターを狩り続けていました.",
            "%sは%s秒の時間を有意義に過ごしました.", 
            "%sは%s秒間の記憶がないようです.", 
            "%sは%s秒前まで元気でした.",
            "%sによると %s秒間を返してください.とのこと.",
            "%sは右クリックを夢中で押していただけなのに%s秒が経過していました.",
        ]

        reply_text = random.choice(text) % (member.name, duration_time_adjust)

        embed = discord.Embed(color=0x30DADD)
        embed.set_author(name=member.name, icon_url=member.avatar_url_as(size=32))
        embed.add_field(
            name=reply_text, 
            #value="connected : " + str(duration_time_adjust) +" second."
            value=before.channel.name + "　|　" + before.channel.category.name
        )

        await reply_channel.send(embed = embed)

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

client.run("NjA3NDE3NjI0MDE5NzMwNDcz.XUZT4w.htoQtwySz16AI_zrU83Swan_C2A")