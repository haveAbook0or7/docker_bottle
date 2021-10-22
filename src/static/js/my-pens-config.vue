<template>
	<div id="propertyBase" :style="elementColor">
        
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
            colorPalette: {black: "#000000", one: "#ff0000", two: "#00ff00", three: "#0000ff", four: "#ffff00", five: "#ffffff"},
            color: "#000000",
            pen: "marker",
            alpha: 0.8,
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
            this.color = "#ffffff";
            this.$emit('click-eraser', this.color);
        },
        changeAlpha(){
            this.$emit('change-alpha', this.alpha);
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
    
</style>