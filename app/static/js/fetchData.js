document.getElementById("MeasurmentOnOff").addEventListener("click", startStopMeasurement);
document.getElementById("ButtonOnline").addEventListener("click", goOnline);

let gaugeSpeed = document.getElementById("gaugeSpeed").contentDocument;
let gaugeTorque = document.getElementById("gaugeTorque").contentDocument;

let cpuram;
let fetchInterval;
let sliderValues = new Object();
let timeInterval = 200;
let alphaMax = 260;
let nMax = 3000;
let MMax = 300;
let disPerChar = 32.02;
let breakData = {
    nEng: 0,
    mEng: 0,
    TBreak: 0
};

const grey = '#555';
const bg = '#212121';
const green = '#00f962';
const blue = '#0F6BE9';
const orange = '#F46105';
const maxLength = 1000 / timeInterval * 25;
let startPlot = 0;
let count = 0;
let plotData = {
    timestamp: [],
    nEng: [],
    mEng: [],
    throttle: []
}
updatePlot();

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

function goOnline() {
    let buttonOnline = document.getElementById("ButtonOnline");
    let measurementButton = document.getElementById("MeasurmentOnOff");
    if (buttonOnline.value == 0) {
        buttonOnline.value = 1;
        buttonOnline.className = "btn btn-meas-on";
        buttonOnline.innerHTML = "Go Offline";
        startPlot = 0;
        for (let member in plotData) {
            let pdLen = plotData[member].length;
            x = plotData[member];
            plotData[member].length = 0;
            plotData[member] = [x[pdLen]];
        }
        updatePlot();
        fetchInterval = setInterval(fetchData, timeInterval);
        // cpuram = setInterval(fetchCPURAM, 1000);
    } else if (buttonOnline.value == 1) {
        if (measurementButton.value == 0) {
            buttonOnline.value = 0;
            buttonOnline.className = "btn btn-meas-off";
            buttonOnline.innerHTML = "Go Online";
            clearInterval(fetchInterval);
            // clearInterval(cpuram);
            hardwareState();
        }
        else {
            alert("Messung wird aufgezeichnet.\nOffline gehen im Moment nicht möglich!")
        }
    }
}

function fetchCPURAM() {
    postData(`${window.origin}/Dashboard/CPU`, {})
        .then((data) => {
            console.log(data)
        })
}

function hardwareState() {
    function setClass(fields) {
        if (fields.length > 0) {
            for (let valueField of fields) {
                if (sliderSwitch.value == 1 && online == 1) {
                    valueField.setAttribute("style", "color: white");
                }
                else {
                    valueField.setAttribute("style", "color: var(--gh-grey)");
                }
            }
        }
    }
    online = document.getElementById("ButtonOnline").value;
    let listSlider = document.getElementsByClassName("slider round");
    for (let slider of listSlider) {
        sliderSwitch = slider.previousElementSibling;
        sliderValues[sliderSwitch.id] = sliderSwitch.value;
        parent = slider.parentElement;
        while (parent.className != "row") {
            parent = parent.parentElement;
        }
        container = parent.parentElement;
        let fields = container.getElementsByClassName("wsb-2");
        setClass(fields);
        let AMAFields = container.getElementsByClassName("val-ama");
        setClass(AMAFields);
    }
}

function fetchData() {
    let update = false;
    hardwareState();
    for (let [key, value] of Object.entries(sliderValues)) {
        if (value == 1) {
            if (key == "checkbox_break" || key == "checkbox_throttle") {
                window[`fetch_${key}`]();
                update = true;
            }
        }
    }
    if (update) {
        ++count;
        updatePlotValues("timestamp", count * timeInterval / 1000);
        for (let val in plotData) {
            if (plotData[val].length < plotData.timestamp.length) {
                plotData[val].push(null);
            }
            if (plotData[val].length > maxLength) {
                plotData[val].shift();
            }
        }
        updatePlot();
    }
}

function fetch_checkbox_break() {
    function updateGauge(gaugeName, name, val, maxVal) {
        let gauge = document.getElementById(gaugeName).contentDocument;
        let needle = gauge.getElementById(`${name}needle`);
        let number = gauge.getElementById(`${name}number`);
        let x = needle.lastElementChild.getAttribute("cx");
        let y = needle.lastElementChild.getAttribute("cy");
        val = parseInt(val);
        let alpha = val / maxVal * alphaMax;
        needle.setAttribute("transform", `rotate(${alpha}, ${x}, ${y})`);
        let valLenght = val.toString().length
        transformX = 300 - (disPerChar * valLenght);
        number.innerHTML = val;
        let xy = number.getAttribute("transform");
        let transformY = parseFloat(xy.substring(xy.lastIndexOf(" ") + 1, xy.lastIndexOf(")")));
        number.setAttribute("transform", `translate(${transformX} ${transformY})`);
    }
    let com = document.getElementById("comBreak").value;
    let setpoint = document.getElementById("nEngSetpoint");
    if (setpoint.value.length == 0) {
        setpoint.value = parseInt(setpoint.placeholder);
    }
    postData(`${window.origin}/Dashboard/fetch/Break`,
        {
            com: com,
            setpoint: setpoint.value,
        })
        .then((data) => {
            console.log(data);
            if (data.flag == 1) {
                breakData = {
                    nEng: parseInt(data.nEng),
                    mEng: parseInt(data.mEng),
                    TBreak: parseInt(data.TBreak)
                }
            }
            console.log(breakData);
                document.getElementById("nEng").innerHTML = breakData.nEng;
                document.getElementById("mEng").innerHTML = breakData.mEng;
                document.getElementById("TBreak").innerHTML = breakData.TBreak;
                updatePlotValues("nEng", breakData.nEng);
                updatePlotValues("mEng", breakData.mEng);
                console.log(data.ErrorList);
                // for (let [key, value] of Object.entries(data)) {
                //     if (key != "flag") {
                //     document.getElementById(key).innerHTML = parseInt(value);
                //     if (key in plotData) {
                //         updatePlotValues("nEng", parseInt(data.nEng));
                //     }
                // }
                // }
                updateGauge("gaugeSpeed", "speed", breakData.nEng, nMax);
                updateGauge("gaugeTorque", "torque", breakData.mEng, MMax);
        })
}

