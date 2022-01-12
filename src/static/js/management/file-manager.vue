<template>
	<div class="filemanagerBase" @contextmenu="openMinWindow($event, 'default', null, null)" @click="$refs.minwin.closeModal()">
        <manage-window ref="minwin" @reload="reload" @rename="reNameStart"></manage-window>
        <div class="overlay" v-show="renameShowFlg" @click="$event.stopPropagation()" @contextmenu="$event.stopPropagation();$event.preventDefault();"></div>
		<div id="nowdir" @contextmenu="openMinWindow($event, 'none', null, null)">
            <!-- パス -->
            <span v-show="isLogin" v-for="(path, index) in [loginUser].concat(pathlist)" :key="index" @click="clickFolder(path)">
                {{path}} > 
            </span>
            <!-- エラーメッセージ -->
            <span id="error" v-show="!this.isLogin">{{message}}</span>
            <!-- ログインユーザー -->
            <table border="0">
            <tr style="height: 22px;">
                <td>{{this.loginUser}}</td>
            </tr>
            <tr><td colspan="3" style="font-size: 22px;">らくがきちょう</td></tr>
            </table>
        </div>
        <div id="filelist">
            <span v-show="isLogin" class="listbutton" v-for="(file, index) in filelist" :key="index" 
                :style="index == 0 ? 'border-top: 1px solid #cfd982;':''"
                @click="file.split('.').length == 1 ? clickFolder(file) : clickFile(file)" 
                @contextmenu="openMinWindow($event, file.split('.').length == 1 ? 'folder' : 'file', file, index)">
                    <label :class="file.split('.').length == 1 ? 'folder' : 'file'"></label>
                    <input type="text" :value="file.split('.')[0]" @click="eventStop($event, isreads[index])" 
                        :readonly="isreads[index]" ref="texts" 
                        @input="reNameNow(index, $event.target.value)"
                        @blur="reNameEnd(index, file)"
                        @keydown.enter="$event.target.blur()">
                    <label class="action" @click="openMinWindow($event, file.split('.').length == 1 ? 'folder' : 'file', file, index)"></label>
            </span>
        </div>
    </div>
</template>

