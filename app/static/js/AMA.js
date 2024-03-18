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

document.getElementById("checkbox_AMA").addEventListener("click", checkbox_AMA);



// function updateSerBreak() {
//     let com = document.getElementById("comBreak");
//     console.log(com.value);
// }

function checkbox_AMA() {
    let checkbox = document.getElementById("checkbox_AMA");
    if (checkbox.value == 0) {
        checkbox.value = 1;
    } else {
        checkbox.value = 0;
    }
}