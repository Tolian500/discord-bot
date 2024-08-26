import discord
import asyncio
import os
from discord.ext import commands

BOT_TOKEN = os.environ['BOT_TOKEN']
DISCORD_CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])


class DiscordBotManager:
    def __init__(self):
        # Create an instance of a bot with the necessary intents
        intents = discord.Intents.default()
        self.bot = commands.Bot(command_prefix="!", intents=intents)

        # Event for checking if the bot is ready
        self.ready_event = asyncio.Event()

        # Register the event handlers
        self.bot.event(self.on_ready)

    async def setup_hook(self):
        """Called after the bot has been initialized and is ready for asynchronous setup."""
        await self.bot.start(BOT_TOKEN)

    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        self.ready_event.set()  # Notify that the bot is ready

    async def send_message(self, message: str):
        """Send a custom message to the predefined channel."""
        if not self.bot.is_ready():
            print("Bot is not ready. Exiting...")
            return

        channel = self.bot.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            try:
                await channel.send(message)
                print('Message sent successfully!')
            except discord.DiscordException as e:
                print(f'Failed to send message: {e}')
        else:
            print(f'Channel with ID {DISCORD_CHANNEL_ID} not found.')


async def send_message(message: str):
    bot_manager = DiscordBotManager()

    # Start the bot
    asyncio.create_task(bot_manager.setup_hook())

    # Wait until the bot is ready
    await bot_manager.ready_event.wait()

    # Send the message
    await bot_manager.send_message(message)
