/**
 * Vue component for status
 */

Vue.component('status', {
    template: '#status-template',
    props: ["statuses"],
    methods: {
        "restart": function (key) {
            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", "/restart-"+key, true);
            xhttp.send();
        },
        "healthClass": function (health) {
            if (health == "Health.HEALTHY") {
                return "bg-success";
            } else if (health == "Health.DEAD") {
                return "bg-danger";
            } else if (health == "Health.SICK" || health == "Health.DIEING") {
                return "bg-warning";
            }
            return "";
        },
        "healthMessage": function (health) {
            return health.replace("Health.", "");
        }
    }
});