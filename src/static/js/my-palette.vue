<template>
	<div id="paletteBase" :style="elementColor">
        <span id="colors">
            <input id="black" name="colors" type="radio" v-model="color" value="#000000" @change="changeColor"><label for="black"></label>
            <input id="one"   name="colors" type="radio" v-model="color" value="#ff0000" @change="changeColor"><label for="one" class="upper"></label>
            <input id="two"   name="colors" type="radio" v-model="color" value="#00ff00" @change="changeColor"><label for="two"></label>
            <input id="three" name="colors" type="radio" v-model="color" value="#0000ff" @change="changeColor"><label for="three" class="upper"></label>
			<input id="four"  name="colors" type="radio" v-model="color" value="#ffff00" @change="changeColor"><label for="four"></label>
            <input id="five"  name="colors" type="radio" v-model="color" value="#ffffff" @change="changeColor"><label for="five" class="upper"></label>
        </span>
        <span id="pens">
            <input id="marker"   name="pens" type="radio" v-model="pen" value="marker"   @change="changePen"><label for="marker"></label>
            <input id="thinPen"  name="pens" type="radio" v-model="pen" value="thinPen"  @change="changePen"><label for="thinPen"></label>
            <input id="thickPen" name="pens" type="radio" v-model="pen" value="thickPen" @change="changePen"><label for="thickPen"></label>
            <!-- <input id="eraser"   type="button" value="" @change="clickEraser"><label for="eraser"></label> -->
        </span>
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
            color: "#000000",
            pen: "marker",
			drawCanvas: null, drawCxt: null,
            previewCanvas: null, previewCxt: null,
            isClicked: false,

            mouse: {x:0, y:0},
		}
	},
	methods: {
		changeColor(){
            this.$emit('change-color', this.color);
        },
        changePen(){
            this.$emit('change-pen', this.pen);
        },
        clickEraser(){

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
        mask-image: url(../img/14743.png);
        -webkit-mask-image: url(../img/pen9.png);
    }
    #pens #thinPen + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: var(--dynamic-color);
        border: solid 2px #777777;
        mask-image: url(../img/14743.png);
        -webkit-mask-image: url(../img/pen7.png);
    }
    #pens #thickPen + label{
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: var(--dynamic-color);
        border: solid 2px #777777;
        mask-image: url(../img/14743.png);
        -webkit-mask-image: url(../img/pen8.png);
    }
    #pens input[type=radio]:checked + label{
        border: solid 2px palevioletred !important;
		/* background: chartreuse !important; */
	}

</style>