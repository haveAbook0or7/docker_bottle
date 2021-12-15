<template>
	<div class="filemanagerBase" :style="variables" @contextmenu="openMinWindow($event, 'default', pathstr, null)" @click="$refs.minwin.closeModal()">
        <manage-window ref="minwin" @reload="reload" @rename="reNameStart"></manage-window>
		<div id="nowdir" @contextmenu="openMinWindow($event, 'none', null, null)">
            <span v-for="(path, index) in pathlist" :key="index" @click="clickFolder(path)">
                {{path}} > 
            </span>
            <table border="0">
            <tr style="height: 22px;">
                <td>{{this.loginUser}}</td>
            </tr>
            <tr><td colspan="3" style="font-size: 22px;">らくがきちょう</td></tr>
            </table>
        </div>
        <div id="filelist">
            <span class="listbutton" v-for="(file, index) in filelist" :key="index" 
                :style="index == 0 ? 'border-top: 1px solid #cfd982;':''"
                @click="file.split('.').length == 1 ? clickFolder(file) : clickFile(file)" 
                @contextmenu="openMinWindow($event, file.split('.').length == 1 ? 'folder' : 'file', pathstr+'/'+file, index)">
                    <label :class="file.split('.').length == 1 ? 'folder' : 'file'"></label>
                    <input type="text" :value="file.split('.')[0]" @click="eventStop($event, isreads[index])" 
                        :readonly="isreads[index]" ref="texts" 
                        @input="reNameNow(index, $event.target.value)"
                        @blur="reNameEnd">
                    <label class="action"></label>
            </span>
        </div>
    </div>
</template>

<script>
module.exports = {
    components: {
		'manage-window': httpVueLoader('./manage-window.vue'),
    },
    mounted() {
        axios.get("/mngfiles/getnowdir")
		.then(response => {
			console.log(response.data);
            this.loginUser = response.data.data.user;
            this.pathlist = response.data.data.path;
            this.pathstr = "";
            for(var i = 1; i < this.pathlist.length; i++){
                this.pathstr += "/"+this.pathlist[i];
            }
            console.log(this.pathstr)
            this.filelist = response.data.data.dirlist;
            this.isreads = [];
            for(var i = 0; i < this.filelist.length; i++){
                this.isreads.push(true);
            }
		})
		.catch(function (error) {
			console.log(error);
		});
    },
	computed: {
		variables() {
			return {
				"--scrollbar": this.filelist.length <= 10 ? "none" : "auto",
			}
		},
	},
	data: function () {
		return {
            loginUser: "guest",
            pathlist: [],
            pathstr: "",
			filelist: [],
            isreads: [],
            renameFile: null,
            renameIndex: null,
		}
	},
	methods: {
		clickFolder(folder){
            let nowdir = "";
            if(this.loginUser != folder){
                for(var i = 1; i < this.pathlist.length; i++){
                    if(this.pathlist[i] == folder){
                        break;
                    }
                    nowdir += "/"+this.pathlist[i];
                }
                nowdir += "/"+folder
            }
            axios.post("/mngfiles/getnowdir",{
                nowdir: nowdir
            })
            .then(response => {
                console.log(response.data);
                this.loginUser = response.data.data.user;
                this.pathlist = response.data.data.path;
                this.pathstr = "";
                for(var i = 1; i < this.pathlist.length; i++){
                    this.pathstr += "/"+this.pathlist[i];
                }
                console.log(this.pathstr)
                this.filelist = response.data.data.dirlist;
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        clickFile(file){
            axios.post("/mngfiles/openfile",{
                openfile: this.pathstr + "/"+file
            })
            .then(response => {
                console.log(response.data);
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
            if(!flg){
                e.stopPropagation();
            }
        },
        openMinWindow(e, mode, item, index){
            e.stopPropagation();
            e.preventDefault();
            console.log(mode);
            console.log(index);
            // console.log(e);
            this.$refs.minwin.openModal(mode, e.pageX, e.pageY, item, index);
        },
        reNameStart(index){
            this.$set(this.isreads, index, false);
            this.$refs.texts[index].focus();
        },
        reNameNow(index, value){
            console.log(index)
            console.log(e);
            this.renameIndex = index;
            this.renameFile = value;
        },
        reNameEnd(){

        },
        reload(path){
            axios.post("/mngfiles/getnowdir",{
                nowdir: path
            })
            .then(response => {
                console.log(response.data);
                this.loginUser = response.data.data.user;
                this.pathlist = response.data.data.path;
                this.pathstr = "";
                for(var i = 1; i < this.pathlist.length; i++){
                    this.pathstr += "/"+this.pathlist[i];
                }
                console.log(this.pathstr)
                this.filelist = response.data.data.dirlist;
            })
            .catch(function (error) {
                console.log(error);
            });
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
    #nowdir{
        position: relative;
        height: 50px;
        background: #d4d9ad;
        font-size: 18px;
    }
    span{
        cursor: default;
        font-size: 18px;
        color: #000;
    }
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
    #filelist{
        box-sizing: border-box;
        height: 400px;
        margin: 90px 0;
        border: 1.5px inset #0e121a;
        border-left: 0;
        border-right: 0;
        overflow-y: scroll;
        -ms-overflow-style: var(--scrollbar);/* IE, Edge 対応 */
        scrollbar-width: var(--scrollbar); /* Firefox 対応 */
    }
    #filelist::-webkit-scrollbar {
        display: var(--scrollbar);
    }
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
        box-sizing: border-box;
        background: #fff;
        color: #0e121a;
        border: 1px solid #cfd982;
    }
    /* input[type=button]{
        box-sizing: border-box;
        width: 100%;
        height: 40px;
        text-align: left;
        padding-left: 55px;
        background: transparent;
        border-bottom: 1px solid #cfd982;
    }
    input[type=button]:active{
        background: #1c305c;
    } */
    .listbutton{
        position: relative;
        display: block;
        box-sizing: border-box;
        width: 100%;
        height: 40px;
        background: transparent;
        border-bottom: 1px solid #cfd982;
    }
    .listbutton:active{
        background: #1c305c;
    }
    label{
        position: absolute;
		display: inline-block;
        margin: 5px;
        width: 30px;
        height: 30px;
        mask: no-repeat center/100%;
        -webkit-mask: no-repeat center/100%;
        background: #c3d825;
    }
    .folder{
        left: 15px;
        mask-image: url(../../img/folder.png);
        -webkit-mask-image: url(../../img/folder.png);
    }
    .file{
        left: 15px;
        mask-image: url(../../img/file.png);
        -webkit-mask-image: url(../../img/file.png);
    }
    .action{
        right: 0;
        mask-image: url(../../img/action.png);
        -webkit-mask-image: url(../../img/action.png);
    }
    .manage-window{
        position: absolute;
        z-index: 7;
    }
</style>