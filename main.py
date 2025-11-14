import discord
from discord.ext import commands
import json
from datetime import datetime
import os
import webserver
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# --- Configuración base ---
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Datos ---
contadores = {}
canal_contador_id = None
rol_autorizado = None
canal_logs_id = None

# --- Guardar / Cargar ---
def guardar():
    with open("contadores.json", "w") as f:
        json.dump({
            "contadores": contadores,
            "canal_id": canal_contador_id,
            "rol_autorizado": rol_autorizado,
            "canal_logs": canal_logs_id
        }, f, indent=4)

def cargar():
    global contadores, canal_contador_id, rol_autorizado, canal_logs_id
    try:
        with open("contadores.json", "r") as f:
            data = json.load(f)
            contadores = data.get("contadores", {})
            canal_contador_id = data.get("canal_id")
            rol_autorizado = data.get("rol_autorizado")
            canal_logs_id = data.get("canal_logs")
    except FileNotFoundError:
        contadores = {}
        canal_contador_id = None
        rol_autorizado = None
        canal_logs_id = None

# --- Función de permiso ---
def tiene_permiso(user: discord.Member):
    if user.guild_permissions.manage_guild:
        return True
    if rol_autorizado:
        for rol in user.roles:
            if rol.name == rol_autorizado:
                return True
    return False

