$(document).ready(function(){
	$("#follow-form").submit(function(event){
		event.preventDefault();
		dataString = $("#follow-form").serialize();
		$.ajax({
			type: 'POST',
			url: "/accounts/followtoggle/",
			data: dataString,
			success: function(result){
				if(result["success"])
				{
					if(result["following_flag"])
					{
						$("#follow-toggle").removeClass("btn-primary")
						$("#follow-toggle").addClass("btn-secondary")
						$("#follow-toggle").text("Following")
					}
					else
					{
						$("#follow-toggle").removeClass("btn-secondary")
						$("#follow-toggle").addClass("btn-primary")
						$("#follow-toggle").text("Follow")
					}
				}
			}
		});
	});
});