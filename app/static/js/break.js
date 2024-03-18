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

document.getElementById("checkbox_break").addEventListener("click", checkbox_break);
document.getElementById("nEngSetpoint").addEventListener("change", updateSetpoint);

function checkbox_break() {
    let checkbox = document.getElementById("checkbox_break");
    let com = document.getElementById("comBreak");
    let setpoint = document.getElementById("nEngSetpoint");
    postData(`${window.origin}/Dashboard/Break`,
        {
            mode: "activate",
            value: checkbox.value,
            com: com.value
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
    val = val <= 3000 ? val : 3000;
    element.target.value = val;
    let com = document.getElementById("comBreak");
    postData(`${window.origin}/Dashboard/Break`,
        {
            mode: "set",
            value: element.target.value,
            com: com.value
        })
        .then((data) => {
            element.target.value = data.value;
        })
}