import { merge } from "webpack-merge";
import { default as webpackDevServer } from "webpack-dev-server";
import common from "./webpack.common";
import * as path from "path";

const getConfig = () =>
  merge(common(), {
    mode: "development",
    devServer: {
      static: {
        directory: path.join(__dirname, "public"),
      },
    },
    devtool: "inline-source-map",
  });

export default getConfig;
