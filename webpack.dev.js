import { merge } from "webpack-merge";
import webpack from "webpack";
import common from "./webpack.common.js";

export default merge(common, {
  mode: "development",
  devServer: {
    hot: true,
    compress: true,
    client: {
      overlay: {
        errors: true,
        warnings: false,
      },
    },
  },

  devtool: false,

  plugins: [
    new webpack.SourceMapDevToolPlugin({
      filename: "dist/[file].map",
      fileContext: "public",
    }),
  ],
  optimization: {
    minimize: false,
  },
});
