 btn = document.getElementById("btn1")
                btn.onclick = function (ev) {
                    cate_id = $("#cate").val()
                    title = $("#title").val()
                    thumb = $("#thumb").val()
                    intro = $("#intro").val()
                    content = CKEDITOR.instances["content"].getData()

                    if (title == ""){
                        $("#title").focus()
                        return false
                    }
                    if (intro == ""){
                        $("#intro").focus()
                        return false
                    }

                    $.ajax({
                         type:"post",
                         data:{"cate":cate_id,
                               "title":title,
                               "thumb":thumb,
                               "intro":intro,
                               "content":content
                               },
                         dataType:"json",
                         beforeSend:function(xhr){
                            xhr.setRequestHeader("X-CSRFToken", csrf_token)
                         },
                         success: function(data){
                             console.log(data)

                             //表单重置，相当于点击重设按钮

                             if (data.res=="success"){
                                 $("#message").html(data.res+"<a href='javascript:window.close()'>关闭</a>")
                             } else {
                                 $("#message").html(data.res)
                             }
                         }
                    })

                }