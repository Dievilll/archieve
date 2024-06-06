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

<script>
            
            function prev() {

                alert("Калибровка начата, ожидайте сообщения...");
                var response = fetch('/prev_page').then(response => response.json()).then(data => {
                    var frames = data.message;
                    var id = data.id;
                    frames.forEach((element) => {

                        const titles = document.getElementById("title_" + (id + 10));
                        const datas = document.getElementById("data_" + (id + 10))
                        titles.id = "title_" + id;
                        datas.id = "data_" + id;
                        titles.innerText = element[0];
                        datas.innerText = element[1];

                
                    });
                });
            }

            function next() {
                alert("Калибровка начата, ожидайте сообщения...");
                var response = fetch('/next_page').then(response => response.json()).then(data => {
                    var frames = data.message;
                    var id = data.id;
                    for(var i = id-10; i <= id; i++){
                        
                    }
                    frames.forEach((element) => {

                        const titles = document.getElementById("title_" + (id - 10));
                        const datas = document.getElementById("data_" + (id - 10))
                        titles.id = "title_" + id;
                        datas.id = "data_" + id;
                        titles.innerText = element[0];
                        datas.innerText = element[1];

                
                    });
                    alert("Калибровка начата, ожидайте сообщения...");
                });
            }

        </script>