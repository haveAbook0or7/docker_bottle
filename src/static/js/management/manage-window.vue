<template>
    <div v-show="this.showFlg" class="manage-window" :style="variables" @click="$event.stopPropagation()">
        <input type="button" v-show="this.modeFlg == null" value="フォルダを作成" @click="createFolder">
		<input type="button" v-show="this.modeFlg" value="削除" @click="$refs.alert.openModal(mode, item)">
		<alert-modal ref="alert" :media="media" @cancel="closeModal" @delete="deleteItem"></alert-modal>
		<input type="button" v-show="this.modeFlg" value="名前を変更" @click="changeItemName">
    </div>
</template>

<script>
module.exports = {
	components: {
		'alert-modal': httpVueLoader('./alert-modal.vue'),
    },
	props: {
		media: {default:"PC"},
		login_user: {default:null},
	},
	computed: {
		variables() {
			let styles = {
				"--mouse-x": this.mouse.x+"px",
				"--mouse-y": this.mouse.y+"px",
			};
			switch(this.media){
				case "PC":
					this.width = 180;
					Object.assign(styles, {
                        "--FS": "13px",
						"--W": this.width+"px",
						"--H": "35px",
						"--divH": this.h,
					});
                    break;
				case "TabletPC":
					this.width = 210;
					Object.assign(styles, {
                        "--FS": "18px",
						"--W": this.width+"px",
						"--H": "50px",
						"--divH": this.h,
					});
                    break;
				case "SmartPhone":
					this.width = 350;
					Object.assign(styles, {
                        "--FS": "38px",
						"--W": this.width+"px",
						"--H": "90px",
						"--divH": this.h,
					});
                    break;
			}
			return styles;
		},
	},
	data: function () {
		return {
			showFlg: false,
			width: 180,
			h: 3,
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
			height = 0;
			this.h = 0;
			switch(mode){
				case "default":
					this.modeFlg = null;
					height = 35;
					this.h = 1;
					break;
				case "folder":
				case "file":
					this.modeFlg = true;
					height = 70;
					this.h = 2;
					break;
				case "none":
					this.modeFlg = false;
					break;
			}
			this.pathlist = pathArray;
			this.item = item;
			this.itemIndex = index;
			let screenW = document.documentElement.clientWidth;
			let screenH = document.documentElement.clientHeight;
			if(mouse.x + this.width > screenW){
				mouse.x -= this.width;
			}
			if(mouse.y + height > screenH){
				mouse.y -= height;
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
		font-size: var(--FS);
		color: #fff;
	}
	div{
		z-index:4;
		width: var(--W);
		height: var(--divH);
		background-color: #fff;
		position: absolute;
		top: var(--mouse-y);
		left: var(--mouse-x);
	}
	input[type=button]{
		-webkit-appearance: none;
		-webkit-touch-callout: none;
		-webkit-text-size-adjust: 100%;
		border-radius: 0;
		box-sizing: border-box;
		width: var(--W);
		height: var(--H);
		padding: 0 5px;
		background: #cfd982;
		border-bottom: 1px solid #0f2350;
	}
</style>