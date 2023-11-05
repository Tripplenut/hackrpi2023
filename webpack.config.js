const path = require("path");

module.exports = {
  entry: {
    index: "./src/index.js",
  },
  mode: "production",
  module: {
     rules: [
       {
          test: /\.jsx?$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
          }
       },
       {
          test: /\.css$/,
          use: [
            "style-loader","css-loader"
          ]
       }
     ]
   },
  resolve: {
    extensions: [".js",".jsx"],
  },
  output: {
    path: path.resolve(__dirname, "./build"),
    filename: "[name].js",
  },
};