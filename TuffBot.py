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
        
        # Hafıza veritabanı (Bot kapanırsa sıfırlanmaması için ID'leri manuel girebilirsin)
        self.trap_channel_id = None
        self.panel_message_id = None
        self.ban_count = 0

bot = AntiScamBot()

# SPECIAL_OWNER_ID: Kendi Discord ID'ni buraya yaz (s!sync komutunu sadece sen kullanabil diye)
SPECIAL_OWNER_ID = 1424590067577655358  

# ==========================================
# MODERN EMBED OLUŞTURUCU (MODERN GOLD AESTHETIC)
# ==========================================
def create_scam_embed(ban_count):
    embed = discord.Embed(
        title="⚠️ SECURITY WARNING: HONEYPOT TRAP ⚠️",
        description=(
            "**DO NOT TALK HERE, UNLESS YOU WANT TO GET BANNED FROM THIS SERVER**\n\n"
            "This channel is created to catch compromised (hacked) accounts.\n"
            "Saying anything will get you **INSTANTLY BANNED**.\n\n"
            " We will not unban you if you decide to 'troll' around.\n"
            "*No second chances, this will be your problem, not ours.*"
        ),
        color=discord.Color.from_rgb(212, 175, 55) # Modern Gold / Altın Sarısı Rengi
    )
    
    # Alt kısım (Footer) ve şık bir alan ile ban sayısını gösterme
    embed.add_field(name="🛡️ Total Caught Accounts", value=f"```fix\nBans : {ban_count}\n
```", inline=False)
    embed.set_footer(text="Shadow Security System • Automated Protection", icon_url=bot.user.avatar.url if bot.user.avatar else None)
    return embed

# ==========================================
# EVENTS (TUZAK KONTROLÜ)
# ==========================================
@bot.event
async def on_ready():
    print(f"[{bot.user.name}] Anti-Scam Botu aktif! 's!sync' yazarak komutları yükleyin.")

@bot.event
async def on_message(message):
    # Eğer mesajı atan botsa veya tuzak kanalı henüz ayarlanmadıysa işlemi geç
    if message.author.bot or not bot.trap_channel_id:
        return

    # Eğer mesaj tuzak kanala yazıldıysa
    if message.channel.id == bot.trap_channel_id:
        try:
            # Önce yazılan mesajı sil
            await message.delete()
            
            # Kullanıcıyı sunucudan banla
            await message.author.ban(reason="Anti-Scam Honeypot Trap: Sent a message in restricted channel.")
            
            # Ban sayısını 1 arttır
            bot.ban_count += 1
            
            # Mevcut paneli bul ve yeni ban sayısıyla GÜNCELLE (Mesaj silip yenisini atmaz)
            if bot.panel_message_id:
                try:
                    panel_msg = await message.channel.fetch_message(bot.panel_message_id)
                    new_embed = create_scam_embed(bot.ban_count)
                    await panel_msg.edit(embed=new_embed)
                except Exception as e:
                    print(f"Panel güncellenirken hata oluştu (Mesaj silinmiş olabilir): {e}")
                    
        except discord.Forbidden:
            print(f"Hata: {message.author.name} banlanamadı. Botun yetkisi yetersiz veya rol hiyerarşisi düşük!")
        except Exception as e:
            print(f"Beklenmedik bir hata oluştu: {e}")

    await bot.process_commands(message)

# ==========================================
# SLASH COMMAND (/anti-scam)
# ==========================================
@bot.tree.command(name="anti-scam", description="Seçilen kanalı modern bir tuzak kanalına dönüştürür.")
@app_commands.describe(kanal="Tuzak mesajının atılacağı ve yazanların banlanacağı kanal")
@app_commands.checks.has_permissions(administrator=True) # Sadece Yönetici yetkisi olanlar kullanabilir
async def anti_scam_setup(interaction: discord.Interaction, kanal: discord.TextChannel):
    await interaction.response.defer(ephemeral=True)
    
    bot.trap_channel_id = kanal.id
    bot.ban_count = 0 # Yeni kurulumda ban sayısını sıfırla
    
    # Modern Altın Tasarımlı Embed'i oluşturup kanala gönderiyoruz
    embed = create_scam_embed(bot.ban_count)
    panel_message = await kanal.send(embed=embed)
    
    # Mesaj ID'sini hafızaya kaydediyoruz ki ileride güncelleyebilelim
    bot.panel_message_id = panel_message.id
    
    await interaction.followup.send(f"✅ Başarıyla ayarlandı! {kanal.mention} artık aktif bir tuzak kanalı. İlk panel mesajı gönderildi.", ephemeral=True)

# ==========================================
# SENKRONİZASYON KOMUTU
# ==========================================
@bot.command(name="sync")
async def sync_commands(ctx):
    if ctx.author.id != SPECIAL_OWNER_ID and ctx.author.id != ctx.guild.owner_id: 
        return
    await ctx.send("🔄 **Komutlar senkronize ediliyor...**")
    try:
        await bot.tree.sync()
        await ctx.send("✅ **Başarılı!** `/anti-scam` komutu yüklendi.")
    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

# ==========================================
# ÇALIŞTIRMA ALANI
# ==========================================
if __name__ == "__main__":
    # Flask uptime thread başlatılıyor
    t = Thread(target=run_flask)
    t.start()
    
    # Botu çalıştır (Render panelinde DISCORD_TOKEN kısmına tokenını girmelisin)
    bot.run(os.getenv("DISCORD_TOKEN"))
