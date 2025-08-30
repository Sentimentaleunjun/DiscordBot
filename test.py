import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("내가 돌아왔다 이것들아")

@client.event
async def on_message(message):
    if message.content == "안녕":
        await message.channel.send("안녕하세요")
@client.event
async def on_message(message):
    if message.content == "안녕하세요!":
        await message.channel.send("응 아니야")
@client.event
async def on_message(message):
    if message.content == "싸우지마":
        await message.channel.send("시른뒈")
@client.event
async def on_message(message):
    if message.content == "돈좀있니?":
        await message.channel.send("없어")
@client.event
async def on_message(message):
    if message.content == "안녕하세요"or "안녕하세요!":
        await message.channel.send("안물어봤어요^^")
@client.event
async def on_message(message):
    if message.content == "ㅗ":
        await message.channel.send("가다한욕설사용을 멈추세요")
@client.event
async def on_message(message):
    if message.content == "시1발":
        await message.channel.send("욕하지마임마")
@client.event
async def on_message(message):
    if message.content == "니얼굴":
        await message.channel.send("똥")
@client.event
async def on_message(message):
    if message.content == ("바보"):
        await message.channel.send("너")
@client.event
async def on_message(message):
    if message.content == "원주율":
        await message.channel.send("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989")
@client.event
async def on_message(message):
    if message.content == "그만해":
        await message.channel.send("시른데 니뭐돼 걍짜져")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.guild:
        return

    if len(message.content) >= 5:
        member = message.author
        try:
            await member.kick(reason="없음^^")
            await message.channel.send(f"👢 {member.mention} 킥됨 (5글자 이상)")
        except Exception as e:
            await message.channel.send(f"⚠️ 킥 실패: {e}")

    await client.process_commands(message)
    client.run("MTQxMTI1NTk4MjU5MTQ0Mjk2NA.Gx4dcs.jBA53oOMrfcCbu7HEEVkfpaGp3O6iRlJk4jbFM")


