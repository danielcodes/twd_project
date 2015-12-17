$(document).ready(function() {

	// JQuery code to be added in here.

	//add bootstrap classes
	$("#about-btn").addClass('btn btn-primary')

	//on click button event
	$("#about-btn").click( function(event) {
		msgstr = $("#msg").html()
		msgstr = msgstr + "o"
		$("#msg").html(msgstr)
	});

	//hover event
   /* $("p").hover( */
		////hover does mouse in and mouse out events
		//function() {
		//$(this).css('color', 'red');
		//},
		//function() {
			//$(this).css('color', 'blue');
		//});	

});

