<template>
	<view>
		<uni-nav-bar @clickLeft='back' left-icon='back' fixed status-bar background-color='#e54847' color="#fff" :title="item.name.slice(0,10)"></uni-nav-bar>
		<video autoplay v-if="show" style="width: 100%;" :src="src" controls></video>
		<div style="">
			<button v-for="i in list" style="display: inline-block;margin: 0 2vw;" @click="c(i)" type="default">{{i.split('$')[0]}}</button>
		</div>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: '',
				item: {},
				list: [],
				src: '',
				show: true
			}
		},
		onLoad: function(option) {

			this.item = JSON.parse(decodeURIComponent(option.item))

			this.list = this.item.dl[1].split('$' + this.item.dl[0] + '#')


		},
		methods: {
			back() {
				uni.navigateBack()
			},
			c(i) {
				this.src = i.split('$')[1]
				this.show = false
				this.show = true
			}
		}
	}
</script>

<style>

</style>
