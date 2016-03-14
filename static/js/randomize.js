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

function start_loc_img(loc_id, orient_id) {
    var location = {
        'Room 1': '/static/img/_THUMBNAILS_/ArbitraryStart.Thumbnails/',

    }

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

    return [location[loc_id], orients[orient_id]];
}

function furniture_img(id) {
    var dict = {
        '01': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/01.png',
        '02': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/02.png',
        '03': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/03.png',
        '04': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/04.png',
        '05': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/05.png',
        '06': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/06.png',
        '07': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/07.png',
        '08': '/static/img/_THUMBNAILS_/Furniture.Thumbnails/08.png'
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
        var randomStartLinks = start_loc_img();
        var randRoomLink = randomStartLinks[0];
        var randOrientLink = randomStartLinks[1];
        $('#startRoomImg').attr('src', randRoomLink);
        $('#startOrientImg').attr('src', randOrientLink);
    })
    $('#furniture-but').on('click', function (e) {
        var furniture_loc_id = furniture_loc();
        $('#furniture').html(furniture_loc_id);

        $('#furnitureLocationDiv').removeClass('hidden');
        $('#furnitureLocationImg').attr('src', furniture_loc_img(furniture_loc_id));

    })
});