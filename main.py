import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("봇이 로그인 되었습니다.")

@client.event
async def on_message(message):
    if message.content == "안녕":
        await message.channel.send("안녕하세요!")
        if message.content == "안녕":
            await message.channel.send("안녕하세요!")
            if message.content == "안녕":
                await message.channel.send("안녕하세요!")
                if message.content == "안녕":
                    await message.channel.send("안녕하세요!")


client.run("MTQwODcyNDU4OTc3NjczNjM1Nw.GwjTpK.H91Fib_F04U3Sdi4ZZyB0o6wkxocJ0ebNn0dKg")