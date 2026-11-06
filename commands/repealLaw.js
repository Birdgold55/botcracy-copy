const {
  ActionRowBuilder,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle,
} = require("discord.js");
const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("repeal-law")
    .setDescription("Starts the voting process for repealing a law"),
  async execute(interaction) {
    const modal = new ModalBuilder()
      .setCustomId("repealLawModal")
      .setTitle("Repeal Law");

    const lawNameInput = new TextInputBuilder()
      .setCustomId("lawNameInput")
      .setLabel("What is the law name?")
      .setStyle(TextInputStyle.Short)
      .setRequired(true);

    const firstActionRow = new ActionRowBuilder().addComponents(lawNameInput);

    modal.addComponents(firstActionRow);

    // Show the modal to the user
    await interaction.showModal(modal);
  },
};
