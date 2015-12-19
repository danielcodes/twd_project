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

//whenever a key is pressed, a get request is called with the query parameter
//the view returns some html which is 'data' and that is passed to the div on the page
$('#suggestion').keyup(function(){
	//get the value from text box
	//and pass it to the view
	var query;
	query = $(this).val();

	//on the view, the get request is expecting suggestion
	//data contains html, so we can just slap that onto a div with an id
	$.get('/rango/suggest_category/', {suggestion: query}, function(data){
		$('#cats').html(data);
    });
});

//add pages to a category from a search result
$('.rango-add').click(function(){
	//the button has an data-catid attribute, get it
	//get the category id, the search result title and url 
	var catid = $(this).attr("data-catid");
	var url = $(this).attr("data-url");
	var title = $(this).attr("data-title");
	//does this assign the button to 'me'?
	var me = $(this);

	//pass a get request, passing the category id, result title and url, in return we get data
	$.get('/rango/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
		//refresh the div with id pages
		//does not exist yet
		$('#pages').html(data);
		//hide the search result element that was added
		me.hide();
		});
});







