function location_toggle() {
    let physical = document.getElementById("physical_placeholder");
    let online = document.getElementById("online_placeholder");
    let choice = document.querySelector('input[name="location_type"]:checked').value;

    if (choice === 'physical') {
        physical.style.display = 'block';
        online.style.display = 'none';
    } else {
        physical.style.display = 'none';
        online.style.display = 'block';
    }
}

function meeting_toggle() {
    let fixed = document.getElementById("fixed_placeholder");
    let doodle = document.getElementById("doodle_placeholder");
    let choiceElement = document.querySelector('input[name="meeting_type"]:checked');

    if (!choiceElement) {
        fixed.style.display = 'none';
        doodle.style.display = 'none';
        return;
    }
    let choice = choiceElement.value;

    if (choice === 'fixed_meeting') {
        fixed.style.display = 'block';
        doodle.style.display = 'none';
    } else if (choice === 'doodle_meeting') {
        fixed.style.display = 'none';
        doodle.style.display = 'block';
    } else {
        fixed.style.display = 'none';
        doodle.style.display = 'none';
    }
}