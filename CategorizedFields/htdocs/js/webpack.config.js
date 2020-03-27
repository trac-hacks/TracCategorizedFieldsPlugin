module.exports = {
    entry: [
        './ticket.js',
    ],

    output: {
        filename: './bundle.js',
    },
    mode: "development",
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm'
        }
    }
};