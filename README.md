# Botcracy
Botcracy is a discord bot that simulates a government and allows users to vote on roles, create new laws and more.

## Table of Contents
- [Botcracy Overview](#botcracy-overview)
  * [Commands](#commands)
  * [Invite to server](#invite-to-server)
  * [Resources](#resources)
- [Developers](#developers)
  * [Installation](#installation)
  * [Development](#installation)

## Botcracy Overview

### Commands
- #help - DM's all bot commands to member
- #create-law - Stars the process on creating a new law
- #repeal-law - Starts the process to repeal a law
- #executive-order - Creates a new executive order - Requires the President role
- #register-to-vote - Gives the member the voter role - Will be required for voting in the future
- #voter-count - Provides the number of members with the voter role

### Invite to server
https://discord.com/api/oauth2/authorize?client_id=783942469581537280&permissions=397553032256&scope=bot%20applications.commands

### Resources
- Website - https://www.botcracy.com/
- top.gg - https://top.gg/bot/783942469581537280
- discord.bots.gg - https://discord.bots.gg/bots/783942469581537280
- discordbotlist - https://discordbotlist.com/bots/botcracy

- Discord.js Documentation - https://discord.js.org/#/docs/discord.js/main/general/welcome
- Trello Board - https://trello.com/b/zcYAlAjQ/development

## Developers

### Installation

Clone the repository `git clone https://github.com/rjthacker/botcracy.git`

Verify that you are running `Node v18.12.0` or higher with `node -v`

Run `npm ci && npm i nodemon`

Request `.env` files, once aquired they will need to be placed in `root` directory

### Development

`npm run prod` for production testing bot

`npm run dev` for development testing bot
