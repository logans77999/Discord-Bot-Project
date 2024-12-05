import discord
from os import environ
from dotenv import load_dotenv
from discord.ext import commands
from commands import register_commands
import asyncio
import os

class Client(commands.Bot):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try: #sync bot commands to discord server
            guild = discord.Object(id=1307493482562060342)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to server {guild.id}')

        except Exception as e: #error if sync fails
            print(f'Error syncing commands {e}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello') or message.content.startswith('Hello'): #sends message if user says "hello"
            await message.channel.send(f'Hi there {message.author}')

    async def on_member_join(self, member): 
        channel = self.get_channel(1311560487238107156) #server ID for welcome channel

        if channel:
            await channel.send(f'Welcome {member.mention} to the Server!')  #sends welcome message to a new user

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for on_member_join
client = Client(command_prefix='!', intents=intents) #for / commands

#register commands
register_commands(client)

#add leveling system
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with client:
        load_dotenv()
        token = environ["TOKEN"]

        await load_extensions()
        await client.start(token) #individual bot token

asyncio.run(main())
