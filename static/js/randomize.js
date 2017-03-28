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
    var rooms = ["Room 1", "Room 2", "Room 3", "Room 4"];
    var orients = ['0D', '45D', '90D', '135D', '180D', '225D', '270D', '315D'];
    var randomRoom = rooms[Math.floor(Math.random()*rooms.length)];
    var randomOrient = orients[Math.floor(Math.random()*orients.length)];
    return [randomRoom, randomOrient];  
}

function furniture_loc() {
    var arr = ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8"];
    return arr[Math.floor(Math.random()*arr.length)]; 
}

function baby_exit_loc() {
    var arr = ["W1", "W2", "W3", "W4"];
    return arr[Math.floor(Math.random()*arr.length)];
}

function baby_placement_loc() {
    var arr = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"];
    return arr[Math.floor(Math.random()*arr.length)];
}

function puppy_img(id) {
    var dict = {
        'A': '/static/img/_THUMBNAILS_/Dogs.Thumbnails/dog1.png',
        'B': '/static/img/_THUMBNAILS_/Dogs.Thumbnails/dog2.png',
        'C': '/static/img/_THUMBNAILS_/Dogs.Thumbnails/dog3.png'
    }
    return dict[id];
}

function candle_img(id) {
    var dict = {
        'F1': '/static/img/_THUMBNAILS_/Flames.Thumbnails/flame1.png',
        'F2': '/static/img/_THUMBNAILS_/Flames.Thumbnails/flame2.png',
        'F3': '/static/img/_THUMBNAILS_/Flames.Thumbnails/flame3.png',
        'F4': '/static/img/_THUMBNAILS_/Flames.Thumbnails/flame4.png',
        'F5': '/static/img/_THUMBNAILS_/Flames.Thumbnails/flame5.png',
        'F6': '/static/img/_THUMBNAILS_/Flames.Thumbnails/flame6.png',
        'F7': '/static/img/_THUMBNAILS_/Flames.Thumbnails/flame7.png',
        'F8': '/static/img/_THUMBNAILS_/Flames.Thumbnails/flame8.png'
    }
    return dict[id];
}

function start_loc_img(orient_id) {
    var orients = {
        '0D': '/static/img/_THUMBNAILS_/ArbitraryStart.Thumbnails/AS1.png',
        '45D': '/static/img/_THUMBNAILS_/ArbitraryStart.Thumbnails/AS2.png',
        '90D': '/static/img/_THUMBNAILS_/ArbitraryStart.Thumbnails/AS3.png',
        '135D': '/static/img/_THUMBNAILS_/ArbitraryStart.Thumbnails/AS4.png',
        '180D': '/static/img/_THUMBNAILS_/ArbitraryStart.Thumbnails/AS5.png',
        '225D': '/static/img/_THUMBNAILS_/ArbitraryStart.Thumbnails/AS6.png',
        '270D': '/static/img/_THUMBNAILS_/ArbitraryStart.Thumbnails/AS7.png',
        '315D': '/static/img/_THUMBNAILS_/ArbitraryStart.Thumbnails/AS8.png'    
    }

    return orients[orient_id];
}

function furniture_img(id) {
    var dict = {
        'O1': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/O1_merged.png',
        'O2': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/O2_merged.png',
        'O3': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/O3_merged.png',
        'O4': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/O4_merged.png',
        'O5': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/O5_merged.png',
        'O6': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/O6_merged.png',
        'O7': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/O7_merged.png',
        'O8': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/O8_merged.png'
    }

    return dict[id];
}

function baby_exit_loc_img(id) {
    var dict = {
        'W1': '/static/img/_THUMBNAILS_/Targets.Thumbnails/W1.png',
        'W2': '/static/img/_THUMBNAILS_/Targets.Thumbnails/W2.png',
        'W3': '/static/img/_THUMBNAILS_/Targets.Thumbnails/W3.png',
        'W4': '/static/img/_THUMBNAILS_/Targets.Thumbnails/W4.png'
    }

    return dict[id];
}

function baby_place_loc_img(id) {
    var dict = {
        'C1': '/static/img/_THUMBNAILS_/Cradle.Thumbnails/cradle1.png',
        'C2': '/static/img/_THUMBNAILS_/Cradle.Thumbnails/cradle2.png',
        'C3': '/static/img/_THUMBNAILS_/Cradle.Thumbnails/cradle3.png',
        'C4': '/static/img/_THUMBNAILS_/Cradle.Thumbnails/cradle4.png',
        'C5': '/static/img/_THUMBNAILS_/Cradle.Thumbnails/cradle5.png',
        'C6': '/static/img/_THUMBNAILS_/Cradle.Thumbnails/cradle6.png',
        'C7': '/static/img/_THUMBNAILS_/Cradle.Thumbnails/cradle7.png',
        'C8': '/static/img/_THUMBNAILS_/Cradle.Thumbnails/cradle8.png'
    }

    return dict[id];
}

$(document).ready(function() {
    $('#candle-but').on('click', function (e) {
        var candle_loc_id = candle_loc();
        $('#candle').html(candle_loc_id);

        $('#candleLocationDiv').removeClass('hidden');
        $('#candleLocationImg').attr('src', candle_img(candle_loc_id));
    })
    $('#puppy-but').on('click', function (e) {
        var puppy_loc_id = puppy_loc();
        $('#puppy').html(puppy_loc_id);

        $('#puppyLocationDiv').removeClass('hidden');
        $('#puppyLocationImg').attr('src', puppy_img(puppy_loc_id));
    })
    $('#start-but').on('click', function (e) {
        var randomStart = start_loc();
        var randomRoom = randomStart[0];
        var randomOrient = randomStart[1];
        
        $('#start').html(randomRoom + ' ' + randomOrient);

        $('#startLocationDiv').removeClass('hidden');
        $('#roomImgDiv').removeClass('hidden');
        var randOrientLink = start_loc_img(randomOrient);
        $('#startOrientImg').attr('src', randOrientLink);
    })
    $('#furniture-but').on('click', function (e) {
        var furniture_loc_id = furniture_loc();
        $('#furniture').html(furniture_loc_id);

        $('#furnitureLocationDiv').removeClass('hidden');
        $('#furnitureLocationImg').attr('src', furniture_img(furniture_loc_id));

    })
    $('#baby-exit-but').on('click', function (e) {
        var baby_exit_id = baby_exit_loc();
        $('#baby-exit').html(baby_exit_id);
        
        $('#babyExitDiv').removeClass('hidden');
        $('#babyExitImg').attr('src', baby_exit_loc_img(baby_exit_id));
    })
    $('#baby-placement-but').on('click', function (e) {
        var baby_placement_id = baby_placement_loc();
        $('#baby-placement').html(baby_placement_id);

        $('#babyLocationDiv').removeClass('hidden');
        $('#babyLocationImg').attr('src', baby_place_loc_img(baby_placement_id));
    })
});