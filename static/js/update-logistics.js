"use strict";

//Updates for race registration status.
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


//Updates for hotel reservation status.
function updateHotel(results) {
    var status = results;
    $('#hotel-status').html(status);
}


function updateHotelStatus() {
    var race_id = $('#race-id').val();
    console.log(race_id);
    $.get('/update_hotel_status/' + race_id, updateHotel);
}

$('#update-hotel-status').click(updateHotelStatus);


//Updates for airfare status.
function updateAirfare(results) {
    var status = results;
    $('#airfare-status').html(status);
}

function updateAirfareStatus() {
    var race_id = $('#race-id').val();
    console.log(race_id);
    $.get('/update_airfare_status/' + race_id, updateAirfare);
}

$('#update-airfare-status').click(updateAirfareStatus);


//Update for transportation.

function updateTransportation(results) {
    var status = results;
    $('#transportation-status').html(status);
}


function updateTransportationStatus() {
    var race_id = $('#race-id').val();
    console.log(race_id);
    $.get('/update_transportation_status/' + race_id, updateTransportation);
}


$('#update-transportation-status').click(updateTransportationStatus);