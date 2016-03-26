/** Pops up a confirmation prompt when a judge clicks on
  * "Advance to next level" button
  */
function confirm_promote() {
    bootbox.confirm("Are you sure you want to advance the robot to the next level? This action is IRREVERSIBLE!", function(result) {
        if (result == true) {
            document.forms[0].submit();
        }
    });
    return false; //prevents default action of "submit" button
}


function confirm_newrun() {
    bootbox.confirm("Are you sure you want to submit this run?", function(result) {
        if (result == true) {
            document.forms[0].submit();
        }
    });
    return false; //prevents default action of "submit" button
}