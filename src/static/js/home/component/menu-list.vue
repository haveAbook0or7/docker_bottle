<template>
	<div :style="variable">
        <a class="menuitem" v-for="menu in menu" :key="menu.name" :href="menu.url" target="_blank" v-show="menu.show">{{menu.name}}</a>
		<input class="menuitem" type="button" :value="sign.name" @click="clickSign(sign.value)">
	</div>
</template>

<script>
module.exports = {
    props: {
		login_user: {default:null},
	},
    computed: {
		variable() {
			return {
				"--dynamic-color": this.isOpen ? "#da3c41" : "#1b2538",
                "--top": this.isOpen ? "0px" : "15px",
                "--bottom": this.isOpen ? "15px" : "0px",
			}
		},
	},
	data: function () {
		return {
            isOpen: false,
            menu: [
                {name: "マイメモ", url: ""+this.login_user, show: this.login_user != "ゲスト"}
            ],
            sign: {
                name: this.login_user == "ゲスト" ? "サインイン" : "サインアウト",
                value: this.login_user == "ゲスト" ? "signin" : "signout",
                }
		}
	},
	methods: {
        clickSign(value){
            console.log(value);
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
        width: 100px;
        position: relative;
        display: inline-block;
        text-align: center;
	}
    div{
        position: absolute;
        left: 0;
        top: 20px;
    }
    a{
        height: 25px;
        line-height: 25px;
        color: slategray;
        text-decoration: none;
        background: #fff;
        box-sizing: border-box;
        border-bottom: 1px solid #aaa;
    }
    input[type=button]{
		height: 25px;
		color: #fff;
		background: #da3c41;
        box-sizing: border-box;
    }
    input[type=button]:active{
		box-sizing: border-box;
		border: 2px inset #c0353a;
	}
</style>