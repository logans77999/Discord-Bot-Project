import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import math
import random

#Create leveling system
class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling online!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        #register user to database
        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()
        guild_id = message.guild.id
        user_id = message.author.id

        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))

        result = cursor.fetchone()
        #set user level and xp
        if result is None:
            cur_level = 0
            xp = 0
            level_up_xp = 100
            cursor.execute("INSERT INTO Users (guild_id, user_id, level, xp, level_up_xp) Values (?,?,?,?,?)", (guild_id, user_id, cur_level, xp, level_up_xp))
        #update xp
        else:
            cur_level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            xp += random.randint(1, 25)
        #update level and xp needed
        if xp >= level_up_xp:
            cur_level += 1
            new_level_up_xp = math.ceil(50 * cur_level ** 2 + 100 * cur_level + 50) 

            await message.channel.send(f"{message.author.mention} has leveled up to level {cur_level}!")

            cursor.execute("UPDATE Users SET level = ?, xp = ?, level_up_xp = ? WHERE guild_id = ? AND user_id = ?", (cur_level, xp, new_level_up_xp, guild_id, user_id))

        cursor.execute("UPDATE Users SET xp = ? WHERE guild_id = ? AND user_id = ?", (xp, guild_id, user_id))

        connection.commit()
        connection.close()

    #Command needs work
    """@app_commands.command(name="level", description="Check the level and XP of a user.")
    async def level(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        member_id = member.id
        guild_id = interaction.guild.id

        connection = sqlite3.connect("./levels.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, member_id))
        result = cursor.fetchone()
        #check a users level
        if result is None:
            await interaction.response.send_message(f'{member.name} does not have a level.')
        
        else:
            level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            await interaction.response.send_message(f'Level Statistics for {member.name}: \nLevel: {level} \nXP: {xp} \nXP To Level Up: {level_up_xp}')

        connection.close()"""

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))


    