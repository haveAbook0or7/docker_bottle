<template>
    <span>
	<div id="canvasBase">
        <canvas id="drawCanvas"></canvas>
        <canvas id="previewCanvas" 
            @mousedown="mousedown" 
            @mousemove="mousemove" 
            @mouseup="mouseup"></canvas>
    </div>
    {{mouse.x}}, {{mouse.y}}
    </span>
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
        console.log(this.baseSize.width);
        console.log(this.baseSize.height);
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
            color: "#000000",
            pen: 10,
            alpha: 0.5,
		}
	},
	methods: {
		mousedown(e){
            // キャンバスの位置とサイズを取得
            var rect = e.target.getBoundingClientRect();
            // マウスの位置
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
            // 描画の開始
            this.drarLineStart();
            // クリック中フラグ
            this.isClicked = true;
        },
        mousemove(e){
            // クリック中以外の時は無視
            if(!this.isClicked) {return;}
            // キャンバスの位置とサイズを取得
            var rect = e.target.getBoundingClientRect();
            // マウスの位置
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
            // クリック中なら線を引く
            this.drawLine();
        },
        mouseup(){
            // プレビューを消して、描画
            this.previewCxt.clearRect(0,0,this.baseSize.width,this.baseSize.height);
            this.drawCxt.stroke();
            // クリック終了
            this.isClicked = false;
        },
        drarLineStart() {
            // 線の太さを指定
            this.drawCxt.lineWidth = this.pen;
            this.previewCxt.lineWidth = this.pen;
            // 線の色を指定
            this.drawCxt.strokeStyle = this.color;
            this.drawCxt.globalAlpha = this.alpha;
            this.previewCxt.strokeStyle = this.color;
            this.previewCxt.globalAlpha = this.alpha;
            // 今からパスを書きますよと云う宣言
            this.drawCxt.beginPath();
            this.previewCxt.beginPath();
            // 先端を丸くする
            this.drawCxt.lineCap = "butt"
            this.previewCxt.lineCap = "butt"
            this.drawCxt.lineJoin = "round"
            this.previewCxt.lineJoin = "round"
            // パスの開始点に移動
            this.drawCxt.moveTo(this.mouse.x, this.mouse.y);
        },
        drawLine() {
            // 指定の位置までパスを引く
            this.drawCxt.lineTo(this.mouse.x, this.mouse.y);
            // パスに線を載せる
            this.previewCxt.clearRect(0,0,this.baseSize.width,this.baseSize.height);
            this.previewCxt.lineTo(this.mouse.x, this.mouse.y);
            this.previewCxt.stroke();
        },
        changeColor(value){
            this.color = value;
        },
        changePen(value){
            var pensize = {marker: 15, thinPen: 2, thickPen: 5};
            console.log(pensize[value]);
            this.pen = pensize[value];
        },
        clickEraser(value){
            this.color = value;
            this.alpha = 1.0;
        },
        changeAlpha(value){
            this.alpha = value;
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