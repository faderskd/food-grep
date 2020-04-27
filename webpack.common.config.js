const VueLoaderPlugin = require('vue-loader/lib/plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: {
    index: './src/index.js',
  },
  module: {
    rules: [
      {
        test: /\.html$/,
        use: ['html-loader'],
      },
      {
        test: /\.(svg|eot|woff|woff2|ttf)$/,
        use: {
          loader: 'file-loader',
          options: {
            name: '[path][name].[ext]',
            outputPath: 'images',
            esModule: false,
          },
        },
      },
      {
        test: /font-awesome\.config\.js/,
        use: [
          {loader: 'style-loader'},
          {loader: 'font-awesome-loader'},
        ],
      },
      {
        test: /\.vue$/,
        use: 'vue-loader',
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.js', '.vue', '.json'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    },
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
    }),
    new VueLoaderPlugin(),
  ],
};
