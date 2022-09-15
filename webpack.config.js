var path = require('path')
var CopyWebpackPlugin = require('copy-webpack-plugin')


let resolve = (dir) => {
    return path.join(__dirname, dir)
}

module.exports = {
    devtool: 'source-map',
    entry: {
        'gs-dashboard/gs_dashboard/static/bundle/gs-dashboard': resolve('./gs-dashboard/assets/application/application.js'),
        'gs-business/gs_business/static/bundle/gs-business': resolve('./gs-business/assets/application/application.js')
    },

    output: {
        path: resolve("."),
        filename: '[name].js',
        publicPath: '/static'
    },

    resolve: {
        extensions: ['.js', '.vue'],
        alias: {
            '@dashboard': resolve('./gs-dashboard/assets/application'),
            '@business': resolve('./gs-business/assets/application'),
            '@share': resolve('./gs-share/assets/application'),
            '@security': resolve('./gs-security/assets/application'),
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
            // gs-dashboard
            { from: resolve('node_modules/bootstrap/dist/css/bootstrap.css'), to: './gs-dashboard/gs_dashboard/static/bundle' },
            { from: resolve('node_modules/bootstrap-vue/dist/bootstrap-vue.css'), to: './gs-dashboard/gs_dashboard/static/bundle' },
            { from: resolve('node_modules/@fortawesome/fontawesome-free-webfonts/css'), to: "./gs-dashboard/gs_dashboard/static/bundle/font-awesome/css", ignore: ["*.map"] },
            { from: resolve('node_modules/@fortawesome/fontawesome-free-webfonts/webfonts'), to: "./gs-dashboard/gs_dashboard/static/bundle/font-awesome/webfonts" },
            
            // gs-business
            { from: resolve('node_modules/bootstrap/dist/css/bootstrap.css'), to: './gs-business/gs_business/static/bundle' },
            { from: resolve('node_modules/bootstrap-vue/dist/bootstrap-vue.css'), to: './gs-business/gs_business/static/bundle' },
            { from: resolve('node_modules/@fortawesome/fontawesome-free-webfonts/css'), to: "./gs-business/gs_business/static/bundle/font-awesome/css", ignore: ["*.map"] },
            { from: resolve('node_modules/@fortawesome/fontawesome-free-webfonts/webfonts'), to: "./gs-business/gs_business/static/bundle/font-awesome/webfonts" }
        ])
    ]
}
