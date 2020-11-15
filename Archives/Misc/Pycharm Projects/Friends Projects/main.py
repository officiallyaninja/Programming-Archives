import discord
import json
import asyncio
import re
from discord import utils
from pathlib import Path
from datetime import datetime
from discord.ext import commands
import time


# JSON data

with open("sconfig.json") as f:
    data = json.load(f)

# JSON variables

prefix = data["server"]["prefix"]
banned_words = data["server"]["banned_words"]
access_key = data["server"]["access_key"]
access_key_channel_id = data["server"]["access_key_channel_id"]
role_to_give_id = data["server"]["role_to_give_id"]
welcome_channel_id = data["server"]["welcome_channel_id"]
welcome_message = data["server"]["welcome_message"]
banned_channels = data["server"]["banned_channels"]
roles_on_join = data["server"]["roles_on_join"]

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))

# Owner/admin check


def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator or await bot.is_owner(ctx.author)
    return commands.check(predicate)

# Basic connection-related events


@bot.event
async def on_connect():
    print("{} | Connected to Websocket!".format(datetime.utcnow().strftime("%I:%M:%S %p")))


@bot.event
async def on_ready():
    print("{} | Bot has successfully loaded!".format(datetime.utcnow().strftime("%I:%M:%S %p")))
    bot.uptime = datetime.utcnow()
    await bot.change_presence(activity=discord.Game(f"with {len(set(bot.get_all_members()))} users"))


@bot.event
async def on_resumed():
    print("{} | Resumed Websocket Connection!".format(datetime.utcnow().strftime("%I:%M:%S %p")))


# takes out the newbie role when level 5
@bot.event
async def on_member_update(before, after):
    newbie = utils.get(before.roles, id=int(role_to_give_id))
    rester = utils.get(after.roles, name="Rester (lvl. 5)")
    if newbie and rester:
        await after.remove_roles(newbie)

# On message event - access key and censoring
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    with open("sconfig.json") as f:
        data = json.load(f)
    banned_words = data["server"]["banned_words"]
    access_key = data["server"]["access_key"]
    access_key_channel_id = data["server"]["access_key_channel_id"]
    role_to_give_id = data["server"]["role_to_give_id"]
    welcome_channel_id = data["server"]["welcome_channel_id"]
    welcome_message = data["server"]["welcome_message"]
    banned_channels = data["server"]["banned_channels"]
    rank_command_censor = data["server"]["rank_command_censor"]
    roles_on_join = data["server"]["roles_on_join"]

    # Correct password in the channel ...

    if access_key_channel_id and welcome_channel_id and role_to_give_id:

        welcome_role = utils.get(message.guild.roles, id=int(role_to_give_id))

        role_list = []
        [role_list.append(role) for role in roles_on_join]
        roles_to_add = [(utils.get(message.guild.roles, id=int(role))) for role in role_list]
        roles_to_add.append(welcome_role)  # appends the welcome role to the list
        # adds just the welcome role
        if message.channel.id == int(access_key_channel_id) and any(x in message.content.lower() for x in access_key) and not roles_on_join:
            await message.delete()
            await message.author.add_roles(welcome_role)
            await (bot.get_channel(int(welcome_channel_id))).send(welcome_message.format(user=message.author.mention, server=message.guild.name))
        # adds multiple roles
        if message.channel.id == int(access_key_channel_id) and any(x in message.content.lower() for x in access_key) and roles_on_join:
            await message.delete()
            await message.author.add_roles(*roles_to_add)
            await (bot.get_channel(int(welcome_channel_id))).send(welcome_message.format(user=message.author.mention, server=message.guild.name))

        # Incorrect password in the channel ...
        if message.channel.id == int(access_key_channel_id) and not any(x in message.content.lower() for x in access_key):
            await message.delete()
            await message.channel.send(":x: Incorrect answer. Please read the rules again.", delete_after=3)

    # !rank command censoring on/off 1 ON - 0 OFF
    if rank_command_censor == 1:
        if message.content.lower() == "!rank" and message.channel.id == 234235463697825792:
            mee6 = await bot.wait_for('message', check=lambda m: m.author.id == 159985870458322944 and m.channel == message.channel)
            await mee6.delete()
            await message.delete()
            await message.channel.send(f":warning: {message.author.mention}, do **NOT** use the `!rank` command here! Go to <#316194492107718656> for that.", delete_after=5)
            await message.author.send(f"Please do **NOT** use the `!rank` command in {message.channel.mention}. Go to <#316194492107718656> for that.")

        # If message contains ANY word in the banned words list ...
    if banned_words and banned_channels:
        if any(x in message.content for x in banned_words) and str(message.channel.id) in banned_channels:

            singular = "is"
            singular_1 = "The word:"
            plural = "are"
            plural_1 = "The words:"

            words_to_filter = []
            [words_to_filter.append(word) for word in banned_words if word in message.content]

            await message.delete()
            await message.channel.send(f":warning: {singular_1 if len(words_to_filter) == 1 else plural_1}" +
                                       f" {', '.join(words_to_filter)} {singular if len(words_to_filter) == 1 else plural} forbidden here, {message.author.mention}.", delete_after=5)
            await message.author.send(f":warning: {singular_1 if len(words_to_filter) == 1 else plural_1}" +
                                      f" {', '.join(words_to_filter)} {singular if len(words_to_filter) == 1 else plural} forbidden in {message.channel.mention}")

    await bot.process_commands(message)


@bot.event
async def on_message_edit(before, after):
    if banned_words and banned_channels:

        with open("sconfig.json") as f:
            data = json.load(f)
        banned_words_ = data["server"]["banned_words"]
        banned_channels_ = data["server"]["banned_channels"]

        if any(x in after.content for x in banned_words_) and str(after.channel.id) in banned_channels_:
            await after.delete()
            await after.channel.send(
                f":warning: Please do **NOT** edit your messages to include censored words, {after.author.mention}.",
                delete_after=5)
            await after.author.send(
                f":warning: Please do **NOT** edit your messages to include censored words in {after.channel.mention}!")


@bot.group(aliases=["s"])
@commands.guild_only()
@is_admin()
async def setup(ctx):
    if ctx.invoked_subcommand is None:
        return await ctx.send("No argument or invalid subcommand passed. Valid subcommands:\n\n1. start\n2. edit\n3. reset\n4. check")


