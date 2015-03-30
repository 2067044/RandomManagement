$(document).ready(function () {
    recalculateHeight();
});

$(window).on("resize", function () {
    recalculateHeight();
});




function recalculateHeight() {
    var viewPortH = $(window).height();
    var $sidePanel = $(".side-panel");
    var $centralPanel = $(".central-panel");
    var $body = $("body");

    var bodyPaddingTop = $body.css("padding-top").replace("px", "");

    if ($body.height() > viewPortH) {
        $sidePanel.css("height", "" + $body.height() + "px");
        $centralPanel.css("height", "" + $body.height() + "px");
    } else {
        $sidePanel.css("height", "" + viewPortH - bodyPaddingTop + "px");
        $centralPanel.css("height", "" + viewPortH - bodyPaddingTop + "px");
    }


}

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
    $.get("/send_invitation/", {"project_id": projectId, "username": username}, function (data) {
        // Bootstrap call display error/succcess message to the user
        $parentDiv.popover({"content": data, "placement": "left"});
        $parentDiv.popover("show");
        $parentDiv.popover().on('hidden.bs.popover', function () {
            $parentDiv.popover("destroy");
        });
    });

});

//Neither of these two functions are woking yet...?
$("#project_details").on("click", function () {
    var project_id = $(this).attr("data-projectid");
    $.get("/project_details/", {"project_id": project_id});
});

$("#end_project").on("click", function () {
    if (confirm("Are you sure?\nEnding this project will delete it and all its tasks.")) {
        var project_id = $(this).attr("data-projectid");
        $.get("/end_project/", {"project_id": project_id});
    }
});


$(".remove_admin").click(function () {
    var user_id = $(this).attr("data-userid");
    var project_id = $(this).attr("data-projectid");
    $.get("/remove_admin/", {"user_id": user_id, "project_id": project_id});
});

$(".remove_member").click(function () {
    var user_id = $(this).attr("data-userid");
    var project_id = $(this).attr("data-projectid");
    $.get("/remove_member/", {"user_id": user_id, "project_id": project_id});
});

$(".promote_member").click(function () {
    var user_id = $(this).attr("data-userid");
    var project_id = $(this).attr("data-projectid");
    $.get("/promote_member/", {"user_id": user_id, "project_id": project_id});
});

$(".demote_admin").click(function () {
    var user_id = $(this).attr("data-userid");
    var project_id = $(this).attr("data-projectid");
    $.get("/demote_admin/", {"user_id": user_id, "project_id": project_id});
});

