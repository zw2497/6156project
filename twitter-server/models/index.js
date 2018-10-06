const mongoose = require("mongoose");
mongoose.set("debug", true);
mongoose.set('useCreateIndex', true);
mongoose.Promise = Promise;
mongoose.connect("mongodb://localhost:27017/twitter", {
    keepAlive: true,
    useNewUrlParser: true
});

module.exports.User = require("./user");
module.exports.Message = require("./message");

