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
        path: resolve("../static/bundle"),
        filename: '[name].js',
        publicPath: '/static'
    },
    resolve: {
        extensions: ['.js', '.vue'],
        alias: {
            '@': resolve('application'),
            '@share': resolve('../../../gs-share/assets/application'),
            'vue$': 'vue/dist/vue.js'
        },
        modules: ["/home/alexander/projects/gs/gs-business/gs_business/assets/node_modules"]
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
                query: {
                    presets: 'es2015',
                    plugins: ['transform-es2015-destructuring', 'transform-object-rest-spread']
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.scss$/,
                use: ["style-loader", "css-loader", "sass-loader"]
            }
        ]
    },
    plugins: [
        new CopyWebpackPlugin([
            { from: resolve('node_modules/bootstrap/dist/css/bootstrap.css') },
            { from: resolve('node_modules/bootstrap-vue/dist/bootstrap-vue.css') },
            { from: resolve('node_modules/@fortawesome/fontawesome-free-webfonts/css'), to: "font-awesome/css", ignore: ["*.map"] },
            { from: resolve('node_modules/@fortawesome/fontawesome-free-webfonts/webfonts'), to: "font-awesome/webfonts" },
        ])
    ]
}