@setup.command(aliases=["s"])
@commands.guild_only()
@is_admin()
async def start(ctx):
    e = discord.Embed(title="1. Access Key Channel",
                      description="Setup initiated. Please enter the **Channel ID** you'd like to set up for the Access Key. Type `exit` to cancel the setup.")
    embed = await ctx.send(embed=e)

    # Checks

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:

        # FIRST step, access key channel ID

        response = await bot.wait_for('message', check=check, timeout=60.0)

        if response.content == "exit":
            await response.delete()
            e = discord.Embed(description="Cancelled!")
            return await embed.edit(embed=e)

        while not discord.utils.get(ctx.guild.channels, id=int(response.content)):
            e = discord.Embed(title="1. Access Key Channel",
                              description="Invalid Channel ID passed. Please try again. Type `exit` to cancel.")
            await embed.edit(embed=e)

            response_1 = await bot.wait_for('message', check=check, timeout=60.0)

            if response_1.content == "exit":
                await response_1.delete()
                e = discord.Embed(description="Cancelled!")
                return await embed.edit(embed=e)

            if not response_1.content.isdigit():
                await response_1.delete()
                continue

            # If a channel is FOUND, break out from the while loop ...
            if discord.utils.get(ctx.guild.channels, id=int(response_1.content)):

                await response_1.delete()

                # Assigns value to JSON variable
                data["server"]["access_key_channel_id"] = response_1.content
                with open("sconfig.json", "w") as f:
                    json.dump(data, f, indent=1)

                e = discord.Embed(title="1. Access Key Channel",
                                  description=f"Successfully set <#{response_1.content}> as the access key channnel!")
                await embed.edit(embed=e)
                break

        # If msg ...
        if discord.utils.get(ctx.guild.channels, id=int(response.content)):
            await response.delete()

            data["server"]["access_key_channel_id"] = response.content
            with open("sconfig.json", "w") as f:
                json.dump(data, f, indent=1)

            e = discord.Embed(title="1. Access Key Channel",
                              description=f"Successfully set <#{response.content}> as the access key channnel!")
            await embed.edit(embed=e)
        await asyncio.sleep(2)

        # SECOND PHASE, asks for Access Key
        e = discord.Embed(title="2. Access Key (Password)",
                          description="Great, now please enter the **Access Key** (password) for that channel. Type `exit` to cancel.")
        await embed.edit(embed=e)

        key = await bot.wait_for('message', check=check, timeout=60.0)
        await key.delete()

        if key.content.lower() == "exit":
            e = discord.Embed(description="Cancelled.")
            return await embed.edit(embed=e)

        key_list = data["server"]["access_key"]

        while key.content.lower() in key_list:
            e = discord.Embed(title="2. Access Key (Password)",
                              description=":warning: This key is already in the list. Please add another one! Type `skip` to skip this step.")
            await embed.edit(embed=e)

            key_1 = await bot.wait_for('message', check=check, timeout=30.0)
            await key_1.delete()

            if key_1.content == "skip":
                e = discord.Embed(description="Skipping...")
                await embed.edit(embed=e)
                break

            if key_1.content not in key_list and key_1.content != "skip":
                key_list.append(key_1.content.lower())

                with open("sconfig.json", "w") as f:
                    json.dump(data, f, indent=1)
                e = discord.Embed(title="2. Access Key (Password)",
                                  description=f"The Access Key `{key_1.content}` was saved!")
                await embed.edit(embed=e)
                break

        if key.content.lower() not in key_list and key.content != "skip":
            key_list.append(key.content.lower())

            with open("sconfig.json", "w") as f:
                json.dump(data, f, indent=1)
            e = discord.Embed(title="2. Access Key (Password)",
                              description=f"The Access Key `{key.content}` was saved!")
            await embed.edit(embed=e)
        await asyncio.sleep(2)

        # THIRD PHASE, asks for Role ID
        e = discord.Embed(title="3. Welcome Role ID",
                          description="Next, introduce the **Role ID** to give to new members.")
        await embed.edit(embed=e)

        role = await bot.wait_for('message', check=check, timeout=60.0)
        await role.delete()

        # If the role is NOT found ...
        while not discord.utils.get(ctx.guild.roles, id=int(role.content)):
            e = discord.Embed(title="3. Welcome Role ID",
                              description="Invalid Role ID passed. Please try again. Type `exit` to cancel.")
            await embed.edit(embed=e)

            role_1 = await bot.wait_for('message', check=check, timeout=60.0)
            await role_1.delete()

            if role_1.content == "exit":                   #
                e = discord.Embed(description="Cancelled!")  # EXIT
                return await embed.edit(embed=e)           #

            if not role_1.content.isdigit():
                continue

            # If msg3 ...
            elif discord.utils.get(ctx.guild.roles, id=int(role_1.content)):

                data["server"]["role_to_give_id"] = role_1.content
                with open("sconfig.json", "w") as f:
                    json.dump(data, f, indent=1)

                e = discord.Embed(title="3. Welcome Role ID",
                                  description=f"Role: `{(discord.utils.get(ctx.guild.roles, id=int(role_1.content))).name}` set!")
                await embed.edit(embed=e)
                break

        # If msg2 ...
        if discord.utils.get(ctx.guild.roles, id=int(role.content)):

            data["server"]["role_to_give_id"] = role.content
            with open("sconfig.json", "w") as f:
                json.dump(data, f, indent=1)

            e = discord.Embed(title="3. Welcome Role ID",
                              description=f"Role: `{(discord.utils.get(ctx.guild.roles, id=int(role.content))).name}` set!")
            await embed.edit(embed=e)

        await asyncio.sleep(2)

        # FOURTH step. Welcome CHANNEL ID
        e = discord.Embed(title="4. Welcome Channel ID",
                          description="Now introduce the **Channel ID** of the welcome channel.")
        await embed.edit(embed=e)

        welcome = await bot.wait_for('message', check=check, timeout=60.0)
        await welcome.delete()

        while not discord.utils.get(ctx.guild.channels, id=int(welcome.content)):
            e = discord.Embed(title="4. Welcome Channel ID",
                              description="Invalid Channel ID passed. Please try again. Type `exit` to cancel.")
            await embed.edit(embed=e)

            welcome_1 = await bot.wait_for('message', check=check, timeout=60.0)
            await welcome_1.delete()

            if welcome_1.content == "exit":
                e = discord.Embed(description="Command cancelled. Welcome channel was not set!")
                return await embed.edit(embed=e)
            if not welcome_1.content.isdigit():
                continue

            # If a CHANNEL is FOUND, break
            if discord.utils.get(ctx.guild.channels, id=int(welcome_1.content)):
                data["server"]["welcome_channel_id"] = welcome_1.content

                with open("sconfig.json", "w") as f:
                    json.dump(data, f, indent=1)
                e = discord.Embed(title="4. Welcome Channel ID",
                                  description=f"Welcome channel: <#{welcome_1.content}> succesfully set!")
                await embed.edit(embed=e)
                break

        if discord.utils.get(ctx.guild.channels, id=int(welcome.content)):

            data["server"]["welcome_channel_id"] = welcome.content
            with open("sconfig.json", "w") as f:
                json.dump(data, f, indent=1)
            e = discord.Embed(title="4. Welcome Channel ID",
                              description=f"Welcome channel: <#{welcome.content}> succesfully set.")
            await embed.edit(embed=e)

        # FIFTH step, add welcome message
        await asyncio.sleep(2)
        e = discord.Embed(title="5. Welcome Message",
                          description="Now set a welcome message. Placeholders are `{server}` and `{user}`. You have 5 minutes to type it.")
        await embed.edit(embed=e)

        welcome_msg = await bot.wait_for('message', check=check, timeout=300.0)
        await welcome_msg.delete()

        while "user" not in welcome_msg.content or "server" not in welcome_msg.content:
            e = discord.Embed(title="5. Welcome Message",
                              description="One or both placeholders were not used. Please use them!")
            await embed.edit(embed=e)

            welcome_msg_2 = await bot.wait_for('message', check=check, timeout=300.0)
            await welcome_msg_2.delete()

            if "user" in welcome_msg_2.content and "server" in welcome_msg_2.content:
                data["server"]["welcome_message"] = welcome_msg_2.content

                with open("sconfig.json", "w") as f:
                    json.dump(data, f, indent=1)
                e = discord.Embed(title="5. Welcome Message",
                                  description=f"New welcome message set:\n```{welcome_msg_2.content}```")
                await embed.edit(embed=e)
                break

        if "user" in welcome_msg.content and "server" in welcome_msg.content:
            data["server"]["welcome_message"] = welcome_msg.content

            with open("sconfig.json", "w") as f:
                json.dump(data, f, indent=1)
            e = discord.Embed(title="5. Welcome Message",
                              description=f"Welcome message set:\n```{welcome_msg.content}```")
            await embed.edit(embed=e)

        # SIXTH step, channels to ban if any
        await asyncio.sleep(2)

        e = discord.Embed(title="6. Channel Censoring",
                          description="Please now enter a **Channel ID** to censor characters/words in. Type `exit` to cancel.")
        await embed.edit(embed=e)

        ban_chan = await bot.wait_for('message', check=check, timeout=60.0)
        await ban_chan.delete()

        if ban_chan.content == "exit":
            e = discord.Embed(description="Cancelled!")
            return await embed.edit(embed=e)

        while not discord.utils.get(ctx.guild.channels, id=int(ban_chan.content)):
            e = discord.Embed(title="6. Channel Censoring",
                              description="Invalid Channel ID/channel already in list passed. Please try again. Type `exit` to cancel.")
            await embed.edit(embed=e)

            ban_chan_1 = await bot.wait_for('message', check=check, timeout=60.0)
            await ban_chan_1.delete()

            if ban_chan_1.content == "exit":
                e = discord.Embed(description="Command cancelled. Welcome channel was not set!")
                return await embed.edit(embed=e)
            if not ban_chan_1.content.isdigit():
                continue

            # If a CHANNEL is FOUND, break
            if discord.utils.get(ctx.guild.channels, id=int(ban_chan_1.content)):
                if ban_chan_1.content in banned_channels:
                    continue
                banned_channels.append(ban_chan_1.content)
                with open("sconfig.json", "w") as f:
                    json.dump(data, f, indent=1)
                e = discord.Embed(title="6. Channel Censoring",
                                  description=f"Added channel: <#{ban_chan_1.content}> to the list!")
                await embed.edit(embed=e)
                break

        # If channel is FOUND ...
        if discord.utils.get(ctx.guild.channels, id=int(ban_chan.content)):
            banned_channels.append(ban_chan.content)

            with open("sconfig.json", "w") as f:
                json.dump(data, f, indent=1)

            e = discord.Embed(title="6. Channel Censoring",
                              description=f"Added channel: <#{ban_chan.content}> to the list!")
            await embed.edit(embed=e)

        await asyncio.sleep(2)

        # SEVENTH STEP - WOORD CENSORING
        e = discord.Embed(title="7. Word Censoring",
                          description="Enter words you would like to censor. Type `skip` to go to the next step.")
        await embed.edit(embed=e)

        message = await bot.wait_for('message', check=check, timeout=300)
        await message.delete()

        word_list = message.content.split()
        already_in_list = []

        if message.content == "skip":
            e = discord.Embed(title="Success!",
                              description="Setup completed. No words were added to censor.")
            return await embed.edit(embed=e)

        for banned_word in word_list:
            if banned_word in banned_words:
                already_in_list.append(banned_word)
            if banned_word not in banned_words:
                banned_words.append(banned_word)

        with open("sconfig.json") as f:
            data1 = json.load(f)
        banned_words_2 = data1["server"]["banned_words"]  # no idea why it works as well

        if not already_in_list:
            with open("sconfig.json", "w") as f:
                json.dump(data, f, indent=1)

            e = discord.Embed(
                title="Censored Words", description=f":white_check_mark: Added words to the list: {', '.join([w for w in word_list])}")
            await embed.edit(embed=e)

        if already_in_list:
            if len([w for w in word_list if w not in banned_words_2]) == 0:
                e = discord.Embed(title="Censored Words",
                                  description=f":x: No words were added because they were all already in list!")
                return await embed.edit(embed=e)
            else:
                e = discord.Embed(title="Censored Words",
                                  description=f""":white_check_mark: Added words to the list: {', '.join([w for w in word_list if w not in banned_words_2])}\n\n:warning: The following words were **NOT** added because they were already in list: {', '.join([w for w in already_in_list])}
                """)
                with open("sconfig.json", "w") as f:
                    json.dump(data, f, indent=1)
                await embed.edit(embed=e)

        await asyncio.sleep(3)
        e = discord.Embed(title="Success ", description="Setup completed! :white_check_mark:")
        await embed.edit(embed=e)

    # Exceptions
    except ValueError:
        await ctx.send("Invalid input passed. Integer expected. Restarting setup...")
        await asyncio.sleep(1)
        await ctx.reinvoke()

    except asyncio.TimeoutError:
        await ctx.send("Time limit reached: 60 seconds.")


