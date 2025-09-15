# takkari_bot/cogs/patchnote_auto.py
import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio

PATCHNOTE_CHANNEL_ID = 1417051773318991913  # 업데이트-로그 채널
GITHUB_REPO = "sentimentaleunjun/DiscordBot"  # 깃허브 리포지토리
GITHUB_API_URL = f"https://api.github.com/sentimentaleunjun/DiscordBot/commits"
GITHUB_TOKEN = "ghp_YourTokenHere"  # 필요하면 개인 토큰

class PatchnoteAuto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_commit_sha = None
        self.check_commits.start()

    @tasks.loop(minutes=5)
    async def check_commits(self):
        headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
        async with aiohttp.ClientSession() as session:
            async with session.get(GITHUB_API_URL, headers=headers) as resp:
                if resp.status != 200:
                    return
                data = await resp.json()
                latest_commit = data[0]
                sha = latest_commit['sha']
                if sha == self.last_commit_sha:
                    return
                self.last_commit_sha = sha

                embed = discord.Embed(
                    title="🆕 새 패치노트!",
                    description=latest_commit['commit']['message'],
                    color=0x00ff00,
                    url=latest_commit['html_url']
                )
                embed.set_author(name=latest_commit['commit']['author']['name'])
                embed.set_footer(text="패치노트 자동 업데이트")

                channel = self.bot.get_channel(PATCHNOTE_CHANNEL_ID)
                if channel:
                    await channel.send(embed=embed)

    @check_commits.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(PatchnoteAuto(bot))