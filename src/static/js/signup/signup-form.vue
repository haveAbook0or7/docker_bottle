<template>
	<div class="signupBase">
		<span>らくがきちょう</span>
		<!-- トークン照合クリア -->
		<div class="form" v-show="tokenflg && !signupflg">
			<label id="id">ユーザーID</label><span id="iderr">{{this.idErr}}</span>
			<input type="text" v-model="id" @input="inputId" @keydown.enter="signup">
			<label id="pass">パスワード</label><span id="pass">{{this.psErr}}</span>
			<input type="password" v-model="pass" @input="inputPass" @keydown.enter="signup">
			<label id="email">メールアドレス</label><span id="email">{{this.emErr}}</span>
			<input type="text" v-model="email" @input="inputEmail" @keydown.enter="signup">
			<input type="button" value="サインアップ" :disabled="!errFlg" @click="signup" @keydown.enter="signup">
		</div>
		<!-- エラー -->
		<div class="form" v-show="!tokenflg">
			{{this.msg}}
		</div>
		<!-- 登録完了 -->
		<div class="form" v-show="signupflg">
			{{this.msg}}下記リンクからログインを行ってください。<br>
			<a href="/signin.html">ログイン</a>
		</div>
    </div>
</template>

<script>
module.exports = {
	mounted() {
		// URLを取得
		var url = new URL(window.location.href);
		// URLSearchParamsオブジェクトを取得
		var params = url.searchParams;
		// getメソッド
		this.token = params.get('token');
		console.log(this.token);
		// token照合
		axios.post("/userlogins/signup",{
			flg: "mounted",
			data: {token: this.token}
		})
		.then(response => {
			console.log(response.data);
			this.tokenflg = response.data.data.flg;
			this.email = response.data.data.email;
			this.emFlg = true;
			this.msg = response.data.message;
		})
		.catch(function (error) {
			console.log(error);
		});
	},
	computed: {
		errFlg: {
            get(){
				console.log(this.idFlg && this.psFlg && this.emFlg ? true : false);
                return this.idFlg && this.psFlg && this.emFlg ? true : false;
			}
        }
	},
	data: function () {
		return {
			token: null,
			tokenflg: false,
            signupflg: false,
			msg: "",
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
			if(this.errFlg){
				this.idErr = "";
				this.psErr = "";
				this.emErr = "";
				axios.post("/userlogins/signup",{
					flg: "signup",
					data: {
						id: this.id,
						pass: this.pass,
						email: this.email,
					}
				})
				.then(response => {
					console.log(response.data);
					console.log(response.data.data.flg);
					if(response.data.data.flg){
						this.msg = response.data.message;
						this.signupflg = true;
						console.log(this.signupflg);
					}else{
						switch(response.data.data.err){
							case "err":
								this.msg = response.data.message;
								this.tokenflg = false;
								break;
							case "idErr":
								this.idErr = response.data.message;
								break;
							case "psErr":
								this.psErr = response.data.message;
								break;
							case "emErr":
								this.emErr = response.data.message;
								break;
						}
					}
				})
				.catch(function (error) {
					console.log(error);
				});
			}
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
	.form > span{
		position: absolute;
		top: 5px;
		left: 85px;
		width: 300px;
		color: #d93a25;
	}
	#pass{
		top: 50px;
	}
	#email{
		top: 95px;
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