import path from 'path'
import webpack from 'webpack'
import ExtractTextPlugin from 'extract-text-webpack-plugin'

const extractSass = new ExtractTextPlugin({
  filename: "styles.css",
});

var DIST_PATH = path.resolve( __dirname, 'dist' );
var SOURCE_PATH = path.resolve( __dirname, 'src' );

export default {
    entry: SOURCE_PATH + '/app/app.js',
    output: {
        path: DIST_PATH,
        filename: 'app.dist.js',
        publicPath: '/app/'
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        ignore: './node_modules/',
                    }
                }
            },
            {
                test: /\.css$/,
                use: extractSass.extract({
                    fallback: 'style-loader',
                    //resolve-url-loader may be chained before sass-loader if necessary
                    use: [{
                        loader: "css-loader" // translates CSS into CommonJS
                    }, {
                        loader: "sass-loader" // compiles Sass to CSS
                    }]
                })
            }
        ]
    },
    plugins: [
        extractSass
    ]
};
