<template>
	<div :style="variables">
		
    </div>
</template>

<script>
module.exports = {
	components: {
		'my-canvas': httpVueLoader('./my-canvas.vue'),
        'my-palette': httpVueLoader('./my-palette.vue'),
		'my-control': httpVueLoader('./my-control.vue'),
		'my-menu': httpVueLoader('./my-menu.vue'),
    },
	created() {
		// ユーザー認証
		// axios.get("/userlogins/getuser")
		// .then(response => {
		// 	console.log(response.data);
		// 	this.loginUser = response.data.data.user;
		// })
		// .catch(function (error) {
		// 	console.log(error);
		// });
	},
	mounted() {
		
	},
	computed: {
		variables() {
			return {
				"--height": this.canvasheight+"px",
			}
		},
	},
	data: function () {
		return {
			loginUser: null,
			baseheight: null,
			canvasheight: null,
		}
	},
	methods: {
		
	},
}
// export default { Node.jsじゃないから、これだとダメだった。 }
</script>

<style scoped>
	*{
		margin: 0;
		padding: 0;
		border: 0;
		font-size: 13px;
	}
</style>