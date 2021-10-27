<template>
	<div id="propertyBase">
		<table border="0">
			<tr>
				<td>サイズ</td>
				<td><input id="size" type="range" min="0" max="100" step="1" v-model="size" @change="changeSize"></td>
				<td><input type="text" v-model="size" @change="changeSize"></td>
			</tr>
			<tr>
				<td>不透明度</td>
				<td><input id="alpha" type="range" min="0.0" max="1.0" step="0.1" v-model="alpha" @change="changeAlpha"></td>
				<td><input type="text" v-model="alpha" @change="changeAlpha"></td>
			</tr>
		</table>
    </div>
</template>

<script>
module.exports = {
	components: {
		
    },
	props: {
		id_name: {default: ""},
		init_size: {default: 5},
		init_alpha: {default: 0.5},
	},
	mounted() {
        
	},
	computed: {
	},
	data: function () {
		return {
            size: this.init_size,
            alpha: this.init_alpha,
		}
	},
	methods: {
        changeSize(){
			this.$emit('change-size', this.id_name, "size", this.size);
        },
        changeAlpha(){
            this.$emit('change-alpha', this.id_name, "alpha", this.alpha);
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
		background: #777777;
	}
	div{
		display: inline-block;
		width: 220px;
		height: 85px;
		position: absolute;
		bottom: -85px;
		right: 0;
	}
	input[type=range]{
		width: 125px;
	}
	input[type=text]{
		border: solid 1px goldenrod;
		box-sizing: border-box;
		width: 25px;
	}
    
</style>