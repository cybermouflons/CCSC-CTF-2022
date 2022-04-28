$(document).ready(function () {
    $.getJSON("/locations", function (data) {
        var items = [];
        $.each(data, function (key, val) {
            items.push("<option value='" + val + "'>" + val + "</li>");
        });

        $("#locations").append(items.join("\n"));
    });

    $("#portalButton").click(function () {
        var selected_location = $('#locations').find(":selected").text().trim();

        $("#warn-me").click(function () {
            $(document).trigger("add-alerts", [{
                "message": "This is a warning.",
                "priority": 'warning'
            }]);
        });
        $.post("/portal", JSON.stringify({
            "filter": {
                "name": selected_location
            }
        }), function (data, status, jqXHR) {
            data = JSON.parse(data);
            if (data["error"]){
                $(document).trigger("add-alerts", [{
                    "message": data["error"],
                    "priority": 'error'
                }]);
            } else {
                $(".portal").html(`<div class="card">
                <div class="card-header">
                  ${data["name"]} (${data["type"]})
                </div>
                <div class="card-body">
                  <blockquote class="blockquote mb-0">
                    <p><img id="buttonImage"
                        src="https://static1.squarespace.com/static/570413982eeb8114b6631016/59cffa294c0dbf7579528461/59cffc5937c5819421e5d541/1506803258457/Portal.gif"></p>
                  </blockquote>
                  <div id="author">“Wubba Lubba Dub Dub!</div>
                </div>
              </div>`)
            }
        }).fail(function (response) {
            data = JSON.parse(response.responseText);
            $(document).trigger("add-alerts", [{
                "message": data["error"],
                "priority": 'error'
            }]);
        });
    });
});