<script>
module.exports = {
    components: {
		'manage-window': httpVueLoader('./manage-window.vue'),
    },
    beforeCreate(){
        /** 
         * 正規表現のフォーマットファイル(js)読み込み。
         * <body>に<script>を生成して無理やり読み込む。
         * ファイルパスはhtmlファイルがある位置からの相対パスなので注意。
         */
        let script = document.createElement('script');
        script.src = "../static/js/component/regularExpression.js"; //ファイルパス
        document.body.appendChild(script);
    },
    updated(){
        // ここで外部jsの関数を読み込む。
        this.renameRegex = window.getREGEX("FILE_NAME_REGEX");
    },
    mounted() {
        axios.get("/mngfiles/getnowdir")
		.then(response => {
            this.resProcess(response.data);
		})
		.catch(function (error) {
			console.log(error);
		});
    },
	data: function () {
		return {
            isLogin: true,
            message: "",
            loginUser: "guest",
            pathlist: [],
			filelist: [],
            isreads: [],
            renameRegex: null,
            renameShowFlg: false,
            renameFlg: false,
            renameFile: null,
            reNameMode: null,
		}
	},
	methods: {
        reload(pathArray){
            axios.post("/mngfiles/getnowdir",{
                nowdir: pathArray
            })
            .then(response => {
                this.resProcess(response.data);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        resProcess(resData){
            console.log(resData);
            this.isLogin = resData.data.flg;
            this.message = resData.message;
            this.loginUser = resData.data.user;
            this.pathlist = resData.data.path;
            this.filelist = resData.data.dirlist;
            this.isreads = [];
            for(const index in this.filelist){
                this.isreads.push(true);
            }
            console.log(this.message)
            console.log(this.isLogin);
        },
		clickFolder(folder){
            // 移動するフォルダのパスを求める。遡る場合もこれでOK
            let nowdir = [];
            if(this.loginUser != folder){
                for(const item of this.pathlist){
                    if(item == folder){
                        break;
                    }
                    nowdir.push(item);
                }
                nowdir.push(folder);
            }
            // 求めたパスで表示
            this.reload(nowdir);
        },
        clickFile(file){
            // クリックしたファイルを別ウィンドウで開く
            axios.post("/mngfiles/openfile",{
                openfile: this.pathlist.concat(file)
            })
            .then(response => {
                console.log(response.data);
                // <a>を生成して無理やり開く。
                const fileLink = document.createElement('a');
                fileLink.href = "/?fileopen="+response.data.data.flg;;
                fileLink.target = "_blank";
                document.body.appendChild(fileLink);
                fileLink.click();
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        eventStop(e, flg){
            // 名前変更処理時にクリック動作を止める。
            if(!flg){ e.stopPropagation()}
        },
        openMinWindow(e, mode, item, index){
            // 下敷きになってるコンポーネントの動作を拾わないようにする。
            e.stopPropagation();
            // デフォルトの右クリックメニューを止める。
            e.preventDefault();
            // カスタム右クリックメニュー表示。
            this.$refs.minwin.openModal(mode, {x: e.pageX, y: e.pageY}, this.pathlist, item, index);
        },
        reNameStart(index, mode){
            // ファイルかフォルダか記録
            this.reNameMode = mode;
            // 他の動作を止めるオーバーレイを表示
            this.renameShowFlg = true;
            // <input>をread-writeにしてフォーカスあてて名前変更開始
            this.$set(this.isreads, index, false);
            this.$refs.texts[index].focus();
        },
        reNameNow(index, value){
            // console.log(index)
            // console.log(value);
            // console.log(this.renameRegex.test(value));
            // 正規表現が通ったら仮保存変数に保存。フラグ立てる
            if(this.renameRegex.test(value)){
                this.renameFile = value;
            }
            this.renameFlg = this.renameRegex.test(value);
        },
        reNameEnd(index, file){
            // <input>をread-onlyにする
            this.$set(this.isreads, index, true);
            // [正規表現が通ってる][仮保存変数が空じゃない][前の名前と同じじゃない]の条件が通ったら変更処理
            if(this.renameFlg && this.renameFile != null && this.renameFile != file.split('.')[0]){
                // ファイルの名前変更なら最後にファイル形式(.png)をくっつける
                this.renameFile += this.reNameMode == "file" ? "."+file.split('.')[1] : "";
                // 変更処理
                axios.post("/mngfiles/renameitem",{
                    before: this.pathlist.concat(file),
                    after: this.pathlist.concat(this.renameFile)
                })
                .then(response => {
                    console.log(response.data);
                    // 完了したらリロード
                    this.reload(this.pathlist);
                })
                .catch(function (error) {
                    console.log(error);
                });
            }
            // 仮保存変数を初期化してオーバーレイを消す
            this.renameFile = null;
            this.renameShowFlg = false;
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
		color: #fff;
		height: initial;
	}
	.filemanagerBase{
        background: #0f2350;
        height: 100%;
    }
    /* 現在のパス */
    #nowdir{
        position: relative;
        height: 50px;
        background: #cfd982;
    }
    span{
        cursor: default;
        font-size: 18px;
        color: #000;
    }
    /* エラーメッセージ */
    #error{
        white-space: pre-line;
        font-size: 16px;
    }
    /* ユーザー名表示 */
    table{
        position: absolute;
        top: 0;
        right: 0;
        height: 50px;
        text-align: right;
        border-collapse: collapse;
        border-spacing: 0;
    }
    td{color: #000;}
    /* アイテム表示スペース */
    #filelist{
        box-sizing: border-box;
        height: 400px;
        margin: 90px 0;
        border: 1.5px inset #0e121a;
        border-left: 0;
        border-right: 0;
        overflow-y: scroll;
    }
    /* アイテム表示スペースのスクロールバー */
    #filelist::-webkit-scrollbar {
        display: auto;
        width: 12px;
    }
    #filelist::-webkit-scrollbar-track {
        background-color: #e4e4e4;
        border-radius: 50px;
    }
    
    #filelist::-webkit-scrollbar-thumb {
        background-color: #c3d825;
        border: 2px outset #a0aa52;
        border-radius: 50px;
    }
    /* 各アイテム名(名前変更時のデザイン) */
    input[type=text]{
        text-align: left;
        margin: 5px auto 5px 55px;
        height: 30px;
        outline: none;
    }
    input[type=text]:read-only{
        background: transparent;
        border: none;
        cursor: default;
    }
    input[type=text]:read-write{
        position: relative;
        z-index: 2;
        box-sizing: border-box;
        background: #fff;
        color: #0e121a;
        border: 1px solid #cfd982;
    }
    /* 名前変更処理時のオーバーレイ */
    .overlay{
		z-index:1;
		position:fixed;
		top:0;
		left:0;
		width:100%;
		height:100%;
		background-color:rgba(0,0,0,0.5);
		display: flex;
		align-items: center;
		justify-content: center;
	}
    /* 各アイテム */
    .listbutton{
        position: relative;
        display: block;
        box-sizing: border-box;
        width: 100%;
        height: 40px;
        background: transparent;
        border-bottom: 1px solid #cfd982;
    }
    .listbutton:hover{
        background: #1c305c;
    }
    /* アイコン */
    label{
        position: absolute;
		display: inline-block;
        margin: 5px;
        width: 30px;
        height: 30px;
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
    }
    .folder{
        left: 15px;
        background: #c3d825;
        mask-image: url(../../img/folder.png);
        -webkit-mask-image: url(../../img/folder.png);
    }
    .file{
        left: 15px;
        background: #cfd982;
        mask-image: url(../../img/file.png);
        -webkit-mask-image: url(../../img/file.png);
    }
    .action{
        right: 0;
        background: #c3d825;
        mask-image: url(../../img/action.png);
        -webkit-mask-image: url(../../img/action.png);
    }
</style>