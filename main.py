import discord, os, json, re
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

from sequences import sequences

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='sequence!', intents=intents)

guild_sequences = {}

@bot.event
async def on_ready():
    print("loaded")
    if not guild_sequences:
        # Load data from JSON files
        for filename in os.listdir("guilds"):
            if filename.endswith(".json"):
                guild_id = int(filename.split(".")[0])
                with open(os.path.join("guilds", filename), "r") as file:
                    guild_sequences[guild_id] = json.loads(file.read())

@bot.command(name="sequence")
async def _create_sequence(ctx,arg):
    if arg not in sequences:
        ctx.reply("Unknown sequence: "+arg+". Please try again")
        return

    channel = ctx.channel
    sequence_thread = await channel.create_thread(
        name=arg+" sequence",
        message=ctx.message
    )
    print(sequence_thread.id)
    await sequence_thread.send((await sequences[arg](0)))

    counter_template = {
                    "sequence":arg,
                    "highest_indice":0,
                    "current_indice":-1,
                    "last_user_id":0,
                }
    guild_json = {}
    if os.path.isfile(f"guilds/{ctx.guild.id}.json"):
        with open(f"guilds/{ctx.guild.id}.json","r+") as file:
            guild_json = json.loads(file.read())
            guild_json[str(sequence_thread.id)] = counter_template
            file.seek(0)
            file.write(json.dumps(guild_json))
            file.truncate()
    else:
        with open(f"guilds/{ctx.guild.id}.json","x") as file:
            guild_json = {
                str(sequence_thread.id):counter_template
            }
            file.write(json.dumps(guild_json))
    
    guild_sequences[ctx.guild.id] = guild_json
    return


@bot.listen("on_message")
async def _check_counter(ctx):
    if ctx.author.id == bot.user.id:
        return
    if ctx.guild.id not in guild_sequences:
        return
    if str(ctx.channel.id) not in guild_sequences[ctx.guild.id]:
        return
    counter = guild_sequences[ctx.guild.id][str(ctx.channel.id)]

    try:
        value = int(re.search("[0-9]*", ctx.content).group(0))
    except Exception:
        return

    if ctx.author.id == counter["last_user_id"] and not str(ctx.guild.id) == os.getenv("TEST_SERVER"):
        await reset(ctx.guild.id,str(ctx.channel.id))
        await ctx.reply(f"Ruined it! Same person can't go twice in a row! Start again at {(await sequences[counter['sequence']](0))}")
        return
    
    expected_value = await sequences[counter["sequence"]](counter["current_indice"]+1)
    
    print(expected_value)


    if value == expected_value:
        if counter["current_indice"] > counter["highest_indice"]:
            await ctx.add_reaction("☑")
            counter["highest_indice"] = counter["current_indice"]
        else:
            await ctx.add_reaction("✅")
        counter["current_indice"] += 1
        counter["last_user_id"]=ctx.author.id
    else:
        await ctx.add_reaction("❌")
        await ctx.reply(f"Ruined it! Expected answer {str(expected_value)}. Start again at {(await sequences[counter['sequence']](0))}")
        await reset(ctx.guild.id,str(ctx.channel.id))
        return

    with open(f"guilds/{ctx.guild.id}.json","w") as file:
        file.write(json.dumps(guild_sequences[ctx.guild.id]))

async def reset(guild,thread):
    print(guild_sequences)
    guild_sequences[guild][thread]["current_indice"]=-1
    guild_sequences[guild][thread]["last_user_id"]=0
    await sequences[guild_sequences[guild][thread]["sequence"]](-1)
    with open(f"guilds/{guild}.json","w") as file:
        file.write(json.dumps(guild_sequences[guild]))

bot.run(os.getenv("TOKEN"))
