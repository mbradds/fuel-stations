import express from "express";
import compression from "compression";
import path from "path";

const __dirname = path.resolve();
const port = process.env.PORT || 8080;
const app = express();

function shouldCompress(req, res) {
  if (req.headers["x-no-compression"]) {
    // don't compress responses with this request header
    return false;
  }
  // fallback to standard filter function
  return compression.filter(req, res);
}

function cachePolicy(req, res, next) {
  const periodLong = 31536000; // 1 year
  const contentHash = new RegExp("\\.[0-9a-f]{20}\\.");
  if (req.method === "GET") {
    if (req.url.match(contentHash)) {
      res.set("Cache-control", `public, max-age=${periodLong}`);
    } else {
      res.set("Cache-control", `no-store`);
    }
  } else {
    // for the other requests set strict no caching parameters
    res.set("Cache-control", `no-store`);
  }
  next();
}

app.disable("x-powered-by");
app.use(cachePolicy);
app.use(compression({ filter: shouldCompress }));
// the __dirname is the current directory from where the script is running
app.use(express.static(path.resolve(__dirname, "dist")));
// send the user to index html page inspite of the url
app.get("*", (req, res) => {
  res.sendFile(path.resolve(__dirname, "dist/index.html"));
});

app.listen(port);
