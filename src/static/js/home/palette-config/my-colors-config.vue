<template>
	<div class="my-colors-config" :style="variables">
        <table border="0">
            <tr>
                <td colspan="3" style="text-align: right;">
                    #<input id="rgb16" type="text" maxlength="6" v-model="rgbhex" @change="changeColor" @keydown.enter="$event.target.blur()">
                </td>
            </tr>
            <tr>
                <td>R</td>
                <td><input id="r" type="range" min="0" max="255" step="1" v-model="v_red" @change="changeColor"></td>
                <td><input type="text" maxlength="3" v-model="v_red" @change="changeColor" @keydown.enter="$event.target.blur()"></td>
            </tr>
            <tr>
                <td>G</td>
                <td><input id="g" type="range" min="0" max="255" step="1" v-model="v_green" @change="changeColor"></td>
                <td><input type="text" maxlength="3" v-model="v_green" @change="changeColor" @keydown.enter="$event.target.blur()"></td>
            </tr>
            <tr>
                <td>B</td>
                <td><input id="b" type="range" min="0" max="255" step="1" v-model="v_blue" @change="changeColor"></td>
                <td><input type="text" maxlength="3" v-model="v_blue" @change="changeColor" @keydown.enter="$event.target.blur()"></td>
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
						"--W": "230px",
                        "--H": "100px",
                        "--rangeW": "180px",
                        "--textW": "25px",
                        "--text16W": "75px",
					};
				case "TabletPC":
					return {
                        "--FS": "24px",
						"--W": "350px",
                        "--H": "180px",
                        "--rangeW": "270px",
                        "--textW": "50px",
                        "--text16W": "100px",
					};
				case "SmartPhone":
					return {};
			}
        },
        rgbhex: {
			get(){
				return this.dectohex(this.red)+this.dectohex(this.green)+this.dectohex(this.blue);
			},
            set(value){
                const regex = /^[0-9a-f]{6}$/
                if(regex.test(value)){
                    this.red = this.hextodec(value[0]+value[1]);
                    this.green = this.hextodec(value[2]+value[3]);
                    this.blue = this.hextodec(value[4]+value[5]);
                }
            }
		},
        v_red:{
			get(){return this.red},
			set(value){
				const regex = /^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))$/
				if(regex.test(value)){
					this.red = value;
				}
			}
        },
        v_green:{
			get(){return this.green},
			set(value){
				const regex = /^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))$/
				if(regex.test(value)){
					this.green = value;
				}
			}
        },
        v_blue:{
			get(){return this.blue},
			set(value){
				const regex = /^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))$/
				if(regex.test(value)){
					this.blue = value;
				}
			}
        },
	},
	data: function () {
		return {
            red: null,
            green: null,
            blue: null,
		}
	},
	methods: {
        setInitValue(value){
            this.rgbhex = value.substr(1);
        },
        dectohex(num){
            const henkan = "0123456789abcdef";
            var re = "";
            var n = num;
            while(true){
                re += henkan[n%16];
                if(n < 16){
                    break;
                }
                n  = n / 16 | 0;
            }
            var res = re.split("").reverse().join("");
            return res.padStart(2, "0");
        },
        hextodec(num){
            const henkan = "0123456789abcdef";
            return henkan.indexOf(num[0]) * 16 + henkan.indexOf(num[1]) * 1;
        },
        changeColor(){
            // DOMを更新するためStringにして入れ直す
            this.red = String(this.red);
            this.green = String(this.green);
            this.blue = String(this.blue);
            // my-paletteに渡す
			this.$emit('change', "#"+this.rgbhex);
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
    #rgb16{
        width: var(--text16W);
    }
</style>