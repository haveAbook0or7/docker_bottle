<template>
	<div id="paletteBase" :style="variables">
        <span id="colors">
            <input id="black" name="colors" type="radio" v-model="color" value="black" @change="changeColor">
            <label for="black" :style="'background: '+colorPalette.black+';'"></label>
            <input id="one"   name="colors" type="radio" v-model="color" value="one" @change="changeColor">
            <label for="one" class="upper" :style="'background: '+colorPalette.one+';'" @dblclick="showColorConf('one')"></label>
            <input id="two"   name="colors" type="radio" v-model="color" value="two" @change="changeColor">
            <label for="two" :style="'background: '+colorPalette.two+';'" @dblclick="showColorConf('two')"></label>
            <input id="three" name="colors" type="radio" v-model="color" value="three" @change="changeColor">
            <label for="three" class="upper" :style="'background: '+colorPalette.three+';'" @dblclick="showColorConf('three')"></label>
			<input id="four"  name="colors" type="radio" v-model="color" value="four" @change="changeColor">
            <label for="four" :style="'background: '+colorPalette.four+';'" @dblclick="showColorConf('four')"></label>
            <input id="five"  name="colors" type="radio" v-model="color" value="five" @change="changeColor">
            <label for="five" class="upper" :style="'background: '+colorPalette.five+';'" @dblclick="showColorConf('five')"></label>
        </span>
        <span id="pens">
            <input id="marker"   name="pens" type="radio" v-model="pen" value="marker"   @change="changePen"><label for="marker" @dblclick="showPenConf('marker')"></label>
            <input id="thinPen"  name="pens" type="radio" v-model="pen" value="thinPen"  @change="changePen"><label for="thinPen" @dblclick="showPenConf('thinPen')"></label>
            <input id="thickPen" name="pens" type="radio" v-model="pen" value="thickPen" @change="changePen"><label for="thickPen" @dblclick="showPenConf('thickPen')"></label>
            <input id="eraser"   name="pens" type="radio" v-model="pen" value="eraser"   @change="changePen"><label for="eraser" @dblclick="showPenConf('eraser')"></label>
        </span>
        <span id="colorsConfig">
            <my-colors-config v-show="this.colorConfFlg.one" 
                id_name="one" :init_rgbhex="colorPalette.one"
                @change="changeColorConf"></my-colors-config>
            <my-colors-config v-show="this.colorConfFlg.two" 
                id_name="two" :init_rgbhex="colorPalette.two"
                @change="changeColorConf"></my-colors-config>
            <my-colors-config v-show="this.colorConfFlg.three" 
                id_name="three" :init_rgbhex="colorPalette.three"
                @change="changeColorConf"></my-colors-config>
            <my-colors-config v-show="this.colorConfFlg.four" 
                id_name="four" :init_rgbhex="colorPalette.four"
                @change="changeColorConf"></my-colors-config>
            <my-colors-config v-show="this.colorConfFlg.five" 
                id_name="five" :init_rgbhex="colorPalette.five"
                @change="changeColorConf"></my-colors-config>
        </span>
        <span id="penConfig">
            <my-pens-config v-show="this.penConfFlg.marker" 
                id_name="marker" :init_size="this.penSize.marker" :init_alpha="this.penAlpha.marker" 
                @change-size="changePenConf" @change-alpha="changePenConf"></my-pens-config>
            <my-pens-config v-show="this.penConfFlg.thinPen" 
                id_name="thinPen" :init_size="this.penSize.thinPen" :init_alpha="this.penAlpha.thinPen" 
                @change-size="changePenConf" @change-alpha="changePenConf"></my-pens-config>
            <my-pens-config v-show="this.penConfFlg.thickPen" 
                id_name="thickPen" :init_size="this.penSize.thickPen" :init_alpha="this.penAlpha.thickPen" 
                @change-size="changePenConf" @change-alpha="changePenConf"></my-pens-config>
            <my-pens-config v-show="this.penConfFlg.eraser" 
                id_name="eraser" :init_size="this.penSize.eraser" :init_alpha="this.penAlpha.eraser" 
                @change-size="changePenConf" @change-alpha="changePenConf"></my-pens-config>
        </span>
    </div>
</template>

