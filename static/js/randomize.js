/*
 * Randomize puppy, candle, start and furniture location
 */
 
function puppy_loc() {
    var arr = ["A", "B", "C"];
    return arr[Math.floor(Math.random()*arr.length)];
}

function candle_loc() {
    var arr = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"];
    return arr[Math.floor(Math.random()*arr.length)];
}

function start_loc() {
    var arr = ["Room 1", "Room 2", "Room 3", "Room 4"];
    return arr[Math.floor(Math.random()*arr.length)];  
}

function furniture_loc() {
    var arr = ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8"];
    return arr[Math.floor(Math.random()*arr.length)]; 
}


$(document).ready(function() {
    $('#candle-but').on('click', function (e) {
        $('#candle').replaceWith(candle_loc());
    })
    $('#puppy-but').on('click', function (e) {
        $('#puppy').replaceWith(puppy_loc());
    })
    $('#start-but').on('click', function (e) {
        $('#start').replaceWith(start_loc());
    })
    $('#furniture-but').on('click', function (e) {
        $('#furniture').replaceWith(furniture_loc());
    })
});