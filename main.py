import discord
from os import environ
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

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

GUILD_ID = discord.Object(id=1307493482562060342) #specify discord server

#/hello - bot says Hi there!
@client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")

#/printer input - bot says whatever input is given
@client.tree.command(name="printer", description="Prints input", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

load_dotenv()
token = environ["TOKEN"]
client.run(token) #individual bot token
