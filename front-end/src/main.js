import {createApp} from 'vue'
import App from './App.vue'
import * as d3 from "d3"
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(ElementPlus)
app.use(d3)
app.mount('#app')

createApp(App).mount('#app')
