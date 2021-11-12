<template>
	<div id="Base" :style="variables" @wheel="scroll">
        <my-palette @change-color="changeColor" @change-pen="changePen" @back-next="backNext"></my-palette>
        <my-canvas ref="myCanvas"></my-canvas>
    </div>
</template>

<script>
module.exports = {
	components: {
		'my-canvas': httpVueLoader('./my-canvas.vue'),
        'my-palette': httpVueLoader('./my-palette.vue'),
    },
	mounted() {
		// キャンバスサイズを取得
		this.baseheight = document.documentElement.clientHeight;
		this.canvasheight = document.documentElement.clientHeight;
	},
	computed: {
		variables() {
			return {
				"--height": this.canvasheight+"px",
			}
		},
	},
	data: function () {
		return {
			baseheight: null,
			canvasheight: null,
		}
	},
	methods: {
		scroll(e){
			var scrollLimit = this.canvasheight - this.baseheight;
			if(scrollLimit == e.view.pageYOffset){
				this.canvasheight += e.deltaY > 0 ? e.deltaY : 0;
			}
			this.$refs.myCanvas.canvasResize(this.canvasheight);
		},
		changeColor(value){
            this.$refs.myCanvas.changeColor(value);
        },
        changePen(color, size, alpha, cap){
            this.$refs.myCanvas.changePen(color, size, alpha, cap);
        },
		backNext(id){
			switch(id){
                case "back":
                    this.$refs.myCanvas.prevCanvas();
                    break;
                case "next":
                    this.$refs.myCanvas.nextCanvas();
                    break;
            }
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
	#Base{
		width: 100%;
		height: var(--height);
		background: brown;
	}
</style>