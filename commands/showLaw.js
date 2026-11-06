const { SlashCommandBuilder } = require("@discordjs/builders");
const moment = require("moment");

const lawModel = require("../src/models/law");

function capitalizeFirstLetters(str) {
  return str.replace(/^\w|\s\w/g, function (letter) {
    return letter.toUpperCase();
  });
}

function capitalizeFirstLetter(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

module.exports = {
  data: new SlashCommandBuilder()
    .setName("show-law")
    .setDescription("Provides information about a law")
    .addStringOption((option) =>
      option
        .setName("law-name")
        .setDescription("Shows information on specific law")
        .setRequired(true)
    ),
  async execute(interaction) {
    lawModel
      .find({
        guildID: interaction.guild.id,
        name: interaction.options.getString("law-name").toLowerCase(),
      })
      .then(function (law) {
        const lawEmbed = {
          color: 0x0099ff,
          author: {
            name: `${interaction.guild.name}'s' law book`,
          },
          thumbnail: {
            url: interaction.guild.iconURL(),
          },
          fields: [
            {
              name: "Name",
              value: capitalizeFirstLetters(law[0].name),
            },
            {
              name: "Description",
              value: capitalizeFirstLetter(law[0].description),
            },
            {
              name: "Representative ",
              value: law[0].representative,
            },
            {
              name: "Date Passed",
              value: moment(law[0].createdDate).format("dddd, MMMM Do YYYY"),
              inline: false,
            },
          ],
        };
        interaction.reply({ embeds: [lawEmbed], ephemeral: true });
      })
      .catch(function (error) {
        console.log(error);
        interaction.reply("That law does not exist!");
      });
  },
};
