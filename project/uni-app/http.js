export function httpget(url) {
	return new Promise((resolve, reject) => {
		uni.request({
			url: url,
			method: 'GET',
			success: (res) => {
				resolve(res)
			},
			fail: (x) => {
				reject(x)
			},
		});
	})
}
