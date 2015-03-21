$(function () {
    $(window).resize(function () {
        // These should refer to left panel and right panel
        var $sidePanel = $('.side-panel');
        var $centralPanel = $('.central-panel');
        // FIX THIS
        if (Math.max($sidePanel.height(), $centralPanel.height()) < $(window).height()) {
            $($sidePanel).height($(window).height() - $($sidePanel).offset().top);
            $($centralPanel).height($(window).height() - $($centralPanel).offset().top);
        }
    });
    $(window).resize();
});

// Function responsible for posting the required data to the view which sends invitations
$("#invite-user").on("click", function (e) {
    e.preventDefault();
    var username = $(this).prev().val();
    var $parentDiv = $(this);
    if (username == "") {
        $parentDiv.popover({"content": "Please enter a username", "placement": "left"});
        $parentDiv.popover("show");
        $parentDiv.popover().on('hidden.bs.popover', function () {
            $parentDiv.popover("destroy");
        });
    }
    var projectId = $(this).attr("data-projectid");
    $.get("/send_invitation/", {"project_id": projectId, "username": username}, function(data) {
        // Bootstrap call display error/succcess message to the user
        $parentDiv.popover({"content": data, "placement": "left"});
        $parentDiv.popover("show");
        $parentDiv.popover().on('hidden.bs.popover', function () {
            $parentDiv.popover("destroy");
        });
    });

});

$("#remove_admin").on("click", function(e){
	var user_id = $(this).attr("data-userid");
	var project_id = $(this).attr("data-projectid")
	$.get("/remove_admin/",{"user_id": user_id, "project_id": project_id});
});


