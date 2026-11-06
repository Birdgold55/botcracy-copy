const mongoose = require('mongoose');

const showLaws = mongoose.model('active-laws', {
  guildID: {
    type: Number,
    required: true,
  },
  guildName: {
    type: String,
    required: true,
    trim: true,
  },
  description: {
    type: String,
    required: true,
    trim: true,
    default: 'No description provided',
  },
  votes: {
    type: Number,
    required: true,
    default: 0,
    validate(value) {
      if (value < 0) {
        throw new Error('Amount of votes must be a positive number');
      }
    },
  },
});

module.exports = showLaws;
