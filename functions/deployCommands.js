const { REST, Routes } = require("discord.js");
const fs = require("node:fs");

// Changes path based on environment
require("dotenv").config({ path: `.env.${process.env.NODE_ENV}` });

// Environemnt variables
const TOKEN = process.env.BOT_TOKEN;
const CLIENT_ID = process.env.CLIENT_ID;
const GUILD_ID = process.env.GUILD_ID;

const commands = [];

const commandFiles = fs
  .readdirSync("./commands")
  .filter((file) => file.endsWith(".js"));

for (const file of commandFiles) {
  const command = require(`../commands/${file}`);
  commands.push(command.data.toJSON());
}
//
const rest = new REST({ version: "10" }).setToken(TOKEN);

// Deploys all commands
(async () => {
  try {
    console.log(
      `Started refreshing ${commands.length} application (/) commands.`
    );

    let data;
    if (process.env.NODE_ENV === "production") {
      data = await rest.put(Routes.applicationCommands(CLIENT_ID), {
        body: commands,
      });
    } else {
      data = await rest.put(
        Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID),
        {
          body: commands,
        }
      );
    }

    console.log(
      `Successfully reloaded ${data.length} application (/) commands.`
    );
  } catch (error) {
    console.error(error);
  }
})();
