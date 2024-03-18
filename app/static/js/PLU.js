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

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}


document.getElementById("checkbox_PLU").addEventListener("click", checkbox_PLU);
document.getElementById("PLU_start").addEventListener("click", startPLU);
document.getElementById("PLU_stop").addEventListener("click", stopPLU);
document.getElementById("PLU_meas_stat").addEventListener("click", PLUMeasTyp);
document.getElementById("PLU_meas_grav").addEventListener("click", PLUMeasTyp);
document.getElementById("PLU_meas_vol").addEventListener("click", PLUMeasTyp);


let checkbox = document.getElementById("checkbox_PLU");
let com = document.getElementById("comPLU");
let btnStart = document.getElementById("PLU_start");
let btnStop = document.getElementById("PLU_stop");

let fetchPLU;

function checkbox_PLU() {
    postData(`${window.origin}/Dashboard/PLU`,
        {
            mode: "activate",
            value: checkbox.value,
            com: com.value
        })
        .then((data) => {
            checkbox.value = data.value;
            if (data.value == 0) {
                checkbox.checked = false;
            }
        }
        )
}

function PLUMeasTyp(element) {
    let measButtons = document.getElementById("measurement_buttons");
    for (let button of measButtons.children) {
        button.value = 0;
        button.className = "btn btn-plu-off";
    }
    element.target.value = 0;
    element.target.className = "btn btn-plu-on";
    statMeas();
}

function startPLU() {
    if (checkbox.value == 1) {
        btnStart.innerHTML = "<span class='loader'></span>";
        postData(`${window.origin}/Dashboard/PLU`,
            {
                mode: "start",
                value: btnStart.value,
                com: com.value,
            })
            .then((data) => {
                if (data.value == 1) {
                    document.getElementById("PLU_meas_stat").click();
                    btnStart.className = "btn btn-plu-on";
                    btnStart.innerHTML = "Aktiv";
                    btnStart.value = data.value;
                    fetchPLU = setInterval(statMeas, 1500);
                }
                else {
                    btnStart.className = "btn btn-plu-off";
                    btnStart.innerHTML = "Start";
                    btnStart.value = data.value;
                }
            }
            )
    }
    else {
        alert("Kraftstoffwaage wurde nicht initialisiert!")
    }
}

function stopPLU() {
    clearInterval(fetchPLU);
    if (btnStart.value == 1) {
        btnStop.innerHTML = "<span class='loader'></span>";
        postData(`${window.origin}/Dashboard/PLU`,
            {
                mode: "stop",
                value: btnStop.value,
                com: com.value,
            })
            .then((data) => {
                console.log(data);
                if (data.value == 1) {
                    btnStart.className = "btn btn-plu-off";
                    btnStart.innerHTML = "Start";
                }
                btnStop.className = "btn btn-plu-off";
                btnStop.innerHTML = "Stop";
            }
            )
    }
}

function statMeas() {
    postData(`${window.origin}/Dashboard/fetch/PLU`,
        {
            com: com.value,
            mode: "stat"
        })
        .then((data) => {
            let temp = parseFloat(data["respond_temperature"]).toFixed(2);
            let val = parseFloat(data["respond_mean_value"]).toFixed(3);

            document.getElementById("PLUstat").innerHTML = val;
            document.getElementById("PLUTemp").innerHTML = temp;
        })
}