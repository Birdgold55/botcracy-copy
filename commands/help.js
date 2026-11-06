const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("help")
    .setDescription("Provides info about Botcracy"),
  async execute(interaction) {
    await interaction.reply({
      content: `**Greetings!**\n\nWe are excited to announce that Botcracy is undergoing a complete rebuild utilizing the latest Discord API and Discord.js Version 14. This will allow us to implement new slash commands and enhance the overall user experience.\n\nHowever, please note that this process may take some time as we work to update all existing commands.\n\nTo stay informed on our progress and receive updates, we invite you to join the Botcracy Discord server: https://discord.gg/5XFCa65S5F`,
      ephemeral: true,
    });
  },
};
