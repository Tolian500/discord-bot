import discord
import asyncio
import os
from discord.ext import commands

# Default BOT_TOKEN and DISCORD_CHANNEL_ID from environment variables
DEFAULT_BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEFAULT_DISCORD_CHANNEL_ID = int(os.environ.get('DISCORD_CHANNEL_ID', 0))


class DiscordBotManager:
    def __init__(self, bot_token=DEFAULT_BOT_TOKEN):
        # Create an instance of a bot with the necessary intents
        intents = discord.Intents.default()
        self.bot = commands.Bot(command_prefix="!", intents=intents)

        # Event for checking if the bot is ready
        self.ready_event = asyncio.Event()

        # Store the bot token
        self.bot_token = bot_token

        # Register the event handlers
        self.bot.event(self.on_ready)

    async def setup_hook(self):
        """Called after the bot has been initialized and is ready for asynchronous setup."""
        await self.bot.start(self.bot_token)

    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        self.ready_event.set()  # Notify that the bot is ready

    async def send_message(self, message: str, channel_id: int, silent: bool = False):
        """Send a custom message to the predefined or specified channel."""
        if not self.bot.is_ready():
            print("Bot is not ready. Exiting...")
            return

        channel = self.bot.get_channel(channel_id)
        if channel:
            try:
                silent_chose = False
                if silent:
                    silent_chose = True
                # Send the message with the flags
                await channel.send(content=message, silent=silent_chose)
                print('Message sent successfully!')
            except discord.DiscordException as e:
                print(f'Failed to send message: {e}')
        else:
            print(f'Channel with ID {channel_id} not found.')


async def send_message(message: str, token: str = DEFAULT_BOT_TOKEN, channel_id: int = DEFAULT_DISCORD_CHANNEL_ID,
                       silent: bool = False):
    """Send a message to a Discord channel with options for custom token, channel_id, and silent mode."""
    if not token or not channel_id:
        print("Bot token or channel ID not provided. Exiting...")
        return

    bot_manager = DiscordBotManager(bot_token=token)

    # Start the bot
    asyncio.create_task(bot_manager.setup_hook())

    # Wait until the bot is ready
    await bot_manager.ready_event.wait()

    # Send the message with the provided channel_id and silent mode
    await bot_manager.send_message(message=message, channel_id=channel_id, silent=silent)
