'use strict';
let path = require('path');
let webpack = require('webpack');


let entry= {
    'welcome': './app/welcome/index.js',
    'operation-system': './app/operation-system/index.js',
    'hpc': './app/hpc/index.js'
};

let webpack_rules= {
    rules: [
        {
            test: /\.js$/,
            use: [ 'babel-loader' ],
            exclude: /node_modules/,
            include: __dirname
        }
    ]
};

let externals= {
    'react': 'React',
    'react-dom': 'ReactDOM',
    'redux': 'Redux',
    'react-redux': 'ReactRedux',
    'echarts': 'echarts',
    'moment': 'moment',
    'react-router': 'ReactRouter',
    'react-router-redux': 'ReactRouterRedux',
    'redux-thunk': 'ReduxThunk'
};

if( process.env.NODE_ENV === 'production' ) {
    module.exports = {
        entry: entry,
        output: {
            path: path.join(__dirname, 'dist'),
            filename: "[name].entry.min.js",
            sourceMapFilename: '[file].map'
        },
        module: webpack_rules,
        externals: externals,
        plugins: [
            new webpack.optimize.UglifyJsPlugin({
                test: /(\.jsx|\.js)$/,
                compress: {
                    warnings: false
                },
                sourceMap: true
            })
        ]
    };
}else{
    console.log('use develop build');
    module.exports = {
        devtool: "source-map",
        entry: entry,
        output: {
            path: path.join(__dirname, 'dist'),
            filename: "[name].entry.js",
            sourceMapFilename: '[file].map'
        },
        module: webpack_rules,
        externals: externals
    };
}
