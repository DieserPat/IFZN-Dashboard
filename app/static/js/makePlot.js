"use strict";
let grey = '#555';
let bg = '#212121';
let green = '#00f962';
let blue = '#0F6BE9';
let orange = '#F46105';
const maxLength = 250;

let x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25];
let n = [0, 3000, 3000, 1446, 1460, 1448, 1456, 1447, 1450, 1447, 1756, 1746, 1741, 1740, 1755, 1251, 1245, 1258, 1244, 1242, 1253, 1252, 1248, 1240, 1240];
let M = [0, 0, 300, 300, 66, 69, 67, 67, 66, 66, 67, 100, 102, 101, 101, 101, 18, 18, 19, 17, 21, 21, 18, 18, 18, 18];
let a = [100, 100, 36, 36, 36, 35, 35, 36, 35, 35, 35, 53, 54, 55, 54, 54, 16, 14, 15, 14, 16, 14, 15, 16, 15, 14];

var trace1 = {
    x: x,
    y: n,
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
    x: x,
    y: M,
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
    x: x,
    y: a,
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

Plotly.newPlot('dashPlot', data, layout);