<script>
module.exports = {
	components: {
		'my-pens-config': httpVueLoader('./my-pens-config.vue'),
        'my-colors-config': httpVueLoader('./my-colors-config.vue'),
    },
	created() {
        axios.post("/userconfig/select",{
			id: this.login_user
		})
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

            penConfShow: {id: "marker", flg: false},
            penConfFlg: {marker: false, thinPen: false, thickPen: false, eraser: false},
            colorConfShow: {id: "one", flg: false},
            colorConfFlg: {one: false, two: false, three: false, four: false, five: false},
            color: "black",
            pen: "marker",
		}
	},
	methods: {
		changeColor(){
            if(this.colorConfShow.flg){
                this.colorConfFlg[this.colorConfShow.id] = false;
                this.showColorConf(this.color);
            }
            this.$emit('change-color', this.pen != "eraser" ? this.colorPalette[this.color] : "#ffffff");
        },
        changePen(){
            if(this.penConfShow.flg){
                this.penConfFlg[this.penConfShow.id] = false;
                this.showPenConf(this.pen);
            }
            this.$emit('change-pen', 
                this.pen != "eraser" ? this.colorPalette[this.color] : "#ffffff", 
                this.penSize[this.pen], 
                this.penAlpha[this.pen],
                this.penCap[this.pen]
            );
        },
        showPenConf(id){
            for(k in this.penConfFlg){
                if(k == id){
                    continue;
                }
                this.penConfFlg[k] = false;
            }
            this.penConfFlg[id] = !this.penConfFlg[id];
            this.penConfShow.id = id;
            this.penConfShow.flg = this.penConfFlg[id];
        },
        changePenConf(id, lbl, value){
            switch(lbl){
                case "size":
                    this.penSize[id] = value;
                    break;
                case "alpha":
                    this.penAlpha[id] = value;
                    break;
            }
            this.changePen();
        },
        showColorConf(id){
            for(k in this.colorConfFlg){
                if(k == id){
                    continue;
                }
                this.colorConfFlg[k] = false;
            }
            this.colorConfFlg[id] = !this.colorConfFlg[id];
            this.colorConfShow.id = id;
            this.colorConfShow.flg = this.colorConfFlg[id];
        },
        changeColorConf(id, color){
            this.colorPalette[id] = color;
            this.changeColor();
        },
        clickBackNext(id){
            this.$emit('back-next', id);
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
        z-index: 3;
	}
    #paletteBase{
        display: inline-block;
    }
    /* ラジオボタン */
	input[type=radio]{
		position: absolute;
		z-index: -1;
		opacity: 0;
	}
    /* カラー */
	#colors input[type=radio] + label{
		position: relative;
		display: inline-block;
        margin: 15px 2px 5px 2px;
        border-radius: 50%;
        width: 30px;
        height: 30px;
	}
    .upper{
        margin: 5px 2px 15px 2px !important;
    }
    /* ペン */
    #pens input[type=radio] + label{
		position: relative;
		display: inline-block;
        margin: 2.5px 2px;
        width: 40px;
        height: 40px;
	}
    #pens #marker + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: var(--dynamic-color);
        border: solid 2px #777777;
        mask-image: url(../img/pen12.png);
        -webkit-mask-image: url(../img/pen12.png);
    }
    #pens #thinPen + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: var(--dynamic-color);
        border: solid 2px #777777;
        mask-image: url(../img/pen10.png);
        -webkit-mask-image: url(../img/pen10.png);
    }
    #pens #thickPen + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: var(--dynamic-color);
        border: solid 2px #777777;
        mask-image: url(../img/pen11.png);
        -webkit-mask-image: url(../img/pen11.png);
    }
    #pens #eraser + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: #fff;
        border: solid 2px #777777;
        mask-image: url(../img/ere2.png);
        -webkit-mask-image: url(../img/ere2.png);
    }
    #pens input[type=radio]:checked + label{
        border: solid 2px palevioletred !important;
	}
    /* 詳細設定 */
    #penConfig{
        z-index: 5;
    }
    #colorsConfig{
        z-index: 5;
    }
    /* パレット移動 */
    #paletteMove{
        background: #ffff00;
        position: absolute;
		display: inline-block;
        right: 0;
        /* margin: 15px 2px 5px 2px;
        border-radius: 50%; */
        width: 20px;
        height: 50px;
    }
</style>