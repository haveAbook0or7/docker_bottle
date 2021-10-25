<template>
	<div id="paletteBase" :style="elementColor">
        <span id="colors">
            <input id="black" name="colors" type="radio" v-model="color" :value="colorPalette.black" @change="changeColor"><label for="black" :style="'background: '+colorPalette.black+';'"></label>
            <input id="one"   name="colors" type="radio" v-model="color" :value="colorPalette.one" @change="changeColor"><label for="one" class="upper" :style="'background: '+colorPalette.one+';'"></label>
            <input id="two"   name="colors" type="radio" v-model="color" :value="colorPalette.two" @change="changeColor"><label for="two" :style="'background: '+colorPalette.two+';'"></label>
            <input id="three" name="colors" type="radio" v-model="color" :value="colorPalette.three" @change="changeColor"><label for="three" class="upper" :style="'background: '+colorPalette.three+';'"></label>
			<input id="four"  name="colors" type="radio" v-model="color" :value="colorPalette.four" @change="changeColor"><label for="four" :style="'background: '+colorPalette.four+';'"></label>
            <input id="five"  name="colors" type="radio" v-model="color" :value="colorPalette.five" @change="changeColor"><label for="five" class="upper" :style="'background: '+colorPalette.five+';'"></label>
        </span>
        <span id="pens">
            <input id="marker"   name="pens" type="radio" v-model="pen" value="marker"   @change="changePen"><label for="marker" @dblclick="showConfig('marker')"></label>
            <input id="thinPen"  name="pens" type="radio" v-model="pen" value="thinPen"  @change="changePen"><label for="thinPen" @dblclick="showConfig('thinPen')"></label>
            <input id="thickPen" name="pens" type="radio" v-model="pen" value="thickPen" @change="changePen"><label for="thickPen" @dblclick="showConfig('thickPen')"></label>
            <input id="eraser"   name="pens" type="radio" v-model="pen" value="eraser"   @change="changePen"><label for="eraser" @dblclick="showConfig('eraser')"></label>
        </span>
        <span id="penConfig">
            <my-pens-config v-show="this.showFlg.marker" 
                id_name="marker" :init_size="this.penSize.marker" :init_alpha="this.penAlpha.marker" 
                @change-size="changeConfig" @change-alpha="changeConfig"></my-pens-config>
            <my-pens-config v-show="this.showFlg.thinPen" 
                id_name="thinPen" :init_size="this.penSize.thinPen" :init_alpha="this.penAlpha.thinPen" 
                @change-size="changeConfig" @change-alpha="changeConfig"></my-pens-config>
            <my-pens-config v-show="this.showFlg.thickPen" 
                id_name="thickPen" :init_size="this.penSize.thickPen" :init_alpha="this.penAlpha.thickPen" 
                @change-size="changeConfig" @change-alpha="changeConfig"></my-pens-config>
            <my-pens-config v-show="this.showFlg.eraser" 
                id_name="eraser" :init_size="this.penSize.eraser" :init_alpha="this.penAlpha.eraser" 
                @change-size="changeConfig" @change-alpha="changeConfig"></my-pens-config>
        </span>
    </div>
</template>

<script>
module.exports = {
	components: {
		'my-pens-config': httpVueLoader('./my-pens-config.vue'),
    },
	props: {
		// mydbname: {default:"H1_2_DefaultDataMax"},
	},
	mounted() {
        axios.post("/py",{
			id: 1
		})
		.then(response => {
            this.colorPalette = response.data.data.palette;
            this.penSize = response.data.data.size;
            this.penAlpha = response.data.data.alpha;
		})
		.catch(function (error) {
			console.log(error);
		});
	},
	computed: {
		elementColor() {
			return {
				"--dynamic-color": this.color
			}
		},
	},
	data: function () {
		return {
            colorPalette: {black: "#000000", one: "#ff0000", two: "#00ff00", three: "#0000ff", four: "#ffff00", five: "#ffffff"},
            penSize: {marker: 15, thinPen: 2, thickPen: 5, eraser: 15},
            penAlpha: {marker: 0.3, thinPen: 0.9, thickPen: 0.9, eraser: 1.0},
            configShow: {id: "marker", flg: false},
            showFlg: {marker: false, thinPen: false, thickPen: false, eraser: false},
            color: "#000000",
            pen: "marker",
		}
	},
	methods: {
		changeColor(){
            this.$emit('change-color', this.pen != "eraser" ? this.color : "#ffffff");
        },
        changePen(){
            if(this.configShow.flg){
                this.showFlg[this.configShow.id] = false;
                this.showConfig(this.pen);
            }
            this.$emit('change-pen', 
                this.pen != "eraser" ? this.color : "#ffffff", 
                this.penSize[this.pen], 
                this.penAlpha[this.pen]
            );
        },
        showConfig(id){
            for(k in this.showFlg){
                if(k == id){
                    continue;
                }
                this.showFlg[k] = false;
            }
            this.showFlg[id] = !this.showFlg[id];
            this.configShow.id = id;
            this.configShow.flg = this.showFlg[id];
        },
        changeConfig(id, lbl, value){
            switch(lbl){
                case "size":
                    this.penSize[id] = value;
                    break;
                case "alpha":
                    this.penAlpha[id] = value;
                    break;
            }
            this.changePen();
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
    #paletteBase{
        background: #777777;
        width: 450px;
        height: 50px;
        position: relative;
        box-sizing: border-box;
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
        background: beige;
	}
    .upper{
        margin: 5px 2px 15px 2px !important;
    }
	#colors input[type=radio]:checked + label{
		background: goldenrod;
	}
    /* ペン */
    #pens input[type=radio] + label{
		position: relative;
		display: inline-block;
        margin: 2.5px 2px;
        width: 40px;
        height: 40px;
        background: beige;
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
		/* background: chartreuse !important; */
	}
    #penConfig{
        z-index: 5;
    }
</style>