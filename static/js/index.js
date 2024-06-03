function loadJson(selector) {
    return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

window.onload = function () {
    var jsonData = loadJson('#data');
  
    var data = jsonData.map((item) => item.value);
    //var labels = jsonData.map((item) => item.date);
  
    console.log(data);
    //console.log(labels);
}