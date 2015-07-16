// JavaScript Document
//鼠标移动到工具栏图标时改变图标
$(".toolbox").mouseover(function(){
    var src = $(this).attr("src");
    var a = src.substring(0,src.length-4);
    a=a+"_over.svg";
    $(this).attr("src",a);
});
//鼠标离开图标时恢复
$(".toolbox").mouseout(function(){
    var src = $(this).attr("src");
    var a = src.substring(0,src.length-9);
    a=a+".svg";
    $(this).attr("src",a);
});

function getDownloadURL(filename){
    $.get("downloadurl/"+filename,function(data){
        window.location.href = "http://" + data;
    });
}

function changeCurrentDir(dirname){
    if(dirname == '..')
        dirname = 'parentdir';
    $("#file_list").load("changecurrentdir/"+dirname,function(){
        bind_objects();
        $("#cur_path").load("getcurrentpath/");
    });
}
//弹出上传文件框
$("#upload").click(function(){
    $("#upload_div").css("visibility","visible");
});

$("#upload").mouseover(function(){
    $(this).css("box-shadow","1px 1px 2px #888888");
    $(this).css("top","112px");
});

$("#upload").mouseout(function(){
    $(this).css("box-shadow","3px 3px 2px #888888");
    $(this).css("top","110px");
});

function select_file(file){
    $("#file_list").append("<p>"+file.name+" - "+file.size+"Byte</p>");
}
//以上为上传div处理函数
//注销账户函数
$("#logout").click(function(){
    $.get("logout/",function(data){
        alert(data);
        window.top.location.reload();
    });
});

//通过AJAX刷新文件列表
$("#refresh_button").click(function(){
    $("#file_list").load("filelist/",function(){
        bind_objects();
        $("#cur_path").load("getcurrentpath/");
    });
});
//绑定事件
function bind_objects(){
    $("[filename='..']").html("返回上一级");
    $("[filename='..']").parent().prev().text("");
    $("[filename='.']").parent().parent().remove();
    $("[href='#']").click(function(){
        //重新绑定
        if($(this).parent().next().html() == "文件")
        {
            var downloadURL = getDownloadURL($(this).html());
        }
        else
        {
            changeCurrentDir($(this).attr('filename'));
        }
    });
    //全选按钮
    $("#selectall").click(function(){
        if($(this).html() == '全选')
        {
            var t = $(":checkbox");
            for (var i = 0;i < t.length;i++){
                t[i].checked = true;
            }
            $(this).html('取消');
        }
        else{
            var t = $(":checkbox");
            for (var i = 0;i < t.length;i++){
                t[i].checked = false;
            }
            $(this).html('全选');
        }
    });
}

//删除文件或目录
$("#delete_button").click(function(){
    var t = $(":checkbox");
    var to_delete = new Array();
    for (var i = 0;i < t.length;i++){
        if(t[i].checked){
            to_delete.push(t[i].value);
        }
    }
    if(to_delete.length == 0)alert("未选择项目！");
    else
    {
        var s = String(to_delete);
        $.get("delete/" + to_delete,function(){
            $("#file_list").load("filelist/",function(){
                bind_objects();
            });
        });
    }
});
//显示添加文件夹div
$("#new_button").click(function(){
    $("#newfolder_div").css("visibility","visible");
    $("#newfolder_name").val("");
});

//添加文件夹处理函数
$("#newfolder_button").click(function(){
    var name = $("#newfolder_name").val();
    if(name == "")
        $("#name_null_notice").css("display","block");
    else{
        $.post("newdir/",{dirname:name},function(data){
            if(data == "0")alert("对不起，创建失败！");
            else{
                $("#newfolder_div").css("visibility","hidden");
                $("#refresh_button").click();
            }
        });
    }
});

//返回主目录按钮
$("#backhome").click(function(){
    $.get('backhome/',function(){
        $("#refresh_button").click();
        $("#cur_path").load("getcurrentpath/");
        bind_objects();
    });
});

//文件分享功能
$("#share_button").click(function(){
    var t = $(":checkbox");
    var to_share = new Array();
    for (var i = 0;i < t.length;i++){
        if(t[i].checked && $(t[i]).parent().next().next().html()=="文件"){
            to_share.push(t[i].value);
        }
    }
    if(to_share.length == 0)alert("请选择要分享的文件！");
    else
    {
        $("#fileshare_div").css("visibility","visible");
        for(var i = 0; i < to_share.length; i++)
            $("#filesharelist").append('<li>'+to_share[i]+'</li>');
    }
});

$("#cancelshare").click(function(){
    $("#fileshare_div").css("visibility","hidden");
    $("#filesharelist").children().remove();
});

$("#suretoshare").click(function(){
    var str = $("#filesharelist").html();
    str = str.split("</li>");
    var data = {};
    for(var i=0;i<str.length-1;i++){
        str[i]=str[i].substring(4);
        data[i.toString()] = str[i];
    }
    str.pop();
    $.post("sharefile/",data,function(data){
        if(data == "1"){
            alert("分享成功");
            $("#cancelshare").click();
        }
    });
});
