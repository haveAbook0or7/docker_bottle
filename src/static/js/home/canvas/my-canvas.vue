<template>
    <span>
	<div id="canvasBase">
        <canvas id="drawCanvas"></canvas>
        <canvas id="previewCanvas" 
            @mousedown="mousedown" @touchstart="mousedown" 
            @mousemove="mousemove" @touchmove="mousemove" 
            @mouseup="mouseup" @touchend="mouseup"></canvas>
    </div>
    </span>
</template>

<script>
module.exports = {
    props: {
        media: {default:"PC"},
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
        // ストレージの初期化
        this.myStorage = localStorage;
        this.myStorage.setItem("__log", JSON.stringify([]));
        this.setLocalStoreage();
	},
	data: function () {
		return {
            baseSize: null,
			drawCanvas: null, drawCxt: null,
            previewCanvas: null, previewCxt: null,
            isClicked: false,
            myStorage: null,
            temp: [],
            currentCanvas: 0,

            mouse: {x:0, y:0},
            nn: "",
            color: "#000000",
            pen: 15,
            alpha: 0.3,
            cap: "butt"
		}
	},
	methods: {
        // 保存
        upload(mode, path, filename){
            var logs = JSON.parse(this.myStorage.getItem("__log"));
            console.log(logs[0]['png']);
            if(mode == "download"){
                const fileLink = document.createElement('a');
                fileLink.href = logs[0]['png'];
                fileLink.setAttribute('download', filename);
                document.body.appendChild(fileLink);
                fileLink.click();
                this.$emit('save_end', true);
            }else{
                axios.post("/upfiles/upload",{
                    mode: mode,
                    path: path,
                    name: filename,
                    png: logs[0]['png'],
                })
                .then(response => {
                    console.log(response.data);
                    this.$emit('save_end', response.data.data.flg);
                })
                .catch(function (error) {
                    console.log(error);
                });
            }
        },
        // スクロールして画面拡大
        canvasResize(newHeight){
            // 高さを更新
            this.baseSize.height = newHeight;
            this.drawCanvas.setAttribute("height", this.baseSize.height);
            this.previewCanvas.setAttribute("height", this.baseSize.height);
            // ローカルストレージから配列を取得
            var logs = JSON.parse(this.myStorage.getItem("__log"));
            const thisvc = this;
            setTimeout(function(){
                //画像を描写する
                if(logs.length != 0){
                    thisvc.drawImg(logs[0]['png']);
                }
            }, 0);
        },
        // ペン動作
        drarLineStart() {
            // 線の太さ・色・不透明度を指定
            this.drawCxt.lineWidth = this.pen;
            this.previewCxt.lineWidth = this.pen;
            this.drawCxt.strokeStyle = this.color;
            this.previewCxt.strokeStyle = this.color;
            this.drawCxt.globalAlpha = this.alpha;
            this.previewCxt.globalAlpha = this.alpha;
            // 今からパスを書きますよと云う宣言
            this.drawCxt.beginPath();
            this.previewCxt.beginPath();
            // 先端を指定、つなぎ目を丸くする
            this.drawCxt.lineCap = this.cap;
            this.previewCxt.lineCap = this.cap;
            this.drawCxt.lineJoin = "round";
            this.previewCxt.lineJoin = "round";
            // パスの開始点に移動
            this.drawCxt.moveTo(this.mouse.x, this.mouse.y);
            this.previewCxt.moveTo(this.mouse.x, this.mouse.y);
        },
		mousedown(e){
            if(this.media == "SmartPhone"){
                return;
            }
            e.preventDefault();
            // キャンバスの位置とサイズを取得
            var rect = e.target.getBoundingClientRect();
            // マウスの位置
            switch(e.type){
                case "mousedown":
                    this.mouse.x = e.clientX - rect.left;
                    this.mouse.y = e.clientY - rect.top;
                    break;
                case "touchstart":
                    this.mouse.x = e.touches[0].clientX - rect.left;
                    this.mouse.y = e.touches[0].clientY - rect.top;
                    break;
            }
            // 描画の開始
            this.drarLineStart();
            // クリック中フラグ
            this.isClicked = true;
        },
        mousemove(e){
            if(this.media == "SmartPhone"){
                return;
            }
            // クリック中以外の時は無視
            if(!this.isClicked) {return;}
            // キャンバスの位置とサイズを取得
            var rect = e.target.getBoundingClientRect();
            // マウスの位置
            switch(e.type){
                case "mousemove":
                    this.mouse.x = e.clientX - rect.left;
                    this.mouse.y = e.clientY - rect.top;
                    break;
                case "touchmove":
                    this.mouse.x = e.touches[0].clientX - rect.left;
                    this.mouse.y = e.touches[0].clientY - rect.top;
                    break;
            }
            // クリック中なら線を引く
            // 指定の位置までパスを引く
            this.drawCxt.lineTo(this.mouse.x, this.mouse.y);
            // パスに線を載せる
            this.previewCxt.clearRect(0,0,this.baseSize.width,this.baseSize.height);
            this.previewCxt.lineTo(this.mouse.x, this.mouse.y);
            this.previewCxt.stroke();
        },
        mouseup(){
            if(this.media == "SmartPhone"){
                return;
            }
            // プレビューを消して、描画
            this.previewCxt.clearRect(0,0,this.baseSize.width,this.baseSize.height);
            this.drawCxt.stroke();
            // ローカルストレージに保存
            this.setLocalStoreage();
            // クリック終了
            this.isClicked = false;
        },
        // 戻る進む
        setLocalStoreage(){
            // 画像化
            var png = this.drawCanvas.toDataURL("image/png");
            // ローカルストレージから配列を取得
            var logs = JSON.parse(this.myStorage.getItem("__log"));
            // 一度だけ処理する
            const thisvc = this;
            setTimeout(function(){
                // 配列の先頭にに画像を格納
                logs.unshift({png});
                // ローカルストレージに配列を保存
                thisvc.myStorage.setItem("__log", JSON.stringify(logs));
                // 履歴を初期化
                thisvc.currentCanvas = 0;
                thisvc.temp = [];
            }, 0);
        },
        prevCanvas(){
            // ローカルストレージから配列を取得
            var logs = JSON.parse(this.myStorage.getItem("__log"));
            if(logs.length > 0){
                this.temp.unshift(logs.shift());
                const thisvc = this;
                setTimeout(function(){
                    thisvc.myStorage.setItem("__log", JSON.stringify(logs));
                    //Canvasを初期化する
                    thisvc.drawCxt.clearRect(0, 0, thisvc.baseSize.width,thisvc.baseSize.height);
                    //画像を描写する
                    if(logs.length != 0){
                        thisvc.drawImg(logs[0]['png']);
                    }
                }, 0);
            }
        },
        nextCanvas(){
            // ローカルストレージから配列を取得
            var logs = JSON.parse(this.myStorage.getItem("__log"));
            if(this.temp.length > 0){
                logs.unshift(this.temp.shift());
                const thisvc = this;
                setTimeout(function(){
                    thisvc.myStorage.setItem("__log", JSON.stringify(logs));
                    //Canvasを初期化する
                    thisvc.drawCxt.clearRect(0, 0, thisvc.baseSize.width,thisvc.baseSize.height);
                    //画像を描写する
                    thisvc.drawImg(logs[0]['png']);
                }, 0);
            }
        },
        drawImg(src, firstset = false){
            var img = new Image();
            img.src = src;
            img.onload = () => {
                this.drawCxt.globalAlpha = 1.0;
                this.drawCxt.drawImage(img, 0, 0);
                if(firstset){
                    this.setLocalStoreage();
                }
            }
        },
        // ペン設定変更
        changeColor(value){
            this.color = value;
        },
        changePen(color, size, alpha, cap){
            this.color = color;
            this.pen = size;
            this.alpha = alpha;
            this.cap = cap;
        },
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
        width: 900px;
        height: 100%;
        position: relative;
        box-sizing: border-box;
        margin: 0px auto;
    }
    #drawCanvas {
        width: 100%;
        height: 100%;
        background: #ffffff;
        box-sizing: border-box;
        position: absolute;
	}
    #previewCanvas {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        position: absolute;
        z-index: 2;
	}
</style>