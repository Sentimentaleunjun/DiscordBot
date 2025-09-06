import discord
from discord.ext import commands, tasks
from datetime import datetime

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.schedules = []
        self.check_schedules.start()

    @commands.command(name="schedule")
    async def schedule(self, ctx, time: str, *, content: str):
        if ctx.author.id != self.bot.admin_id:
            await ctx.send("??愿由ъ옄留?媛?ν빀?덈떎.")
            return

        try:
            when = datetime.strptime(time, "%Y-%m-%d %H:%M")
        except ValueError:
            await ctx.send("?좑툘 ?쒓컙 ?뺤떇? YYYY-MM-DD HH:MM")
            return

        self.schedules.append((when, content, ctx.channel.id))
        await ctx.send(f"???덉빟?? {when} ??{content}")

    @tasks.loop(seconds=30)
    async def check_schedules(self):
        now = datetime.now()
        for sched in self.schedules[:]:
            when, content, channel_id = sched
            if now >= when:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    await channel.send(f"???덉빟 怨듭?: {content}")
                self.schedules.remove(sched)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
