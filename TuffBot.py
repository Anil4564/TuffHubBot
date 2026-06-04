import discord
from discord import app_commands
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ==========================================
# FLASK SUNUCUSU (RENDER 7/24 UPTIME İÇİN)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "TuffHubBot is Alive"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ==========================================
# BOT YAPILANDIRMASI
# ==========================================
class AntiScamBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Mesajları okumak için şart
        intents.guilds = True
        intents.moderation = True       # Ban atabilmesi için şart
        super().__init__(command_prefix="s!", intents=intents)
        
        self.trap_channel_id = None
        self.panel_message_id = None
        self.ban_count = 0

bot = AntiScamBot()

# SPECIAL_OWNER_ID: Kendi Discord ID'ni buraya yazabilirsin
SPECIAL_OWNER_ID = 1424590067577655358  

# ==========================================
# MODERN EMBED OLUŞTURUCU (MODERN GOLD AESTHETIC)
# ==========================================
def create_scam_embed(ban_count):
    embed = discord.Embed(
        title="⚠️ SECURITY WARNING: HONEYPOT TRAP ⚠️",
        description=(
            "**DO NOT TALK HERE, UNLESS YOU WANT TO GET BANNED FROM THIS SERVER**\n\n"
            "THIS CHANNEL IS CREATED TO CATCH COMPROMISED ACCOUNTS\n"
            "SAYING ANYTHING WILL GET YOU BANNED\n\n"
            "WE WILL NOT UNBAN YOU IF YOU DECIDE TO \"TROLL\" AROUND\n"
            "NO SECOND CHANCES, THIS WILL BE YOUR PROBLEM, NOT OURS"
        ),
        color=discord.Color.from_rgb(212, 175, 55) # Modern Gold Rengi
    )
    
    # Hata veren alan tamamen tek satırda güvenli hale getirildi
    embed.add_field(name="🛡️ Total Caught Accounts", value=f"
http://googleusercontent.com/immersive_entry_chip/0
