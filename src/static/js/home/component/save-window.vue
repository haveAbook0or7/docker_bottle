<template>
	<div id="overlay" v-show="showFlg" @click="closeModal()" :style="variables">
        <div id="modal" v-show="showFlg" @click="$event.stopPropagation();">
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
		media: {default:"PC"},
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
	computed: {
        variables() {
            switch(this.media){
				case "PC":
					return {
						"--FS": "15px",
						"--W": "485px",
						"--H": "300px",
						"--tdminW": "70px",
						"--tdH": "40px",
						"--inputW": "200px",
						"--inputH": "20px",
						"--pathFS": "14px",
						"--toggleS": "1",
						"--saveW": "100px",
						"--saveH": "30px",
					};
				case "TabletPC":
					return {
						"--FS": "24px",
						"--W": "700px",
						"--H": "360px",
						"--tdminW": "150px",
						"--tdH": "75px",
						"--inputW": "260px",
						"--inputH": "35px",
						"--pathFS": "20px",
						"--toggleS": "2",
						"--saveW": "150px",
						"--saveH": "45px",
					};
				case "SmartPhone":
					return {};
			}
        }
	},
	data: function () {
		return {
			showFlg: false,
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
			this.showFlg = true;
            this.filename = filename;
			this.filepath = filepath;
			console.log(this.filepath)
		},
		closeModal(){
			this.showFlg = false;
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
		font-size: calc(var(--FS) - 2px);
	}
	#overlay{
		/*　要素を重ねた時の順番　*/
		z-index: 4;
		/*　画面全体を覆う設定　*/
		position: fixed;
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
		width: var(--W);
		height: var(--H);
		background-color: #fff;
		position: absolute;
        display: flex;
		align-items: center;
		justify-content: center;
	}
	td{
		height: var(--tdH);
		min-width: var(--tdminW);
	}
	input[type=text]:read-write{
		font: var(--FS) sans-serif;
		box-sizing: border-box;
		width: var(--inputW);
		padding: 0.3em;
		color: #aaaaaa;
		border: none;
		border-bottom: 2px solid #cfd982;
		background: transparent;
	}
	input[type=text]:read-write:focus {
		color: #1b2538;
		border-bottom: 2px solid #0f2350;
		outline: none;
	}
	.path{
		position: relative;
	}
	.select-path{
		position: absolute;
		top: 5px;
		width: var(--inputW);
		--pathFS: var(--pathFS);
		--buttonH: var(--inputH);
	}
	.buttons{
		height: 60px;
		vertical-align: bottom;
	}
	#download,#save,#save_new{
		width: var(--saveW);
		height: var(--saveH);
		color: #fff;
		background: #0f2350;
		z-index: 2;
	}
	#download:active,#save:active,#save_new:active{
		box-sizing: border-box;
		border: 2px inset #1c305c;
	}
</style>