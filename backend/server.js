const fs = require("fs");
const url = require("url");
const path = require("path");
const querystring = require("querystring");

const { spawn } = require("child_process");

const PORT = process.env.PORT || 8080;
const PY_PROC = "python3";

const searcher = spawn(PY_PROC, ["crawl.py"], {
  "stdio": [ "pipe", "pipe", "inherit" ],
});

const wolfram = spawn(PY_PROC, ["wolfram_proxy.py"], {
  "stdio": [ "pipe", "pipe", "inherit" ],
});

let onData = null;
let wolfOnData = null;

searcher.stdout.on("data", data => {
  if (onData) onData(data);
});

wolfram.stdout.on("data", data => {
  if (wolfOnData) wolfOnData(data);
});

(async () => {
  await startSearch();

  require("http").createServer((req, res) => {
    const parsed = url.parse(req.url);
    const args = querystring.parse(parsed.query);

    const reorderStr = args.reorder;

    if (reorderStr !== undefined) {
      const reorder = JSON.parse(reorderStr);
      console.log(reorder, req.url);

      wolfOnData = data => {
        data = data.toString().trim();

        if (data.startsWith("OUT"))
          data = data.slice(3);

        if (data.endsWith("DONE")) {
          data = data.slice(0, -4);
          wolfOnData = null;
          res.writeHead(200, { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type", "Content-Type": "text/plain" });
          res.end(data);
        }
        else {
          res.write(data);
        }
      };

      wolfram.stdin.write(reorderStr);
      wolfram.stdin.write("\n");
    }
    else {
      const q = args.q;
      const uri = args.url;

      console.log(q, uri, req.url);

      if (q === undefined || uri === undefined) {
        res.writeHead(400, { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type", "Content-Type": "text/plain" });
        res.end("Invalid");
        return;
      }

      onData = data => {
        data = data.toString().trim();

        if (data.startsWith("OUT"))
          data = data.slice(3);

        if (data.endsWith("DONE")) {
          data = data.slice(0, -4);
          onData = null;
          res.writeHead(200, { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type", "Content-Type": "text/plain" });
          res.end(data);
        }
        else {
          res.write(data);
        }
      };

      searcher.stdin.write(uri.trim())
      searcher.stdin.write("\n");
      searcher.stdin.write(q.trim())
      searcher.stdin.write("\n");
    }

    // const filename = parsed.pathname == "/" ? "/index.html" : parsed.pathname;

    // fs.readFile("." + filename, (err, data) => {
    //   if (err) {
    //     res.writeHead(400);
    //     res.end(`${filename} not found`);
    //   }
    //   else {
    //     res.writeHead(200, { "Content-Type": getMimeType(filename) });
    //     res.end(data, "utf-8");
    //   }
    // });
  }).listen(PORT, () => console.log(`Listening on port ${PORT}`));
})();

async function startSearch() {
  return new Promise(res => {
    onData = data => {
      console.assert(data.toString().trim() == "START");
      onData = null;
      res();
    };
  });
}

function getMimeType(filename) {
  switch (path.extname(filename)) {
    case ".js":   return "text/javascript";
    case ".css":  return "text/css";
    case ".json": return "application/json";
    case ".png":  return "image/png";
    case ".jpg":  return "image/jpg";
    case ".wav":  return "audio/wav";
    default:      return "text/html";
  }
}
