const {
  ActionRowBuilder,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle,
} = require("discord.js");
const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("create-law")
    .setDescription("Starts the voting process for creating a new law"),
  async execute(interaction) {
    const modal = new ModalBuilder()
      .setCustomId("createLawModal")
      .setTitle("Law Creator");

    const lawNameInput = new TextInputBuilder()
      .setCustomId("lawNameInput")
      .setLabel("What is the law name?")
      .setStyle(TextInputStyle.Short)
      .setRequired(true);

    const lawDescriptionInput = new TextInputBuilder()
      .setCustomId("lawDescriptionInput")
      .setLabel("Provide a description of what the law does.")
      .setStyle(TextInputStyle.Paragraph)
      .setRequired(true);

    const firstActionRow = new ActionRowBuilder().addComponents(lawNameInput);
    const secondActionRow = new ActionRowBuilder().addComponents(
      lawDescriptionInput
    );
    modal.addComponents(firstActionRow, secondActionRow);

    // Show the modal to the user
    await interaction.showModal(modal);
  },
};
