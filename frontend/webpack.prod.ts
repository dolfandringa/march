import { merge } from "webpack-merge";
import common from "./webpack.common";

const getConfig = () =>
  merge(common(), {
    mode: "production",
  });

export default getConfig;
