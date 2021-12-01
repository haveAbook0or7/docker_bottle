<template>
	<div class="signupBase">
		<meta v-if="reFlg" http-equiv="refresh" content=" 0; url=/">
		<span>らくがきちょう</span>
		<div class="form">
			<label id="id">ユーザーID</label><span id="iderr">{{this.idErr}}</span>
			<input type="text" v-model="id" @input="inputId" @keydown.enter="signup">
			<label id="pass">パスワード</label><span id="pserr">{{this.psErr}}</span>
			<input type="password" v-model="pass" @input="inputPass" @keydown.enter="signup">
			<label id="email">メールアドレス</label><span id="emerr">{{this.emErr}}</span>
			<input type="text" v-model="email" @input="inputEmail" @keydown.enter="signup">
			<input type="button" value="サインアップ" :disabled="!errFlg" @click="signup" @keydown.enter="signup">
		</div>
    </div>
</template>

<script>
module.exports = {
	props: {
        token: {default:null},
    },
	mounted() {
		
	},
	computed: {
		errFlg: {
            get(){
				console.log(this.id);
                return this.idFlg && this.psFlg && this.emFlg ? true : false;
			}
        }
	},
	data: function () {
		return {
			id: "",
			pass: "",
			email: "",
			reFlg: false,
			idErr: "", psErr: "", emErr: "",
			idFlg: false, psFlg: false, emFlg: false,
		}
	},
	methods: {
		signup(){

		},
		inputId(){
			const regex = /^[a-zA-Z0-9]{2,40}$/;
			if(regex.test(this.id)){
				this.idErr = "";
				this.idFlg = true;
            }else{
				this.idErr = "IDは英数字2～40文字です。";
				this.idFlg = false;
			}
		},
        inputPass(){
			const regex = /^[a-zA-Z0-9]{6,8}$/;
			if(regex.test(this.pass)){
				this.psErr = "";
				this.psFlg = true;
            }else{
				this.psErr = "パスワードは英数字6～10文字です。";
				this.psFlg = false;
			}
		},
		inputEmail(){
			const regex = /^[a-zA-Z0-9_+-]+(\.[a-zA-Z0-9_+-]+)*@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/;
			if(regex.test(this.email)){
				this.emErr = "";
				this.emFlg = true;
            }else{
				this.emErr = "これはメールアドレスの形式ではありません。";
				this.emFlg = false;
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
		font-size: 13px;
		background: #0f2350;
		color: #fff;
		height: initial;
	}
	.signupBase{
		height: 100%;
		display: flex;
		-webkit-flex-direction: column;
		flex-direction: column;
		-webkit-justify-content: center;
		justify-content: center;
		-webkit-align-items: center;
		align-items: center;
	}
	.signupBase > span{
		display: block;
		height: 45px;
		width: 100%;
		background: #1c305c;
		line-height: 50px;
		text-align: center;
		font-size: 30px;
	}
	.form{
		position: relative;
		height: 150px;
		margin: 10px;
	}
	label{
		position: absolute;
		left: -10px;
		top: 5px;
	}
	#pass{
		top: 50px;
	}
	.form > span{
		position: absolute;
		top: 5px;
		left: 80px;
		width: 300px;
		color: #d93a25;
	}
	#pserr{
		top: 50px;
	}
	input[type=text], input[type=password]{
		display: block;
		width: 200px;
		height: 20px;
		margin: 25px 0 0 0;
		padding-left: 3px;
		background: #fff;
		color: #2b2b2b;
	}
	input[type=text]:focus, input[type=password]:focus{
		outline: none;
	}
	input[type=button]{
		width: 100px;
		height: 30px;
		margin: 20px 50px;
		background: #c3d825;
	}
	input[type=button]:active{
		box-sizing: border-box;
		border: 2px inset #cad957;
	}
</style>