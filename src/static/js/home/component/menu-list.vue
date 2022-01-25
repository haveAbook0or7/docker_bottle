<template>
	<div class="menu-list" :style="variables">
        <meta v-if="reloadFlg" http-equiv="refresh" content=" 0; url=/">
        <meta v-if="signinFlg" http-equiv="refresh" content=" 0; url=/signin.html">
        <a class="menuitem" v-for="menu in menu" :key="menu.name" :href="menu.url" target="_blank" v-show="menu.show">{{menu.name}}</a>
		<input class="menuitem" type="button" :value="sign.name" @click="clickSign(sign.value)">
	</div>
</template>

<script>
module.exports = {
    props: {
        media: {default:"PC"},
		login_user: {default:null},
	},
    computed: {
        variables() {
            switch(this.media){
				case "PC":
					return {
                        "--FS": "13px",
						"--T": "20px",
                        "--R": "initial",
                        "--L": "0px",
                        "--H": "20px",
                        "--W": "120px",
                        "--border": "1px",
					};
				case "TabletPC":
					return {
                        "--FS": "18px",
						"--T": "75px",
                        "--R": "0px",
                        "--L": "initial",
                        "--H": "40px",
                        "--W": "180px",
                        "--border": "1px",
					};
				case "SmartPhone":
					return {
                        "--FS": "38px",
						"--T": "70px",
                        "--R": "initial",
                        "--L": "0px",
                        "--H": "80px",
                        "--W": "420px",
                        "--border": "2px",
					};
			}
        }
	},
	data: function () {
		return {
            reloadFlg: false,
            signinFlg: false,
            isOpen: false,
            menu: [
                {name: "マイメモ", url: "/userfile.html", show: this.login_user != "guest"}
            ],
            sign: {
                name: this.login_user == "guest" ? "サインイン" : "サインアウト",
                value: this.login_user == "guest" ? "signin" : "signout",
            }
		}
	},
	methods: {
        clickSign(value){
            console.log(value);
            switch(value){
                case "signin":
                    this.signinFlg = true;
                    break;
                case "signout":
                    axios.get("/userlogins/signout")
                    .then(response => {
                        console.log(response.data);
                        this.reloadFlg = true;
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
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
		font-size: var(--FS);
        width: var(--W);
        position: relative;
        display: inline-block;
        text-align: center;
	}
    div{
        position: absolute;
        left: var(--L);
        right: var(--R);
        top: var(--T);
        border: var(--border) solid gray;
    }
    a{
        height: var(--H);
        width: var(--W);
        line-height: 25px;
        color: slategray;
        text-decoration: none;
        background: #fff;
        box-sizing: border-box;
        border-bottom: 1px solid #aaa;
        cursor: default;
        display: table-cell;
        vertical-align:middle;
    }
    input[type=button]{
		height: var(--H);
        width: var(--W);
		color: #fff;
		background: #1c305c;
        box-sizing: border-box;
    }
    input[type=button]:active{
		box-sizing: border-box;
		border: 2px inset #4c505a;
	}
</style>