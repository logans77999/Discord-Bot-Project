import discord

class Client(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello') or message.content.startswith('Hello'):
            await message.channel.send(f'Hi there {message.author}')

    async def on_member_join(self, member):
        await client.channel.send(f'Welcome {member} to the Server!') #not working properly right now

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('') #individual bot token
