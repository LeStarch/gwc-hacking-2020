
let keylog = "" +
    "Logging started ...\n" +
    "\n" +
    "2020-12-27 13:33:07-0800 > <RShft>TODO<RShft>:\n" +
    "2020-12-27 13:33:12-0800 > <Enter>- <RShft>Buy veggies\n" +
    "2020-12-27 13:33:17-0800 > <Enter>- <RShft>Seel<BckSp><BckSp>ll a potatoe to the neighbor\n" +
    "2020-12-27 13:33:33-0800 > <Enter>- <RShft>Check computer for viruses\n" +
    "2020-12-27 13:33:42-0800 > <Enter>face\n" +
    "2020-12-27 13:33:51-0800 > <Enter>thementor<RShft>@awesome.mentorthe.com<Tab><RShft>IB4the<RShft>Mentory<BckSp><#+26><RShft>IB4the<RShft>Mentor<RShft>$facebook\n" +
    "2020-12-27 13:34:52-0800 > <Enter><RShft>This facebook post is the <RShft>BEST ever woot<RShft>!\n" +
    "2020-12-27 13:35:05-0800 > <Enter><LShft>\n" +
    "2020-12-27 13:35:06-0800 > <Enter>- <RShft>Check facebook messgaes <BckSp><BckSp><BckSp><BckSp>ag<BckSp><BckSp><BckSp>ages for scamstwitte.co<#+4><BckSp><BckSp><BckSp>r.com\n" +
    "2020-12-27 13:35:36-0800 > <Enter>thementor8455<RShft>@gmail.com<RShft>IB4the<RShft>Mentor<RShft>$twitter\n" +
    "2020-12-27 13:36:16-0800 > <Enter><RShft>Tweet<RShft>! <RShft>Tweet<RShft>! <RShft>Tweet<RShft>! <RShft>Happy <RShft>NEw <RShft>Years<RShft>!\n" +
    "2020-12-27 13:36:41-0800 > <Enter>gmail\n" +
    "2020-12-27 13:37:11-0800 > <Enter>thementor8455<RShft>@gmail.com\n" +
    "2020-12-27 13:39:19-0800 > <Enter><RShft>IB4the<RShft>Mentor<RShft>$gpail<BckSp><BckSp><BckSp><BckSp>mail2020\n" +
    "2020-12-27 13:40:21-0800 > <Enter>60211\n" +
    "2020-12-27 13:40:27-0800 > <Enter>sudo apt install xeyes\n" +
    "2020-12-27 13:43:35-0800 > <Enter>sudo apt install xeyes\n" +
    "2020-12-27 13:43:53-0800 > <Enter><RShft>IB4the<RShft>Mentor<RShft>$\n" +
    "2020-12-27 13:44:05-0800 > <Enter>y\n" +
    "2020-12-27 13:44:07-0800 > <Enter><Up><Up><Up>\n" +
    "2020-12-27 13:44:17-0800 > <Enter>\n" +
    "\n" +
    "Logging stopped at 2020-12-27 13:44:17-0800\n" +
    "\n";


function send(user, pass, service, endpoint) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let hint = "";
            let messages = this.responseText;
            let index = messages.indexOf("-hint-");
            if (index > 0) {
                hint = messages.substr(index + 6);
                messages = messages.substr(0, index);
            }
            document.getElementById("messages").innerText = messages;
            document.getElementById("hints").innerText = hint;
        }
    }
    let form = new FormData();
    form.set("user", user);
    form.set("password", pass);
    if (service != null) {
        form.set("service", service);
    }
    xhttp.open("POST", endpoint, true);
    xhttp.send(form);
}

function onsub(endpoint) {
    let service = null;
    let user = document.getElementById("user").value;
    let password = document.getElementById("password").value;
    try {
        service = document.getElementById("service").value;
    } catch {
        service = null;
    }
    send(user, password, service, endpoint);
}

function setup() {
    try {
        document.getElementById("keylog").innerText = keylog;
    } catch (e) {}
}

document.addEventListener('DOMContentLoaded', setup, false);