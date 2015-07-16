$("#add-download").click(function(){
    var url = $("#url-input").val();
   aria_rpc('[["' + url + '"],{"dir":"' + $("#select-btn").text().replace(/\s/g,"") + '"}]',
    "aria2.addUri",
    "1");
   $("#url-input").val("");
   refresh();
});
//RPC AJAX函数
function aria_rpc(params,method,id,func){
    $.ajax({
        url:"http://192.168.1.10:6800/jsonrpc",
        type:"POST",
        data:'{"id":"'+id+'","jsonrpc":"2.0","params":'+params+',"method":"'+method+'"}',
        contentType:"application/text",
        processData:false,
        async:false,
        error:function(){
                alert(":-(出错了!");
            },
        success:function(data){
                func(data);
            }
        });
}
//选择路径按钮
function select_path(obj){
    var dir=$(obj).html();
    $.post("dirindir/",{"dir":dir},function(data){
        var list = data.split("\n");
        $("#select-path ul li").remove();
        for(var i = 0;i < list.length;i++){
            $("#select-path ul").append("<li><a onclick='select_path(this);'>" + list[i] + "</a></li>");
        }
        $.get("/main/getcurrentpath/",function(data){
            $("#select-btn").html(data.substring(5) + '<span class="caret"></span>');
        });
    });
}

var download_list = new Array();
setInterval(refresh,2000);

$(refresh());
//刷新下载列表
function refresh(){
    $("#download-table tbody tr:gt(0)").remove();

    download_list.length = 0;
    aria_rpc('[]','aria2.tellActive','1',add_to_list);
    aria_rpc('[0,20]','aria2.tellWaiting','1',add_to_list);
    aria_rpc('[0,20]','aria2.tellStopped','1',add_to_list);

    for(var i = 0;i < download_list.length;i++){
        var status = '下载中';
        var control = '暂停';
        switch(download_list[i].status){
            case 'waiting':
                status = '等待';
                break;
            case 'paused':
                status = '暂停';
                control = '开始';
                break;
            case 'error':
                status = '错误';
                control = '';
                break;
            case 'complete':
                status = '完成';
                control = '';
                break;
            case 'removed':
                status = '已移除';
                control = '';
                break;
        }
        $("#download-table tbody").append('<tr><td>'+status+'</td><td>'+
            download_list[i].filename+'</td><td>'+
            (download_list[i].completedLength/download_list[i].totalLength*100).toString().split('.')[0]+'%</td><td>'+
            (download_list[i].totalLength/(1024*1024)).toString().substring(0,4)+'MB</td><td>'+
            (download_list[i].downloadSpeed/1024).toString().substring(0,4)+'KB/s</td><td>'+
            download_list[i].dir+'</td><td>'+
            '<a onclick="pause_item(this)" gid="'+
            download_list[i].gid+'">'+control+'</a>'+'</td></tr>');
        if(status == '下载中'){
            $("#download-table tbody tr:last td:last").append('<a onclick="pause_item(this)" gid="'+
            download_list[i].gid+'">删除</a>');
        }
    }
}

function add_to_list(data){
    for(var i = 0;i < data.result.length;i++){
        var s = data.result[i].files[0].path.split('/');
        s = s[s.length - 1];
        var t = new dowload_item(
                data.result[i].gid,
                data.result[i].status,
                data.result[i].totalLength,
                data.result[i].completedLength,
                data.result[i].downloadSpeed,
                data.result[i].uploadSpeed,
                data.result[i].dir,
                s
            );
        download_list.push(t);
    }

    //$("#main-area").css("height",(parseInt($("#download-table").css("height").substring(0,$("#download-table").css("height").length-2)) + 291).toString()+'px');
}

function dowload_item(gid,status,totalLength,completedLength,downloadSpeed,uploadSpeed,dir,filename)
{
    this.gid=gid;
    this.status=status;
    this.totalLength=totalLength;
    this.completedLength=completedLength;
    this.downloadSpeed=downloadSpeed;
    this.uploadSpeed=uploadSpeed;
    this.dir=dir;
    this.filename=filename;
}
//删除已完成
function remove_completed_download(obj){
    aria_rpc('[]','aria2.purgeDownloadResult','1',null_func);
    refresh();
}
//空函数
function null_func(data){}
//暂停任务
function pause_item(obj){
    if($(obj).text()=="暂停"){
        var gid = $(obj).attr("gid")
        aria_rpc('["'+gid+'"]','aria2.pause','1',null_func);
        $(obj).text("开始");
        refresh();
    }else if($(obj).text()=="开始"){
        var gid = $(obj).attr("gid")
        aria_rpc('["'+gid+'"]','aria2.unpause','1',null_func);
        $(obj).text("暂停");
        refresh();
    }else if($(obj).text()=="删除"){
        var gid = $(obj).attr("gid")
        aria_rpc('["'+gid+'"]','aria2.remove','1',null_func);
        refresh();
        $.post("delofflinefile/",{"path":$(obj).parent().prev().text(),
            "filename":$(obj).parent().prev().prev().prev().prev().prev().text()},
            function(data){});
    }
}

function pause_all(){
     aria_rpc('[""]','aria2.pauseAll','1',null_func);
     refresh();
}

function unpause_all(){
     aria_rpc('[""]','aria2.unpauseAll','1',null_func);
     refresh();
}