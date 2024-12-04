import discord
import urllib.parse
import urllib.request
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

GUILD_ID = discord.Object(id=1307493482562060342) #specify discord server

load_dotenv()
spotify_id = os.getenv("SPOT_ID")
spotify_secret = os.getenv("SPOT_SECRET")
auth_manager = SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def register_commands(client):
    #/hello - bot says Hi there!
    @client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
    async def sayHello(interaction: discord.Interaction):
        await interaction.response.send_message("Hi there!")

    #/printer input - bot says whatever input is given
    @client.tree.command(name="printer", description="Prints input", guild=GUILD_ID)
    async def printer(interaction: discord.Interaction, printer: str):
        await interaction.response.send_message(printer)

    #/youtube input - bot provides first youtube link based off input
    @client.tree.command(name="youtube", description="Search Youtube", guild=GUILD_ID)
    async def youtube(interaction: discord.Interaction, search: str):
        query_string = urllib.parse.urlencode({'search_query': search})
        html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_content= html_content.read().decode()
        search_results = re.findall(r'\/watch\?v=\w+', search_content)
        #print(search_results)
        if search_results:
            await interaction.response.send_message(f'Here is the search result:\n https://www.youtube.com' + search_results[0])

        else:
            await interaction.response.send_message("No results found.")

    #/spotify playlist - bot provides first spotify playlist based off input
    #If the first result is a curated spotify playlist, it doesn't work 
    @client.tree.command(name="spotify", description="Search Spotify playlists", guild=GUILD_ID)
    async def spotify(interaction: discord.Interaction, search: str):
        try:
            results = sp.search(q=search, type="playlist", limit=1)
            
            if results and "playlists" in results and "items" in results["playlists"]:
                # Filter out None values from items
                valid_items = [item for item in results["playlists"]["items"] if item is not None]
                
                if valid_items:
                    playlist = valid_items[0]
                    name = playlist["name"]
                    url = playlist["external_urls"]["spotify"]
                    await interaction.response.send_message(f"Playlist: {name}\nURL: {url}")
                else:
                    await interaction.response.send_message("No valid playlists found.")
            else:
                await interaction.response.send_message("No playlists found or invalid response.")
        except Exception as e:
            await interaction.response.send_message("Error accessing Spotify API. Please check the logs.")
            print(f"Spotify API Error: {e}")


load_dotenv()


