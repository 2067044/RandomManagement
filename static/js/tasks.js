$('.datepicker').datepicker();

$("#task_form").submit(function(event){

    var error = false;
    var $title = $('#id_title');
    var $description = $("#id_description");
    var $date = $("#id_due_date");

    if ($title.val() == 0 ) {
        error = true;
        $title.addClass("bad-input");
        $title.attr("placeholder", "This field is required.");
    }

    if ($description.val() == 0 ) {
        error = true;
        $description.addClass("bad-input");
        $description.attr("placeholder", "This field is required.");
    }

    if ($date.val() == 0 ) {
        error = true;
        $date.addClass("bad-input");
        $date.attr("placeholder", "This field is required.");
    }

    // This regex doesnt work at this point
    if (!(/\d\d\/\d\d\/\d\d\d\d/.test($date.val()))) {
        error = true;
        $date.addClass("bad-input");
        $date.attr("placeholder", "This field is required.");
    }

    if (error) {event.preventDefault(); return;}

    $(this).submit();
});

// This call here allows for async task completion; and task completion reversal
$('#complete-task').on("click", function(){
    var taskId = $(this).attr("data-taskid");
    var $button = $(this);
    $.get("/complete_task/" , {task_id: taskId}, function(data) {
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

// Tasks AJAX calls
var taskPage;
$(document).ready(function(){taskPage = 0});
$('#left-tasks').on("click", function() {
    // go back
});

$('#right-tasks').on("click", function() {
    taskPage += 1;
    $.get("/get_tasks/", {page: taskPage}, function(data) {
        console.log(data);
    });
});