function cancelshare(obj){
	filename = $(obj).val();
	path = $(obj).attr('path');
	$.post("cancelshare/",{'filename':filename,'path':path},function(data){
		alert(data);
		location.reload();
	});
}

function download(obj){
	var filename = $(obj).parent().prev().prev().html();
	var path = $(obj).attr("path");
	$.post("downloadurl/",{"filename":filename,"path":path},function(data){
        window.location.href = "http://" + data;
    });
}