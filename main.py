import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('MTMwNzQ5MjEyNzE4NTQzNjczNQ.GWmkno.AW1KiloEVsuobhuI_DWn8aLjDTefM1bnUQj0Jw') #unique key, this is not a real one
