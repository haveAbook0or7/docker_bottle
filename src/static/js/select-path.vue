<template>
	<div :style="variable">
        <input class="select" type="button" :value="selected" @click="openOption">
        <span class="toggle" @click="openOption"></span>
        <tree-path class="item" v-show="isOpen" :item="treeData" @select="selectItem"></tree-path>
    </div>
</template>

<script>
module.exports = {
    components: {
		'tree-path': httpVueLoader('./tree-path.vue'),
    },
	props: {
		init_select: {default:null},
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
    mounted() {
        this.selectItem(this.init_select == null ? this.options.name+"/" : this.init_select);
	},
	computed: {
		variable() {
			return {
				"--dynamic-color": this.isOpen ? "#da3c41" : "#1b2538",
                "--top": this.isOpen ? "0px" : "8px",
                "--bottom": this.isOpen ? "8px" : "0px",
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
            this.selected = path;
            this.$emit('select', this.selected);
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
		font-size: 13px;
        position: relative;
        display: block;
        width: 200px;
        text-align: left;
	}
    .select{
        width: 200px;
        height: 20px;
        background: #fff;
        color: darkslategrey;
        border-bottom:  2px solid var(--dynamic-color);
    }
    .toggle{
        position: absolute;
        top: 5px;
        right: 3px;
        border-top: var(--top) solid var(--dynamic-color);
        border-bottom: var(--bottom) solid var(--dynamic-color);
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        width: 0;
        height: 0;
    }
</style>