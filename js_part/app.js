const crypto = require("crypto");

const algorithm = "aes-256-cbc";

const initVector = crypto.randomBytes(16).toString('hex');

console.log(initVector);

// const message = "This is a secret message";

const SecurityKey = crypto.randomBytes(32).toString('hex');

console.log(SecurityKey);

// const cipher = crypto.createCipheriv(algorithm, SecurityKey, initVector);

// let encryptedData = cipher.update(message, "utf-8", "hex");

// encryptedData += cipher.final("hex");

// console.log("Encrypted message: " + encryptedData);
