'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  proxyTable: {
    '/api': {
      target: 'http://127.0.0.1:5000',
      changeOrigin: true
    }
  },
})
