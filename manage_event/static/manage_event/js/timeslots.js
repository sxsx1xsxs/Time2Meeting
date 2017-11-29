var TestVariable = 1;
var originalTimeslots;
var originaltimeslotsjson = $.getJSON("../initialize_timeslots", function(json) {
    console.log("success");
    console.log(json);
    originalTimeslots = json;

    var timeslots = {};
    var date;

    for (entry in originalTimeslots) {
        var items = entry.split(" ");
        if (date != items[0]) {
            date = items[0];
            timeslots[date] = {};
            timeslots[date][items[1]] = originalTimeslots[entry];
        } else {
            timeslots[date][items[1]] = originalTimeslots[entry];
        }
    }

    var firstColumn = timeslots[Object.keys(timeslots)[0]];
    var counter = 0;

    for (day in timeslots) {
        firstColumn = timeslots[day];
        document.getElementById("firstRow").innerHTML += "<td>" + day + "</td>";
    }

    for (time in firstColumn) {
        if (counter % 2 == 0) {
            document.getElementById("power_schedule").innerHTML += "<tr id= " + time + ">" + "<td>" + time + "</td>" + "</tr>";
        } else {
            document.getElementById("power_schedule").innerHTML += "<tr id= " + time + ">" + "<td>" + "" + "</td>" + "</tr>";
        }
        for (day in timeslots) {
            if (timeslots[day][time] == "Blank") {
                document.getElementById(time).innerHTML += "<td class='selectable' id='" + day + " " + time + "'> </td>";
            } else {
                document.getElementById(time).innerHTML += "<td class='selectable highlighted' id='" + day + " " + time + "'> </td>";
            }
        }
        counter += 1;
    }
    $(function() {
        // Create table dragging functionality
        var isMouseDown = false;
        var highlighted
        console.log("event listner");
        $("table#power_schedule td.selectable")
            .mousedown(function() {
                console.log("mouse down");
                isMouseDown = true;
                highlighted = $(this).hasClass('highlighted')

                if (highlighted) {
                    $(this).removeClass('highlighted')
                } else {
                    $(this).addClass('highlighted')
                }
                return false; // prevent text selection
            })
            .mouseover(function() {
                if (isMouseDown) {
                    if (highlighted) {
                        $(this).removeClass('highlighted')
                    } else {
                        $(this).addClass('highlighted')
                    }
                }
            })
            .bind("selectstart", function() {
                return false; // prevent text selection in IE
            })

        $('table#power_schedule td:first-child')
            .mousedown(function() {
                isMouseDown = true;

                $(this).parent().find('td:not(:first-of-type)').toggleClass('highlighted')
                $(this).css('cursor', 'pointer')
                return false
            })
            .mouseover(function() {
                if (isMouseDown) {
                    $(this).parent().find('td:not(:first-of-type)').toggleClass('highlighted')
                }
            })
            .bind("selectstart", function() {
                return false; // prevent text selection in IE
            })

        $(document)
            .mouseup(function() {
                isMouseDown = false
            })
    });
})


function myFunction() {

    for (entry in originalTimeslots) {
        var currentcell = document.getElementById(entry);
        if (currentcell.className.includes("highlighted")) {
            originalTimeslots[entry] = "Selected";
        } else {
            originalTimeslots[entry] = "Blank";
        }
    }

    $.ajax({
            type: "POST",
            url: "../read_timeslots/",
            data: JSON.stringify(originalTimeslots),
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        })
        .done(function(data) {
            console.log("Response");
            window.location = "../select_publish_render";
        });
    console.log(originalTimeslots);
}