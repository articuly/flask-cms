CKEDITOR.replace( 'content',{
                    filebrowserUploadUrl : upload_url,
                    filebrowserBrowseUrl: browser_url,
                    //CSRF启用后，需要按照CSRF要求传递CSRF_TOKEN
                    fileTools_requestHeaders :{
                             'X-Requested-With': 'XMLHttpRequest',
                             'X-CSRF-Token': csrf_token
                           }

                })