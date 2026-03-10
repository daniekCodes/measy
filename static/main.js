// main calendar
document.addEventListener('DOMContentLoaded', function() {
    const calendar_element = document.getElementById("calendar")
    const calendar_config = new FullCalendar.Calendar(calendar_element, {
        // Standard month view
        initialView: "dayGridMonth",
        // Custom buttons
        customButtons: {
            add_event_button: {
                text:"+",
                click: function() {
                    window.location.href = "/create_event";
                }
            }
        },

        // top menu
        headerToolbar: {
            left: "dayGridMonth,timeGridWeek,timeGridDay",
            center: "title",
            right: "prev,today,next add_event_button",
        }
    })
    // Render calendar
    calendar_config.render();
})