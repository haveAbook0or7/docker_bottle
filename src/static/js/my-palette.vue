<template>
	<div id="paletteBase">
        
    </div>
</template>

<script>
module.exports = {
	components: {
		
    },
	props: {
		// mydbname: {default:"H1_2_DefaultDataMax"},
	},
	mounted() {
        // キャンバスサイズを取得
        this.baseSize = document.querySelector('#canvasBase').getBoundingClientRect();
        // オブジェクト取得後サイズを設定
		this.drawCanvas = document.querySelector('#drawCanvas');
        this.drawCanvas.setAttribute("width", this.baseSize.width);
        this.drawCanvas.setAttribute("height", this.baseSize.height);
        this.previewCanvas = document.querySelector('#previewCanvas');
        this.previewCanvas.setAttribute("width", this.baseSize.width);
        this.previewCanvas.setAttribute("height", this.baseSize.height);
        // コンテキスト取得
        this.drawCxt = this.drawCanvas.getContext('2d');
        this.previewCxt = this.previewCanvas.getContext('2d');
	},
	computed: {
		// showFlg: {
		// 	get(){
		// 		return this.mydbname == "H1_2_DefaultDataMax" ? false : true;
		// 	}
		// },
	},
	data: function () {
		return {
            baseSize: null,
			drawCanvas: null, drawCxt: null,
            previewCanvas: null, previewCxt: null,
            isClicked: false,

            mouse: {x:0, y:0},
		}
	},
	methods: {
		

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
    div{
        height: 100%;
        position: relative;
        box-sizing: border-box;
        margin: 0px 50px;
    }
    #drawCanvas {
        width: 100%;
        height: 100%;
        background: #ffffff;
        box-sizing: border-box;
        position: absolute;
		border: solid 1px #cc77cc;
	}
    #previewCanvas {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        position: absolute;
        z-index: 2;
	}
</style>