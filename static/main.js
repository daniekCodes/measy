function location_toggle() {
    // Check which boxes are assigned to this toggle
    let physical = document.getElementById("physical_placeholder");
    let online = document.getElementById("online_placeholder");

    // Which radio button is selected
    let choice = document.querySelector('input[name="location_type"]:checked').value;

    // If/else display choice logic
    if (choice === 'physical') {
        physical.style.display = 'block';
        online.style.display = 'none';
    } else {
        physical.style.display = 'none';
        online.style.display = 'block';
    }
}

function meeting_toggle() {
    // Check which boxes are assigned to this toggle
    let fixed = document.getElementById("fixed_placeholder");
    let doodle = document.getElementById("doodle_placeholder");

    // Which radio button is selected
    let choice = document.querySelector('input[name="meeting_type"]:checked').value;

    // FIX: Changed 'physical' to 'fixed_meeting'
    if (choice === 'fixed_meeting') {
        fixed.style.display = 'block';
        doodle.style.display = 'none';
    } else {
        fixed.style.display = 'none';
        doodle.style.display = 'block';
    }
}