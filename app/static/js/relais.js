"use strict";
async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        cache: 'no-cache',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}

document.getElementById("checkbox_relais").addEventListener("click", ckb_relais);
let buttons = document.getElementById("list_buttons_relais");
for (let btn of buttons.children) {
    for (let list of btn.children) {
        let curBtn = list.lastElementChild;
        document.getElementById(curBtn.id).addEventListener("click", function (event) {
            OnOffBtn(this.id);
        });
    }
}


function ckb_relais() {
    let checkbox = document.getElementById("checkbox_relais");
    let ip = document.getElementById("IPRelais");
    let port = document.getElementById("PortRelais");
    let value = checkbox.value;
    postData(`${window.origin}/Dashboard/Relais`,
        {
            mode: "activateRelais",
            value: value,
            ip: ip.value,
            port: port.value
        })
        .then((data) => {
            if (data.value == 1) {
                checkbox.value = 1;
            } else if (data.value == 0) {
                let buttons = document.getElementById("list_buttons_relais");
                for (let btn of buttons.children) {
                    for (let list of btn.children) {
                        let curBtn = list.lastElementChild;
                        if (curBtn.value == 1) {
                            curBtn.value = 0;
                            setButtonClass(curBtn);
                        }
                    }
                }
                checkbox.value = 0;
                checkbox.checked = false;
            }
        }
        )
}

function OnOffBtn(id) {
    let checkbox = document.getElementById("checkbox_relais");
    let ip = document.getElementById("IPRelais");
    let port = document.getElementById("PortRelais");
    if (checkbox.value == 1) {
        let button = document.getElementById(id);
        button.innerHTML = "<span class='loader'></span>"
        let entry = {
            id: id,
            value: button.value,
            mode: 'setRelais',
            ip: ip.value,
            port: port.value
        }
        postData(`${window.origin}/Dashboard/Relais`, entry)
            .then((data) => {
                setButtonClass(data);
            })
    } else {
        alert("Relais nicht freigegeben!")
    }
}

function setButtonClass(button) {
    let btn = document.getElementById(button.id)
    let value = button.value
    if (value == 1) {
        btn.className = "btn btn-on";
        btn.innerHTML = "ON";
        btn.value = 1;
    } else if (value == 0) {
        btn.className = "btn btn-off";
        btn.innerHTML = "OFF";
        btn.value = 0;
    }
}