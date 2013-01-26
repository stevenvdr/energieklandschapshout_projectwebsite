function hideForm() {
    $('#calendar_form_container').hide();
    form_shown = false;
}

function showForm() {
    $('#calendar_form_container').show();
    form_shown = true;
}

function changeFormDate(val) {
    $('[name="date"]').val(val);
}

function clickSubscribe(val) {
    showForm();
    changeFormDate(val);
    return false;
}
function hideContact() {
    $('#calendar_contact_container').hide();
    contact_shown = false;
    return false;
}

function showContact() {
    $('#calendar_contact_container').show();
    contact_shown = true;
}

function renderContact(date, name, email, phone, approved) {
    contact_content = '';
    contact_content += '<div id="calendar_contact">';
    contact_content += '<a href="#" onclick="return hideContact();">Sluit dit venster</a>';

    //Contact information
    contact_content += '<h3>Reservatie voor '+ date + ':</h3>';
    contact_content += '<h4>Contact informatie:</h4>';
    contact_content += '<p><b>Naam:</b> ' + name + '</p>';
    contact_content += '<p><b>E-mailadres:</b> ' + email + '</p>';
    contact_content += '<p><b>Telefoonnummer:</b> ' + phone + '</p>';

    //Admin Controls
    contact_content += '<h4>Bewerk reservatie:</h4>';
    if (!approved)
        contact_content += '<p><a href="?approve=' + date + '">Keur de reservatie goed</a></p>';
    else
        contact_content += '<p>De reservatie is goedgekeurd</p>';

    contact_content += '<p><a href="?delete=' + date + '">Delete de reservatie</a></p>';

    contact_content += '</div>'

    div = $('#calendar_contact_container');
    div.html(contact_content);
}

function clickReservation(date, name, email, phone, approved) {
    renderContact(date, name, email, phone, approved);
    showContact();
    return false;
}