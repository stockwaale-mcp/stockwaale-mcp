const { StockwaaleClient } = require("../index.js");

const client = new StockwaaleClient();

client.price("RELIANCE")
  .then((result) => console.log(JSON.stringify(result, null, 2)))
  .catch((error) => {
    console.error(error.message);
    process.exit(1);
  });
