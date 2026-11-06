const mongoose = require("mongoose");

const law = mongoose.model("active-laws", {
  guildID: {
    type: Number,
    required: true,
  },
  guildName: {
    type: String,
    required: true,
    trim: true,
  },
  name: {
    type: String,
    required: true,
    trim: true,
    lowercase: true,
  },
  description: {
    type: String,
    required: true,
    trim: true,
    default: "No description provided",
    lowercase: true,
  },
  representative: {
    type: Number,
    required: true,
    trim: true,
  },
  createdDate: {
    type: Date,
    required: true,
    default: Date.now,
  },
  totalVotes: {
    type: Number,
    required: true,
    default: 0,
    validate(value) {
      if (value < 0) {
        throw new Error("Amount of votes must be a positive number");
      }
    },
  },
  yes: {
    type: Number,
    required: true,
    default: 0,
  },
  no: {
    type: Number,
    required: true,
    default: 0,
  },
});

module.exports = law;