@setup.command(aliases=["c"])
@is_admin()
@commands.guild_only()
async def check(ctx):

    with open("sconfig.json") as f:
        data = json.load(f)

    prefix_2 = data["server"]["prefix"]
    banned_words_2 = data["server"]["banned_words"]
    banned_channels_2 = data["server"]["banned_channels"]
    welcome_message_2 = data["server"]["welcome_message"]
    welcome_channel_id_2 = data["server"]["welcome_channel_id"]
    role_to_give_id_2 = data["server"]["role_to_give_id"]
    access_key_2 = data["server"]["access_key"]
    access_key_channel_id_2 = data["server"]["access_key_channel_id"]
    rank_command_censor_2 = data["server"]["rank_command_censor"]
    roles_on_join_2 = data["server"]["roles_on_join"]

    nl = "\n"
    access_singular = "Password"
    access_plural = "Passwords"
    rank_enabled = "Enabled"
    rank_disabled = "Disabled"

    e = discord.Embed(title=f"{ctx.guild.name} Settings",
                      description="Check that all modules are properly set up.")

    e.add_field(name="Server Prefix", value=f"{prefix_2}", inline=False)  # PREFIX

    a_list = len([word for word in banned_words_2])
    e.add_field(name="Censoring",  # CENSORING
                value=f"Words [{a_list}]: "
                f"{', '.join([word for word in banned_words_2]) if banned_words_2 else None}{nl}"
                f"Channels [{len([channel for channel in banned_channels_2])}]: "
                f"{' '.join([(utils.get(ctx.guild.channels, id=int(channel))).mention for channel in banned_channels_2]) if banned_channels_2 else None}\n"
                f"Rank Command Censoring: **{rank_enabled if rank_command_censor_2 == 1 else rank_disabled}**", inline=False)

    e.add_field(name="Access Key",  # ACCESS KEY
                value=f"Passwords [{len([key for key in access_key_2])}]: {', '.join([key for key in access_key_2]) if access_key_2 else None}{nl}"
                f"Channel: {(utils.get(ctx.guild.channels, id=int(access_key_channel_id_2))).mention if access_key_channel_id_2 else None}", inline=False)

    e.add_field(name="Autoroles",  # AUTOROLES
                value=f"Roles [{len([role for role in roles_on_join_2])}]: "
                f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in roles_on_join_2]) if roles_on_join_2 else None}\n", inline=False)

    e.add_field(name="Welcome",  # WELCOME STUFF
                value=f"Role: {(utils.get(ctx.guild.roles, id=int(role_to_give_id_2))).mention if role_to_give_id_2 else None}\n"
                f"Channel: {(utils.get(ctx.guild.channels, id=int(welcome_channel_id_2))).mention if welcome_channel_id_2 else None}{nl}"
                f"Message:{nl}```{welcome_message_2 if welcome_message_2 else None}```{nl}", inline=False)

    await ctx.send(embed=e)


@setup.command(aliases=["r"])
@commands.guild_only()
@is_admin()
async def reset(ctx):
    msg = await ctx.send("Are you sure to want reset all the settings for this server?")
    await msg.add_reaction("\U00002705")
    await msg.add_reaction("\U0000274c")

    try:
        reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: u == ctx.author and r.message.id == msg.id, timeout=15)

        if str(reaction.emoji) == "\U00002705":
            await msg.clear_reactions()

            banned_words.clear()
            banned_channels.clear()
            access_key.clear()
            roles_on_join.clear()
            data["server"]["prefix"] = "$"
            data["server"]['welcome_channel_id'] = ""
            data["server"]['welcome_message'] = ""
            data["server"]['access_key_channel_id'] = ""
            data["server"]['role_to_give_id'] = ""
            data["server"]["rank_command_censor"] = 1

            with open("sconfig.json", "w") as f:
                json.dump(data, f, indent=1)

            await msg.edit(content=":white_check_mark: Settings were successfully reset!")

        elif str(reaction.emoji) == "\U0000274c":
            await msg.clear_reactions()
            await msg.edit(content=":x: Settings were **NOT** reset!")

    except asyncio.TimeoutError:
        await msg.clear_reactions()
        await msg.edit(content="Command cancelled due to time out.")


