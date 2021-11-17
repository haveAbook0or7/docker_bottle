<template>
	<div :style="elementColor">
        <input class="select" type="button" :value="selected"><span id="sankaku" @click="clickSelect"></span>
        <!-- <span id="ul"> -->
            <tree-path class="item" :item="treeData"></tree-path>
        <!-- </span> -->
    </div>
</template>

<script>
module.exports = {
    components: {
		'tree-path': httpVueLoader('./tree-path.vue'),
    },
	props: {
        item: Object,
		initial: {default:()=>[]},
		// options: {default: ()=>[{key: "ホーム", value: null},]},
		// disabled: {default: false},
	},
	computed: {
		elementColor() {
			return {
				"--dynamic-color": this.underColor
			}
		},
        treeData: {
            get(){
                return {
                    name: 'My Tree',
                    children: [
                        {name: 'hello'},
                        {name: 'wat'},
                        {
                            name: 'child folder',
                            children: [
                                {
                                    name: 'child folder',
                                    children: [
                                        {name: 'hello'},
                                        {name: 'wat'}
                                    ]
                                },
                                {name: 'hello'},
                                {name: 'wat'},
                                {
                                    name: 'child folder',
                                    children: [
                                        {name: 'hello'},
                                        {name: 'wat'}
                                    ]
                                }
                            ]
                        }
                    ]
                };
            }
        },
        // option: {
        //     get(){
        //         return [
        //             {key: "ホーム1", value: null},
        //             {key: "ホーム2", value: [
        //                 {key: "ホーム2-1", value: null},
        //                 {key: "ホーム2-2", value: null},
        //             ]},
        //             {key: "ホーム3", value: null},
        //         ];
        //     }
        // }
	},
	data: function () {
		return {
			selected: this.initial,
			// isDisabled: this.disabled,

			// underColor: "#705b67",
            isOpen: false,
            
		}
	},
	methods:{
	// 	chengeDisabled(value){
	// 		this.isDisabled = value;
	// 	},
	// 	updateValue(value){
	// 		this.$emit('up-value', value.target.id, value.target.value);
	// 	},
	// 	chengeValue(value){
	// 		this.selected = value;
	// 	},
	// 	chengeUnderC(value){
	// 		this.underColor = value;
	// 	},
        clickSelect(){
            console.log("www");
        }
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
	}
    .select{
        width: 200px;
        height: 20px;
        background: #fff;
        color: darkslategrey;
        border-bottom:  2px solid var(--dynamic-color);
    }
    #sankaku{
        position: absolute;
        top: 5px;
        right: 3px;
        border-top: 8px solid slategray;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        width: 0;
    }
</style>