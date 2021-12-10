<template>
	<!-- <div :class="this.modalClass+' manage-window'" id="overlay" :style="variables" @click="closeModal()"> -->
        <div id="modal" :class="this.modalClass+' manage-window'" :style="variables" @click="stop()">
            <!-- <table border="0">
            <tr>
                <td>ファイル名</td>
                <td>
                    <input type="text" v-model="filename">
                </td>
            </tr>
            <tr v-if="ifGuest">
                <td>保存場所</td>
                <td class="path">
                    <select-path :options="filepathData" v-model="filepath"></select-path>
                </td>
            </tr>
			<tr>
				<td colspan="2" class="buttons">
					<input id="download" type="button" value="ダウンロード" @click="clickSave('download')">
					<input id="save" type="button" v-if="ifGuest" value="上書き保存" @click="clickSave('save')">
					<input id="save_new" type="button" v-if="ifGuest" value="新規保存" @click="clickSave('save_new')">
				</td>
			</tr>
            </table> -->
			
        </div>
    <!-- </div> -->
</template>

<script>
module.exports = {
	components: {
		
    },
	props: {
		login_user: {default:null},
	},
	computed: {
		variables() {
			return {
				"--width": this.width+"px",
				"--height": this.height+"px",
				"--mouse-x": this.mouse.x+"px",
				"--mouse-y": this.mouse.y+"px",
			}
		},
	},
	data: function () {
		return {
			modalClass: "hidden",
			width: 200,
			height: 300,
			mouse: {x: 0, y:0},
		}
	},
	methods: {
		openModal(x, y){
			this.modalClass = "";
			let screenW = document.documentElement.clientWidth;
			let screenH = document.documentElement.clientHeight;
			if(x+this.width > screenW){
				x -= this.width;
			}
			if(y+this.height > screenH){
				y -= this.height;
			}
			this.mouse.x = x;
			this.mouse.y = y;
			console.log(this.mouse)
		},
		closeModal(){
			this.modalClass = "hidden";
		},
		stop(){
			event.stopPropagation();
		},
	},
}
// export default { Node.jsじゃないから、これだとダメだった。 }
</script>

<style scoped>
	*{
		margin: 0;
		padding: 0;
		border: 0;
	}
	.hidden{
		display: none !important;
	}
	#overlay{
		/*　要素を重ねた時の順番　*/
		z-index:3;
		/*　画面全体を覆う設定　*/
		position: absolute;
		top: 0;
		left: 0;
		width:100%;
		height:100%;
		background: transparent;
		background-color:rgba(0,0,0,0.5);
	}
	#modal{
		z-index:4;
		width: var(--width);
		height: var(--height);
		background-color: #fff;
		position: absolute;
		top: var(--mouse-y);
		left: var(--mouse-x);
	}
</style>