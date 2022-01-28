<template>
	<div class="signupBase" :style="variable">
		<span>らくがきちょう</span>
		<!-- トークン照合クリア -->
		<div class="form" v-show="tokenflg && !signupflg">
			<label id="id">ユーザーID</label><span id="iderr">{{this.idErr}}</span>
			<input type="text" v-model="id" @input="inputId" @keydown.enter="signup">
			<label id="pass">パスワード</label><span id="passerr">{{this.psErr}}</span>
			<input type="password" v-model="pass" @input="inputPass" @keydown.enter="signup">
			<label id="email">メールアドレス</label><span id="emailerr">{{this.emErr}}</span>
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
		// 端末の種類取得
		this.media = getMedia();
		console.log(this.media);
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
		variable(){
			switch(this.media){
				case "PC":
					return {
						"--FS": "13px",
						"--spanFS": "30px",
						"--passT": "50px",
						"--emailT": "95px",
						"--passerT": "50px",
						"--emailerT": "95px",
						"--spanT": "5px",
						"--spanL": "80px",
						"--spanW": "300px",
						"--textW": "200px",
						"--textH": "20px",
						"--textM": "25px",
						"--buttonW": "100px",
						"--buttonH": "30px",
						"--buttonM": "20px 50px",
						"--aFS": "17px",
					};
				case "TabletPC":
					return {
						"--FS": "18px",
						"--spanFS": "30px",
						"--passT": "80px",
						"--emailT": "157px",
						"--passerT": "80px",
						"--emailerT": "157px",
						"--spanT": "5px",
						"--spanL": "130px",
						"--spanW": "450px",
						"--textW": "300px",
						"--textH": "40px",
						"--textM": "35px",
						"--buttonW": "200px",
						"--buttonH": "50px",
						"--buttonM": "20px 50px",
						"--aFS": "25px",
					};
				case "SmartPhone":
					return {
						"--FS": "35px",
						"--spanFS": "45px",
						"--passT": "190px",
						"--emailT": "367px",
						"--passerT": "230px",
						"--emailerT": "407px",
						"--spanT": "50px",
						"--spanL": "0px",
						"--spanW": "800px",
						"--textW": "700px",
						"--textH": "80px",
						"--textM": "100px",
						"--buttonW": "400px",
						"--buttonH": "90px",
						"--buttonM": "60px 150px",
						"--aFS": "50px",
					};
			}
		},
		errFlg: {
            get(){
				console.log(this.idFlg && this.psFlg && this.emFlg ? true : false);
                return this.idFlg && this.psFlg && this.emFlg ? true : false;
			}
        }
	},
	data: function () {
		return {
			media: "PC",
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
		font-size: var(--FS);
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
		font-size: var(--spanFS);
	}
	.form{
		position: relative;
		/* height: 150px; */
		margin: 10px;
		text-align: center;
	}
	label{
		position: absolute;
		left: -10px;
		top: 5px;
	}
	.form > span{
		position: absolute;
		top: var(--spanT);
		left: var(--spanL);
		width: var(--spanW);
		color: #d93a25;
		text-align: left;
	}
	#pass{
		top: var(--passT);
	}
	#email{
		top: var(--emailT);
	}
	#passerr{
		top: var(--passerT);
	}
	#emailerr{
		top: var(--emailerT);
	}
	input[type=text], input[type=password]{
		display: block;
		width: var(--textW);
		height: var(--textH);
		margin-top: var(--textM);
		padding-left: 3px;
		background: #fff;
		color: #2b2b2b;
	}
	input[type=text]:focus, input[type=password]:focus{
		outline: none;
	}
	input[type=button]{
		width: var(--buttonW);
		height: var(--buttonH);
		margin: var(--buttonM);
		background: #c3d825;
	}
	input[type=button]:active{
		box-sizing: border-box;
		border: 2px inset #cad957;
	}
	a{
		font-size: var(--aFS);
	}
</style>