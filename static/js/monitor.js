/**
 monitor.js: JavaScript used to build the monitoring interface for the various hacking activities for GWC>
 */
import "./status.vue.js"


let app = null;
/**
 * Grab the data from the backend and update our app
 */
function monitor() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            app.statuses = JSON.parse(this.responseText)["statuses"];
        }
    }
    xhttp.open("GET", "/status", true);
    xhttp.send();
}


function setup() {
    app = new Vue({el: "#app", "data": {"statuses": []}});
    setInterval(monitor, 500);
}

document.addEventListener('DOMContentLoaded', setup, false);