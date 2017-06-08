import discord
from discord.ext import commands
from config import Config
import asyncio


description = "A helper bot created by jkings454"

conf = Config()

bot = commands.Bot(command_prefix="j.", description=description)

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
    await bot.say("Hello, {0.mention}!".format(ctx.message.author))

@bot.group(pass_context=True)
async def announce(ctx):
    if not ctx.message.author.permissions_in(ctx.message.channel).administrator:
        await bot.say("Only administrators can use this command!")
        return
    if ctx.invoked_subcommand is None:
        await bot.say('Invalid command passed...')


@announce.command(pass_context=True)
async def set_channel(ctx, channel : discord.Channel):
    if not channel:
        await bot.say("That's not a valid channel!")
        return

    conf.settings[ctx.message.server.id]["enabledChannel"] = channel.id
    conf.save()
    await bot.say("Announcements will now be made in {0.name}".format(channel))

@announce.command(pass_context=True)
async def user_join(ctx, message : str):
    await bot.say("when this is implemented, this will be the message i say: " + message)

@announce.command(pass_context=True)
async def role_add(ctx, role : discord.Role, message : str):
    tmp = {"id": role.id, "message": message}
    if "role_add" not in conf.settings[ctx.message.server.id]["events"]:
        conf.settings[ctx.message.server.id]["events"]["role_add"] = {role.id: message}
        conf.save()
    else:
        conf.settings[ctx.message.server.id]["events"]["role_add"][role.id] = message
        conf.save()

    await bot.say("Whenever a user gains the `{0}` role, I'll say \"{1}\".".format(role.name, message))

bot.run(conf.settings["token"])