<template>
	<div class="my-pens-config" :style="variables">
		<table border="0">
			<tr><td colspan="2">サイズ</td></tr>
			<tr>
				
				<td><input id="size" type="range" min="0" max="100" step="1" v-model="size" @change="changeValue"></td>
				<td><input type="text" maxlength="3" :value="size" @change="changeValue('size', $event.target.value)" @keydown.enter="$event.target.blur()"></td>
			</tr>
			<tr><td colspan="2">不透明度</td></tr>
			<tr>
				
				<td><input id="alpha" type="range" min="0.0" max="1.0" step="0.1" v-model="alpha" @change="changeValue"></td>
				<td><input type="text" maxlength="3" :value="alpha" @change="changeValue('alpha', $event.target.value)" @keydown.enter="$event.target.blur()"></td>
			</tr>
		</table>
    </div>
</template>

<script>
module.exports = {
	props: {
        media: {default:"PC"},
    },
	computed: {
        variables() {
            switch(this.media){
				case "PC":
					return {
                        "--FS": "13px",
						"--W": "220px",
                        "--H": "100px",
                        "--rangeW": "125px",
                        "--textW": "25px",
					};
				case "TabletPC":
					return {
                        "--FS": "22px",
						"--W": "350px",
                        "--H": "180px",
                        "--rangeW": "250px",
                        "--textW": "45px",
					};
				case "SmartPhone":
					return {};
			}
        },
	},
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
		font-size: var(--FS);
		background: #cfd982;
	}
	div{
		display: inline-block;
		width: var(--W);
		height: var(--H);
	}
	input[type=range]{
		width: var(--rangeW);
	}
	input[type=text]{
		border: solid 1px #e6b422;
		box-sizing: border-box;
		width: var(--textW);
	}
	input[type=text]:focus{
        outline-color: #928c36;
    }
</style>