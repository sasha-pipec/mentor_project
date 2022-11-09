function default_text(){
    $("#input-comment").attr('placeholder','Оставьте комментарий');
}

function click_text(){
    $("#input-comment").attr('placeholder','Что пишешь?');
}

function open_answer_textarea(id){
    $(".answer-for-comment").css({'display':'none'});
    $("#answer-for-comment-"+id).css({'display':'block'});
}

function close_answer_comment(){
    $(".answer-comment-textarea").val('');
    $(".answer-for-comment").css({'display':'none'});
}

function open_all_answer_for_comment(idd){
    $(".other-answer-to-comments-"+idd).css({'display':'inline-flex'});
    $("#open-all-answer-for-comment-"+idd).css({'display':'none'});
}

function close_all_answer_for_comment(idd){
    $(".other-answer-to-comments-"+idd).css({'display':'none'});
    $("#open-all-answer-for-comment-"+idd).css({'display':'block'});
}

function edit_a_comment(id,content){
    $(".edit-comment").css({'display':'none'});
    $("#edit-comment-"+id).css({'display':'block'});
    $("#edit-comment-"+id+"-textarea").val(''+content);
    $("#comment-content-detail-info-"+id).css({'display':'none'});
    $("#comment-content-detail-info-date-"+id).css({'display':'none'});
}

function close_edit_comment(id,content){
    $(".answer-comment-textarea").val('');
    $(".edit-comment").css({'display':'none'});
    $("#comment-content-detail-info-"+id).css({'display':'block'});
    $("#comment-content-detail-info-date-"+id).css({'display':'block'});
}

function edit_a_photo(id,content,name,photo){
    $(".row-personal-photo").css({'display':'none'});
    $(".row-add-photo-form").css({'display':'block'});
    $(".pagination").css({'display':'none'});
    $("#col-add-photo-form-"+id).css({'display':'flex'});
    $("#old-photo-"+id).attr('src',photo);
    $("#id_photo_"+id).val('');
    $("#id_photo_name_"+id).val(''+name);
    $("#id_photo_content_"+id).val(''+content);
}

function close_edit_a_photo(){
    $(".pagination").css({'display':'flex'});
    $(".row-add-photo-form").css({'display':'none'});
    $(".col-add-photo-form").css({'display':'none'});
    $(".row-personal-photo").css({'display':'flex'});
}