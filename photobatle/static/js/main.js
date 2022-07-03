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