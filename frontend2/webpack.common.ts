import * as path from "path";
import * as webpack from "webpack";
import HtmlWebpackPlugin from "html-webpack-plugin";
import MiniCssExtractPlugin from "mini-css-extract-plugin";

const getConfig = (): webpack.Configuration => {
  return {
    entry: "./src/index.tsx",
    output: {
      filename: "bundle.[contenthash].js",
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
            /*{
            //  loader: MiniCssExtractPlugin.loader,
            },*/
            "style-loader",
            {
              loader: "css-loader",
              options: {
                sourceMap: true,
                /*url: {
                  filter: (url: string, resourcePath: string) => {
                    // resourcePath - path to css file

                    // Don't handle `data:` urls
                    if (url.startsWith("data:")) {
                      return false;
                    }

                    return true;
                  },
                },*/
              },
            },
            {
              loader: "less-loader",
              options: {
                lessOptions: {
                  sourceMap: true,
                  math: "always",
                },
              },
            },
          ],
        },
        // fonts
        {
          test: /\.(eot|woff|woff2|ttf|svg)(\?.*$|$)/i,
          //use: ["file-loader"],
          use: [
            {
              loader: "file-loader",
              options: {
                name: "[name].[contenthash].[ext]",
              }
            },
          ],
        },
        // this rule handles images
        {
          test: /\.jpe?g$|\.gif$|\.ico$|\.png$|\.svg$/,
          use: "file-loader",
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
      new MiniCssExtractPlugin({
        filename: "[name].[contenthash].css",
      }),
    ],
    resolve: {
      extensions: [".ts", ".tsx", ".js", ".json"],
      alias: {
        src: path.resolve(__dirname, "/src"),
        "../../theme.config$": path.join(
          __dirname,
          "/src/semantic-ui/theme.config"
        ),
      },
    },
  };
};

export default getConfig;
