<template>
	<div id="overlay" class="alert-modal" :style="variables" v-show="this.showFlg" @click="showFlg = false;$emit('cancel')" @contextmenu="$event.stopPropagation();$event.preventDefault();">
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
					<input class="delete" type="button" value="削除" @click="showFlg = false;$emit('delete')">
				</td>
			</tr>
            </table>
        </div>
    </div>
</template>

<script>
module.exports = {
	props: {
		media: {default:"PC"},
		login_user: {default:null},
	},
	computed: {
		variables() {
            switch(this.media){
				case "PC":
					return {
                        "--FS": "13px",
						"--W": "485px",
						"--H": "300px",
						"--tableH": "50px",
                        "--buttonW": "100px",
						"--buttonH": "30px",
					};
				case "TabletPC":
					return {
                        "--FS": "18px",
						"--W": "485px",
						"--H": "300px",
						"--tableH": "60px",
                        "--buttonW": "130px",
						"--buttonH": "45px",
					};
				case "SmartPhone":
					return {
                        "--FS": "38px",
						"--W": "765px",
						"--H": "800px",
						"--tableH": "300px",
                        "--buttonW": "270px",
						"--buttonH": "90px",
					};
			}
		},
	},
	data: function () {
		return {
            showFlg: false,
			message:{
                folder: "を削除しますか。\nフォルダの中身ごと削除されます。",
                file: "を削除しますか。"
            },
            item: "dddddddddddd",
            mode: "folder",
			data: [],
		}
	},
	methods: {
		openModal(mode, item){
			this.showFlg = true;
            this.mode = mode;
			this.item = item;
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
		z-index:3;
		position:fixed;
		top:0;
		left:0;
		width:100%;
		height:100%;
		background-color:rgba(0,0,0,0.5);
		display: flex;
		align-items: center;
		justify-content: center;
	}
	#modal{
        all: initial;
		z-index:4;
		width: var(--W);
		height: var(--H);
		background-color: #fff;
		position: absolute;
        display: flex;
		align-items: center;
		justify-content: center;
	}
	table{
		display: inline-table;
		position: relative;
		min-width: 250px;
		height: var(--tableH);
		margin: auto;
	}
	.buttons{
		height: 60px;
		vertical-align: bottom;
	}
	input[type=button]{
		width: var(--buttonW);
		height: var(--buttonH);
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