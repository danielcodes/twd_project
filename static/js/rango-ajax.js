//bumping up likes on a category
$('#likes').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
	//get request, passing category_id as a parameter
	//since the views returns the number of likes, that gets passed to data
	//it is then displayed back in #likes_count and then hide the button after it's been liked
    $.get('/rango/like_category/', {category_id: catid}, function(data){
	   $('#like_count').html(data);
	   $('#likes').hide();
    });
});

$('#suggestion').keyup(function(){
	//get the value from text box
	//and pass it to the view
	var query;
	query = $(this).val();
	$.get('/rango/suggest_category/', {suggestion: query}, function(data){
		$('#cats').html(data);
    });
});
