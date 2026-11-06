const { ActivityType } = require("discord.js");
const { Events } = require("discord.js");

module.exports = {
  name: Events.ClientReady,
  once: true,
  execute(client) {
    client.user.setPresence({
      // activities: [{ name: `Being Updated`, type: ActivityType.Playing }],
      status: "online",
    });
    console.log(`Logged in as ${client.user.tag}!`);
    console.log(`I am in ${client.guilds.cache.size} servers`);
  },
};
