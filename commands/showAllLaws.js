const { SlashCommandBuilder } = require("@discordjs/builders");

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
    .setName("show-all-laws")
    .setDescription("Provides information about all laws"),
  async execute(interaction) {
    lawModel
      .find({ guildID: interaction.guild.id })
      .then(function (law) {
        let fields = [];
        for (let i = 0; i < law.length; i++) {
          fields.push({
            name: capitalizeFirstLetters(law[i].name),
            value: capitalizeFirstLetter(law[i].description),
          });
        }

        const lawEmbed = {
          color: 0x0099ff,
          author: {
            name: `${interaction.guild.name}'s law book`,
          },
          thumbnail: {
            url: interaction.guild.iconURL(),
          },
          fields,
        };

        interaction.reply({ embeds: [lawEmbed], ephemeral: true });
      })
      .catch(function (error) {
        console.log(error);
        interaction.reply("That law does not exist!");
      });
  },
};
