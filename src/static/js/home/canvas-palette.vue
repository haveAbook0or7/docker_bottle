<template>
	<div id="Base" :style="variables" @wheel="scroll">
		<div id="tools">
			<my-palette :login_user="loginUser" @change-color="changeColor" @change-pen="changePen" @back-next="backNext"></my-palette>
			<my-control :login_user="loginUser" :file_name="initfileName" @back-next="backNext" @save="saves"></my-control>
			<my-menu :login_user="loginUser" id="menu"></my-menu>
		</div>
		<!-- <br><br><br> -->
        <my-canvas ref="myCanvas" :open_file="openfile"></my-canvas>
    </div>
</template>

<script>
module.exports = {
	components: {
		'my-canvas': httpVueLoader('./canvas/my-canvas.vue'),
        'my-palette': httpVueLoader('./palette/my-palette.vue'),
		'my-control': httpVueLoader('./palette/my-control.vue'),
		'my-menu': httpVueLoader('./palette/my-menu.vue'),
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
		// getを取得
		var url = new URL(window.location.href);
		var params = url.searchParams;
		let fileopen = params.get('fileopen');
        // 既存ファイルを開く処理
		if(fileopen == "true"){
			axios.get("/mngfiles/openfile")
			.then(response => {
				console.log(response.data);
				if(response.data.data.flg){
					this.openfile = response.data.data.openfile_img;
					this.initfileName = response.data.data.openfile_neme;
				}
			})
			.catch(function (error) {
				console.log(error);
			});
		}
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
			openfile: null,
			initfileName: "新しいメモ帳",
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
        width: 100%;
        height: 50px;
        position: fixed;
        box-sizing: border-box;
		z-index: 3;
	}
	#menu{
		position: absolute;
		top: 0;
		right: 0;
		}
</style>