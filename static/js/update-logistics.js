"use strict";

//Updates for race registration status.
function updateRace(results) {
    var status = results;
    $('#race-status').html(status);
}


function updateRaceRegistration(evt) {
    var race_id = $('#race-id').val();
    console.log('update race registration');
    $.post('/update_race_status/' + race_id, updateRace);
}

$(document).ready(function(){
$('#update-race-registration').click(updateRaceRegistration);
})

//Updates for hotel reservation status.
function updateHotel(results) {
    var status = results;
    $('#hotel-status').html(status);
}


function updateHotelStatus(evt) {
    var race_id = $('#race-id').val();
    console.log('update hotel');
    $.post('/update_hotel_status/' + race_id, updateHotel);
}

$('#update-hotel-status').click(updateHotelStatus);


//Updates for airfare status.
function updateAirfare(results) {
    var status = results;
    $('#airfare-status').html(status);
}

function updateAirfareStatus(evt) {
    var race_id = $('#race-id').val();
    console.log('update airfare');
    $.post('/update_airfare_status/' + race_id, updateAirfare);
}

$('#update-airfare-status').click(updateAirfareStatus);


//Update for transportation.
function updateTransportation(results) {
    var status = results;
    $('#transportation-status').html(status);
}


function updateTransportationStatus(evt) {
    var race_id = $('#race-id').val();
    console.log('update transportation');
    $.post('/update_transportation_status/' + race_id, updateTransportation);
}


$('#update-transportation-status').click(updateTransportationStatus);


// Update for the first email notification.
function updateFirstEmail(results) {
    var status = results;
    $('#email-start-date').html(status);
}

function updateEmailStartDate(evt) {
    var race_id = $('#race-id').val();
    console.log('update email start date');
    var newStartDate = {
        'start_date': $('#update-email-start-date').val()
    };
    $.post('/update_email_start_date/' + race_id, newStartDate, updateFirstEmail);
}

$('#update-email-start-date-button').click(updateEmailStartDate);


//Update the last email notification date.
function updateLastEmail(results) {
    var status = results;
    $('#email-end-date').html(status);
}

function updateEmailEndDate(evt) {
    var race_id = $('#race-id').val();
    console.log('update email end date');
    var newEndDate = {
        'end_date': $('#update-email-end-date').val()
    };
    $.post('/update_email_end_date/' + race_id, newEndDate, updateLastEmail);
}


$('#update-email-end-date-button').click(updateEmailEndDate);

//Feature to be implemeted at a later time.
//Update email notification frequency.
// function updateInterval(results) {
//     var status = results;
//     $('#email-interval').html(status);
// }


// function updateEmailInterval(evt) {
//     var race_id = $('#race-id').val()
//     console.log('update reminder frequency');
//     var emailFrequency = {
//         'hour_frequency': $('#update-email-interval').val()
//     }
//     $.post('/update_email_interval/' + race_id, emailFrequency, updateInterval);
// }


// $('#update-email-interval-button').click(updateEmailInterval);

//Update email notification frequency.
// function updateNeedSubsequentEmailIndicator(results) {
//     var status = results;
//     $('#next-email-indicator').html(status);
// }


// function updateNeedSubsequentEmail(evt) {
//     var race_id = $('#race-id').val();
//     console.log('update need subsequent email');
//     $.post('/update_need_subsequent_email/' + race_id, updateNeedSubsequentEmailIndicator);
// }


// $('#update-next-email-indicator').click(updateNeedSubsequentEmail);



//Send email immediately for tracked race confirmation.
function successfulEmailSent(results) {
    var status = results;
    alert(status);
}


function sendEmail(evt) {
    var race_id = $('#race-id').val();
    console.log("before AJAX call")
    $.post('/send_email/' + race_id, successfulEmailSent);
    console.log("email sent?")
}

$('#email-notification-button').click(sendEmail);