function fetch_checkbox_throttle() {
    let ip = document.getElementById("IPThrottle").value;
    let port = document.getElementById("PortThrottle").value;
    postData(`${window.origin}/Dashboard/fetch/Throttle`,
        {
            ip: ip,
            port, port
        })
        .then((data) => {
            let pos = parseFloat(data["throttlePos"]).toFixed(1);
            document.getElementById("throttlePos").innerHTML = pos;
            updatePlotValues("throttle", pos);
        })
}

function updatePlotValues(key, value) {
    plotData[key].push(value);
}

function startStopMeasurement() {
    let buttonMeasurement = document.getElementById("MeasurmentOnOff");
    let buttonOnline = document.getElementById("ButtonOnline");
    if (buttonOnline.value == 1) {
        if (buttonMeasurement.value == 0) {
            buttonMeasurement.value = 1;
            buttonMeasurement.className = "btn btn-meas-on";
            buttonMeasurement.setAttribute("style", "background-color: var(--gh-candy)");
            buttonMeasurement.innerHTML = "Messung läuft";
            let inputFreq = document.getElementById("measurementFreq");
            let inputDuration = document.getElementById("measurementDur");
            let measFreq = inputFreq.value.length > 0 ? parseInt(inputFreq.value) : parseInt(inputFreq.placeholder);
            let measDuration = inputDuration.value.length > 0 ? parseInt(inputDuration.value) : parseInt(inputDuration.placeholder);
            inputDuration.value = measDuration;
            inputFreq.value = measFreq;
            let interval = 1 / measFreq * 1000;
            let start = Date.now();
            let timestamp = Date.now();
            measurementInterval(interval, measDuration, timestamp, start);
        }
    }
}

function measurementInterval(interval, measDuration, timestamp, start) {
    let runningTime = document.getElementById("measurementTime");
    let buttonMeasurement = document.getElementById("MeasurmentOnOff");
    setInterval(function () {
        if (timestamp <= (start + (measDuration * 1000))) {
            runningTime.setAttribute("style", "color: white; border: 2px solid; border-color: var(--gh-candy);");
            runningTime.innerHTML = ((timestamp - start) / 1000).toFixed(1);
            timestamp = Date.now();
        } else {
            runningTime.innerHTML = (measDuration).toFixed(1);
            buttonMeasurement.value = 0;
            buttonMeasurement.className = "btn btn-meas-off";
            buttonMeasurement.setAttribute("style", "background-color: var(--gh-grey)");
            buttonMeasurement.innerHTML = "Start Messung";
            runningTime.setAttribute("style", "color: var(--gh-grey)");
            clearInterval(this);
        }
    }, interval);
}

function updatePlot() {
    var trace1 = {
        x: plotData["timestamp"],
        y: plotData["nEng"],
        mode: 'lines',
        name: 'Drehzahl',
        line: {
            dash: 'solid',
            width: 4,
            color: orange
        },
        yaxis: 'y1'
    };

    var trace2 = {
        x: plotData["timestamp"],
        y: plotData["mEng"],
        mode: 'lines',
        name: 'Drehmoment',
        line: {
            dash: 'solid',
            width: 4,
            color: blue
        },
        yaxis: 'y2'
    };

    var trace3 = {
        x: plotData["timestamp"],
        y: plotData["throttle"],
        mode: 'lines',
        name: 'Fahrpedal',
        line: {
            dash: 'solid',
            width: 4,
            color: green
        },
        yaxis: 'y3'
    };


    var data = [trace1, trace2, trace3];

    var layout = {
        margin: {
            t: 25,
        },
        height: 550,
        xaxis: {
            title: 'Zeit [s]',
            titlefont: { color: 'white' },
            domain: [0.17, 1],
            autorange: true,
            linecolor: grey,
            linewidth: 2,
            gridcolor: grey,
            gridwidth: 2,
            tickfont: {
                color: 'white'
            }
        },
        yaxis: {
            title: 'Drehzahl [1/min]',
            titlefont: { color: orange },
            tickfont: { color: orange },
            range: [0, 3000],
            autorange: false,
            showline: false,
            gridcolor: grey,
            gridwidth: 2,
            anchor: 'free',
            position: 0.15,
            margin: { l: 5 }
        },
        yaxis2: {
            title: 'Drehmoment [Nm]',
            titlefont: { color: blue },
            tickfont: { color: blue },
            range: [0, 300],
            anchor: 'free',
            overlaying: 'y',
            side: 'left',
            position: 0.075,
            showgrid: false
        },
        yaxis3: {
            title: 'Fahrpedalsteller [%]',
            titlefont: { color: green },
            tickfont: { color: green },
            range: [0, 100],
            anchor: 'free',
            overlaying: 'y',
            side: 'left',
            position: 0,
            showgrid: false
        },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        showlegend: false
    };

    Plotly.newPlot('dashPlot', data, layout, { displaylogo: false });
}

//  {responsive: true});