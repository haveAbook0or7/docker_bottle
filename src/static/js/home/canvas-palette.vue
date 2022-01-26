<template>
	<div id="Base" :style="variables" @wheel="scroll">
		<div id="tools">
			<my-palette v-if="media != 'SmartPhone'" :media="media" :login_user="loginUser" 
				@change-color="changeColor" @change-pen="changePen" @back-next="backNext"></my-palette>
			<my-control v-if="media != 'SmartPhone'" :media="media" :login_user="loginUser" :file_name="initfileName" :file_path="initfilepath" 
				@back-next="backNext"  @save="saves" ref="control"></my-control>
			<my-menu :media="media" :login_user="loginUser" id="menu"></my-menu>
		</div>
		<div class="space"></div>
        <my-canvas :media="media" ref="myCanvas" @save_end="saveEnd"></my-canvas>
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
	beforeCreate() {
		// ユーザー認証
		axios.get("/userlogins/getuser")
		.then(response => {
			// console.log(response.data);
			this.loginUser = response.data.data.user;
			this.initfilepath = this.loginUser+"/";
			// console.log(this.initfilepath);
		})
		.catch(function (error) {
			console.log(error);
		});
	},
	mounted() {
		// 端末の種類取得
		this.media = getMedia();
		console.log(this.media);
		// キャンバスサイズを取得
		this.baseheight = document.documentElement.clientHeight;
		this.canvasheight = document.documentElement.clientHeight;
		// getを取得
		var url = new URL(window.location.href);
		var params = url.searchParams;
		let fileopen = params.get('fileopen');
		console.log(fileopen)
        // 既存ファイルを開く処理
		if(fileopen == "true"){
			axios.get("/mngfiles/openfile")
			.then(response => {
				console.log(response.data);
				if(response.data.data.flg){
					this.openfile = response.data.data.openfile_img;
					this.initfileName = response.data.data.openfile_neme;
					this.initfilepath = response.data.data.openfile_path;
					if(this.openfile != null){
						this.$refs.myCanvas.drawImg(this.openfile, true);
					}
				}
			})
			.catch(function (error) {
				console.log(error);
			});
		}
	},
	computed: {
		variables() {
			let styles = {
				"--height": this.canvasheight+"px",
			};
            switch(this.media){
				case "PC":
					Object.assign(styles, {
						"--paletteH": "50px",
						"--space": "60px"
					});
					break;
				case "TabletPC":
					Object.assign(styles, {
						"--paletteH": "80px",
						"--space": "90px"
					});
					break;
				case "SmartPhone":
					Object.assign(styles, {
						"--paletteH": "100px",
						"--space": "110px"
					});
					break;
			}
			return styles;
		},
	},
	data: function () {
		return {
			media: "PC",
			loginUser: null,
			baseheight: null,
			canvasheight: null,
			openfile: null,
			initfileName: "新しいメモ帳",
			initfilepath: "",
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
		},
		saveEnd(flg){
			this.$refs.control.closeSaveWin(flg);
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
		background: #0f2350;
	}
	#tools{
		background: #cfd982;
        width: 100%;
        height: var(--paletteH);
        position: fixed;
        box-sizing: border-box;
		z-index: 3;
	}
	#menu{
		position: absolute;
		top: 0;
		right: 0;
	}
	.space{
		height: var(--space);
	}
</style>