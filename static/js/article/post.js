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
                             $("#message").html(data.message)
                             //表单重置，相当于点击重设按钮
                             $("#title").val("")
                             $("#intro").val()
                             // 清空隐藏域
                             $("#thumb").val("")
                             // 清空上传
                             myDropzone.dropzone.removeAllFiles()
                             // 清空ckeditor
                             CKEDITOR.instances["content"].setData()
                         }
                    })

                }