import path from "path";
import HtmlWebpackPlugin from "html-webpack-plugin";
import MiniCssExtractPlugin from "mini-css-extract-plugin";
import { CleanWebpackPlugin } from "clean-webpack-plugin";

const __dirname = path.resolve();

export default {
  entry: `./src/index.ts`,
  output: {
    path: path.resolve(__dirname, "dist"),
    publicPath: "/",
    filename: "[name].[contenthash].js",
  },

  plugins: [
    new HtmlWebpackPlugin({
      filename: "index.html",
      template: "src/components/index.hbs",
      minify: { collapseWhitespace: true },
    }),
    new MiniCssExtractPlugin({
      filename: "main.[contenthash].css",
    }),
    new CleanWebpackPlugin(),
  ],

  module: {
    rules: [
      {
        test: /\.ts?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        exclude: /node_modules/,
        use: [MiniCssExtractPlugin.loader, "css-loader"],
        sideEffects: true,
      },
      {
        test: /\.css$/,
        include: /node_modules/,
        use: [
          { loader: "style-loader" },
          { loader: "css-loader", options: { url: false } },
        ],
        sideEffects: true,
      },
      {
        test: /\.png$/,
        exclude: /node_modules/,
        use: {
          loader: "file-loader",
          options: {
            publicPath: "dist/images/",
            outputPath: "images",
            name: "[name].[contenthash].png",
          },
        },
        type: "javascript/auto",
      },
      {
        test: /\.hbs$/,
        loader: "handlebars-loader",
        options: {
          precompileOptions: {
            noEscape: true,
            strict: true,
            knownHelpersOnly: false,
          },
        },
      },
    ],
  },

  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },

  optimization: {
    usedExports: true,
    // runtimeChunk: {
    //   name: "shared/runtime.js",
    // },
    splitChunks: {
      chunks: "all",
      cacheGroups: {
        defaultVendors: {
          enforce: true,
          test: /node_modules/,
          filename: "js/vendor/vendor.[contenthash].js",
          reuseExistingChunk: true,
        },
      },
    },
  },
};
