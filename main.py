import os

import discord
import dotenv
from discord.ext.commands import Bot
from discord.ext.commands.context import Context

import text_classification
from text_gen import generate_text

# Load the environment variables from .env file
dotenv.load_dotenv()

BOT_PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True
bot = Bot(command_prefix=BOT_PREFIX, intents=intents)

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
async def hello(ctx: Context):
    await ctx.send('Hello! I\'m a bot!')


# Invite command
@bot.command()
async def invite(ctx: Context):
    link = 'https://discord.com/oauth2/authorize?client_id=1255787959538552885'
    description = f'[Click here to invite Yapatron to your server!]({link})'
    embed = discord.Embed(title='Invite Fluffy', type='rich', description=description, color=discord.Color.purple())
    await ctx.send(embed=embed)


@bot.command()
async def liam(ctx: Context):
    path_to_liam = 'text files/liam.txt'
    with open(path_to_liam, 'r') as f:
        liam_text = f.read()
        await ctx.send(liam_text)


@bot.command()
async def ping(ctx: Context):
    # Get the latency of the bot
    latency = bot.latency

    # Return in milliseconds
    await ctx.send(f'Pong! {latency * 1000:.2f}ms')


# Simple command that takes one argument
@bot.command()
async def echo(ctx: Context, *, content: str):
    await ctx.send(content)


@bot.command()
async def yap(ctx: Context, *, content: str = ''):
    print(type(ctx))
    # # Check if argument is empty
    if content == '':
        # Send info about the command in an embed
        embed = discord.Embed(title='Yap Command', type='rich',
                              description='Generate text based on a prompt.\nUsage: !yap <prompt>',
                              color=discord.Color.purple())
        await ctx.send(embed=embed)
    else:
        # Make embed for generating text
        embed = discord.Embed(title='Generating text...', type='rich', description=content,
                              color=discord.Color.purple())
        await ctx.send(embed=embed)
        async with ctx.typing():
            response = generate_text(content)
            # Create fancy embed for the response
            embed = discord.Embed(title='Generated text', type='rich', description=response,
                                  color=discord.Color.purple())
            await ctx.reply(embed=embed)


# Classify text
@bot.command()
async def classify(ctx: Context, *, content: str = ''):
    if ctx.message.reference and content == '':
        # Check if they replied to another message that only contains "!classify"
        replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
        replied_content = replied_message.content
        if replied_content == '!classify':
            # Send "Now why would I wanna classify that?"
            await ctx.send('Now why would I wanna classify that?')
        else:
            await classify_reply(ctx)
    elif not ctx.message.reference and content == '':
        await classify_info(ctx)
    else:
        # Notify the user that the bot is classifying the text
        await ctx.send(f'Classifying text... "{content}"')
        await classify_thing(content, ctx)


async def classify_thing(content, ctx: Context):
    result = text_classification.classify(content)
    emotion = result[0]['label']
    confidence = result[0]['score'] * 100

    description = f"Text is classified as: {emotion} with {confidence:.2f}% confidence.\n{await emotion_check(emotion)}"

    embed = discord.Embed(title='Text Classification', type='rich', description=description,
                          color=discord.Color.purple())
    await ctx.send(embed=embed)


@bot.command()
async def dm(ctx: Context):
    # Opens a dm with the user with a nice embed
    embed = discord.Embed(title='DM', type='rich',
                          description='Hello!\n\nFeel free to chat with me here!\n\nType !help for a list of commands.',
                          color=discord.Color.purple())
    await ctx.author.send(embed=embed)
    await ctx.send('Sent you a DM!')


@bot.command()
async def image(ctx: Context):
    # Print image support coming soon
    embed = discord.Embed(title='Image Support', type='rich', description='Image support coming soon!',
                          color=discord.Color.purple())
    await ctx.send(embed=embed)


@bot.command()
async def rick_roll(ctx: Context):
    embed = discord.Embed(title='Rick Roll', type='rich', description='Launching Rick Roll on Fluffy\'s computer...',
                          color=discord.Color.purple())
    await ctx.send(embed=embed)

    # Launch Rick Roll in browser
    os.system('start https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    # Notify success
    embed = discord.Embed(title='Rick Roll', type='rich', description='Rick Roll launched! 💀',
                          color=discord.Color.purple())
    await ctx.send(embed=embed)


async def classify_info(ctx: Context):
    # Send info about the command in an embed
    embed = discord.Embed(title='Classify Command', type='rich',
                          description='Classify text based on emotion.\nUsage: !classify <text>',
                          color=discord.Color.purple())
    await ctx.send(embed=embed)


async def classify_reply(ctx: Context):
    # Get the message that the user replied to
    replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
    content = replied_message.content
    # Notify the user that the bot is classifying the text
    response_content = content
    if len(content) > 100:
        response_content = content[:100] + '...'
    await ctx.send(f'Classifying text... "{response_content}"')
    async with ctx.typing():
        await classify_thing(content, ctx)


async def emotion_check(emotion) -> str:
    if emotion == 'joy':
        return 'I\'m glad you\'re happy! 😄'
    elif emotion == 'sad':
        return 'I hope you feel better soon. 😢'
    elif emotion == 'angry':
        return 'I hope you feel better soon. 😡'
    elif emotion == 'fear':
        return 'I hope you feel better soon. 😱'
    elif emotion == 'surprise':
        return 'I hope you feel better soon. 😲'
    elif emotion == 'neutral':
        return 'I hope you feel better soon. 😐'
    elif emotion == 'disgust':
        return 'I hope you feel better soon. 🤢'
    else:
        return 'I hope you feel better soon. 🤔'


# Event to confirm bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


bot.run(BOT_TOKEN)
