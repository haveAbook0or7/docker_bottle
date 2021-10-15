<template>
	<div id="paletteBase">
        <span id="color">
            <input id="black" name="color" type="radio" v-model="penColor" value="#000000" @change="changeColor"><label for="black"></label>
            <input id="one"   name="color" type="radio" v-model="penColor" value="#ff0000" @change="changeColor"><label for="one" class="upper"></label>
            <input id="two"   name="color" type="radio" v-model="penColor" value="#00ff00" @change="changeColor"><label for="two"></label>
            <input id="three" name="color" type="radio" v-model="penColor" value="#0000ff" @change="changeColor"><label for="three" class="upper"></label>
			<input id="four"  name="color" type="radio" v-model="penColor" value="#ffff00" @change="changeColor"><label for="four"></label>
            <input id="five"  name="color" type="radio" v-model="penColor" value="#ffffff" @change="changeColor"><label for="five" class="upper"></label>
        </span>
        <span id="pen">
            <input id="marker"   name="pens" type="radio" v-model="pen" value="marker"   @change="changePen" checked><label for="marker"></label>
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
		// showFlg: {
		// 	get(){
		// 		return this.mydbname == "H1_2_DefaultDataMax" ? false : true;
		// 	}
		// },
	},
	data: function () {
		return {
            penColor: "#000000",
            pen: "marker",
			drawCanvas: null, drawCxt: null,
            previewCanvas: null, previewCxt: null,
            isClicked: false,

            mouse: {x:0, y:0},
		}
	},
	methods: {
		changeColor(){

        },
        changePen(){

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
	#color input[type=radio] + label{
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
	#color input[type=radio]:checked + label{
		background: goldenrod;
	}

    #pen input[type=radio] + label{
		position: relative;
		display: inline-block;
        margin: 2.5px 2px;
        width: 45px;
        height: 45px;
        background: beige;
	}
    #pen #marker + label{
        mask: no-repeat center/70%;
        -webkit-mask: no-repeat center/70%;
        background: darkorange;
        mask-image: url(../img/14743.png);
        -webkit-mask-image: url(../img/14743.png);
    }
    #pen input[type=radio]:checked + label{
		background: goldenrod !important;
	}

</style>