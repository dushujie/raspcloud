$("#submit").click(function(){
	var text = $("#inputtext").val();
	$.post("chatinput/",{"text":text},function(data){
		location.reload();
	});
});