<template>
	<div id="menubase" :style="variable">
		<table border="0">
		<tr class="menus">
			<td class="menu" @click="openMenu">{{login_user}}</td>
            <td class="menu"><span id="mtoggle" @click="openMenu"></span></td>
			<td class="signup"><a id="tosignup" href="../../../signup-pre.html">サインアップ</a></td>
		</tr>
		<tr><td colspan="3" class="name">らくがきちょう</td></tr>
		</table>
        <menu-list :media="media" :login_user="login_user" v-show="isOpen"></menu-list>
	</div>
</template>

<script>
module.exports = {
    components: {
		'menu-list': httpVueLoader('../component/menu-list.vue'),
    },
    props: {
        media: {default:"PC"},
		login_user: {default:null},
	},
    computed: {
		variable() {
            let styles = {
                "--top": this.isOpen ? "0px" : "12px",
                "--bottom": this.isOpen ? "12px" : "0px",
            };
            switch(this.media){
				case "PC":
					Object.assign(styles, {
                        "--FS": "13px",
						"--nameDis": "table-cell",
						"--signupW": "100px",
						"--signupH": "20px",
                        "--minW": "21px",
						"--menuP": "relative",
                        "--menuT": "0",
                        "--menuR": "0",
                        "--toggleT": "3.5px",
                        "--toggleR": "3.5px",
                        "--toggleS": "1",
					});
                    break;
				case "TabletPC":
					Object.assign(styles, {
                        "--FS": "24px",
						"--nameDis": "none",
						"--signupW": "160px",
						"--signupH": "35px",
                        "--minW": "21px",
						"--menuP": "absolute",
                        "--menuT": "42px",
                        "--menuR": "20px",
                        "--toggleT": "8px",
                        "--toggleR": "-18px",
                        "--toggleS": "1",
					});
                    break;
				case "SmartPhone":
					Object.assign(styles, {
                        "--FS": "38px",
						"--nameDis": "none",
						"--signupW": "230px",
						"--signupH": "70px",
                        "--minW": "48px",
						"--menuP": "relative",
                        "--menuT": "0",
                        "--menuR": "0",
                        "--toggleT": "15px",
                        "--toggleR": "7.5px",
                        "--toggleS": "2",
					});
                    break;
			}
			return styles;
		},
	},
	data: function () {
		return {
            isOpen: false,
		}
	},
	methods: {
        openMenu(){
            this.isOpen = !this.isOpen;
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
        z-index: 3;
	}
    #menubase{
        position: relative;
        display: inline-block;
    }
    table{
        height: 50px;
        text-align: right;
        border-collapse: collapse;
        border-spacing: 0;
    }
    td{
        position: relative;
        min-width: var(--minW);
    }
    #mtoggle{
        position: absolute;
        top: var(--toggleT);
        right: var(--toggleR);
        width: 0;
        height: 0;
        border-top: calc(var(--top) * var(--toggleS)) solid #1c305c;
        border-bottom: calc(var(--bottom) * var(--toggleS)) solid #1c305c;
        border-left: calc(7px * var(--toggleS)) solid transparent;
        border-right: calc(7px * var(--toggleS)) solid transparent;
	}
    a{
        width: var(--signupW);
        height: var(--signupH);
        line-height: calc(var(--FS) + 7px);
        display: inline-block;
        color: #fff;
        text-decoration: none;
        text-align: center;
        background: #1c305c;
        box-sizing: border-box;
        cursor: default;
        display: table-cell;
        vertical-align:middle;
    }
    a:active{
		border: 2px inset #4c505a;
	}
    .menus{
        height: 22px;
        position: relative;
    }
    .menu{
        cursor: default;
        position: var(--menuP);
        top: var(--menuT);
        right: var(--menuR);
    }
    .name{
        font-size: 22px;
        display: var(--nameDis);
    }
</style>