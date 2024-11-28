import discord
from os import environ
from dotenv import load_dotenv
class Client(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello') or message.content.startswith('Hello'):
            await message.channel.send(f'Hi there {message.author}')

    async def on_member_join(self, member):
        channel = self.get_channel(1311560487238107156)

        if channel:
            await channel.send(f'Welcome {member.mention} to the Server!') #not working properly right now

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
client = Client(intents=intents)
token = environ["TOKEN"]
client.run(token) #individual bot token
