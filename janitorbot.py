import discord
from discord.ext import commands
from config import Config
import asyncio


description = "A helper bot created by jkings454"

conf = Config()

bot = commands.Bot(command_prefix="j.", description=description)

startup_extensions = ['announce']

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("---------")

@bot.event
async def on_server_join(server):
    conf.settings[server.id] = {"events":{}}
    conf.save()

@bot.event
async def on_server_remove(server):
    conf.settings[server.id].pop()
    conf.save()

@bot.event
async def on_member_update(before, after):
    if "role_add" in conf.settings[before.server.id]["events"]:
        for role in after.roles:
            if role not in before.roles and role.id in conf.settings[before.server.id]["events"]["role_add"].keys():
                channel = discord.Object(id=conf.settings[before.server.id]["enabledChannel"])
                message = conf.settings[before.server.id]["events"]["role_add"][role.id]
                await bot.send_message(channel, message.format(after))

@bot.command(pass_context=True)
async def test(ctx):
    """Test to see if the bot is working!"""
    await bot.say("Hello, {0.mention}!".format(ctx.message.author))

@bot.command()
async def invite():
    """Get the invite URL for the bot"""
    await bot.say(discord.utils.oauth_url(discord.AppInfo.id))


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
    bot.run(conf.settings["token"])