<template>
	<div id="propertyBase">
        <input id="size" type="range" min="0" max="100" step="1" v-model="size" @change="changeSize">
		<input id="alpha" type="range" min="0.0" max="1.0" step="0.1" v-model="alpha" @change="changeAlpha">
    </div>
</template>

<script>
module.exports = {
	components: {
		
    },
	props: {
		initSize: {default: 5},
		initAlpha: {default: 0.5},
	},
	mounted() {
        
	},
	computed: {
	},
	data: function () {
		return {
            size: this.initSize,
            alpha: this.initAlpha,
		}
	},
	methods: {
        changeSize(){
            console.log(this.size);
        },
        changeAlpha(){
			console.log(this.alpha);
            // this.$emit('change-alpha', this.alpha);
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