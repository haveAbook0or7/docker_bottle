<template>
	<div id="propertyBase">
        <table border="0">
            <tr><td colspan="3" style="text-align: right;">#<input id="rgb16" type="text" maxlength="6" v-model="rgbhex" @change="changeColor"></td></tr>
            <tr>
                <td>R</td>
                <td><input id="r" type="range" min="0" max="255" step="1" v-model="r" @change="changeColor"></td>
                <td><input type="text" maxlength="3" v-model="r" @input="inputNum('r', r)" @change="changeColor"></td>
            </tr>
            <tr>
                <td>G</td>
                <td><input id="g" type="range" min="0" max="255" step="1" v-model="g" @change="changeColor"></td>
                <td><input type="text" maxlength="3" v-model="g" @input="inputNum('g', g)" @change="changeColor"></td>
            </tr>
            <tr>
                <td>B</td>
                <td><input id="b" type="range" min="0" max="255" step="1" v-model="b" @change="changeColor"></td>
                <td><input type="text" maxlength="3" v-model="b" @input="inputNum('b', b)" @change="changeColor"></td>
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
        init_rgbhex: {default: "ffffff"},
	},
	mounted() {
        
	},
	computed: {
        rgbhex: {
            cache: false,
			get(){
				return this.dectohex(this.r)+this.dectohex(this.g)+this.dectohex(this.b);
			},
            set(v){
                if(!/^[0-9a-f]{6}$/.test(v)){
                    return;
                }
                this.r = this.hextodec(v[0]+v[1]);
                this.g = this.hextodec(v[2]+v[3]);
                this.b = this.hextodec(v[4]+v[5]);
            }
		},
	},
	data: function () {
        var v = this.init_rgbhex.slice(1);
        var rr = this.hextodec(v[0]+v[1]);
        var gg = this.hextodec(v[2]+v[3]);
        var bb = this.hextodec(v[4]+v[5]);
		return {
            r: rr,
            g: gg,
            b: bb,
		}
	},
	methods: {
        dectohex(num){
            var henkan = "0123456789abcdef";
            var re = [];
            var n = num;
            while(true){
                re.push(henkan[n%16]);
                if(n < 16){
                    break;
                }
                n  = n / 16 | 0;
            }
            re = re.reverse();
            var res = "";
            for(var i = 0; i < re.length; i++){
                res += re[i];
            }
            return res.padStart(2, "0");
        },
        hextodec(num){
            var henkan = "0123456789abcdef";
            return henkan.indexOf(num[0]) * 16 + henkan.indexOf(num[1]) * 1;
        },
        inputNum(lbl, n){
            if(n < 0 || n == ""){
                this[lbl] = 0;
            }
            if(n > 255){
                this[lbl] = 255;
            }
        },
        changeColor(){
			this.$emit('change', this.id_name, "#"+this.rgbhex);
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
		background: #777777;
	}
	div{
		display: inline-block;
		width: 230px;
		height: 100px;
		position: absolute;
		bottom: -100px;
		left: 0;
	}
	input[type=range]{
		width: 180px;
	}
	input[type=text]{
		border: solid 1px goldenrod;
		box-sizing: border-box;
		width: 25px;
	}
    #rgb16{
        width: 75px;
    }
    
</style>