<template>
	<div class="select-path" :style="variable">
        <div class="path">
            <input class="select" type="text" readonly :value="value" @click="openOption">
            <span class="toggle" @click="openOption"></span>
        </div>
        <div class="back">
            <tree-path class="item" v-show="isOpen" :item="treeData" @select="selectItem"></tree-path>
        </div>
    </div>
</template>

<script>
module.exports = {
    components: {
		'tree-path': httpVueLoader('./tree-path.vue'),
    },
    model: {
		prop: 'value',
		event: 'change'
	},
	props: {
        value: {default: null},
		options: {default:()=>{
            return {
                name: 'home', children: [
                    {name: 'folder1', children: [
                        {name: 'folder2'},
                        {name: 'folder3'}
                    ]},
                    {name: 'folder4'},
                    {name: 'folder5', children: [
                        {name: 'folder6'}
                    ]}
                ]
            };
        }},
		disabled: {default: false},
	},
	computed: {
		variable() {
			return {
				"--dynamic-color": this.isOpen ? "#0f2350" : "#cfd982",
                "--top": this.isOpen ? "0px" : "8px",
                "--bottom": this.isOpen ? "8px" : "0px",
                "--open": this.isOpen ? "auto" : "0px"
			}
		},
        treeData: {
            get(){
                return this.options;
            }
        },
	},
	data: function () {
		return {
			selected: "",
			isDisabled: this.disabled,
            isOpen: false,
		}
	},
	methods:{
		chengeDisabled(value){
			this.isDisabled = value;
		},
        openOption(){
            if(!this.isDisabled){
                this.isOpen = !this.isOpen;
            }
        },
        selectItem(path){
            this.$emit('change', path);
        },
	}
}
// export default { Node.jsじゃないから、これだとダメだった。 }
</script>

<style scoped>
    *{
		margin: 0;
		padding: 0;
		border: 0;
		font-size: 14px;
        font-size: var(--pathFS);
        position: relative;
        display: block;
        text-align: left;
	}
    .back{
        display: inline-block;
        background: rgba(255, 255, 255, 0.5);
        height: var(--open);
        max-height: 280px;
        width: 207px;
        width: 100%;
        overflow:scroll;
    }
    .back::-webkit-scrollbar{
        display: auto;
        width: 7px;
        height: 7px;
        width: calc(7px * var(--toggleS));
        height: calc(7px * var(--toggleS));
    }
    .back::-webkit-scrollbar-track {
        background-color: #e4e4e4;
        border-radius: 50px;
        width: 5px;
        width: calc(5px * var(--toggleS));
    }
    .back::-webkit-scrollbar-thumb {
        background-color: #c3d825;
        border: 2px outset #a0aa52;
        border-radius: 50px;
        width: 5px;
        width: calc(5px * var(--toggleS));
    }
    .path{
        width: 200px;
        width: 100%;
        border-bottom: 2px solid var(--dynamic-color);
    }
    .select{
        width: 185px;
        width: 100%;
        height: 30px;
        padding-right: 1em;
        background: #fff;
        color: darkslategrey;
        border: none;
        outline: none;
        direction: rtl;
        overflow:scroll;
        text-overflow: ellipsis;
    }
    .select::-webkit-scrollbar{
        display: none;
    }
    .toggle{
        position: absolute;
        top: calc(12px / var(--toggleS));
        right: 3px;
        border-top: var(--top) solid var(--dynamic-color);
        border-bottom: var(--bottom) solid var(--dynamic-color);
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: calc(var(--top) * var(--toggleS)) solid var(--dynamic-color);
        border-bottom: calc(var(--bottom) * var(--toggleS)) solid var(--dynamic-color);
        border-left: calc(5px * var(--toggleS)) solid transparent;
        border-right: calc(5px * var(--toggleS)) solid transparent;
        width: 0;
        height: 0;
    }
</style>