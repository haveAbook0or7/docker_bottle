<template>
	<div id="menubase" :style="variable">
		<table border="0">
		<tr style="height: 22px;">
			<td style="cursor: default;" @click="openMenu">{{login_user}}</td>
            <td><span id="mtoggle" @click="openMenu"></span></td>
			<td><input type="button" value="サインアップ"></td>
		</tr>
		<tr><td colspan="3" style="font-size: 22px;">らくがきちょう</td></tr>
		</table>
        <menu-list :login_user="login_user" v-show="isOpen"></menu-list>
	</div>
</template>

<script>
module.exports = {
    components: {
		'menu-list': httpVueLoader('./menu-list.vue'),
    },
    props: {
		login_user: {default:null},
	},
    computed: {
		variable() {
			return {
				"--dynamic-color": this.isOpen ? "#da3c41" : "#1b2538",
                "--top": this.isOpen ? "0px" : "12px",
                "--bottom": this.isOpen ? "12px" : "0px",
			}
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
		font-size: 13px;
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
        min-width: 21px;
    }
    #mtoggle{
        position: absolute;
        top: 3.5px;
        right: 3.5px;
        width: 0;
        height: 0;
        border-top: var(--top) solid #da3c41;
        border-bottom: var(--bottom) solid #da3c41;
        border-left: 7px solid transparent;
        border-right: 7px solid transparent;
	}
    input[type=button]{
		width: 100px;
		height: 20px;
		color: #fff;
		background: #da3c41;
        box-sizing: border-box;
    }
    input[type=button]:active{
		box-sizing: border-box;
		border: 2px inset #c0353a;
	}
</style>