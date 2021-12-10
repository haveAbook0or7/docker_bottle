<template>
	<div id="controlBase">
        <span id="backnext">
            <input id="back" type="button" @click="clickBackNext('back')"><label for="back"></label>
            <input id="next" type="button" @click="clickBackNext('next')"><label for="next"></label>
        </span>
        <span id="saves">
            <input id="save" type="button" @click="clickSaveModalOpen"><label for="save"></label>
            <save-window ref="modal" :login_user="login_user" @save="clickSave"></save-window>
        </span>
    </div>
</template>

<script>
module.exports = {
    components: {
		'save-window': httpVueLoader('../component/save-window.vue'),
    },
    props: {
		login_user: {default:null},
        file_name: {default:null},
	},
	data: function () {
		return {
		}
	},
	methods: {
        clickBackNext(id){
            this.$emit('back-next', id);
        },
        clickSaveModalOpen(){
            console.log(this.file_name);
            this.$refs.modal.openModal(this.file_name);
        },
        clickSave(mode, path, filename){
            // canvas-paletteへ渡す
            this.$emit('save', mode, path, filename);
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
        width: 30px;
        height: 30px;
	}
    #backnext #back + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: steelblue;
        mask-image: url(../../../img/back.png);
        -webkit-mask-image: url(../../../img/back.png);
    }
    #backnext #next + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: steelblue;
        mask-image: url(../../../img/next.png);
        -webkit-mask-image: url(../../../img/next.png);
    }
    /* 保存 */
    #saves #save + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: steelblue;
        mask-image: url(../../../img/save.png);
        -webkit-mask-image: url(../../../img/save.png);
    }
</style>