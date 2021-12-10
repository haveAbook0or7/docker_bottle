<template>
	<div id="overlay" :class="this.modalClass" @click="closeModal()">
        <div id="modal" :class="this.modalClass" @click="stop()">
            <table border="0">
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
            </table>
			
        </div>
    </div>
</template>

<script>
module.exports = {
	components: {
		'select-path': httpVueLoader('../../component/select-path.vue'),
    },
	props: {
		login_user: {default:null},
	},
	created() {
		// ユーザーのフォルダ取得
		axios.get("/upfiles/getdir")
		.then(response => {
			console.log(response.data);
			this.ifGuest = !(response.data.message == "guest");
			this.filepathData = response.data.data;
		})
		.catch(function (error) {
			console.log(error);
		});
	},
	data: function () {
		return {
			modalClass: "hidden",
			ifGuest: true,
            filename: null,
			filepath: "",
			filepathData: {},
			data: [],
			message: [],
		}
	},
	methods: {
		openModal(filename, filepath){
			this.modalClass = "";
            this.filename = filename;
			this.filepath = filepath;
			console.log(this.filepath)
		},
		closeModal(){
			this.modalClass = "hidden";
		},
		stop(){
			event.stopPropagation();
		},
		clickSave(buttonMode){
			// my-controlへ渡す
			this.$emit('save', buttonMode, this.filepath, this.filename+".png");
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
	}
	.hidden{
		display: none !important;
	}
	#overlay{
		/*　要素を重ねた時の順番　*/
		z-index:3;
		/*　画面全体を覆う設定　*/
		position:fixed;
		top:0;
		left:0;
		width:100%;
		height:100%;
		background-color:rgba(0,0,0,0.5);
		/*　画面の中央に要素を表示させる設定　*/
		display: flex;
		align-items: center;
		justify-content: center;
	}
	#modal{
		z-index:4;
		width: 485px;
		height: 300px;
		background-color: #fff;
		position: absolute;
        display: flex;
		align-items: center;
		justify-content: center;
	}
	td{
		height: 40px;
		min-width: 70px;
	}
	input[type=text]{
		font: 15px sans-serif;
		box-sizing: border-box;
		width: 200px;
		padding: 0.3em;
		color: #aaaaaa;
		border: none;
		border-bottom: 2px solid #1b2538;
		background: transparent;
	}
	input[type=text]:focus {
		color: #1b2538;
		border-bottom: 2px solid #da3c41;
		outline: none;
	}
	.path{
		position: relative;
	}
	.select-path{
		position: absolute;
	}
	.buttons{
		height: 60px;
		vertical-align: bottom;
	}
	#download,#save,#save_new{
		width: 100px;
		height: 30px;
		color: #fff;
		background: #da3c41;
		z-index: 2;
	}
	#save:active{
		box-sizing: border-box;
		border: 2px inset #c0353a;
	}
</style>