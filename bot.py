import asyncio
import importlib.util
import logging
import os
import sqlite3
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


PROJECT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_FILE = PROJECT_DIR / "requirements.txt"
ENV_FILE = PROJECT_DIR / ".env"
DATABASE_FILE = PROJECT_DIR / "leggi.sqlite3"


def install_dependencies_if_needed() -> None:
    if importlib.util.find_spec("discord") is not None and importlib.util.find_spec(
        "dotenv"
    ) is not None:
        return

    print("Installazione delle librerie necessarie al primo avvio...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            "Non riesco a installare le librerie. Controlla la connessione "
            "Internet e riprova."
        ) from error


def create_environment_file_if_needed() -> None:
    if ENV_FILE.exists():
        return

    ENV_FILE.write_text(
        "BOT_TOKEN=\nBOT_ENV=production\nGUILD_ID=\n",
        encoding="utf-8",
    )
    print(
        "Ho creato il file .env. Aprilo con Blocco note, inserisci il token "
        "del bot Discord dopo BOT_TOKEN=, salva il file e rilancia py bot.py."
    )
    raise SystemExit(0)


install_dependencies_if_needed()

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv(ENV_FILE)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("botcracy")

VOTING_DURATION = 60
MINIMUM_VOTES = 1
YES_EMOJI = "👍"
NO_EMOJI = "👎"

TOKEN = os.getenv("BOT_TOKEN")
BOT_ENV = os.getenv("BOT_ENV", os.getenv("NODE_ENV", "production")).lower()
GUILD_ID = os.getenv("GUILD_ID")

create_environment_file_if_needed()

if not TOKEN or not TOKEN.strip():
    raise RuntimeError(
        "Il token BOT_TOKEN non è impostato. Apri il file .env, inserisci "
        "il token del bot Discord dopo BOT_TOKEN= e rilancia py bot.py."
    )
if BOT_ENV == "development" and not GUILD_ID:
    raise RuntimeError("Imposta GUILD_ID per registrare i comandi di sviluppo.")

intents = discord.Intents.default()
intents.guilds = True
intents.guild_reactions = True


@contextmanager
def connect_database() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> None:
    with connect_database() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS leggi (
                id INTEGER PRIMARY KEY,
                guild_id TEXT NOT NULL,
                guild_name TEXT NOT NULL,
                name TEXT NOT NULL COLLATE NOCASE,
                description TEXT NOT NULL,
                representative TEXT NOT NULL,
                created_date TEXT NOT NULL,
                total_votes INTEGER NOT NULL,
                yes INTEGER NOT NULL,
                no INTEGER NOT NULL,
                UNIQUE (guild_id, name)
            )
            """
        )


async def find_laws(guild_id: int, name: str | None = None) -> list[dict]:
    def query_database() -> list[dict]:
        with connect_database() as connection:
            if name is None:
                cursor = connection.execute(
                    "SELECT * FROM leggi WHERE guild_id = ? ORDER BY name",
                    (str(guild_id),),
                )
            else:
                cursor = connection.execute(
                    "SELECT * FROM leggi WHERE guild_id = ? AND name = ?",
                    (str(guild_id), name.strip()),
                )
            return [dict(row) for row in cursor.fetchall()]

    return await asyncio.to_thread(query_database)


async def save_law(law: dict) -> None:
    def insert_law() -> None:
        with connect_database() as connection:
            connection.execute(
                """
                INSERT INTO leggi (
                    guild_id, guild_name, name, description, representative,
                    created_date, total_votes, yes, no
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    law["guild_id"],
                    law["guild_name"],
                    law["name"],
                    law["description"],
                    law["representative"],
                    law["created_date"],
                    law["total_votes"],
                    law["yes"],
                    law["no"],
                ),
            )

    await asyncio.to_thread(insert_law)


async def remove_law(law_id) -> None:
    def delete_law() -> None:
        with connect_database() as connection:
            connection.execute("DELETE FROM leggi WHERE id = ?", (law_id,))

    await asyncio.to_thread(delete_law)


class Botcracy(commands.Bot):
    async def setup_hook(self) -> None:
        await asyncio.to_thread(initialize_database)

        if BOT_ENV == "development" and GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
        else:
            synced = await self.tree.sync()
        logger.info("Registrati %s comandi slash.", len(synced))


bot = Botcracy(command_prefix=commands.when_mentioned, intents=intents)


