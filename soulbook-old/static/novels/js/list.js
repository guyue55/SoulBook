/**
 * Created by howie on 21/02/2017.
 */
$(document).ready(function () {
    var content_url = $("#content_url").val();
    var chapter_url = $("#url").val();
    var novels_name = $("#novels_name").val();
    $(".container a").each(function () {
        var url = $(this).attr('href');
        if (typeof(url) != "undefined") {
            if (url.indexOf("soulbook") < 0) {
                content_url = "";
                var name = $(this).text();
                // if(url.substr(0, 4) == "http"){
                //         content_url = "";
                // }
                // // 当content_url为1，表示该链接不用拼接
                // else if (content_url == '1') {
                //     content_url = ''
                // } else if (content_url == '0') {
                //     content_url = ""
                //     // content_url=0表示章节网页需要当前url拼接
                //     // content_url = chapter_url;
                //     // 以“/”进行分割
                //     // var list = chapter_url.split('/');
                //     // // 协议, http 或 https
                //     // var http_type = list[0];
                //     // // 域名
                //     // var domain = list[2];
                //     // // var urlReg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+.?/;
                //     // // var domain=urlReg.exec(chapter_url);
                //     //
                //     // content_url = "https://" + domain;
                //     //
                //     // if(url.substr(0, 4) == "http"){
                //     //     content_url = "";
                //     // }
                //     // else if(url.substr(0, 1) != "/"){
                //     //     content_url = chapter_url;
                //     // }
                //     // else if(url.substr(0, 2) == "//"){
                //     //     content_url = http_type;
                //     // }else{
                //     //     content_url = http_type + "//" + domain;
                //     // }
                // } else if (content_url == '-1') {
                //     // content_url=-1 表示特殊情况
                //     content_url = chapter_url;
                // }
                show_url = "owllook_content?url=" + content_url + url + "&name=" + name + "&chapter_url=" + chapter_url + "&novels_name=" + novels_name;
                $(this).attr('href', show_url);
                // $(this).attr('target', '_blank');
            }
        }
    });
});