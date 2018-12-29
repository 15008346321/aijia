function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get('/house/area_facility/', function(data){
        if(data.code == '200'){
            for(var i=0; i<data.areas.length; i++){
                area_str = '<option value="' + data.areas[i].id + '">' + data.areas[i].name + '</option>'
                $('#area-id').append(area_str)
            }

            for(var j=0; j<data.facilitys.length; j++){
                facility_str = '<li><div class="checkbox"><label>'
                facility_str += '<input type="checkbox" name="facility" value="' + data.facilitys[j].id + '">' + data.facilitys[j].name
                facility_str += '</label></div></li>'

                $('.house-facility-list').append(facility_str)
            }

        }
    });

    $('#form-house-info').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/newhouse/',
            type:'POST',
            dataType:'json',
            success:function(data){
                if(data.code == '200'){
                    $('#form-house-image').show()
                    $('#form-house-info').hide()
                    alert(data.house_id)
                    $('#house-id').val(data.house_id)
                }
            },
            error:function(data){
                alert('失败')
            }
        });
    });

    $('#form-house-image').submit(function(e){
        e.preventDefault()
        $(this).ajaxSubmit({
            url:'/house/house_images/',
            dataType:'json',
            type:'POST',
            success:function(data){
                if(data.code == '200'){
                    var img_src = '<img src="/static/media/' + data.image_url + '">'
                    $('.house-image-cons').append(img_src)
                }
            },
            error:function(data){
                alert('请求失败')
            }
        })
    });
});