async def report_interaction_error(
    interaction: discord.Interaction, error: Exception
) -> None:
    logger.error(
        "Errore durante un'interazione Discord.",
        exc_info=(type(error), error, error.__traceback__),
    )
    message = "Si è verificato un errore. Riprova più tardi."
    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


async def run_vote(
    interaction: discord.Interaction,
    title: str,
    description: str,
    action: str,
) -> tuple[int, int, int]:
    await interaction.response.send_message(
        f"{interaction.user.mention} propone di {action} **{title}**.\n"
        f"{description}\n\nLa votazione dura {VOTING_DURATION} secondi. "
        f"Reagisci con {YES_EMOJI} per votare a favore o {NO_EMOJI} per votare contro."
    )
    announcement = await interaction.original_response()
    await announcement.add_reaction(YES_EMOJI)
    await announcement.add_reaction(NO_EMOJI)

    votes: dict[int, str] = {}
    deadline = asyncio.get_running_loop().time() + VOTING_DURATION

    while True:
        remaining = deadline - asyncio.get_running_loop().time()
        if remaining <= 0:
            break
        try:
            reaction, user = await bot.wait_for(
                "reaction_add",
                timeout=remaining,
                check=lambda reaction, user: (
                    reaction.message.id == announcement.id
                    and not user.bot
                    and str(reaction.emoji) in (YES_EMOJI, NO_EMOJI)
                ),
            )
        except asyncio.TimeoutError:
            break
        votes[user.id] = str(reaction.emoji)

    yes_votes = sum(vote == YES_EMOJI for vote in votes.values())
    no_votes = sum(vote == NO_EMOJI for vote in votes.values())
    return yes_votes, no_votes, len(votes)


def vote_result(yes_votes: int, no_votes: int, total: int) -> str:
    if total < MINIMUM_VOTES:
        return "insufficiente"
    if yes_votes > no_votes:
        return "approvata"
    if yes_votes < no_votes:
        return "respinta"
    return "parità"


