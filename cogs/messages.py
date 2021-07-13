import discord
from discord.ext import commands, tasks


import json

with open("config.json", "r") as read_file:
    config = json.load(read_file)


class Mesages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GUILD = self.bot.get_guild(config["GUILD_ID"])
        self.GROUP_STUDY_CATEG = discord.utils.get(
            self.GUILD.categories, id=config["CATEGORY"]["GROUP"]
        )
        self.VIDEO_STUDY_CATEG = discord.utils.get(
            self.GUILD.categories, id=config["CATEGORY"]["VIDEO"]
        )
        self.SILENT_CATEG = discord.utils.get(
            self.GUILD.categories, id=config["CATEGORY"]["SILENT"]
        )
        self.EXTRACURRICULAR_CATEG = discord.utils.get(
            self.GUILD.categories, id=config["CATEGORY"]["EXTRACURRICULAR"]
        )
        self.LOUNGE_VC = discord.utils.get(
            self.GUILD.voice_channels, id=config["CHANNELS"]["VOICE"]["LOUNGE"]
        )
        self.COUNTER = discord.utils.get(
            self.GUILD.voice_channels, id=config["CHANNELS"]["VOICE"]["COUNTER"]
        )
        self.BOT_CHANNEL = discord.utils.get(
            self.GUILD.text_channels, id=config["CHANNELS"]["TEXT"]["KOMI_MESSAGES"]
        )
        self.TOMODACHI = self.GUILD.get_role(config["ROLES"]["TOMODACHI"])
        self.STUDYING = self.GUILD.get_role(864364341960638465)
        #self.kick_stalkers.start()

    ################# LOOPS #################


    """
    @tasks.loop(minutes=config["KICK_STALKERS_AFTER"])
    async def kick_stalkers(self):
        # MOVE MEMBERS WHO DONT HAVE VIDEO OR SCREENSHARE
        for vc in self.VIDEO_STUDY_CATEG.voice_channels:
            for mem in vc.members:
                if not (mem.voice.self_video or mem.voice.self_stream):
                    await mem.move_to(channel=self.LOUNGE_VC)
                    await self.BOT_CHANNEL.send(
                        f"{mem.mention} was moved <:komi_sleep:843170281438576671>\n<#{vc.id}> -> <#{self.LOUNGE_VC.id}>\nReason : no camera or screenshare"
                    )
        # for vc in self.EXTRACURRICULAR_CATEG.voice_channels:
        #     for mem in vc.members:
        #         if not (mem.voice.self_video or mem.voice.self_stream):
        #             await mem.move_to(channel=self.LOUNGE_VC)
        #             await self.BOT_CHANNEL.send(
        #                 f"{mem.mention} was moved <:komi_sleep:843170281438576671>\n<#{vc.id}> -> <#{self.LOUNGE_VC.id}>\nReason : no camera or screenshare"
        #             )
    """

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot or (before.channel == after.channel):
            return
        study_categ_ids = config["CATEGORY"].values()

        print(after.channel)
        if after.channel != None:
            # WHEN SOMEONE JOINS A STUDY CHANNEL
            print(member, "joined 1")
            print(study_categ_ids)
            if after.channel.category_id in study_categ_ids:
                print(study_categ_ids)
                print(member, "joined 2")
                try:
                  await member.add_roles(self.STUDYING)
                except Exception as err:
                  print("role adding failure", err)
                print(self.STUDYING,  "added")
                await member.remove_roles(self.TOMODACHI)
                perms = after.channel.category.overwrites_for(self.STUDYING)
                perms.view_channel = True
                perms.speak = False
                await after.channel.set_permissions(member, overwrite=perms)
                await member.edit(mute=True)
                msg = f"{member.mention} joined <#{after.channel.id}>\n"
                msg += f"Head over to <#{config['CHANNELS']['TEXT']['ACCOUNTABILITY']}> and post some goals to get started\n"
                await self.BOT_CHANNEL.send(msg)
                if after.channel.category_id == config["CATEGORY"]["PRIVATE"]:
                    await member.edit(mute=False)
            else:
                await member.edit(mute=False)

        elif after.channel == None:
            # WHEN SOMEONE LEAVES A STUDY CHANNEL
            if before.channel.category_id in study_categ_ids:
                await member.add_roles(self.TOMODACHI)
                await member.remove_roles(self.STUDYING)
                await before.channel.set_permissions(member, overwrite=None)
                msg = f"**{member}** left <#{before.channel.id}>\n"
                await self.BOT_CHANNEL.send(msg)
            else:
                pass


def setup(bot):
    bot.add_cog(Mesages(bot))
    print("---> MESSAGES LOADED")
