<template>
    <span :style="variable">
        <span class="li">
            <input type="button" :value="item.name" @click="spreadItem('')">
            <span class="toggle" v-if="isFolder" @click="toggle"></span>
        </span>
        <div v-show="isOpen" v-if="isFolder">
            <tree-path class="item" 
                v-for="(child, index) in item.children"
                :key="index"
                :item="child"
                @select="spreadItem">
            </tree-path>
        </div>
    </span>
</template>

<script>
module.exports = {
    components: {
		'tree-path': httpVueLoader('./tree-path.vue'),
    },
	props: {
        item: Object
	},
	computed: {
		variable() {
			return {
				"--dynamic-color": this.underColor,
                "--top": this.isOpen ? "0px" : "8px",
                "--bottom": this.isOpen ? "8px" : "0px",
			}
		},
        isFolder() {
            return this.item.children && this.item.children.length;
        }
	},
	data: function () {
		return {
            isOpen: false,
		}
	},
	methods:{
        toggle() {
            if (this.isFolder) {
                this.isOpen = !this.isOpen;
            }
        },
        spreadItem(folder){
            this.$emit('select', this.item.name+"/"+folder);
        }
	}
}
// export default { Node.jsじゃないから、これだとダメだった。 }
</script>

<style scoped>
    * {
        text-align: left;
        color: #444;
        margin: 0;
		padding: 0;
		border: 0;
		font-size: 13px;
        cursor: pointer;
    }
    div{
        padding-left: 15px;
    }
    input[type=button]{
        padding: 3px;
        height: 20px;
        width: 200px;
        background: #fff;
        color: darkslategrey;
    }
    input[type=button]:hover{
        background: #ccc;
    }
    
    .toggle{
        top: 5px;
        right: 3px;
        border-top: var(--top) solid #aaa;
        border-bottom: var(--bottom) solid #aaa;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        width: 0;
        height: 0;
    }
    .li{
        display: inline-flex;
        background: #fff;
        border-bottom:  1px solid #ccc;
    }
</style>