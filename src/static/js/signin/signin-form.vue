<template>
	<div class="signinBase" :style="variable">
		<meta v-if="reFlg" http-equiv="refresh" content=" 0; url=/">
		<span>らくがきちょう</span>
		<div class="form">
			<label id="id">ユーザーID</label><span id="iderr">{{this.idErr}}</span>
			<input type="text" v-model="id" @input="inputId" @keydown.enter="signin">
			<label id="pass">パスワード</label><span id="pserr">{{this.psErr}}</span>
			<input type="password" v-model="pass" @input="inputPass" @keydown.enter="signin">
			<input type="button" value="サインイン" :disabled="!errFlg" @touchend="signin" @click="signin" @keydown.enter="signin">
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
						"--passerT": "50px",
						"--iderT": "5px",
						"--spanL": "80px",
						"--spanW": "300px",
						"--textW": "200px",
						"--textH": "20px",
						"--textM": "25px",
						"--buttonW": "100px",
						"--buttonH": "30px",
						"--buttonM": "20px 50px",
					};
				case "TabletPC":
					return {
						"--FS": "18px",
						"--spanFS": "30px",
						"--passT": "75px",
						"--passerT": "75px",
						"--iderT": "5px",
						"--spanL": "100px",
						"--spanW": "400px",
						"--textW": "300px",
						"--textH": "40px",
						"--textM": "30px",
						"--buttonW": "200px",
						"--buttonH": "50px",
						"--buttonM": "20px 50px",
					};
				case "SmartPhone":
					return {
						"--FS": "35px",
						"--spanFS": "45px",
						"--passT": "190px",
						"--passerT": "230px",
						"--iderT": "50px",
						"--spanL": "0px",
						"--spanW": "800px",
						"--textW": "700px",
						"--textH": "80px",
						"--textM": "100px",
						"--buttonW": "400px",
						"--buttonH": "90px",
						"--buttonM": "40px 150px",
					};
			}
		},
		errFlg: {
            get(){
				console.log(this.id);
                return this.idFlg && this.psFlg ? true : false;
			}
        }
	},
	data: function () {
		return {
			media: "PC",
			id: "",
			pass: "",
			reFlg: false,
			idErr: "", psErr: "",
			idFlg: false, psFlg: false,
		}
	},
	methods: {
		signin(){
			if(this.errFlg){
				axios.post("/userlogins/signin",{
					id: this.id,
					pass: this.pass
				})
				.then(response => {
					console.log(response.data);
					this.reFlg = response.data.data.flg;
					this.idErr = response.data.message;
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
	.signinBase{
		height: 100%;
		display: flex;
		-webkit-flex-direction: column;
		flex-direction: column;
		-webkit-justify-content: center;
		justify-content: center;
		-webkit-align-items: center;
		align-items: center;
	}
	.signinBase > span{
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
	}
	label{
		position: absolute;
		left: -10px;
		top: 5px;
		background: transparent;
	}
	#pass{
		top: var(--passT);
	}
	.form > span{
		position: absolute;
		top: var(--spanT);
		left: var(--spanL);
		width: var(--spanW);
		height: 20px;
		color: #d93a25;
	}
	#iderr{
		top: var(--iderT);
	}
	#pserr{
		top: var(--passerT);
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
</style>