var TestVariable = 11;

//the json object of timeslots got from database
//orginalTimeslots[day + time] = something
var originalTimeslots;

//the modified timeslots used to create time table
//timeslots[day][time] = something
var timeslots = {};

//"highlighted" for select_timeslots.html and modify_timeslots.html
//"marked" for make_decision.html
//"" for on_going.html

//the string describing what class name a single cell will have if mouse is pressed down
var MouseMarkName;

var loadTimeSlotsAndCreateTimeTable = function(url, markName) {
    $.getJSON(url, function(json) {
        originalTimeslots = json;

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
                if (timeslots[day][time] == "Blank" || timeslots[day][time] == "0") {
                    document.getElementById(time).innerHTML += "<td class='selectable' id='" + day + " " + time + "'> </td>";
                } else {
                    document.getElementById(time).innerHTML += "<td class='selectable highlighted' id='" + day + " " + time + "'> </td>";
                }
            }
            counter += 1;
        }

        selectAction(markName);
        if (markName != "highlighted"){
            markTimeTableWithNumberOfPeople();
        }

    });
};


var markTimeTableWithNumberOfPeople = function() {
    var firstColumn = timeslots[Object.keys(timeslots)[0]];
    for (time in firstColumn) {
        for (day in timeslots) {
            if (timeslots[day][time] != "0") {
                document.getElementById(day + " " +time).innerHTML +=  timeslots[day][time];
            }
        }
    }
};


//add interaction to the calendar
function selectAction(markName) {
    if (markName == "") return;
    MouseMarkName = markName;

    // Create table dragging functionality
    var isMouseDown = false;
    var highlighted = false;

    $("table#power_schedule td.selectable")
        .mousedown(function() {
            isMouseDown = true;
            highlighted = $(this).hasClass(markName)

            if (highlighted) {
                $(this).removeClass(markName)
            } else {
                $(this).addClass(markName)
            }
            return false; // prevent text selection
        })
        .mouseover(function() {
            if (isMouseDown) {
                if (highlighted) {
                    $(this).removeClass(markName)
                } else {
                    $(this).addClass(markName)
                }
            }
        })
        .bind("selectstart", function() {
            return false; // prevent text selection in IE
        })

    $('table#power_schedule td:first-child')
        .mousedown(function() {
            isMouseDown = true;

            $(this).parent().find('td:not(:first-of-type)').toggleClass(markName)
            $(this).css('cursor', 'pointer')
            return false
        })
        .mouseover(function() {
            if (isMouseDown) {
                $(this).parent().find('td:not(:first-of-type)').toggleClass(markName)
            }
        })
        .bind("selectstart", function() {
            return false; // prevent text selection in IE
        })

    $(document)
        .mouseup(function() {
            isMouseDown = false
        })
}


function postTimeSlotsAndRedirect(postURL, redirectURL) {
    for (entry in originalTimeslots) {
        var currentcell = document.getElementById(entry);
        if (currentcell.className.includes(MouseMarkName)) {
            originalTimeslots[entry] = "Selected";
        } else {
            originalTimeslots[entry] = "Blank";
        }
    }

    $.ajax({
            type: "POST",
            url: postURL,
            data: JSON.stringify(originalTimeslots),
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        })
        .done(function(data) {
            console.log("Response");
            window.location = redirectURL;
        });
}