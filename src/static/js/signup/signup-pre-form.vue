<template>
	<div class="signuppreBase">
		<!-- <meta v-if="reFlg" http-equiv="refresh" content=" 0; url=/"> -->
		<span>らくがきちょう</span>
		<div class="form">
			<label id="email">メールアドレス</label><span id="emerr">{{this.emErr}}</span>
			<input type="text" v-model="email" @input="inputEmail" @keydown.enter="signupPre">
			<input type="button" value="仮登録" :disabled="!emFlg" @click="signupPre" @keydown.enter="signupPre">
		</div>
    </div>
</template>

<script>
module.exports = {
	data: function () {
		return {
			email: "",
			reFlg: false,
			emErr: "",
			emFlg: false,
		}
	},
	methods: {
		signupPre(){
			if(this.emFlg){
				axios.post("/userlogins/signup_pre",{
					email: this.email,
				})
				.then(response => {
					console.log(response.data);
					// this.showflg = response.data.data.flg;
					// this.tempFlg = response.data.data.flg;
					// this.msg = response.data.message;
				})
				.catch(function (error) {
					console.log(error);
				});
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
			console.log(this.emFlg);
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
	.signuppreBase{
		height: 100%;
		display: flex;
		-webkit-flex-direction: column;
		flex-direction: column;
		-webkit-justify-content: center;
		justify-content: center;
		-webkit-align-items: center;
		align-items: center;
	}
	.signuppreBase > span{
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
	.form > span{
		position: absolute;
		top: 5px;
		left: 80px;
		width: 300px;
		color: #d93a25;
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