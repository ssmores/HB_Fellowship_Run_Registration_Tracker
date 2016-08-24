"use strict";

function updateRace(results) {
    var status = results;
    $('#race-status').html(status);
}


function updateRaceRegistration() {
    var race_id = $('#race-id').val();
    console.log(race_id);
    $.get('/update_race_status/' + race_id, updateRace);
    // $.get('/update_race_status/' + race_id, updateStatus);
}

$('#update-race-registration').click(updateRaceRegistration);

function updateHotel(results) {
    var status = results;
    $('#hotel-status').html(status);
}


function updateHotelStatus() {
    var race_id = $('#race-id').val();
    console.log(race_id)
    $.get('/update_hotel_status/' + race_id, updateHotel);
}

$('#update-hotel-status').click(updateHotelStatus);

