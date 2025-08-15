const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {'/api':{target:'http://host.docker.internal:8000/',ws:false}}
  }
})
