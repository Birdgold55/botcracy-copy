const mongoose = require('mongoose');

const settings = mongoose.model('settings', {
  guildID: {
    type: Number,
    required: true,
  },
  votingTime: {
    type: Number,
    required: true,
    default: 60000,
  },
  lawRequiredVotes: {
    type: Number,
    required: true,
    default: 1,
  },
  roleRequiredVotes: {
    type: Number,
    required: true,
    default: 1,
  },
  presidentRequiredVotes: {
    type: Number,
    required: true,
    default: 1,
  },
});

module.exports = settings;
