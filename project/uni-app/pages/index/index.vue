<template>
	<view class="content">
		<uni-nav-bar leftIcon="gear" @clickLeft='doleftclick' @clickRight="dorightclick" :leftText="title" fixed status-bar
		 background-color='#e54847' color="#fff" right-icon="bars" title="狗眼电影"></uni-nav-bar>
		<uni-drawer mode='right' ref='ddd'>

			<scroll-view style="height:100vh" scroll-y="true">
				<div style='height: 45px'></div>
				<div style='height: var(--status-bar-height)'></div>
				<view v-for="item in classobj">
					<!-- <view @click="loaddata(item.ty)" class="uni-title">{{item.name}}</view> -->
					<button @click="loaddata(item.ty)" style="width: 26vw;position: relative;left: -2vw" type="default">{{item.name}}</button>
				</view>
				<div style='height: 45px'></div>
			</scroll-view>
		</uni-drawer>
		<scroll-view style="height: calc(100vh - 45px - var(--status-bar-height));" scroll-y="true">
			<div style='height: 2vw;' />

			<div v-for="item in dataobj" :key="item.id">

				<div @click='govideo(item)' class='videolist'>
					<div style="font-size: 0;padding: 1vw;">
						<image lazy-load style="width: 22vw;border-radius: 1.5vw;height: 33vw;" :src="item.pic" mode="widthFix"></image>
					</div>
					<div style='flex-grow: 1;margin-left: 2vw;padding-top: 2vw;font-size: 30rpx;'>
						<h3>
							{{item.name}}
						</h3>
						<p>更新: {{item.last}}</p>
						<p>区域: {{item.area}}</p>
						<p style='text-overflow: ellipsis;overflow: hidden;white-space: nowrap;width: 73vw;'>演员: {{item.actor}}</p>
						<p style='text-overflow: ellipsis;overflow: hidden;white-space: nowrap;width: 73vw;'>描述: {{item.des}}</p>

					</div>

				</div>
				<div style='background-color: #f5f5f5;height: 1vw;' />

			</div>
			<div v-show='dataobj.length' style='height: 10vw;display: flex;'>
				<button @click="go(-1)" style="width: 20vw " type="default">上一页 </button>
				<div style='width: 60vw;display: flex;'>
					<span style="line-height: 10vw;">当前第{{pg}}</span>

					<text style="line-height: 10vw;">页，共{{pagecount}}页</text>
				</div>
				<button @click="go(1)" style="width: 20vw " type="default">下一页 </button>

			</div>
		</scroll-view>
	</view>
</template>

<script>
	import uniNavBar from "@/components/uni-nav-bar/uni-nav-bar.vue"
	import uniDrawer from "@/components/uni-drawer/uni-drawer.vue"
	import uniPagination from '@/components/uni-pagination/uni-pagination.vue'
	import {
		httpget
	} from '@/http.js'
	export default {
		components: {
			uniNavBar,
			uniDrawer,
			uniPagination
		},

		computed: {
			dataobj: function() {
				if (this.data == []) {
					return []
				} else {
					return this.data.map(x => {
						return {
							name: x.name[0],
							pic: x.pic[0],
							year: x.year[0],
							last: x.last[0],
							id: x.id[0],
							des: x.des[0],
							area: x.area[0],
							actor: x.actor[0],
							dl: [x.dl[0].dd[0].$.flag, x.dl[0].dd[0]._],
							director: x.director[0]
						}
					})
				}
			},
			classobj: function() {
				if (this.class == []) {
					return []
				} else {
					return this.class.map(x => {
						return {
							name: x._,
							ty: x.$.id
						}
					})
				}


			}
		},
		data() {
			return {
				url: 'http://www.zdziyuan.com/inc/api_zuidam3u8.php?',
				data: [],
				pg: 1,
				t: 0,
				class: [],
				title: '',
				pagecount: 0
			}
		},
		created() {
			this.first()

		},

		methods: {
			first() {
				uni.showLoading({
					title: '加载中',
					mask: true
				});
				httpget(this.url)
					.then(res => this.xmljs(res.data))
					.then(x => {
						this.class = x.rss.class[0].ty
					})
				httpget(this.url + 'ac=videolist&pg=1')
					.then(res => this.xmljs(res.data))
					.then(x => {
						this.data = x.rss.list[0].video
						this.pagecount = x.rss.list[0].$.pagecount
						uni.hideLoading()

					})
			},
			loaddata(x) {
				this.pagecount = 0
				this.pg = 1
				this.t = x
				this.renderdata(x, 1)
			},

			go(x) {
				this.renderdata(this.t, this.pg + 1, x)
			},

			//  通过 页数和分类获取请求的promise
			getdata(t, pg) {
				let httpurl = t ? this.url + 'ac=videolist&t=' + t + "&pg=" + pg : this.url + 'ac=videolist&pg=' + pg
				return httpget(httpurl)
			},
			// 通过 页数和分类获取新的试图数据
			renderdata(t, pg, next = 0) {
				uni.showLoading({
					title: '加载中',
					mask: true
				});
				this.data = []
				this.getdata(t, pg)
					.then(x => this.xmljs(x.data))
					.then(x => [x.rss.list[0].$, x.rss.list[0].video])
					.then(x => {
						this.$refs.ddd.close()
						if (!x[1]) {
							uni.showToast({
								title: '没有更多了',
								duration: 2000,
								icon: 'none',
								position: 'bottom',
								mask: true
							});
							return
						}
						this.pg = this.pg + next
						this.data = x[1]
						this.pagecount = x[0].pagecount
						uni.hideLoading()
					})
			},
			govideo(x) {

				uni.navigateTo({
					url: '/pages/video/video?item=' + encodeURIComponent(JSON.stringify(x))
				});
			},
			dorightclick() {
				this.$refs.ddd.open()
			},
			doleftclick() {
				 
			},
		}
	}
</script>

<style>
	.content {
		width: 100vw;
		height: 100vh;

	}

	.videolist {
		display: flex;
	}
</style>
