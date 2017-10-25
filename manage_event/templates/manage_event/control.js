$(function() {
        // Create table dragging functionality
        var isMouseDown = false;
        var highlighted
        $("table#power_schedule td.selectable")
            .mousedown(function() {
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