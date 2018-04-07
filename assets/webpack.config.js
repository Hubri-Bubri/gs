var path = require('path')
var CopyWebpackPlugin = require('copy-webpack-plugin')

let resolve = (dir) => {
    return path.join(__dirname, dir)
}


module.exports = {
    entry: {
        application: resolve('./application/application.js')
    },
    output: {
        path: resolve("../gs/static/bundle"),
        filename: '[name].js',
        publicPath: '/static'
    },
    resolve: {
        extensions: ['.js', '.vue'],
        alias: {
            '@': resolve('application'),
            'vue$': 'vue/dist/vue.js'
        }
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                include: [resolve('application')],
                query: {presets: 'es2015'}
            }
        ]
    },
    plugins: [
        new CopyWebpackPlugin([
            {from: resolve('node_modules/bootstrap/dist/css/bootstrap.css')},
            {from: resolve('node_modules/bootstrap-vue/dist/bootstrap-vue.css')},
            {from: resolve('node_modules/font-awesome/css'), to: "font-awesome/css", ignore: ["*.map"]},
            {from: resolve('node_modules/font-awesome/fonts'), to: "font-awesome/fonts"},
        ])
    ]
}
