const crypto = require('crypto');
const buf = crypto.randomBytes(32);
console.log(buf.toString('hex'));