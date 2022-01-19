<template>
	<div class="my-palette" :style="variables">
        <span id="colors">
            <input id="black" name="colors" type="radio" v-model="color" value="black" @change="changeColor">
                <label for="black" :style="'background: '+colorPalette.black+';'"></label>
            <input id="one"   name="colors" type="radio" v-model="color" value="one" @change="changeColor">
                <label for="one" class="upper" :style="'background: '+colorPalette.one+';'" v-longclick="() => showColorConf(true, 'one')" @dblclick="showColorConf(true, 'one')"></label>
            <input id="two"   name="colors" type="radio" v-model="color" value="two" @change="changeColor">
                <label for="two" :style="'background: '+colorPalette.two+';'" v-longclick="() => showColorConf(true, 'two')" @dblclick="showColorConf(true, 'two')"></label>
            <input id="three" name="colors" type="radio" v-model="color" value="three" @change="changeColor">
                <label for="three" class="upper" :style="'background: '+colorPalette.three+';'" v-longclick="() => showColorConf(true, 'three')" @dblclick="showColorConf(true, 'three')"></label>
			<input id="four"  name="colors" type="radio" v-model="color" value="four" @change="changeColor">
                <label for="four" :style="'background: '+colorPalette.four+';'" v-longclick="() => showColorConf(true, 'four')" @dblclick="showColorConf(true, 'four')"></label>
            <input id="five"  name="colors" type="radio" v-model="color" value="five" @change="changeColor">
                <label for="five" class="upper" :style="'background: '+colorPalette.five+';'" v-longclick="() => showColorConf(true, 'five')" @dblclick="showColorConf(true, 'five')"></label>
        </span>
        <span id="pens">
            <input id="marker"   name="pens" type="radio" v-model="pen" value="marker"   @change="changePen">
                <span><label for="marker" v-longclick="() => showPenConf(true, 'marker')" @dblclick="showPenConf(true, 'marker')"></label></span>
            <input id="thinPen"  name="pens" type="radio" v-model="pen" value="thinPen"  @change="changePen">
                <span><label for="thinPen" v-longclick="() => showPenConf(true, 'thinPen')" @dblclick="showPenConf(true, 'thinPen')"></label></span>
            <input id="thickPen" name="pens" type="radio" v-model="pen" value="thickPen" @change="changePen">
                <span><label for="thickPen" v-longclick="() => showPenConf(true, 'thickPen')" @dblclick="showPenConf(true, 'thickPen')"></label></span>
            <input id="eraser"   name="pens" type="radio" v-model="pen" value="eraser"   @change="changePen">
                <span><label for="eraser" v-longclick="() => showPenConf(true, 'eraser')" @dblclick="showPenConf(true, 'eraser')"></label></span>
        </span>
        <span id="config">
            <my-colors-config v-show="this.configShowColor" 
                ref="colorconfig" @change="changeColorConf"></my-colors-config>
            <my-pens-config v-show="this.configShowPen" 
                ref="penconfig" @change="changePenConf"></my-pens-config>
        </span>
    </div>
</template>

