<template>
	<div class="my-pens-config">
		<table border="0">
			<tr>
				<td>サイズ</td>
				<td><input id="size" type="range" min="0" max="100" step="1" v-model="size" @change="changeValue"></td>
				<td><input type="text" maxlength="3" :value="size" @change="changeValue('size', $event.target.value)" @keydown.enter="$event.target.blur()"></td>
			</tr>
			<tr>
				<td>不透明度</td>
				<td><input id="alpha" type="range" min="0.0" max="1.0" step="0.1" v-model="alpha" @change="changeValue"></td>
				<td><input type="text" maxlength="3" :value="alpha" @change="changeValue('alpha', $event.target.value)" @keydown.enter="$event.target.blur()"></td>
			</tr>
		</table>
    </div>
</template>

<script>
module.exports = {
	data: function () {
		return {
            size: null,
            alpha: null,
		}
	},
	methods: {
		setInitValue(size, alpha){
			this.size = size;
			this.alpha = alpha;
		},
        changeValue(label="range", value=null){
			switch(label){
				case "size":
					let regexS = /^([1-9]?[0-9]|100)$/
					console.log(regexS.test(value))
					if(regexS.test(value)){
						this.size = value;
					}
					break;
				case "alpha":
					let regex = /^(0(\.[0-9][1-9]?)?)|1.0|1$/
					if(regex.test(value)){
						this.alpha = value;
					}
					break;
			}
			// DOMを更新するためStringにして入れ直す
			this.size = String(this.size);
			this.alpha = String(this.alpha);
			// my-paletteに渡す
			this.$emit('change', this.size, this.alpha);
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
		background: #cfd982;
	}
	div{
		display: inline-block;
		width: 220px;
		height: 85px;
	}
	input[type=range]{
		width: 125px;
	}
	input[type=text]{
		border: solid 1px #e6b422;
		box-sizing: border-box;
		width: 25px;
	}
	input[type=text]:focus{
        outline-color: #928c36;
    }
</style>