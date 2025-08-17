import logging
import os
import sys

import discord
from discord import app_commands

logger = logging.getLogger()
intents = discord.Intents.default()
intents.message_content = True



def run_discord_bot():
    logger.info("Starting discord bot")
    discordClient = discord.Client(intents=intents)
    command_tree = app_commands.CommandTree(discordClient)

    @discordClient.event
    def on_ready():
        logger.info(f"[INFO] Client logged in as {discordClient.user}")

    @command_tree.command()
    def get_all_streamers(interaction: discord.Interaction):
        """See all streamers currently being tracked"""
        # TODO: implement
        return

    @command_tree.command()
    def get_online_streamers(interaction: discord.Interaction):
        """See all streamers currently online"""
        # TODO: implement
        return

    @command_tree.command()
    @app_commands.describe(streamer='The name of the streamer')
    @app_commands.check
    def get_streamer_history(interaction: discord.Interaction, streamer: str):
        """See the streaming history of a streamer"""
        # TODO: implement
        return

    @command_tree.command()
    @app_commands.describe(name='The name of the streamer')
    @app_commands.describe(url='The url of the stream')
    @app_commands.describe(selector='The html element selector to check the online status')
    def add_streamer(interaction: discord.Interaction, name: str, url: str, selector: str):
        """Add a new streamer to track"""
        # TODO: implement
        return

    @command_tree.command()
    @app_commands.describe(streamer='The name of the streamer')
    def remove_streamer(interaction: discord.Interaction, streamer: str):
        """Remove a streamer from tracking"""
        # TODO: implement
        return

    try:
        TOKEN = os.getenv('DISCORD_TOKEN')
        discordClient.run(TOKEN)
    except TypeError:
        logger.error("Could not start the discord client. Make sure you have all the necessary env variables.")
        sys.exit(1)

run_discord_bot()