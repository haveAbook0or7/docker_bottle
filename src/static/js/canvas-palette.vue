<template>
	<div id="Base" style="width: 900px; height: 900px;">
        <my-palette @change-color="changeColor" @change-pen="changePen"></my-palette>
        <my-canvas ref="myCanvas"></my-canvas>
    </div>
</template>

<script>
module.exports = {
	components: {
		'my-canvas': httpVueLoader('./my-canvas.vue'),
        'my-palette': httpVueLoader('./my-palette.vue'),
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
            
            
		}
	},
	methods: {
		changeColor(value){
            this.$refs.myCanvas.changeColor(value);
        },
        changePen(color, size, alpha, cap){
            this.$refs.myCanvas.changePen(color, size, alpha, cap);
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
</style>