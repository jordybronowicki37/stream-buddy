import os
import sys

import discord
from discord import app_commands

from data_handler import DataHandler
from logger import get_logger
from discord_client import DiscordClient

logger = get_logger('discord_bot')
intents = discord.Intents.default()
intents.message_content = True
data_handler = DataHandler()


def start_discord_bot():
    logger.info("Starting discord bot")
    discordClient = DiscordClient(intents=intents)

    @discordClient.event
    async def on_ready():
        logger.info(f"Client logged in as {discordClient.user}")

    @discordClient.tree.command(name='streamers')
    async def get_all_streamers(interaction: discord.Interaction):
        """See all streamers currently being tracked"""
        await interaction.response.send_message('Test')

    @discordClient.tree.command(name='streamers-online')
    async def get_online_streamers(interaction: discord.Interaction):
        """See all streamers currently online"""
        # TODO: implement
        return

    @discordClient.tree.command(name='streamer-history')
    @app_commands.describe(streamer='The name of the streamer')
    async def get_streamer_history(interaction: discord.Interaction, streamer: str):
        """See the streaming history of a streamer"""
        # TODO: implement
        return

    @discordClient.tree.command(name='streamer-add')
    @app_commands.describe(name='The name of the streamer')
    @app_commands.describe(url='The url of the stream')
    @app_commands.describe(selector='The html element selector to check the online status')
    async def add_streamer(interaction: discord.Interaction, name: str, url: str, selector: str):
        """Add a new streamer to track"""
        # TODO: implement
        return

    @discordClient.tree.command(name='streamer-remove')
    @app_commands.describe(streamer='The name of the streamer')
    async def remove_streamer(interaction: discord.Interaction, streamer: str):
        """Remove a streamer from tracking"""
        # TODO: implement
        return

    try:
        TOKEN = os.getenv('DISCORD_TOKEN')
        discordClient.run(TOKEN)
    except TypeError:
        logger.error("Could not start the discord client. Make sure you have all the necessary env variables.")
        sys.exit(1)
