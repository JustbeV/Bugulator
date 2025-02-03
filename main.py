import discord
from discord.ext import commands
import random
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  
bot = commands.Bot(command_prefix='!', intents=intents)

# --- Calculator Command ---
@bot.command()
async def calc(ctx, num1: float, operator: str, num2: float):
    try:
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                await ctx.send("Error: Division by zero!")
                return
            result = num1 / num2
        else:
            await ctx.send("Invalid operator! Use +, -, *, or /.")
            return

        await ctx.send(f"The result of {num1} {operator} {num2} = {float(result)}")

    except Exception as e:
        await ctx.send(f"Error: {e}")

# --- Bug Catching Game Command ---
@bot.command()
async def buggame(ctx):
    caught = 0
    bugs = ["🐞", "🪲", "🐜", "🦋", "🐝"]
    game_duration = 20  # Total game time in seconds
    start_time = asyncio.get_event_loop().time()  # Track start time

    await ctx.send("The bug-catching game has started! Type 'catch' when you see a bug!")

    while (asyncio.get_event_loop().time() - start_time) < game_duration:
        bug = random.choice(bugs)
        await ctx.send(f"A wild {bug} appears! Type **'catch'** to catch it!")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == 'catch'

        try:
            msg = await bot.wait_for('message', timeout=5.0, check=check)
            await ctx.send(f"You caught the {bug}! 🎯")
            caught += 1
        except asyncio.TimeoutError:
            await ctx.send(f"The {bug} got away! 🏃💨")

        await asyncio.sleep(2)  # Small delay before the next bug appears

    await ctx.send(f"Game over! You caught {caught} bugs! 🐛")
# --- Bot Ready Event ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot
bot.run(TOKEN)