<template>
	<div class="signuppreBase" :style="variable">
		<span>らくがきちょう</span>
		<!-- 初期画面 -->
		<div class="form" v-show="showflg && !tempFlg">
			<label id="email">メールアドレス</label><span id="emerr">{{this.emErr}}</span>
			<input type="text" v-model="email" @input="inputEmail" @keydown.enter="signupPre">
			<input type="button" value="仮登録" :disabled="!emFlg" @click="signupPre" @keydown.enter="signupPre">
		</div>
		<!-- エラー -->
		<div class="form" v-show="!showflg">
			{{this.msg}}
		</div>
		<!-- 登録完了 -->
		<div class="form" v-show="tempFlg">
			{{this.msg}}<br>
			受信したメールのURLから本登録を行ってください。
		</div>
    </div>
</template>

<script>
module.exports = {
	mounted(){
		// 端末の種類取得
		this.media = getMedia();
		console.log(this.media);
	},
	computed: {
		variable(){
			switch(this.media){
				case "PC":
					return {
						"--FS": "13px",
						"--spanFS": "30px",
						"--passT": "50px",
						"--spanT": "5px",
						"--spanL": "85px",
						"--spanW": "500px",
						"--textW": "200px",
						"--textH": "20px",
						"--textM": "25px",
						"--buttonW": "100px",
						"--buttonH": "30px",
						"--buttonMTB": "20px",
						"--buttonMLR": "50px",
					};
				case "TabletPC":
					return {
						"--FS": "18px",
						"--spanFS": "30px",
						"--passT": "75px",
						"--spanT": "80px",
						"--spanL": "0px",
						"--spanW": "500px",
						"--textW": "300px",
						"--textH": "40px",
						"--textM": "35px",
						"--buttonW": "200px",
						"--buttonH": "50px",
						"--buttonMTB": "35px",
						"--buttonMLR": "50px",
					};
				case "SmartPhone":
					return {
						"--FS": "35px",
						"--spanFS": "45px",
						"--passT": "140px",
						"--spanT": "150px",
						"--spanL": "0px",
						"--spanW": "800px",
						"--textW": "700px",
						"--textH": "80px",
						"--textM": "60px",
						"--buttonW": "400px",
						"--buttonH": "70px",
						"--buttonMTB": "60px",
						"--buttonMLR": "150px",
					};
			}
		},
	},
	data: function () {
		return {
			media: "PC",
			email: "",
			showflg: true,
			tempFlg: false,
			msg: "",
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
					this.showflg = response.data.data.flg;
					this.tempFlg = response.data.data.flg;
					this.msg = response.data.message;
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
		font-size: var(--FS);
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
		font-size: var(--spanFS);
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
		top: var(--spanT);
		left: var(--spanL);
		width: var(--spanW);
		color: #d93a25;
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
		margin: var(--buttonMTB) var(--buttonMLR);
		background: #c3d825;
	}
	input[type=button]:active{
		box-sizing: border-box;
		border: 2px inset #cad957;
	}
</style>