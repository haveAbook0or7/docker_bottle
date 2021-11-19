<template>
	<div id="Base" :style="variables" @wheel="scroll">
		<div id="tools">
			<my-palette :login_user="loginUser" @change-color="changeColor" @change-pen="changePen" @back-next="backNext"></my-palette>
			<my-control :login_user="loginUser" @back-next="backNext" @save="saves"></my-control>
		</div>
        <my-canvas ref="myCanvas"></my-canvas>
    </div>
</template>

<script>
module.exports = {
	components: {
		'my-canvas': httpVueLoader('./my-canvas.vue'),
        'my-palette': httpVueLoader('./my-palette.vue'),
		'my-control': httpVueLoader('./my-control.vue'),
    },
	created() {
		// ユーザー認証
		axios.get("/userlogins/getuser")
		.then(response => {
			console.log(response.data);
			this.loginUser = response.data.data.user;
		})
		.catch(function (error) {
			console.log(error);
		});
	},
	mounted() {
		// キャンバスサイズを取得
		this.baseheight = document.documentElement.clientHeight;
		this.canvasheight = document.documentElement.clientHeight;
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
		scroll(e){
			var scrollLimit = this.canvasheight - this.baseheight;
			if(scrollLimit <= e.view.pageYOffset){
				this.canvasheight += e.deltaY > 0 ? e.deltaY : 0;
				this.$refs.myCanvas.canvasResize(this.canvasheight);
			}
		},
		changeColor(value){
            this.$refs.myCanvas.changeColor(value);
        },
        changePen(color, size, alpha, cap){
            this.$refs.myCanvas.changePen(color, size, alpha, cap);
        },
		backNext(id){
			switch(id){
                case "back":
                    this.$refs.myCanvas.prevCanvas();
                    break;
                case "next":
                    this.$refs.myCanvas.nextCanvas();
                    break;
            }
		},
		saves(mode, path, filename){
			// my-canvasのuploadでアップロード
			this.$refs.myCanvas.upload(mode, path, filename);
		}

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
	#Base{
		width: 100%;
		height: var(--height);
		background: brown;
	}
	#tools{
		background: #777777;
        width: 900px;
        height: 50px;
        position: fixed;
        box-sizing: border-box;
		z-index: 3;
	}
</style>