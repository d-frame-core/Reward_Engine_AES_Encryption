const crypto = require("crypto");

const algorithm = "aes-256-cbc";

const initVector = crypto.randomBytes(32).toString("base64");

console.log(initVector);

const SecurityKey = crypto.randomBytes(32).toString("base64");

console.log(SecurityKey);