# --- Log de acciones ---
async def enviar_log(guild: discord.Guild, mensaje: str):
    if not canal_logs_id:
        return
    canal = guild.get_channel(canal_logs_id)
    if canal:
        embed = discord.Embed(
            description=mensaje,
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Registro de contadores")
        await canal.send(embed=embed)

# --- Crear embed de contadores ---
def crear_embed():
    embed = discord.Embed(
        title="🧮 Contadores del servidor",
        color=discord.Color.green()
    )
    if not contadores:
        embed.description = "📭 **No hay contadores creados todavía.**"
    else:
        for nombre, valor in contadores.items():
            embed.add_field(name=f"➡️ {nombre}", value=f"**{valor}**", inline=False)
    embed.set_footer(text="Usa los botones o comandos si tienes permiso.")
    return embed

# --- Vista con botones interactivos ---
class ContadorView(discord.ui.View):
    def __init__(self, nombre):
        super().__init__(timeout=None)
        self.nombre = nombre

    async def verificar_permiso(self, interaction: discord.Interaction):
        if not tiene_permiso(interaction.user):
            await interaction.response.send_message("🚫 No tienes permiso para usar este botón.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="➕ Sumar", style=discord.ButtonStyle.green)
    async def sumar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.verificar_permiso(interaction): return
        contadores[self.nombre] += 1
        guardar()
        await enviar_log(interaction.guild, f"🔼 **{interaction.user.display_name}** sumó 1 al contador **{self.nombre}** → `{contadores[self.nombre]}`")
        await interaction.response.send_message(f"🔼 **{self.nombre}** ahora vale **{contadores[self.nombre]}**", ephemeral=True)
        await actualizar_mensaje(interaction.guild)

    @discord.ui.button(label="➖ Restar", style=discord.ButtonStyle.blurple)
    async def restar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.verificar_permiso(interaction): return
        contadores[self.nombre] -= 1
        guardar()
        await enviar_log(interaction.guild, f"🔽 **{interaction.user.display_name}** restó 1 al contador **{self.nombre}** → `{contadores[self.nombre]}`")
        await interaction.response.send_message(f"🔽 **{self.nombre}** ahora vale **{contadores[self.nombre]}**", ephemeral=True)
        await actualizar_mensaje(interaction.guild)

    @discord.ui.button(label="🔁 Resetear", style=discord.ButtonStyle.gray)
    async def resetear(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.verificar_permiso(interaction): return
        contadores[self.nombre] = 0
        guardar()
        await enviar_log(interaction.guild, f"🔁 **{interaction.user.display_name}** reseteó el contador **{self.nombre}** a `0`")
        await interaction.response.send_message(f"🔄 **{self.nombre}** ha sido reseteado a **0**", ephemeral=True)
        await actualizar_mensaje(interaction.guild)

    @discord.ui.button(label="❌ Eliminar", style=discord.ButtonStyle.red)
    async def eliminar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.verificar_permiso(interaction): return
        del contadores[self.nombre]
        guardar()
        await enviar_log(interaction.guild, f"🗑️ **{interaction.user.display_name}** eliminó el contador **{self.nombre}**")
        await interaction.response.send_message(f"🗑️ Contador **{self.nombre}** eliminado.", ephemeral=True)
        await actualizar_mensaje(interaction.guild)

# --- Actualizar el panel principal ---
async def actualizar_mensaje(guild: discord.Guild):
    if not canal_contador_id:
        return
    canal = guild.get_channel(canal_contador_id)
    if not canal:
        return

    embed = crear_embed()
    async for msg in canal.history(limit=20):
        if msg.author == bot.user:
            await msg.delete()

    await canal.send(embed=embed)
    for nombre in contadores.keys():
        await canal.send(f"**{nombre}**", view=ContadorView(nombre))

# --- Eventos ---
@bot.event
async def on_ready():
    cargar()
    print(f"✅ Bot conectado como {bot.user}")
    for guild in bot.guilds:
        await actualizar_mensaje(guild)

# --- Comandos ---
@bot.command()
async def set_canal(ctx, canal: discord.TextChannel):
    """Define el canal donde se mostrarán los contadores."""
    if not tiene_permiso(ctx.author):
        await ctx.send("🚫 No tienes permiso para hacer eso.")
        return
    global canal_contador_id
    canal_contador_id = canal.id
    guardar()
    await ctx.send(f"✅ Canal configurado: {canal.mention}")
    await enviar_log(ctx.guild, f"⚙️ **{ctx.author.display_name}** configuró el canal de contadores: {canal.mention}")
    await actualizar_mensaje(ctx.guild)

@bot.command()
async def set_logs(ctx, canal: discord.TextChannel):
    """Configura el canal donde se enviarán los registros."""
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send("🚫 Solo los administradores pueden usar este comando.")
        return
    global canal_logs_id
    canal_logs_id = canal.id
    guardar()
    await ctx.send(f"✅ Canal de logs configurado: {canal.mention}")
    await enviar_log(ctx.guild, f"🪵 **{ctx.author.display_name}** configuró este canal para los registros.")

@bot.command()
async def set_rol(ctx, *, nombre_rol: str):
    """Define el rol autorizado para administrar contadores."""
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send("🚫 Solo los administradores pueden usar este comando.")
        return
    global rol_autorizado
    rol_autorizado = nombre_rol
    guardar()
    await ctx.send(f"✅ Rol autorizado configurado: **{nombre_rol}**")
    await enviar_log(ctx.guild, f"⚙️ **{ctx.author.display_name}** estableció el rol autorizado: `{nombre_rol}`")

@bot.command()
async def crear_contador(ctx, nombre: str, valor_inicial: int = 0):
    """Crea un contador nuevo."""
    if not tiene_permiso(ctx.author):
        await ctx.send("🚫 No tienes permiso para crear contadores.")
        return
    if nombre in contadores:
        await ctx.send("⚠️ Ese contador ya existe.")
        return
    contadores[nombre] = valor_inicial
    guardar()
    await ctx.send(f"📊 Contador **{nombre}** creado con valor inicial {valor_inicial}")
    await enviar_log(ctx.guild, f"🆕 **{ctx.author.display_name}** creó el contador **{nombre}** con valor `{valor_inicial}`")
    await actualizar_mensaje(ctx.guild)

@bot.command()
async def ver(ctx):
    """Muestra el estado actual de los contadores."""
    await ctx.send(embed=crear_embed())

@bot.command()
async def resetear(ctx, nombre: str = None):
    """Resetea un contador o todos."""
    if not tiene_permiso(ctx.author):
        await ctx.send("🚫 No tienes permiso para resetear contadores.")
        return
    global contadores
    if not contadores:
        await ctx.send("📭 No hay contadores.")
        return
    if nombre:
        if nombre not in contadores:
            await ctx.send("❌ Ese contador no existe.")
            return
        contadores[nombre] = 0
        await ctx.send(f"🔄 El contador **{nombre}** se ha reseteado a **0**.")
        await enviar_log(ctx.guild, f"🔁 **{ctx.author.display_name}** reseteó el contador **{nombre}** a `0`")
    else:
        for n in contadores.keys():
            contadores[n] = 0
        await ctx.send("🧹 Todos los contadores se han reseteado a **0**.")
        await enviar_log(ctx.guild, f"🧹 **{ctx.author.display_name}** reseteó todos los contadores.")
    guardar()
    await actualizar_mensaje(ctx.guild)

webserver.keep_alive()
bot.run("DISCORD_TOKEN")
