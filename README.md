# Botcracy

Botcracy è un bot per Discord che simula una democrazia: i membri possono
proporre leggi e votare per approvarle o abrogarle. Comandi e messaggi del bot
sono in italiano.

## Funzionalità

- `/aiuto` — mostra i comandi disponibili.
- `/legge-crea` — propone una legge e avvia la votazione.
- `/legge-abroga` — propone l'abrogazione di una legge.
- `/legge` — mostra i dettagli e i risultati della votazione di una legge.
- `/leggi` — mostra le leggi in vigore nel server.

Ogni membro può votare una volta; se cambia idea reagendo con l'altra emoji,
viene conteggiato il voto più recente. Le votazioni durano un minuto e richiedono
almeno un voto. Per modificare questi valori, cambia `VOTING_DURATION` e
`MINIMUM_VOTES` in `bot.py`.

## Scarica e avvia su Windows

1. Scarica il progetto come archivio ZIP dal pulsante **Code → Download ZIP**
   su GitHub ed estrailo in una cartella.
2. Nel portale sviluppatori di Discord, crea un'applicazione, aggiungi un bot
   e copia il suo token.
3. Apri il **Prompt dei comandi** nella cartella estratta. Al primo avvio, il
   bot installa le librerie necessarie e crea il file `.env` se non esiste:

   ```cmd
   py bot.py
   ```

4. Apri `.env` con Blocco note, inserisci il token dopo `BOT_TOKEN=`, salva e
   rilancia `py bot.py`. Non racchiudere il token tra virgolette e non
   condividerlo.
5. Invita il bot nel tuo server Discord abilitando gli ambiti `bot` e
   `applications.commands` e i permessi per inviare messaggi e aggiungere
   reazioni.

Serve Python 3.10 o successivo, installato da
[python.org](https://www.python.org/downloads/) con il comando `py` disponibile.
Al primo avvio è necessaria una connessione Internet per installare le librerie.
I comandi slash vengono registrati globalmente e Discord potrebbe impiegare un
po' di tempo a mostrarli.

## Database e privacy

Non serve configurare MongoDB o un servizio esterno: le leggi vengono salvate
automaticamente nel file locale `leggi.sqlite3`. Il file rimane nella cartella
del bot, anche dopo averlo chiuso. Non pubblicare il token o il file `.env`.
Se ospiti il bot su un servizio online, assicurati che conservi il file del
database tra un riavvio e l'altro.

## Dati e privacy

Le leggi vengono salvate nella raccolta MongoDB `active-laws`. Per ogni legge
sono conservati il server, il nome, la descrizione, l'ID Discord del proponente,
la data di approvazione e i risultati della votazione. Il bot legge anche i
vecchi dati salvati con il formato numerico degli ID server.