class CreateLawModal(discord.ui.Modal, title="Proponi una legge"):
    name = discord.ui.TextInput(
        label="Nome della legge",
        max_length=100,
        placeholder="Es. Tutela dei parchi",
    )
    description = discord.ui.TextInput(
        label="Descrizione",
        style=discord.TextStyle.paragraph,
        max_length=1000,
        placeholder="Descrivi cosa prevede la legge.",
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        existing = await find_laws(interaction.guild_id, str(self.name))
        if existing:
            await interaction.response.send_message(
                "Esiste già una legge con questo nome.", ephemeral=True
            )
            return

        yes_votes, no_votes, total = await run_vote(
            interaction,
            str(self.name),
            str(self.description),
            "approvare la legge",
        )
        result = vote_result(yes_votes, no_votes, total)
        if result == "approvata":
            await save_law(
                {
                    "guild_id": str(interaction.guild_id),
                    "guild_name": interaction.guild.name,
                    "name": str(self.name).strip().lower(),
                    "description": str(self.description).strip(),
                    "representative": str(interaction.user.id),
                    "created_date": datetime.now(timezone.utc).isoformat(),
                    "total_votes": total,
                    "yes": yes_votes,
                    "no": no_votes,
                }
            )
            message = f"La legge **{self.name}** è stata approvata ed è ora in vigore!"
        elif result == "insufficiente":
            message = f"Votazione annullata: era necessario almeno {MINIMUM_VOTES} voto."
        elif result == "parità":
            message = f"La votazione sulla legge **{self.name}** è finita in parità."
        else:
            message = f"La legge **{self.name}** è stata respinta."
        await interaction.followup.send(
            f"{message} Risultato: {yes_votes} a favore, {no_votes} contrari."
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        await report_interaction_error(interaction, error)


class RepealLawModal(discord.ui.Modal, title="Proponi l'abrogazione"):
    name = discord.ui.TextInput(
        label="Nome della legge da abrogare",
        max_length=100,
        placeholder="Inserisci il nome esatto della legge.",
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        existing = await find_laws(interaction.guild_id, str(self.name))
        if not existing:
            await interaction.response.send_message(
                "Non trovo una legge con questo nome.", ephemeral=True
            )
            return

        yes_votes, no_votes, total = await run_vote(
            interaction,
            str(self.name),
            "Vota per decidere se abrogare questa legge.",
            "abrogare la legge",
        )
        result = vote_result(yes_votes, no_votes, total)
        if result == "approvata":
            await remove_law(existing[0]["id"])
            message = f"La legge **{self.name}** è stata abrogata."
        elif result == "insufficiente":
            message = f"Votazione annullata: era necessario almeno {MINIMUM_VOTES} voto."
        elif result == "parità":
            message = f"La votazione per abrogare **{self.name}** è finita in parità."
        else:
            message = f"La proposta di abrogare **{self.name}** è stata respinta."
        await interaction.followup.send(
            f"{message} Risultato: {yes_votes} a favore, {no_votes} contrari."
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        await report_interaction_error(interaction, error)


@bot.event
async def on_ready() -> None:
    logger.info("Bot avviato come %s.", bot.user)


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
) -> None:
    await report_interaction_error(interaction, error)


@bot.tree.command(name="aiuto", description="Mostra i comandi disponibili.")
async def help_command(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(
        "**Comandi di Botcracy**\n"
        "• `/legge-crea` — proponi una legge e avvia una votazione.\n"
        "• `/legge-abroga` — proponi l'abrogazione di una legge.\n"
        "• `/legge` — consulta una legge in vigore.\n"
        "• `/leggi` — consulta il registro delle leggi del server.",
        ephemeral=True,
    )


@bot.tree.command(name="legge-crea", description="Proponi una nuova legge.")
async def create_law_command(interaction: discord.Interaction) -> None:
    if interaction.guild is None:
        await interaction.response.send_message(
            "Questo comando è disponibile solo in un server.", ephemeral=True
        )
        return
    await interaction.response.send_modal(CreateLawModal())


@bot.tree.command(name="legge-abroga", description="Proponi l'abrogazione di una legge.")
async def repeal_law_command(interaction: discord.Interaction) -> None:
    if interaction.guild is None:
        await interaction.response.send_message(
            "Questo comando è disponibile solo in un server.", ephemeral=True
        )
        return
    await interaction.response.send_modal(RepealLawModal())


@bot.tree.command(name="legge", description="Mostra i dettagli di una legge.")
@app_commands.describe(nome="Nome della legge da consultare")
async def show_law_command(
    interaction: discord.Interaction, nome: str
) -> None:
    if interaction.guild is None:
        await interaction.response.send_message(
            "Questo comando è disponibile solo in un server.", ephemeral=True
        )
        return
    await interaction.response.defer(ephemeral=True)
    laws = await find_laws(interaction.guild_id, nome)
    if not laws:
        await interaction.followup.send("Non trovo una legge con questo nome.")
        return
    law = laws[0]
    date_value = law.get("created_date")
    try:
        date_text = datetime.fromisoformat(date_value).strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        date_text = "Data non disponibile"
    embed = discord.Embed(
        title=law.get("name", "Legge").title(),
        description=law.get("description", "Nessuna descrizione.")[:4096],
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Proponente", value=str(law.get("representative", "Sconosciuto")))
    embed.add_field(name="Approvata il", value=date_text)
    embed.add_field(
        name="Voti",
        value=f"{law.get('yes', 0)} a favore · {law.get('no', 0)} contrari",
        inline=False,
    )
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="leggi", description="Mostra le leggi in vigore nel server.")
async def show_laws_command(interaction: discord.Interaction) -> None:
    if interaction.guild is None:
        await interaction.response.send_message(
            "Questo comando è disponibile solo in un server.", ephemeral=True
        )
        return
    await interaction.response.defer(ephemeral=True)
    laws = await find_laws(interaction.guild_id)
    if not laws:
        await interaction.followup.send("Il registro non contiene ancora leggi.")
        return

    embeds = []
    for offset in range(0, len(laws), 5):
        embed = discord.Embed(
            title=f"Registro delle leggi di {interaction.guild.name}",
            color=discord.Color.blurple(),
        )
        for law in laws[offset : offset + 5]:
            embed.add_field(
                name=law.get("name", "Legge").title()[:256],
                value=law.get("description", "Nessuna descrizione.")[:1024],
                inline=False,
            )
        embeds.append(embed)
    for offset in range(0, len(embeds), 10):
        await interaction.followup.send(embeds=embeds[offset : offset + 10])


if __name__ == "__main__":
    create_environment_file_if_needed()
    bot.run(TOKEN)
