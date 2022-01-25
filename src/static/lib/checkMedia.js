function getMedia(){
	if(window.matchMedia && window.matchMedia('(max-device-width: 640px)').matches){
		return "SmartPhone";
	}else if(window.matchMedia && window.matchMedia('(max-device-width: 800px)').matches){
		return "TabletPC";
	}
    return "PC"
}