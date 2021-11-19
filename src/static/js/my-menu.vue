<template>
	<div id="menubase" :style="variable">
		<table border="0">
		<tr>
			<td>
                {{login_user}}
                <span id="menu"><span id="mtoggle"></span></span>
            </td>
			<td><input type="button" value="サインアップ"></td>
		</tr>
		<tr><td colspan="2">らくがきちょう</td></tr>
		</table>
	</div>
</template>

<script>
module.exports = {
    components: {
		'save-window': httpVueLoader('./save-window.vue'),
        'my-palette': httpVueLoader('./my-palette.vue'),
		'my-control': httpVueLoader('./my-control.vue'),
    },
    props: {
		login_user: {default:null},
	},
    computed: {
		variable() {
			return {
				"--dynamic-color": this.isOpen ? "#da3c41" : "#1b2538",
                "--top": this.isOpen ? "0px" : "15px",
                "--bottom": this.isOpen ? "15px" : "0px",
			}
		},
	},
	data: function () {
		return {
            isOpen: false,
		}
	},
	methods: {
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
        display: inline-block;
    }
    table{
        height: 50px;
        text-align: right;
    }
    td{
        min-width: 100px;
    }
    #menu{
        display: inline-block;
        position: relative;
        width: 20px;
        height: 13px;
    }
    #mtoggle{
        position: absolute;
        top: 2px;
        left: 2px;
        border-top: var(--top) solid #da3c41;
        border-bottom: var(--bottom) solid #da3c41;
        border-left: 8px solid transparent;
        border-right: 8px solid transparent;
        width: 0;
        height: 0;
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