import discord
from discord.ext import commands


class Announce():

    def __init__(self, bot):
        self.bot = bot

    
    @commands.group(pass_context=True)
    async def announce(ctx):
        """Commands related to announcing when events happen. Run "set_channel" first.
        Messages can be formatted to include the user's information using python3's string formatting syntax,
        For instance, {0.name} will get the user's name, and {0.mention} will get the user's mention string."""
        if not ctx.message.author.permissions_in(ctx.message.channel).administrator:
            await bot.say("Only administrators can use this command!")
            return
        if ctx.invoked_subcommand is None:
            await bot.say('Invalid command passed...')


    @announce.command(pass_context=True)
    async def set_channel(ctx, channel: discord.Channel):
        """ Sets the channel where announcements will be announced. """
        if not channel:
            await bot.say("That's not a valid channel!")
            return

        conf.settings[ctx.message.server.id]["enabledChannel"] = channel.id
        conf.save()
        await bot.say("Announcements will now be made in {0.name}".format(channel))


    @announce.command(pass_context=True)
    async def user_join(ctx, message: str):
        """ Not implemented atm """
        await bot.say("when this is implemented, this will be the message i say: " + message)


    @announce.command(pass_context=True)
    async def role_add(ctx, role: discord.Role, message: str):
        """ When a user gains a specified role, the message you send will be announced. """
        if "role_add" not in conf.settings[ctx.message.server.id]["events"]:
            conf.settings[ctx.message.server.id][
                "events"]["role_add"] = {role.id: message}
            conf.save()
        else:
            conf.settings[ctx.message.server.id][
                "events"]["role_add"][role.id] = message
            conf.save()

        await bot.say("Whenever a user gains the `{0}` role, I'll say \"{1}\".".format(role.name, message))


def setup(bot):
    bot.add_cog(Announce(bot))