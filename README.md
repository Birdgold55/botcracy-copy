# Botcracy

Botcracy è un bot per Discord che simula una democrazia: i membri possono
proporre leggi e votare per approvarle o abrogarle. Il bot usa comandi slash e
un'interfaccia interamente in italiano.

## Funzionalità

- `/aiuto` — mostra i comandi disponibili.
- `/legge-crea` — propone una legge e avvia la votazione.
- `/legge-abroga` — propone l'abrogazione di una legge.
- `/legge` — mostra i dettagli e i risultati della votazione di una legge.
- `/leggi` — mostra le leggi in vigore nel server.

Ogni membro può esprimere un voto per votazione: se cambia reazione, viene
conteggiato il voto più recente. Le votazioni durano un minuto e richiedono
almeno un voto. Per modificare questi valori, cambia `VOTING_DURATION` e
`MINIMUM_VOTES` in `bot.py`.

## Requisiti

Python 3.10 o versione successiva e un database MongoDB.

## Installazione e avvio

1. Clona il repository, crea un ambiente virtuale e installa le dipendenze:

   ```sh
   git clone https://github.com/Birdgold55/botcracy-copy.git
   cd botcracy-copy
   python -m venv .venv
   ```

   Attiva l'ambiente virtuale:

   ```powershell
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```

   ```sh
   # macOS o Linux
   source .venv/bin/activate
   ```

2. Installa le dipendenze:

   ```sh
   python -m pip install -r requirements.txt
   ```

3. Crea un file `.env` nella cartella principale del progetto:

   ```env
   BOT_TOKEN=inserisci-il-token-del-bot
   CONNECTION_URL=inserisci-lindirizzo-del-database-mongodb
   BOT_ENV=development
   GUILD_ID=inserisci-lid-del-server-discord
   ```

   `BOT_TOKEN` si crea nel portale sviluppatori di Discord. `CONNECTION_URL` è
   l'indirizzo del database MongoDB e deve includere il nome del database.
   Durante lo sviluppo, `BOT_ENV=development` registra i comandi nel server
   indicato da `GUILD_ID`. Per registrarli globalmente, imposta
   `BOT_ENV=production`; la loro propagazione può richiedere tempo.

4. Avvia il bot:

   ```sh
   python bot.py
   ```

Per aggiungere il bot a un server, abilita gli ambiti `bot` e
`applications.commands` e concedigli i permessi per inviare messaggi e aggiungere
reazioni. Non pubblicare né condividere il token o il file `.env`.

## Dati e privacy

Le leggi vengono salvate nella raccolta MongoDB `active-laws`. Per ogni legge
sono conservati il server, il nome, la descrizione, l'ID Discord del proponente,
la data di approvazione e i risultati della votazione. Il bot legge anche i
vecchi dati salvati con il formato numerico degli ID server.
