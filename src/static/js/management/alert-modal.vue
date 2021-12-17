<template>
	<div id="overlay" class="alert-modal" v-show="this.showFlg" @click="showFlg = false;$emit('cancel')" @contextmenu="$event.stopPropagation();$event.preventDefault();">
        <div id="modal" v-show="this.showFlg" @click="$event.stopPropagation()">
			<table border="0">
            <tr>
                <td colspan="2" style="white-space: pre-wrap;">{{item + message[mode]}}</td>
            </tr>
			<tr class="buttons">
				<td>
					<input class="cancel" type="button" value="キャンセル" @click="showFlg = false;$emit('cancel')">
				</td>
				<td>
					<input class="delete" type="button" value="削除" @click="showFlg = false;$emit('delete', item)">
				</td>
			</tr>
            </table>
        </div>
    </div>
</template>

<script>
module.exports = {
	props: {
		login_user: {default:null},
	},
	data: function () {
		return {
            showFlg: false,
			message:{
                folder: "を削除しますか。\nフォルダの中身ごと削除されます。",
                file: "を削除しますか。"
            },
            item: "",
            mode: null,
			data: [],
		}
	},
	methods: {
		openModal(mode, item){
			this.showFlg = true;
            this.mode = mode;
			this.item = item.split("/")[item.split("/").length-1];
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
		text-align: center;
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
        all: initial;
		z-index:4;
		width: 485px;
		height: 300px;
		background-color: #fff;
		position: absolute;
        display: flex;
		align-items: center;
		justify-content: center;
	}
	table{
		position: relative;
	}
	.buttons{
		height: 60px;
		vertical-align: bottom;
	}
	input[type=button]{
		width: 100px;
		height: 30px;
		z-index: 2;
		text-align: center;
		border: none;
	}
	input[type=button]:active{
		background: #cfd982;
		box-sizing: border-box;
		border: 2px inset #c1c989;
	}
</style>