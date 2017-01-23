const path = require('path'),
      webpack = require("webpack"),
      HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  context: path.resolve('./src'),
  watch: true,
  debug: true,
  devtool: 'source-map',
  devServer: {
    host       : '0.0.0.0',
    port       : 8080,
    contentBase: 'dist/',
    quiet      : false,
    stats      : {
        colors: true
    },
    watchOptions: {
      poll: 1000
    }
  },
  entry: {
    application: path.resolve('./src/index.js')
  },
  output: {
    path: path.resolve('./dist'),
    filename: '[name]_bundle.js'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        include: /src/,
        exclude: /(node_modules|coverage)/,
        loader: 'babel',
        query: {
          presets: ['es2015']
        }
      }
    ],
  },
  plugins: [
    new webpack.optimize.OccurenceOrderPlugin(),
    new HtmlWebpackPlugin({
      template: path.resolve('./src/index.html'),
      title: 'Weatherlab!'
    })
  ],
  resolve: {
    extensions: [
      '',
      '.js'
    ]
  },
};
