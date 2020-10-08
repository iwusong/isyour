import Vue from 'vue'
import App from './App'


Vue.config.productionTip = false

App.mpType = 'app'

Vue.prototype.xmljs = require('xml2js').Parser().parseStringPromise;

const app = new Vue({
	...App
})
app.$mount()
