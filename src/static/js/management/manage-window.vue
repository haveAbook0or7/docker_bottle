<template>
    <div v-show="this.showFlg" class="manage-window" :style="variables" @click="$event.stopPropagation()">
        <input type="button" v-show="this.modeFlg == null" value="フォルダを作成" @click="createFolder">
		<input type="button" v-show="this.modeFlg" value="削除" @click="$refs.alert.openModal(mode, item)">
		<alert-modal ref="alert" @cancel="closeModal" @delete="deleteItem"></alert-modal>
		<input type="button" v-show="this.modeFlg" value="名前を変更" @click="changeItemName">
    </div>
</template>

<script>
module.exports = {
	components: {
		'alert-modal': httpVueLoader('./alert-modal.vue'),
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
			showFlg: false,
			width: 180,
			height: 300,
			mouse: {x: 0, y:0},
			mode: null,
			modeFlg: null,
			pathlist: null,
			item: null,
			itemIndex: null,
		}
	},
	methods: {
		openModal(mode, mouse, pathArray, item, index){
			this.showFlg = true;
			this.mode = mode;
			switch(mode){
				case "default":
					this.modeFlg = null;
					this.height = 35;
					break;
				case "folder":
				case "file":
					this.modeFlg = true;
					this.height = 70;
					break;
				case "none":
					this.modeFlg = false;
					this.height = 0;
					break;
			}
			this.pathlist = pathArray;
			this.item = item;
			this.itemIndex = index;
			let screenW = document.documentElement.clientWidth;
			let screenH = document.documentElement.clientHeight;
			if(mouse.x+this.width > screenW){
				mouse.x -= this.width;
			}
			if(mouse.y+this.height > screenH){
				mouse.y -= this.height;
			}
			this.mouse.x = mouse.x;
			this.mouse.y = mouse.y;
		},
		closeModal(){
			this.showFlg = false;
		},
		createFolder(){
			axios.post("/mngfiles/createfolder",{
                path: this.pathlist
            })
            .then(response => {
                console.log(response.data);
                this.$emit('reload', this.pathlist);
				this.closeModal();
            })
            .catch(function (error) {
                console.log(error);
            });
		},
		deleteItem(){
			axios.post("/mngfiles/deleteitem",{
				mode: this.mode,
                path: this.pathlist.concat(this.item)
            })
            .then(response => {
                console.log(response.data);
                this.$emit('reload', this.pathlist);
				this.closeModal();
            })
            .catch(function (error) {
                console.log(error);
            });
		},
		changeItemName(){
			this.$emit('rename', this.itemIndex, this.mode);
			this.closeModal();
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
		color: #fff;
	}
	div{
		z-index:4;
		width: var(--width);
		/* height: var(--height); */
		background-color: #fff;
		position: absolute;
		top: var(--mouse-y);
		left: var(--mouse-x);
	}
	input[type=button]{
		box-sizing: border-box;
		width: var(--width);
		height: 35px;
		padding: 0 5px;
		background: #cfd982;
		border-bottom: 1px solid #0f2350;
	}
</style>