module.exports = {
    devServer: {
        port: 8082,
        host: 'www.uric.cn',
    },
    publicPath: process.env.NODE_ENV === 'production'
    ? '/production-sub-path/'
    : './'
}