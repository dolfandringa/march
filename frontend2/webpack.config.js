const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: "./src/index.tsx",
  output: {
    filename: "bundle.js",
    path: __dirname + "/dist",
  },
  devtool: "source-map",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        exclude: /(node_modules)/,
        use: ["babel-loader"],
      },
      {
        enforce: "pre",
        test: /\.js$/,
        loader: "source-map-loader",
      },
      {
        test: /\.less$/,
        use: [
          "style-loader",
          {
            loader: "css-loader",
            options: {
              sourceMap: true,
            },
          },
          {
            loader: "less-loader",
            options: {
              lessOptions: {
                sourceMap: true,
              },
            },
          },
        ],
      },
      // this rule handles images
      {
        test: /\.jpe?g$|\.gif$|\.ico$|\.png$|\.svg$/,
        use: "file-loader?name=[name].[ext]",
      },
      // fonts
      {
        test: /\.(woff|woff2|eot|ttf)(\?.*$|$)/i,
        use: ["file-loader"],
      },
    ],
  },
  plugins: [
    new webpack.ProvidePlugin({
      react: "react",
      "react-dom": "react-dom",
      "react-semantic-ui": "react-semantic-ui",
      lodash: "lodash",
    }),
    new HtmlWebpackPlugin({
      template: "./src/index.html",
      filename: path.resolve(__dirname, "./dist/index.html"),
      favicon: "./src/favicon.png",
    }),
  ],
  resolve: {
    extensions: [".ts", ".tsx", ".js", ".json"],
    alias: {
      src: path.resolve(__dirname, "/src"),
      "../../theme.config$": path.join(__dirname, "/semantic-ui/theme.config"),
    },
  },
};
