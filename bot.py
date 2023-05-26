import discord
from discord import ui
from discord import app_commands
from discord import Intents
import datetime
from datetime import datetime
from discord import app_commands, utils

intents = Intents.default()
intents.message_content = True
intents.guild_messages = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False
        self.added = False
        self.mod = 841791743049728061
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 841778954880417812))
            self.synced = True
        if not self.added:
            self.add_view(TicketLaunch())
            self.add_view(main())
            self.added=True      
    async def on_message(self, message):
        if "🐟" in message.content:
            await message.add_reaction("🦈")
            await message.add_reaction("😋")
        if client.user.mentioned_in(message):
            await message.add_reaction("❤️")
            await message.channel.send("🦈")
        if message.channel.id == 1084312319510712340:
            await message.add_reaction("👍")
            await message.add_reaction("👎")
        elif message.channel.id == 841780113636982794:
            await message.add_reaction("🐛")
        elif message.channel.id == 850769936708141056:
            await message.add_reaction("⚠️")
           
    


client = MyClient()
tree = app_commands.CommandTree(client)

class BugModal(discord.ui.Modal, title="Bug Report"):
    Game = ui.TextInput(label="Game Name", placeholder="Airsoft FE or Quickscope Simulator, Etc..", style=discord.TextStyle.short,required=True)
    BugTitle = ui.TextInput(label="Bug Title", placeholder="Type a brief description of the Bug", style=discord.TextStyle.short,required=True)
    BugDescription = ui.TextInput(label="Describe the Bug", placeholder="Give a detailed explanation of the bug and how to recreate it (if possible).", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thank you for submitting a bug report!", ephemeral=True)
        embed= discord.Embed(title=(f"{self.BugTitle}"), description=(f"{self.BugDescription}"),color=0x206694, timestamp=datetime.now())
        embed.add_field(name="Game", value=(f"{self.Game}"), inline=False)
        embed.add_field(name="Bug Report made by", value=(f"{interaction.user.mention}"), inline=False)
        channel = client.get_channel(841780113636982794)
        await channel.send(embed=embed)

class ReportModal(discord.ui.Modal, title="Player Report"):
    PlayerName = ui.TextInput(label="Player username", placeholder="Put the username of the player, not the display name.", style=discord.TextStyle.short,required=True)
    GameName = ui.TextInput(label="Game Name", placeholder="Airsoft FE or Quickscope Simulator, Etc..", style=discord.TextStyle.short,required=True)
    ReportTitle = ui.TextInput(label="Report Title", placeholder="Type a title for the report", style=discord.TextStyle.short,required=True)
    ReportDescription = ui.TextInput(label="Report Description", placeholder="Please describe what the player was doing and provide an image or video url.", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thank you for filing a report!", ephemeral=True)
        embed= discord.Embed(title=(f"{self.ReportTitle}"), description=(f"{self.ReportDescription}"),color=0x206694, timestamp=datetime.now())
        embed.add_field(name="Player Name", value=(f"{self.PlayerName}"), inline=False)
        embed.add_field(name="Game", value=(f"{self.GameName}"), inline=False)
        embed.add_field(name="Player Report made by", value=(f"{interaction.user.mention}"), inline=False)
        channel = client.get_channel(850769936708141056)
        await channel.send(embed=embed)


class SuggestionModal(discord.ui.Modal, title="Suggestion"):
    Suggestion = ui.TextInput(label="Suggestion", placeholder="Type a brief description of your suggestion for a game or for the server", style=discord.TextStyle.short,required=True)
    SuggestionDetails = ui.TextInput(label="Describe your suggestion", placeholder="Elaborate on your suggestion (Optional)", style=discord.TextStyle.paragraph, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thank you for submitting a suggestion!", ephemeral=True)
        embed= discord.Embed(title=(f"{self.Suggestion}"), description=(f"{self.SuggestionDetails}"),color=0x206694, timestamp=datetime.now())
        embed.add_field(name="Suggested by", value=f"{interaction.user.mention}", inline=False)
        channel = client.get_channel(1084312319510712340)
        await channel.send(embed=embed)
        
class TicketLaunch(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.blurple, custom_id="ticket_button")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = utils.get(interaction.guild.text_channels, name=f"ticket-{interaction.user.name}-{interaction.user.discriminator}")
        if ticket is not None: await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!", ephemeral=True)
        else:
            if type(client.mod) is not discord.Role:
                client.mod = interaction.guild.get_role(841791743049728061)
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True),
                client.mod: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
            }
            channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}-{interaction.user.discriminator}", overwrites = overwrites, reason=f"Ticket for {interaction.user}")
            await channel.send(f"{interaction.user.mention} created a ticket!", view=main())
            await interaction.response.send_message(f"Your ticket has been created! {channel.mention}!", ephemeral=True)

class confirm(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Confirm", style= discord.ButtonStyle.red, custom_id="confirm")
    async def confirm_button(self, interaction, button):
        try: await interaction.channel.delete()
        except: await interaction.response.send_message("Channel deletion failed! Insufficent permissions.")

class main(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Close Ticket", style= discord.ButtonStyle.red, custom_id="close")
    async def close(self, interaction, button):
        embed = discord.Embed(title="Are you sure you want to close this ticket?", color = discord.Color.blurple())
        await interaction.response.send_message(embed=embed, view=confirm(), ephemeral = True)




@tree.command(name = "games", description = "Get a quick list of games made by Jetshark Studios!", guild = discord.Object(id = 841778954880417812))
async def self (interaction: discord.Interaction):
    message_text = "Airsoft FE:\n"
    message_text += "https://www.roblox.com/games/6792057800/Airsoft-FE-ALPHA"
    message_text += " \n"
    message_text += "Quickscope Simulator:\n"
    message_text += "https://www.roblox.com/games/9084086006/GunFrameTest"
    message_text += " \n"
    message_text += "Operation Airsoft:\n"
    message_text += "https://www.roblox.com/games/8779836160/Operation-Airsoft"

    await interaction.response.send_message(message_text, ephemeral=True)
@tree.command(name="bug-report", description="File a bug report for one of our games.", guild=discord.Object(id = 841778954880417812))
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(BugModal())
@tree.command(name="player-report", description="File a player report for one of our games.", guild=discord.Object(id = 841778954880417812))
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(ReportModal())
@tree.command(name="suggestion", description="Create a suggestion for one of our games or the server.", guild=discord.Object(id = 841778954880417812))
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(SuggestionModal())
@tree.command(name="ticket", description="Creates a ticket for support or questions", guild=discord.Object(id = 841778954880417812))
@app_commands.default_permissions(manage_guild=True)
async def ticketing(interaction: discord.Interaction):
    embed = discord.Embed(title="If you need support, click the button below and create a ticket!", color = discord.Color.blue())
    await interaction.channel.send(embed=embed, view=TicketLaunch())
    await interaction.response.send_message("Creating ticket!", ephemeral=True)
@tree.command(name="close-ticket", description="Closes the ticket", guild=discord.Object(id = 841778954880417812))
@app_commands.default_permissions(manage_guild=True)
async def close(interaction: discord.Interaction):
    if "ticket-" in interaction.channel.name:
        embed = discord.Embed(title="Are you sure you want to close this ticket?", color = discord.Color.blurple())
        await interaction.channel.send(embed=embed, view=confirm())
    else: await interaction.response.send_message("No ticket found!", ephemeral=True)


client.run('token')
