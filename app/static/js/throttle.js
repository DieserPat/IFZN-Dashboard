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


document.getElementById("checkbox_throttle").addEventListener("click", checkbox_throttle);
document.getElementById("throttleSetpoint").addEventListener("change", updateSetpoint);

function checkbox_throttle() {
    let checkbox = document.getElementById("checkbox_throttle");
    let ip = document.getElementById("IPThrottle");
    let port = document.getElementById("PortThrottle");
    let setpoint = document.getElementById("throttleSetpoint");
    postData(`${window.origin}/Dashboard/Throttle`,
        {
            mode: "activate",
            value: checkbox.value,
            ip: ip.value,
            port: port.value
        })
        .then((data) => {
            if (data.value == 1) {
                checkbox.value = 1;
                setpoint.disabled = false;
            } else if (data.value == 0) {
                setpoint.disabled = true;
                checkbox.value = 0;
                checkbox.checked = false;
            }
        }
        )
}

function updateSetpoint(element) {
    let val = element.target.value;
    val = val >= 0 ? val : 0;
    val = val <= 100 ? val : 100;
    element.target.value = val;
    let ip = document.getElementById("IPThrottle");
    let port = document.getElementById("PortThrottle");
    postData(`${window.origin}/Dashboard/Throttle`,
        {
            mode: "set",
            value: element.target.value,
            ip: ip.value,
            port: port.value
        })
        .then((data) => {
            element.target.value = data.value;
        })
}