@setup.command(aliases=["e"])
@commands.guild_only()
@is_admin()
async def edit(ctx):

    with open("sconfig.json") as f:
        data = json.load(f)

    prefix_2 = data["server"]["prefix"]
    banned_words_2 = data["server"]["banned_words"]
    banned_channels_2 = data["server"]["banned_channels"]
    welcome_message_2 = data["server"]["welcome_message"]
    welcome_channel_id_2 = data["server"]["welcome_channel_id"]
    role_to_give_id_2 = data["server"]["role_to_give_id"]
    access_key_2 = data["server"]["access_key"]
    access_key_channel_id_2 = data["server"]["access_key_channel_id"]
    rank_command_censor_2 = data["server"]["rank_command_censor"]
    roles_on_join_2 = data["server"]["roles_on_join"]

    e = discord.Embed(
        title=f"**{ctx.guild.name}** Settings.",
        description="""
        Select a module to edit.\n\n:one: Server Prefix\n:two: Censoring \n:three: Access Key\n:four: Welcome Features\n:five: Autoroles
        """)
    e.set_footer(text="Command will be automatically cancelled in 15 seconds.")
    r_msg = await ctx.send(embed=e)

    try:
        # Reactions
        await r_msg.add_reaction("\U00000031\U000020e3")  # 1
        await r_msg.add_reaction("\U00000032\U000020e3")  # 2
        await r_msg.add_reaction("\U00000033\U000020e3")  # 3
        await r_msg.add_reaction("\U00000034\U000020e3")  # 4
        await r_msg.add_reaction("\U00000035\U000020e3")  # 5

        reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: u == ctx.author and r.message.id == r_msg.id, timeout=15)

        # IF THE REACTION IS ONE --- 1 -- SERVER PREFIX
        if str(reaction.emoji) == "\U00000031\U000020e3":

            e = discord.Embed(title="Server Prefix", description="""
            What would you like to do?\n\n:one: Change the server prefix\n:two: Exit out from this menu.
            """)
            await r_msg.edit(embed=e)

            await r_msg.remove_reaction("\U00000031\U000020e3", ctx.author)  # authors reaction
            await r_msg.remove_reaction("\U00000035\U000020e3", bot.user)  # remove 5
            await r_msg.remove_reaction("\U00000034\U000020e3", bot.user)  # remove 4
            await r_msg.remove_reaction("\U00000033\U000020e3", bot.user)  # remove 3

            reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: u == ctx.author and r.message.id == r_msg.id, timeout=15)

            if str(reaction.emoji) == "\U00000031\U000020e3":  # Change server prefix - 1
                await r_msg.clear_reactions()
                e = discord.Embed(title="Server Prefix",
                                  description="Please enter your new server prefix.")
                await r_msg.edit(embed=e)  # second edit

                # waits for msg
                server_prefix = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)

                data["server"]["prefix"] = server_prefix.content
                bot.command_prefix = commands.when_mentioned_or(server_prefix.content)
                with open("sconfig.json", "w") as f:
                    json.dump(data, f, indent=1)

                e = discord.Embed(
                    title="Server Prefix", description=f":white_check_mark: New server prefix: `{server_prefix.content}` saved!")
                await r_msg.edit(embed=e)  # third edit
                await server_prefix.delete()

            elif str(reaction.emoji) == "\U00000032\U000020e3":  # Exit from menu - 2
                await r_msg.clear_reactions()
                e = discord.Embed(description=":x: Cancelled")
                await r_msg.edit(embed=e)

        # IF REACTION IS TWO -- 2 - CENSORING
        elif str(reaction.emoji) == "\U00000032\U000020e3":  # 1
            e = discord.Embed(title="Censoring",
                              description="""Select a component of this module to edit.\n\n:one: Censored Words\n:two: Censored Channels\n:three: Rank Command Censoring
            """)
            await r_msg.edit(embed=e)

            await r_msg.remove_reaction("\U00000032\U000020e3", ctx.author)
            await r_msg.remove_reaction("\U00000035\U000020e3", bot.user)  # remove 5
            await r_msg.remove_reaction("\U00000034\U000020e3", bot.user)  # remove 4

            reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

            if str(reaction.emoji) == "\U00000031\U000020e3":  # CENSORED WORDS - 1

                e = discord.Embed(title="Censored Words", description="""What would you like to do?\n\n:one: Add words to the list\n:two: Remove words from the list\n:three: Clear the list
                """)
                await r_msg.edit(embed=e)

                await r_msg.remove_reaction("\U00000031\U000020e3", ctx.author)
                await r_msg.add_reaction("\U00000033\U000020e3")

                reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 - ADD WORDS
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Censored Words",
                                      description=f"""Add words to censor to the list. Separate them with spaces.\n\n**Words in list:** {', '.join([w for w in banned_words_2]) if banned_words_2 else None}
                    """)
                    await r_msg.edit(embed=e)

                    msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)

                    banned_list = msg.content.split()
                    already_in_list = []
                    for banned_word in banned_list:
                        if banned_word in banned_words_2:
                            already_in_list.append(banned_word)
                        if banned_word not in banned_words_2:
                            banned_words_2.append(banned_word)

                    with open("sconfig.json") as f:
                        data1 = json.load(f)
                    banned_words_2 = data1["server"]["banned_words"]  # no idea why it works as well

                    if not already_in_list:
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(
                            title="Censored Words", description=f":white_check_mark: Added words to the list: {', '.join([w for w in banned_list])}")
                        await msg.delete()
                        await r_msg.edit(embed=e)

                    elif already_in_list:
                        if len([w for w in banned_list if w not in banned_words_2]) == 0:
                            e = discord.Embed(title="Censored Words",
                                              description=f":x: No words were added because they were all already in list!")
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(title="Censored Words",
                                              description=f""":white_check_mark: Added words to the list: {', '.join([w for w in banned_list if w not in banned_words_2])}\n\n:warning: The following words were **NOT** added because they were already in list: {', '.join([w for w in already_in_list])}
                            """)
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)

                            await r_msg.edit(embed=e)
                            await msg.delete()

                elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - REMOVE WORDS
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Censored Words",
                                      description=f"""Type words to remove from the list. Separate them with spaces.\n\n**Words in list:** {', '.join([w for w in banned_words_2])}
                    """)
                    await r_msg.edit(embed=e)

                    msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)

                    banned_list = msg.content.split()
                    not_in_list = []
                    for banned_word in banned_list:
                        if banned_word not in banned_words_2:  # if not in list
                            not_in_list.append(banned_word)
                        if banned_word in banned_words_2:  # if in list
                            banned_words_2.remove(banned_word)

                    with open("sconfig.json") as f:
                        data1 = json.load(f)
                    # i have no clue why this works
                    banned_words_2 = data1["server"]["banned_words"]

                    if not not_in_list:
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(
                            title="Censored Words", description=f":white_check_mark: Removed words: {', '.join([w for w in banned_list])}")
                        await msg.delete()
                        await r_msg.edit(embed=e)

                    elif not_in_list:
                        if len([w for w in banned_list if w in banned_words_2]) == 0:
                            e = discord.Embed(title="Censored Words",
                                              description=":x: No words were removed because **NONE** of them were in the list!")
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(title="Censored Words",
                                              description=f""":white_check_mark: Removed words: {', '.join([w for w in banned_list if w in banned_words_2])}\n\n:warning: The following words were **NOT** found in the list: {', '.join([w for w in not_in_list])}
                            """)
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)

                            await r_msg.edit(embed=e)
                            await msg.delete()

                elif str(reaction.emoji) == "\U00000033\U000020e3":  # 3 - Clear list
                    await r_msg.clear_reactions()
                    e = discord.Embed(
                        title="Censored Words", description="Are you sure you want to clear the list of censored words?")
                    await r_msg.edit(embed=e)
                    await r_msg.add_reaction("\U00002705")  # checkmark
                    await r_msg.add_reaction("\U0000274c")  # x

                    reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                    if str(reaction.emoji) == "\U00002705":  # if Checkmark
                        await r_msg.clear_reactions()
                        banned_words_2.clear()
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(
                            title="Censored Words", description=":white_check_mark: List was successfully cleared!")
                        await r_msg.edit(embed=e)

                    elif str(reaction.emoji) == "\U0000274c":  # if X
                        await r_msg.clear_reactions()
                        e = discord.Embed(description="Cancelled.")
                        await r_msg.edit(embed=e)

            elif str(reaction.emoji) == "\U00000032\U000020e3":  # CENSORED CHANNELS - 2

                e = discord.Embed(title="Censored Channels",
                                  description="""Select an action to perform:\n\n:one: Add channels to censor words in\n:two: Remove channels from the list\n:three: Clear the list
                """)
                await r_msg.edit(embed=e)
                await r_msg.remove_reaction("\U00000032\U000020e3", ctx.author)
                await r_msg.add_reaction("\U00000033\U000020e3")

                reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 - ADD CHANNELS
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Censored Channels",
                                      description=f"""Enter the Channel IDs of the channels you would like to censor. Separate them with a space.\n\n**List of censored channels:** {' '.join(['<#'+c+'>'+" (ID: "+c+")" for c in banned_channels_2]) if banned_channels_2 else None}
                    """)
                    await r_msg.edit(embed=e)

                    msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)

                    channels_to_ban = msg.content.split()
                    in_list = []
                    invalid = []
                    another_list = []
                    for channel in channels_to_ban:
                        if channel in banned_channels_2:
                            in_list.append(channel)
                        elif channel not in banned_channels_2 and channel.isdigit():
                            if discord.utils.get(ctx.guild.channels, id=int(channel)):
                                banned_channels_2.append(channel)
                                another_list.append(channel)
                            else:
                                invalid.append(channel)
                        else:
                            invalid.append(channel)

                    with open("sconfig.json") as f:
                        data1 = json.load(f)
                    banned_channels_2 = data1["server"]["banned_channels"]  # JSON LOADING

                    if not in_list and not invalid:
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(
                            title="Censored Channels", description=f":white_check_mark: Added channels to the list: {' '.join(['<#'+c+'>' for c in channels_to_ban])}")
                        await msg.delete()
                        await r_msg.edit(embed=e)

                    elif invalid and not in_list:
                        if another_list:
                            e = discord.Embed(title="Censored Channels",
                                              description=f""":white_check_mark: Added channels to the list: {' '.join(['<#'+c+'>' for c in another_list])}\n\n:warning: Invalid Channel IDs found: {' '.join(['`'+c+'`' for c in invalid])}
                            """)
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(
                                title="Censored Channels", description=f':x: No channels were found.\n\nInvalid IDs passed: {" ".join(["`"+x+"`" for x in invalid])}')
                            await r_msg.edit(embed=e)
                            await msg.delete()

                    elif invalid and in_list:
                        if not another_list:
                            e = discord.Embed(title="Censored Channels",
                                              description=":x: Invalid Channel IDs passed or channels already in list.")
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(title="Censored Channels",
                                              description=f":white_check_mark: Added channels to the list: {' '.join(['<#'+c+'>' for c in another_list])}\n\n:warning: Warning" +
                                              f"""\nInvalid Channel IDs found: {' '.join(['`'+c+'`' for c in invalid])}""" +
                                              f"""\n\nThese channels already in list found: {' '.join(['`'+c+'`' for c in in_list])}""")
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)
                            await r_msg.edit(embed=e)
                            await msg.delete()

                    elif in_list:
                        if len([c for c in channels_to_ban if c not in banned_channels_2]) == 0:
                            e = discord.Embed(title="Censored Channels",
                                              description=f":x: No channels were added because they were all already in list!")
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(title="Censored Channels",
                                              description=f""":white_check_mark: Added channels to the list: {' '.join(['<#'+c+'>' for c in another_list])}\n\n:warning: The following channels were **NOT** added because they were already in list: {' '.join(['<#'+w+'>' for w in in_list])}
                            """)
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)
                            await r_msg.edit(embed=e)
                            await msg.delete()

                elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - REMOVE CHANNELS
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Censored Channels",
                                      description=f"""Enter the Channel IDs of the channels you would like to remove. Separate them with a space.\n\n**List of censored channels:** {' '.join(['<#'+c+'>'+" (ID: "+c+")" for c in banned_channels_2]) if banned_channels_2 else None}
                    """)
                    await r_msg.edit(embed=e)

                    msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)

                    # STARTS HERE ----------
                    channels_to_ban = msg.content.split()
                    not_in_list = []
                    invalid = []
                    another_list = []
                    for channel in channels_to_ban:
                        if channel not in banned_channels_2 and channel.isdigit():
                            if utils.get(ctx.guild.channels, id=int(channel)):
                                not_in_list.append(channel)
                            else:
                                invalid.append(channel)
                        elif channel in banned_channels_2:
                            banned_channels_2.remove(channel)
                            another_list.append(channel)
                        else:
                            invalid.append(channel)

                    with open("sconfig.json") as f:
                        data1 = json.load(f)
                    banned_channels_2 = data1["server"]["banned_channels"]  # JSON LOADING

                    if not not_in_list and not invalid:
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(
                            title="Censored Channels", description=f":white_check_mark: Removed channels from the list: {' '.join(['<#'+c+'>' for c in channels_to_ban])}")
                        await msg.delete()
                        await r_msg.edit(embed=e)

                    elif invalid and not not_in_list:
                        if another_list:
                            e = discord.Embed(title="Censored Channels",
                                              description=f""":white_check_mark: Removed channels from the list: {' '.join(['<#'+c+'>' for c in another_list])}\n\n:warning: Invalid Channel IDs passed: {' '.join(['`'+c+'`' for c in invalid])}
                            """)
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(
                                title="Censored Channels", description=f':x: No channels were found.\n\nInvalid IDs passed: {" ".join(["`"+x+"`" for x in invalid])}')
                            await r_msg.edit(embed=e)
                            await msg.delete()

                    elif invalid and not_in_list:
                        if not another_list:
                            e = discord.Embed(title="Censored Channels",
                                              description=":x: Invalid Channel IDs passed or channels were **NOT** found in list.")
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(title="Censored Channels",
                                              description=f":white_check_mark: Removed channels from the list: {' '.join(['<#'+c+'>' for c in another_list])}\n\n:warning: Warning" +
                                              f"""\n\nInvalid Channel IDs passed: {' '.join(['`'+c+'`' for c in invalid])}""" +
                                              f"""\n\nThese channels were **NOT** found in list: {' '.join(['`'+c+'`' for c in not_in_list])}""")
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)
                            await r_msg.edit(embed=e)
                            await msg.delete()

                    elif not_in_list:
                        if len([c for c in channels_to_ban if c not in banned_channels_2]) == 0:
                            e = discord.Embed(title="Censored Channels",
                                              description=f":x: No channels found in list!")
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(title="Censored Channels",
                                              description=f""":white_check_mark: Removed channels from the list: {' '.join(['<#'+c+'>' for c in another_list])}"""
                                              f"""\n\n:warning: The following channels were **NOT** added because they were already in list:""" +
                                              f"""{' '.join(['<#'+w+'>' for w in not_in_list])}""")
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)
                            await r_msg.edit(embed=e)
                            await msg.delete()

                elif str(reaction.emoji) == "\U00000033\U000020e3":  # 3 - Clear list of channels
                    await r_msg.clear_reactions()
                    e = discord.Embed(
                        title="Censored Channels", description="Are you sure you want to clear the list of censored channels?")
                    await r_msg.edit(embed=e)
                    await r_msg.add_reaction("\U00002705")  # checkmark
                    await r_msg.add_reaction("\U0000274c")  # x

                    reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                    if str(reaction.emoji) == "\U00002705":  # if Checkmark ----- clear channels
                        await r_msg.clear_reactions()
                        banned_channels_2.clear()
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)
                        e = discord.Embed(
                            title="Censored Channels", description=":white_check_mark: List was successfully cleared!")
                        await r_msg.edit(embed=e)

                    elif str(reaction.emoji) == "\U0000274c":  # if X ---- clear channels
                        await r_msg.clear_reactions()
                        e = discord.Embed(description=":x: Cancelled.")
                        await r_msg.edit(embed=e)

            if str(reaction.emoji) == "\U00000033\U000020e3":  # 3 - RANK COMMAND
                e = discord.Embed(title="Rank Command Censoring",
                                  description="""Select an action to perform:\n\n:one: Enable it\n:two: Disable it
                """)
                await r_msg.edit(embed=e)
                await r_msg.remove_reaction("\U00000033\U000020e3", ctx.author)
                await r_msg.remove_reaction("\U00000033\U000020e3", bot.user)

                reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 - TURN ON RANK COMMAND
                    await r_msg.clear_reactions()
                    data["server"]["rank_command_censor"] = 1  # assigns value to json
                    with open("sconfig.json", "w") as f:
                        json.dump(data, f, indent=1)
                    e = discord.Embed(title="Rank Command Censoring",
                                      description=""":white_check_mark: Rank command censoring was **enabled**!""")
                    await r_msg.edit(embed=e)

                elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - TURN OFF RANK COMMAND
                    await r_msg.clear_reactions()
                    data["server"]["rank_command_censor"] = 0      # assigns value to json
                    with open("sconfig.json", "w") as f:
                        json.dump(data, f, indent=1)
                    e = discord.Embed(title="Rank Command Censoring",
                                      description=":warning: Rank command censoring was **disabled**!")
                    await r_msg.edit(embed=e)

        # IF REACTION IS 3 - ACCESS KEY STUFF
        elif str(reaction.emoji) == "\U00000033\U000020e3":
            e = discord.Embed(title="Access Key",
                              description="Select a component of this module to edit:\n\n:one: Access Key (Password)\n:two: Access Key Channel")

            await r_msg.edit(embed=e)
            await r_msg.remove_reaction("\U00000033\U000020e3", ctx.author)  # author
            await r_msg.remove_reaction("\U00000035\U000020e3", bot.user)  # remove 5
            await r_msg.remove_reaction("\U00000034\U000020e3", bot.user)  # remove 4
            await r_msg.remove_reaction("\U00000033\U000020e3", bot.user)  # remove 3

            reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

            if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 - access key password
                e = discord.Embed(title="Access Key",
                                  description="Select an action to perform:\n\n:one: Add passwords to the list\n:two: Remove passwords from the list"
                                  "\n:three: Clear the list of passwords")
                await r_msg.edit(embed=e)
                await r_msg.remove_reaction("\U00000031\U000020e3", ctx.author)
                await r_msg.add_reaction("\U00000033\U000020e3")  # 3

                reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 ADD PASSWORDS TO LIST
                    await r_msg.clear_reactions()

                    e = discord.Embed(title="Access Key",
                                      description="Enter passwords (words) to add to the list. Separate them with spaces.\n\n **List of passwords:**"
                                      f" {', '.join([c for c in access_key_2]) if access_key_2 else None}")
                    await r_msg.edit(embed=e)

                    msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)

                    password_list = msg.content.lower().split()
                    in_list = []

                    for password in password_list:
                        if password in access_key_2:
                            in_list.append(password)
                        elif password not in access_key_2:
                            access_key_2.append(password)

                    with open("sconfig.json") as f:
                        data1 = json.load(f)
                    access_key_2 = data1["server"]["access_key"]  # JSON LOAD

                    if not in_list:
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)
                        e = discord.Embed(
                            title="Access Key", description=f":white_check_mark: Added passwords to the list: {', '.join([w for w in password_list])}")
                        await msg.delete()
                        await r_msg.edit(embed=e)

                    elif in_list:

                        # If the number of passwords passed that ARE NOT in the LIST is 0 ...
                        if len([w for w in password_list if w not in access_key_2]) == 0:
                            e = discord.Embed(title="Access Key",
                                              description=f":x: No passwords were added because they were all already in list!")
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(title="Access Key",
                                              description=f""":white_check_mark: Added passwords to the list: {', '.join([w for w in password_list if w not in access_key_2])}\n\n:warning: The following passwords were **NOT** added because they were already in list: {', '.join([w for w in in_list])}
                            """)
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)
                            await r_msg.edit(embed=e)
                            await msg.delete()

                elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - REMOVE PASSWORDS from list
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Access Key",
                                      description="Enter passwords (words) to remove from the list. Separate them with spaces.\n\n **List of passwords:**"
                                      f" {', '.join([c for c in access_key_2]) if access_key_2 else None}")
                    await r_msg.edit(embed=e)

                    msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)

                    password_list = msg.content.lower().split()
                    not_in_list = []
                    for password in password_list:
                        if password not in access_key_2:  # if not in list
                            not_in_list.append(password)
                        if password in access_key_2:  # if in list
                            access_key_2.remove(password)

                    with open("sconfig.json") as f:
                        data1 = json.load(f)
                    access_key_2 = data1["server"]["access_key"]  # i have no clue why this works

                    if not not_in_list:
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)
                        e = discord.Embed(
                            title="Access Key", description=f":white_check_mark: Removed passwords from the list: {', '.join([w for w in password_list])}")
                        await msg.delete()
                        await r_msg.edit(embed=e)

                    elif not_in_list:
                        if len([w for w in password_list if w in access_key_2]) == 0:
                            e = discord.Embed(title="Access Key",
                                              description=":x: No passwords were removed because **NONE** of them were in the list!")
                            await r_msg.edit(embed=e)
                            await msg.delete()

                        else:
                            e = discord.Embed(title="Access Key",
                                              description=f""":white_check_mark: Removed passwords from the list: {', '.join([w for w in password_list if w in access_key_2])}\n\n:warning: The following words were **NOT** found in the list: {', '.join([w for w in not_in_list])}
                            """)
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)
                            await r_msg.edit(embed=e)
                            await msg.delete()

                elif str(reaction.emoji) == "\U00000033\U000020e3":  # 3 CLEAR LIST - ACCESS KEY
                    await r_msg.clear_reactions()
                    e = discord.Embed(
                        title="Access Key", description="Are you sure you want to clear the list of passwords?")
                    await r_msg.edit(embed=e)
                    await r_msg.add_reaction("\U00002705")  # checkmark
                    await r_msg.add_reaction("\U0000274c")  # x

                    reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                    if str(reaction.emoji) == "\U00002705":  # if Checkmark ----- passwords
                        await r_msg.clear_reactions()
                        access_key_2.clear()
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(
                            title="Access Key", description=":white_check_mark: List was successfully cleared!")
                        await r_msg.edit(embed=e)

                    elif str(reaction.emoji) == "\U0000274c":  # if X ---- clear passwords
                        await r_msg.clear_reactions()
                        e = discord.Embed(description=":x: Cancelled.")
                        await r_msg.edit(embed=e)

            elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - Access Key Channel
                e = discord.Embed(title="Access Key Channel",
                                  description="Select an action to perform:\n\n:one: Set or edit the access key channel\n:two: Remove the access key channel")
                await r_msg.edit(embed=e)
                await r_msg.remove_reaction("\U00000032\U000020e3", ctx.author)
                await r_msg.remove_reaction("\U00000033\U000020e3", bot.user)

                reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 Set/edit channel  - access key channel
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Access Key Channel",
                                      description="Enter the **Channel ID** of the channel you'd like set for the Access Key.")
                    await r_msg.edit(embed=e)

                    main_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                    access_channel = main_msg.content

                    attempt = 0
                    await main_msg.delete()

                    while access_channel.isdigit():
                        if utils.get(ctx.guild.channels, id=int(access_channel)):
                            data["server"]["access_key_channel_id"] = access_channel
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)

                            e = discord.Embed(title="Access Key Channel",
                                              description=f":white_check_mark: The access key channel: <#{access_channel}> was set!")
                            await r_msg.edit(embed=e)
                            break

                        else:  # if channel is not a digit
                            while not utils.get(ctx.guild.channels, id=int(access_channel)):
                                e = discord.Embed(title="Access Key Channel",
                                                  description=":warning: Invalid Channel ID passed. Please enter a valid Channel ID.")
                                attempt = attempt+1
                                e.set_footer(text=f"Attempt #{attempt}")
                                await r_msg.edit(embed=e)

                                msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                                access_chan_2 = msg.content

                                if access_chan_2.isdigit():
                                    if utils.get(ctx.guild.channels, id=int(access_chan_2)):
                                        data["server"]["access_key_channel_id"] = access_chan_2

                                        with open("sconfig.json", "w") as f:  # saves to json
                                            json.dump(data, f, indent=1)

                                        e = discord.Embed(title="Access Key Channel",
                                                          description=f":white_check_mark: The access key channel: <#{access_chan_2}> was set!")
                                        await r_msg.edit(embed=e)
                                        await msg.delete()
                                        break
                                    else:                  # if NOT found
                                        await msg.delete()
                                        continue
                                else:                    # if it's NOT digit
                                    await msg.delete()
                                    continue
                            break

                    while not access_channel.isdigit():
                        e = discord.Embed(title="Access Key Channel",
                                          description=":warning: Invalid Channel ID passed. Please enter a valid Channel ID.")
                        attempt = attempt+1
                        e.set_footer(text=f"Attempt #{attempt}")
                        await r_msg.edit(embed=e)

                        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                        access_chan_3 = msg.content

                        if access_chan_3.isdigit():
                            if utils.get(ctx.guild.channels, id=int(access_chan_3)):
                                data["server"]["access_key_channel_id"] = access_chan_3

                                with open("sconfig.json", "w") as f:  # saves to json
                                    json.dump(data, f, indent=1)

                                e = discord.Embed(title="Access Key Channel",
                                                  description=f":white_check_mark: The access key channel: <#{access_chan_3}> was set!")
                                await r_msg.edit(embed=e)
                                await msg.delete()
                                break
                            else:
                                await msg.delete()
                                continue
                        else:
                            await msg.delete()
                            continue       # end

                elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - remove access key channel
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Access Key Channel",
                                      description="Are you sure you would like to remove the current access key channel?")
                    await r_msg.edit(embed=e)
                    await r_msg.add_reaction("\U00002705")  # checkmark
                    await r_msg.add_reaction("\U0000274c")  # X

                    reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                    if str(reaction.emoji) == "\U00002705":  # checkmark
                        await r_msg.clear_reactions()

                        data["server"]["access_key_channel_id"] = ""

                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(title="Welcome Channel",
                                          description=":white_check_mark: The welcome channel was successfully removed!")
                        await r_msg.edit(embed=e)

                    elif str(reaction.emoji) == "\U0000274c":
                        await r_msg.clear_reactions()
                        e = discord.Embed(title="Access Key Channel",
                                          description=":x: Action cancelled!")
                        await r_msg.edit(embed=e)

        # IF REACTION IS 4 -- WELCOME FEATURES
        elif str(reaction.emoji) == "\U00000034\U000020e3":
            e = discord.Embed(title="Welcome Features",
                              description="Select a component of this module to edit:\n\n:one: Welcome Channel\n:two: Welcome Message\n:three: Welcome Role")
            await r_msg.edit(embed=e)
            await r_msg.remove_reaction("\U00000034\U000020e3", ctx.author)
            await r_msg.remove_reaction("\U00000035\U000020e3", bot.user)  # remove 5
            await r_msg.remove_reaction("\U00000034\U000020e3", bot.user)  # remove 4

            reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

            if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 - Welcome Channel
                e = discord.Embed(title="Welcome Channel",
                                  description="Select an action to perform:\n\n:one: Set or edit the welcome channel\n:two: Remove the welcome channel")
                await r_msg.edit(embed=e)
                await r_msg.remove_reaction("\U00000031\U000020e3", ctx.author)
                await r_msg.remove_reaction("\U00000033\U000020e3", bot.user)

                reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 Set channel  - welcome channel
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Welcome Channel",
                                      description="Enter the **Channel ID** of the channel you'd like to set as welcome.")
                    await r_msg.edit(embed=e)

                    main_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                    welcome_channel = main_msg.content

                    attempt = 0
                    await main_msg.delete()

                    while welcome_channel.isdigit():
                        if utils.get(ctx.guild.channels, id=int(welcome_channel)):
                            data["server"]["welcome_channel_id"] = welcome_channel
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)

                            e = discord.Embed(title="Welcome Channel",
                                              description=f":white_check_mark: The welcome channel: <#{welcome_channel}> was set!")
                            await r_msg.edit(embed=e)
                            break

                        else:  # if channel is not a digit
                            while not utils.get(ctx.guild.channels, id=int(welcome_channel)):
                                e = discord.Embed(title="Welcome Channel",
                                                  description=":warning: Invalid Channel ID passed. Please enter a valid Channel ID.")
                                attempt = attempt+1
                                e.set_footer(text=f"Attempt #{attempt}")
                                await r_msg.edit(embed=e)

                                msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                                welcome_chan_2 = msg.content

                                if welcome_chan_2.isdigit():
                                    if utils.get(ctx.guild.channels, id=int(welcome_chan_2)):
                                        data["server"]["welcome_channel_id"] = welcome_chan_2

                                        with open("sconfig.json", "w") as f:  # saves to json
                                            json.dump(data, f, indent=1)

                                        e = discord.Embed(title="Welcome Channel",
                                                          description=f":white_check_mark: The welcome channel: <#{welcome_chan_2}> was set!")
                                        await r_msg.edit(embed=e)
                                        await msg.delete()
                                        break
                                    else:                  # if NOT found
                                        await msg.delete()
                                        continue
                                else:                    # if it's NOT digit
                                    await msg.delete()
                                    continue
                            break

                    while not welcome_channel.isdigit():
                        e = discord.Embed(title="Welcome Channel",
                                          description=":warning: Invalid Channel ID passed. Please enter a valid Channel ID.")
                        attempt = attempt+1
                        e.set_footer(text=f"Attempt #{attempt}")
                        await r_msg.edit(embed=e)

                        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                        welcome_chan_3 = msg.content

                        if welcome_chan_3.isdigit():
                            if utils.get(ctx.guild.channels, id=int(welcome_chan_3)):
                                data["server"]["welcome_channel_id"] = welcome_chan_3

                                with open("sconfig.json", "w") as f:  # saves to json
                                    json.dump(data, f, indent=1)

                                e = discord.Embed(title="Welcome Channel",
                                                  description=f":white_check_mark: The welcome channel: <#{welcome_chan_3}> was set!")
                                await r_msg.edit(embed=e)
                                await msg.delete()
                                break
                            else:
                                await msg.delete()
                                continue
                        else:
                            await msg.delete()
                            continue

                elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - REMOVE CHANNEL - WELCOME CHANNEL
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Welcome Channel",
                                      description="Are you sure you would like to remove the current welcome channel?")
                    await r_msg.edit(embed=e)
                    await r_msg.add_reaction("\U00002705")  # checkmark
                    await r_msg.add_reaction("\U0000274c")  # X

                    reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                    if str(reaction.emoji) == "\U00002705":  # checkmark
                        await r_msg.clear_reactions()

                        data["server"]["welcome_channel_id"] = ""

                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(title="Welcome Channel",
                                          description=":white_check_mark: The welcome channel was successfully removed!")
                        await r_msg.edit(embed=e)

                    elif str(reaction.emoji) == "\U0000274c":
                        await r_msg.clear_reactions()
                        e = discord.Embed(title="Welcome Channel",
                                          description=":x: Action cancelled!")
                        await r_msg.edit(embed=e)

            elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2  WELCOME MESSAGE
                e = discord.Embed(title="Welcome Message",
                                  description="Select an action to perform:\n\n:one: Set a welcome message\n:two: Remove the welcome message")
                await r_msg.edit(embed=e)
                await r_msg.remove_reaction("\U00000032\U000020e3", ctx.author)
                await r_msg.remove_reaction("\U00000033\U000020e3", bot.user)

                reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 - Sets welcome message
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Welcome Message",
                                      description="Enter the welcome message. Placeholders are `{server}` and `{user}`\n\nThe current welcome message is:" +
                                      f"\n```{welcome_message_2 if welcome_message_2 else None}```")
                    await r_msg.edit(embed=e)

                    w_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)

                    await w_msg.delete()

                    data["server"]["welcome_message"] = w_msg.content
                    with open("sconfig.json", "w") as f:        # saves to json
                        json.dump(data, f, indent=1)

                    e = discord.Embed(title="Welcome Message",
                                      description=f":white_check_mark: Successfully set welcome message:\n\n```{w_msg.content}```")
                    await r_msg.edit(embed=e)

                elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - clear welcome message - welcome message
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Welcome Message",
                                      description="Are you sure you would like to remove the current welcome channel?")
                    await r_msg.edit(embed=e)
                    await r_msg.add_reaction("\U00002705")  # checkmark
                    await r_msg.add_reaction("\U0000274c")  # X

                    reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                    if str(reaction.emoji) == "\U00002705":  # checkmark
                        await r_msg.clear_reactions()
                        data["server"]["welcome_message"] = ""
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(title="Welcome Message",
                                          description=":white_check_mark: The welcome channel was successfully removed!")
                        await r_msg.edit(embed=e)

                    elif str(reaction.emoji) == "\U0000274c":
                        await r_msg.clear_reactions()
                        e = discord.Embed(title="Welcome Message",
                                          description=":x: Action cancelled!")
                        await r_msg.edit(embed=e)  # end of two

            elif str(reaction.emoji) == "\U00000033\U000020e3":  # 3 - WELCOME ROLE - welcome features
                e = discord.Embed(title="Welcome Role",
                                  description="Select an action to perform:\n\n:one: Set or edit the welcome role\n:two: Remove the welcome role")
                await r_msg.edit(embed=e)
                await r_msg.remove_reaction("\U00000033\U000020e3", ctx.author)
                await r_msg.remove_reaction("\U00000033\U000020e3", bot.user)

                reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 SET ROLE  - welcome role
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Welcome Role",
                                      description="Enter the Welcome's **Role ID**.")
                    await r_msg.edit(embed=e)

                    main_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                    welcome_role = main_msg.content

                    attempt = 0
                    await main_msg.delete()

                    while welcome_role.isdigit():
                        if utils.get(ctx.guild.roles, id=int(welcome_role)):
                            data["server"]["role_to_give_id"] = welcome_role
                            with open("sconfig.json", "w") as f:
                                json.dump(data, f, indent=1)

                            e = discord.Embed(title="Welcome Role",
                                              description=f":white_check_mark: The welcome role: `{(utils.get(ctx.guild.roles, id=int(welcome_role))).name}` was set!")
                            await r_msg.edit(embed=e)
                            break

                        else:  # if ROLE is not a digit
                            while not utils.get(ctx.guild.roles, id=int(welcome_role)):
                                e = discord.Embed(title="Welcome Role",
                                                  description=":warning: Invalid Role ID passed. Please enter a valid **Role ID**.")
                                attempt = attempt+1
                                e.set_footer(text=f"Attempt #{attempt}")
                                await r_msg.edit(embed=e)

                                msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                                welcome_role_2 = msg.content

                                if welcome_role_2.isdigit():
                                    if utils.get(ctx.guild.roles, id=int(welcome_role_2)):
                                        data["server"]["role_to_give_id"] = welcome_role_2

                                        with open("sconfig.json", "w") as f:  # saves to json
                                            json.dump(data, f, indent=1)

                                        e = discord.Embed(title="Welcome Role",
                                                          description=f":white_check_mark: The welcome role: `{(utils.get(ctx.guild.roles, id=int(welcome_role_2))).name}` was set!")
                                        await r_msg.edit(embed=e)
                                        await msg.delete()
                                        break
                                    else:                  # if NOT found
                                        await msg.delete()
                                        continue
                                else:                    # if it's NOT digit
                                    await msg.delete()
                                    continue
                            break

                    while not welcome_role.isdigit():
                        e = discord.Embed(title="Welcome Role",
                                          description=":warning: Invalid Role ID passed. Please enter a valid **Role ID**.")
                        attempt = attempt+1
                        e.set_footer(text=f"Attempt #{attempt}")
                        await r_msg.edit(embed=e)

                        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                        welcome_role_3 = msg.content

                        if welcome_role_3.isdigit():
                            if utils.get(ctx.guild.roles, id=int(welcome_role_3)):
                                data["server"]["role_to_give_id"] = welcome_role_3

                                with open("sconfig.json", "w") as f:  # saves to json
                                    json.dump(data, f, indent=1)

                                e = discord.Embed(title="Welcome Role",
                                                  description=f":white_check_mark: The welcome role: `{(utils.get(ctx.guild.roles, id=int(welcome_role_3))).name}` was set!")
                                await r_msg.edit(embed=e)
                                await msg.delete()
                                break
                            else:
                                await msg.delete()
                                continue
                        else:
                            await msg.delete()
                            continue            # END of snippet

                elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - Clear welcome ROLE - welcome
                    await r_msg.clear_reactions()
                    e = discord.Embed(title="Welcome Role",
                                      description="Are you sure you would like to remove the current welcome role?")
                    await r_msg.edit(embed=e)
                    await r_msg.add_reaction("\U00002705")  # checkmark
                    await r_msg.add_reaction("\U0000274c")  # X

                    reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                    if str(reaction.emoji) == "\U00002705":  # checkmark
                        await r_msg.clear_reactions()
                        data["server"]["role_to_give_id"] = ""
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)

                        e = discord.Embed(title="Welcome Role",
                                          description=":white_check_mark: The welcome role was successfully removed!")
                        await r_msg.edit(embed=e)

                    elif str(reaction.emoji) == "\U0000274c":
                        await r_msg.clear_reactions()
                        e = discord.Embed(title="Welcome Role",
                                          description=":x: Action cancelled!")
                        await r_msg.edit(embed=e)  # end

        # IF REACTION IS 5 -- AUTOROLES
        elif str(reaction.emoji) == "\U00000035\U000020e3":
            e = discord.Embed(title="Autoroles",
                              description="Select an action to perform:\n\n:one: Add roles\n:two: Remove roles\n:three: Clear the list of roles")
            await r_msg.edit(embed=e)
            await r_msg.remove_reaction("\U00000035\U000020e3", ctx.author)
            await r_msg.remove_reaction("\U00000035\U000020e3", bot.user)  # remove 5
            await r_msg.remove_reaction("\U00000034\U000020e3", bot.user)  # remove 4

            reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

            if str(reaction.emoji) == "\U00000031\U000020e3":  # 1 - ADD ROLES - autoroles
                await r_msg.clear_reactions()

                e = discord.Embed(title="Autoroles",
                                  description="Enter the roles' **IDs** to assign to new members. Separate them with a space."
                                  "You can get a role's ID via: `\@Role`")
                await r_msg.edit(embed=e)

                message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                roles = message.content.split()
                await message.delete()

                in_list = []
                invalid = []
                another_list = []
                for role in roles:
                    if role in roles_on_join_2:
                        in_list.append(role)
                    elif role not in roles_on_join_2 and role.isdigit():
                        if utils.get(ctx.guild.roles, id=int(role)):
                            roles_on_join_2.append(role)
                            another_list.append(role)
                        else:
                            invalid.append(role)
                    else:
                        invalid.append(role)

                with open("sconfig.json") as f:
                    data1 = json.load(f)
                roles_on_join_2 = data1["server"]["roles_on_join"]  # JSON LOADING

                if not in_list and not invalid:
                    with open("sconfig.json", "w") as f:
                        json.dump(data, f, indent=1)

                    e = discord.Embed(title="Autoroles", description=f":white_check_mark: Added roles to the list: "
                                      f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in roles])}")
                    await r_msg.edit(embed=e)

                elif invalid and not in_list:
                    if another_list:
                        e = discord.Embed(title="Autoroles",
                                          description=f":white_check_mark: Added roles to the list:"
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in another_list])}\n\n"
                                          f":warning: Invalid Role IDs found: {' '.join(['`'+i+'`' for i in invalid])}")
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)
                        await r_msg.edit(embed=e)
                    else:
                        e = discord.Embed(
                            title="Autoroles", description=f':x: No roles were found.\n\nInvalid IDs passed: {" ".join(["`"+x+"`" for x in invalid])}')
                        await r_msg.edit(embed=e)

                elif invalid and in_list:
                    if not another_list:
                        e = discord.Embed(title="Autoroles",
                                          description=":x: Invalid Role IDs passed or roles were already in list.")
                        await r_msg.edit(embed=e)
                    else:
                        e = discord.Embed(title="Autoroles",
                                          description=f":white_check_mark: Added roles to the list: "
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in another_list])}\n\n:warning: Warning"
                                          f"\nInvalid Channel IDs found: {' '.join(['`'+c+'`' for c in invalid])}"
                                          f"\n\nThese channels already in list found: "
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in in_list])}")

                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)
                        await r_msg.edit(embed=e)

                elif in_list:
                    if len([role for role in roles if role not in roles_on_join_2]) == 0:
                        e = discord.Embed(title="Autoroles",
                                          description=f":x: No roles were added because they were all already in list!")
                        await r_msg.edit(embed=e)
                    else:
                        e = discord.Embed(title="Autoroles",
                                          description=f":white_check_mark: Added roles to the list: "
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in another_list])}\n\n"
                                          f":warning: The following roles were **NOT** added because they were already in list:"
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in in_list])}")

                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)
                        await r_msg.edit(embed=e)

            elif str(reaction.emoji) == "\U00000032\U000020e3":  # 2 - REMOVE ROLES - autoroles
                await r_msg.clear_reactions()
                e = discord.Embed(title="Autoroles",
                                  description=f"Enter the Role IDs you would like to remove. Separate them with a space.\n\n**List of autoroles:** "
                                  f"""
                {' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention +" (ID: "+role+")" for role in roles_on_join_2]) if roles_on_join_2 else None}
                """)
                await r_msg.edit(embed=e)

                msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
                roles = msg.content.split()
                await msg.delete()

                # STARTS HERE ----------
                not_in_list = []
                invalid = []
                another_list = []
                for role in roles:
                    if role not in roles_on_join_2 and role.isdigit():
                        if utils.get(ctx.guild.roles, id=int(role)):
                            not_in_list.append(role)
                        else:
                            invalid.append(role)
                    elif role in roles_on_join_2:
                        roles_on_join_2.remove(role)
                        another_list.append(role)
                    else:
                        invalid.append(role)

                with open("sconfig.json") as f:
                    data1 = json.load(f)
                roles_on_join_2 = data1["server"]["roles_on_join"]  # JSON LOADING

                if not not_in_list and not invalid:
                    with open("sconfig.json", "w") as f:
                        json.dump(data, f, indent=1)

                    e = discord.Embed(title="Autoroles",
                                      description=f":white_check_mark: Removed roles from the list: "
                                      f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in roles])}")
                    await r_msg.edit(embed=e)

                elif invalid and not not_in_list:
                    if another_list:
                        e = discord.Embed(title="Autoroles",
                                          description=f":white_check_mark: Removed roles from the list: "
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in another_list])}\n\n"
                                          f":warning: Invalid Channel IDs passed: {' '.join(['`'+i+'`' for i in invalid])}")
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)
                        await r_msg.edit(embed=e)
                    else:
                        e = discord.Embed(
                            title="Autoroles", description=f':x: No roles were found.\n\nInvalid IDs passed: {" ".join(["`"+x+"`" for x in invalid])}')
                        await r_msg.edit(embed=e)

                elif invalid and not_in_list:
                    if not another_list:
                        e = discord.Embed(title="Autoroles",
                                          description=":x: Invalid Role IDs passed or roles were **NOT** found in list.")
                        await r_msg.edit(embed=e)

                    else:
                        e = discord.Embed(title="Autoroles",
                                          description=f":white_check_mark: Removed roles from the list: "
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in another_list])}\n\n:warning: Warning"
                                          f"\n\nInvalid Role IDs passed: {' '.join(['`'+c+'`' for c in invalid])}"
                                          f"\n\nThese roles were **NOT** found in list: "
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in not_in_list])}")
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)
                        await r_msg.edit(embed=e)

                elif not_in_list:
                    if len([role for role in roles if role not in roles_on_join_2]) == 0:
                        e = discord.Embed(title="Autoroles",
                                          description=f":x: No channels found in list!")
                        await r_msg.edit(embed=e)
                    else:
                        e = discord.Embed(title="Autoroles",
                                          description=f":white_check_mark: Removed roles from the list: "
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in another_list])}"
                                          f"\n\n:warning: The following roles were **NOT** added because they were already in list: "
                                          f"{' '.join([(utils.get(ctx.guild.roles, id=int(role))).mention for role in not_in_list])}")
                        with open("sconfig.json", "w") as f:
                            json.dump(data, f, indent=1)
                        await r_msg.edit(embed=e)

            elif str(reaction.emoji) == "\U00000033\U000020e3":  # 3 - CLEAR ROLES - autoroles
                await r_msg.clear_reactions()
                e = discord.Embed(
                    title="Autoroles", description="Are you sure you want to clear the list of autoroles?")
                await r_msg.edit(embed=e)
                await r_msg.add_reaction("\U00002705")  # checkmark
                await r_msg.add_reaction("\U0000274c")  # x

                reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: r.message.id == r_msg.id and u == ctx.author, timeout=15)

                if str(reaction.emoji) == "\U00002705":  # if Checkmark ----- clear roles
                    await r_msg.clear_reactions()
                    roles_on_join_2.clear()
                    with open("sconfig.json", "w") as f:
                        json.dump(data, f, indent=1)
                    e = discord.Embed(
                        title="Autoroles", description=":white_check_mark: List was successfully cleared!")
                    await r_msg.edit(embed=e)

                elif str(reaction.emoji) == "\U0000274c":  # if X ---- clear roles
                    await r_msg.clear_reactions()
                    e = discord.Embed(description=":x: Cancelled.")
                    await r_msg.edit(embed=e)

    except ValueError:
        pass

    except asyncio.TimeoutError:
        await r_msg.edit(embed=None, content="Timed out.")
        await r_msg.clear_reactions()


@bot.command()
async def ping(ctx):
    ping_1 = time.perf_counter()
    message = await ctx.send("Calculating...")
    ping_2 = time.perf_counter()
    await message.edit(content=f"Ping: **{round((ping_2-ping_1)*1000)}ms** | Websocket: **{round(bot.latency*1000)}ms**")


# Load cogs ...
if __name__ == '__main__':
    cogs = [x.stem for x in Path('cogs').glob('*.py')]
    for extension in cogs:
        try:
            bot.load_extension(f'cogs.{extension}')
            print(f'Loaded {extension}')
        except Exception as e:
            error = f'{extension}\n {type(e).__name__} : {e}'
            print(f'failed to load extension {error}')
        print('-' * 10)


bot.run(data["token"])