<script>
module.exports = {
	components: {
		'my-pens-config': httpVueLoader('../palette-config/my-pens-config.vue'),
        'my-colors-config': httpVueLoader('../palette-config/my-colors-config.vue'),
    },
	created() {
        this.loading();
	},
    props: {
		login_user: {default:null},
	},
	computed: {
		variables() {
			return {
				"--dynamic-color": this.colorPalette[this.color],
			}
		},
	},
	data: function () {
		return {
            colorPalette: {black: "#000000", one: "#ff0000", two: "#00ff00", three: "#0000ff", four: "#ffff00", five: "#ffffff"},
            penSize: {marker: 15, thinPen: 2, thickPen: 5, eraser: 15},
            penAlpha: {marker: 0.3, thinPen: 0.9, thickPen: 0.9, eraser: 1.0},
            penCap: {marker: "butt", thinPen: "round", thickPen: "round", eraser: "round"},

            configShowPen: false,
            configShowColor: false,

            color: "black",
            pen: "marker",
		}
	},
	methods: {
        loading(){
            // パレット設定を取得
            axios.get("/userconfig/select")
            .then(response => {
                if(response.data.message == "OK"){
                    this.colorPalette = response.data.data.palette;
                    this.penSize = response.data.data.size;
                    this.penAlpha = response.data.data.alpha;
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        },
		changeColor(){
            // 設定ウィンドウが表示されている場合
            if(this.configShowColor){
                // 設定ウィンドウの値を選択したペンのものに変更(黒は変更できないのでウィンドウ閉じる)
                this.showColorConf((this.color == "black"));
            }
            // my-convasに渡してペン色変える
            this.$emit('change-color', this.pen != "eraser" ? this.colorPalette[this.color] : "#ffffff");
        },
        showColorConf(dbclick=true, color=this.color){
            // v-longclick -> change の順で発火するのでcolorを作っている
            // ダブルクリックならウィンドウ開閉
            if(dbclick){
                this.configShowColor = !this.configShowColor;
            }
            // 設定ウィンドウの値を選択したペンのものに変更
            this.$refs.colorconfig.setInitValue(this.colorPalette[color]);
        },
        changeColorConf(color){
            // 設定ウィンドウで値を変更したら
            this.colorPalette[this.color] = color;
            this.changeColor();
            this.updateUserConf();
        },
        changePen(){
            // 設定ウィンドウが表示されている場合
            if(this.configShowPen){
                // 設定ウィンドウの値を選択したペンのものに変更
                this.showPenConf(false);
            }
            // my-convasに渡してペンを変える
            this.$emit('change-pen', 
                this.pen != "eraser" ? this.colorPalette[this.color] : "#ffffff", 
                this.penSize[this.pen], 
                this.penAlpha[this.pen],
                this.penCap[this.pen]
            );
        },
        showPenConf(dbclick=true, pen=this.pen){
            // v-longclick -> change の順で発火するのでpenを作っている
            // ダブルクリックならウィンドウ開閉
            if(dbclick){
                this.configShowPen = !this.configShowPen;
            }
            // 設定ウィンドウの値を選択したペンのものに変更
            this.$refs.penconfig.setInitValue(this.penSize[pen], this.penAlpha[pen]);
        },
        changePenConf(size, alpha){
            // 設定ウィンドウで値を変更したら
            this.penSize[this.pen] = parseInt(size);
            this.penAlpha[this.pen] = parseFloat(alpha);
            this.changePen();
            this.updateUserConf();
        },
        updateUserConf(){
            // パレット設定を一つの配列にまとめる
            let conf = this.colorPalette;
            for(let key in this.penSize){
                conf[key+"S"] = this.penSize[key];
            }
            for(let key in this.penAlpha){
                conf[key+"A"] = this.penAlpha[key];
            }
            // データベースを更新
            axios.post("/userconfig/update",
                conf
            )
            .then(response => {
                console.log(response.data);
                this.loading();
            })
            .catch(function (error) {
                console.log(error);
            });
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
    .my-palette{
        display: inline-block;
        position: relative;
        height: 50px;
    }
    /* ラジオボタン */
	input[type=radio]{
		position: absolute;
		z-index: -1;
		opacity: 0;
	}
    /* カラー */
	#colors input[type=radio] + label{
        box-sizing: border-box;
		position: relative;
		display: inline-block;
        margin: 15px 2px 5px 2px;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        border: 2px solid #e6b422;
	}
    .upper{
        margin: 5px 2px 15px 2px !important;
    }
    /* ペン */
    #pens input[type=radio] + span > label{
		position: relative;
		display: block;
        width: 40px;
        height: 40px;
	}
    #pens input[type=radio] + span{
        position: relative;
        display: inline-block;
        margin: 2.5px 2px;
        width: 40px;
        height: 40px;
        border: 2px solid transparent;
    }
    #pens #marker + span > label{
        mask: url(../../../img/pen15.png) no-repeat center/100%;
        -webkit-mask: url(../../../img/pen15.png) no-repeat center/100%;
        background: var(--dynamic-color);
    }
    #pens #thinPen + span > label{
        mask: url(../../../img/pen13.png) no-repeat center/100%;
        -webkit-mask: url(../../../img/pen13.png) no-repeat center/100%;
        background: var(--dynamic-color);
    }
    #pens #thickPen + span > label{
        mask: url(../../../img/pen14.png) no-repeat center/100%;
        -webkit-mask: url(../../../img/pen14.png) no-repeat center/100%;
        background: var(--dynamic-color);
    }
    #pens #eraser + span > label{
        mask: url(../../../img/ere3.png) no-repeat center/100%;
        -webkit-mask: url(../../../img/ere3.png) no-repeat center/100%;
        background: #fff;
    }
    #pens input[type=radio]:checked + span{
        border: solid 2px #1c305c !important;
    }
    /* 詳細設定 */
    #config{
        z-index: 5;
        display: inline-flex;
        position: absolute;
		top: 50px;
		left: 0;
        width:450px;
    }
    .my-colors-config{
        position: absolute;
        left: 0;
    }
    .my-pens-config{
        position: absolute;
        right: 0;
    }
</style>