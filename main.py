import asyncio
import os

import discord
import dotenv
from discord.ext import commands

import text_classification
from text_gen import generate_text

# Load the environment variables from .env file
dotenv.load_dotenv()

BOT_PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Get the bot token from environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Hugging face API token TODO: Replace with safer method
# noinspection SpellCheckingInspection
HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')

if BOT_TOKEN is None:
    print('DISCORD_BOT_TOKEN environment variable not found!')
    exit(1)

if HUGGING_FACE_TOKEN is None:
    print('HUGGING_FACE_TOKEN environment variable not found!')
    exit(1)


@bot.command()
async def hello(ctx):
    await ctx.send('Hello! I\'m a bot!')


@bot.command()
async def ping(ctx):
    # Get the latency of the bot
    latency = bot.latency

    # Return in milliseconds
    await ctx.send(f'Pong! {latency * 1000:.2f}ms')


# Simple command that takes one argument
@bot.command()
async def echo(ctx, *, content: str):
    await ctx.send(content)


@bot.command()
async def yap(ctx, *, content: str):
    # Send initial message
    await ctx.send('Generating text...')

    # Generate text
    response = generate_text(content)
    await ctx.send(response)


# Classify text
@bot.command()
async def classify(ctx, *, content: str):
    # Notify the user that the bot is classifying the text
    await ctx.send(f'Classifying text... "{content}"')
    result = text_classification.classify(content)

    # Convert result into human-readable format with confidence percentage
    emotion = result[0]['label']
    confidence = result[0]['score'] * 100
    await ctx.send(f'Text is classified as: {emotion} with {confidence:.2f}% confidence.')

    # Send message related to the emotion
    if emotion == 'joy':
        await ctx.send('I\'m glad you\'re happy! 😄')
    elif emotion == 'sad':
        await ctx.send('I hope you feel better soon. 😢')
    elif emotion == 'angry':
        await ctx.send('I hope you feel better soon. 😡')
    elif emotion == 'fear':
        await ctx.send('I hope you feel better soon. 😱')
    elif emotion == 'surprise':
        await ctx.send('I hope you feel better soon. 😲')
    elif emotion == 'neutral':
        await ctx.send('I hope you feel better soon. 😐')
    elif emotion == 'disgust':
        await ctx.send('I hope you feel better soon. 🤢')
    else:
        await ctx.send('I hope you feel better soon. 🤔')


# Event to confirm bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# Restart on failure
# while True:
#     try:
#         bot.run(BOT_TOKEN)
#     except Exception as e:
#         print(f'Error: {e}')
#         print('Restarting bot...')

# Run the bot
bot.run(BOT_TOKEN)