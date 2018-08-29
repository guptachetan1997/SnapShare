$(document).ready(function(){
	$("#like-form").submit(function(event){
		event.preventDefault();
		dataString = $("#like-form").serialize();
		$.ajax({
			type: 'POST',
			url: "/posts/single/like/",
			data: dataString,
			success: function(result){
				if(result["success"])
				{
					if(result["like_flag"])
					{
						$("#like-toggle").removeClass("btn-primary")
						$("#like-toggle").addClass("btn-secondary")
						$("#like-toggle").text("Liked")
					}
					else
					{
						$("#like-toggle").removeClass("btn-secondary")
						$("#like-toggle").addClass("btn-primary")
						$("#like-toggle").text("Like")
					}
				}
			}
		});
	});
});