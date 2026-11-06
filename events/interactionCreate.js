const { Events } = require("discord.js");
const { createLaw, repealLaw } = require("../functions/voting");

module.exports = {
  name: Events.InteractionCreate,
  async execute(interaction) {
    if (interaction.isChatInputCommand()) {
      const command = interaction.client.commands.get(interaction.commandName);

      if (!command) {
        console.error(
          `No command matching ${interaction.commandName} was found.`
        );
        return;
      }

      try {
        await command.execute(interaction);
      } catch (error) {
        console.error(`Error executing ${interaction.commandName}`);
        console.error(error);
      }
    }

    if (interaction.isModalSubmit()) {
      if (interaction.customId === "createLawModal") {
        createLaw(interaction);
      } else if (interaction.customId === "repealLawModal") {
        repealLaw(interaction);
      }
    }
  },
};
