$('.datepicker').datepicker();

$("#task_form").submit(function (event) {

    var error = false;
    var $title = $('#id_title');
    var $description = $("#id_description");
    var $date = $("#id_due_date");

    if ($title.val() == 0) {
        error = true;
        $title.addClass("bad-input");
        $title.attr("placeholder", "This field is required.");
    }

    if ($description.val() == 0) {
        error = true;
        $description.addClass("bad-input");
        $description.attr("placeholder", "This field is required.");
    }

    if ($date.val() == 0) {
        error = true;
        $date.addClass("bad-input");
        $date.attr("placeholder", "This field is required.");
    }

    if (!(/\d\d\/\d\d\/\d\d\d\d/.test($date.val()))) {
        error = true;
        $date.addClass("bad-input");
        $date.attr("placeholder", "This field is required.");
    }

    if (!$("#id_users option:selected").length) {
        error = true;
        $("#id_users").addClass("bad-input");
    }

    if (error) {
        event.preventDefault();
        return;
    }

    $(this).submit();
});

// This call here allows for async task completion; and task completion reversal
$('#complete-task').on("click", function () {
    var taskId = $(this).attr("data-taskid");
    var $button = $(this);
    $.get("/complete_task/", {task_id: taskId}, function (data) {
        if (data == "True") {
            $button.html("Reverse completion");
            $button.removeClass("btn-primary");
            $button.addClass("btn-warning");
        } else {
            $button.html("Complete task");
            $button.removeClass("btn-warning");
            $button.addClass("btn-primary");
        }
    });
});

// Task search function
$("#task-search").keyup(function () {
    var projectID = $(this).attr("data-projectid");
    var query = $(this).val();
    var $taskDisplay = $("#found-task-display");
    if (query == "") {
        $taskDisplay.empty();
        return;
    }


    $.get("/find_task/", {query: query, project_id: projectID}, function (data) {
        $taskDisplay.empty();
        var text = "";
        for (var i = 0; i < data.length; i++) {
            text = "";
            text += "<h3><a href=\"/task/" + data[i].id + "\">" + data[i].title + "</a></h3>";
            text += "<p>" + data[i].description + "<p>";
            $taskDisplay.append(text);
        }

    });
});

$('#new-task').on('hidden.bs.modal', function () {
    $('#id_title').removeClass("bad-input");
    $("#id_description").removeClass("bad-input");
    $("#id_due_date").removeClass("bad-input");
    $("#id_users").removeClass("bad-input");
});