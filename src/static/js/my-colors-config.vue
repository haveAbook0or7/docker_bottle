<template>
	<div id="propertyBase">
        <table border="0">
            <tr><td colspan="3"><input id="rgb16" type="text" v-model="rgb16" @change="changeSize"></td></tr>
            <tr>
                <td>R</td>
                <td><input id="r" type="range" min="0" max="255" step="1" v-model="r" @change="changeSize"></td>
                <td><input type="text" v-model="r" @change="changeSize"></td>
            </tr>
            <tr>
                <td>G</td>
                <td><input id="g" type="range" min="0" max="255" step="1" v-model="g" @change="changeSize"></td>
                <td><input type="text" v-model="g" @change="changeSize"></td>
            </tr>
            <tr>
                <td>B</td>
                <td><input id="b" type="range" min="0" max="255" step="1" v-model="b" @change="changeSize"></td>
                <td><input type="text" v-model="b" @change="changeSize"></td>
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
		init_r: {default: 100},
		init_g: {default: 100},
        init_b: {default: 50},
	},
	mounted() {
        
	},
	computed: {
        rgb16: {
			get(){
				return this.tento16(this.r)+this.tento16(this.g)+this.tento16(this.b);
			}
		},
	},
	data: function () {
		return {
            r: this.init_r,
            g: this.init_g,
            b: this.init_b,
		}
	},
	methods: {
        tento16(num){
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
        changeSize(){
			// this.$emit('change-size', this.id_name, "size", this.size);
        },
        changeAlpha(){
            // this.$emit('change-alpha', this.id_name, "alpha", this.alpha);
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
		width: 210px;
		height: 120px;
		position: absolute;
		/* bottom: -85px;
		right: 0; */
	}
	input[type=range]{
		width: 128px;
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