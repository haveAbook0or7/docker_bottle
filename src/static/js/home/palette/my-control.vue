<template>
	<div id="controlBase" :style="variables">
        <span id="backnext">
            <input id="back" type="button" @click="clickBackNext('back')"><label for="back"></label>
            <input id="next" type="button" @click="clickBackNext('next')"><label for="next"></label>
        </span>
        <span id="saves">
            <input id="save" type="button" @click="clickSaveModalOpen"><label for="save"></label>
            <save-window ref="modal" :media="media" :login_user="login_user" @save="clickSave"></save-window>
        </span>
    </div>
</template>

<script>
module.exports = {
    components: {
		'save-window': httpVueLoader('../component/save-window.vue'),
    },
    props: {
        media: {default:"PC"},
		login_user: {default:null},
        file_name: {default:null},
        file_path: {default:null},
	},
    computed: {
        variables() {
            switch(this.media){
				case "PC":
					return {
						"--buttonS": "30px",
					};
				case "TabletPC":
					return {
						"--buttonS": "45px",
					};
				case "SmartPhone":
					return {
						"--buttonS": "40px",
					};
			}
        }
	},
	methods: {
        clickBackNext(id){
            this.$emit('back-next', id);
        },
        clickSaveModalOpen(){
            this.$refs.modal.openModal(this.file_name, this.file_path);
        },
        clickSave(mode, path, filename){
            // canvas-paletteへ渡す
            this.$emit('save', mode, path, filename);
        },
        closeSaveWin(flg){
            this.$refs.modal.closeModal(flg);
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
        z-index: 3;
	}
    #controlBase{
        display: inline-block;
    }
    /* 戻る進む */
    input[type=button] + label{
		position: relative;
		display: inline-block;
        margin: 10px 2px;
        width: var(--buttonS);
        height: var(--buttonS);
	}
    #backnext #back + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: #1c305c;
        mask-image: url(../../../img/back.png);
        -webkit-mask-image: url(../../../img/back.png);
    }
    #backnext #next + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: #1c305c;
        mask-image: url(../../../img/next.png);
        -webkit-mask-image: url(../../../img/next.png);
    }
    /* 保存 */
    #saves #save + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: #1c305c;
        mask-image: url(../../../img/save.png);
        -webkit-mask-image: url(../../../img/save.png);
    }
</style>