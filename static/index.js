var serverUrl="http://127.0.0.1:5000/"
//var serverUrl=""

function onload(){
    $(document).keydown(function(event) {
        if ($("#searchText").is(":focus") && (event.key === 13 || event.key == "Enter")) {
            getStockDetails();
        }
    });
    $("#searchText").val('');
    getDeathData();
    getStartFinishData();
}


function getDeathData(){
    url=serverUrl+"deathData"
    fetch(url, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },
    }).then((response) => response.json().then((data) => {
        if (response.status == 200) {
            
            var xValues = data["level"];
            var yValues = data["deathCount"];
            maxy = Math.max(yValues[0])
            if (maxy < 10 ){
                maxy = maxy*2
            }
            new Chart("deathChart", {
            type: "bar",
            data: {
                labels: xValues,
                datasets: [{
                data: yValues,
                backgroundColor: "#BA3A4B"
                }]
            },
            options: {
                legend: {display: false},
                scales: {
                    yAxes: [{
                        ticks: {
                            stepSize: 1,
                            min: 0, 
                            max: maxy,
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Number of Player'
                        }
                    }],
                    xAxes:[{
                        scaleLabel: {
                            display: true,
                            labelString: 'Level'
                            }
                    }]
                }
            }
            });
        }
    })).catch(function(error) {
        console.log(error)
        $('#deathChart').addClass('hide');
        $('#deathChartError').removeClass('hide');
        $("#deathChartError").text("Network Error: Internal Server Error")
    });
}


function getStartFinishData(){
    url=serverUrl+"startFinishData"
    fetch(url, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },
    }).then((response) => response.json().then((data) => {
        if (response.status == 200) {
            console.log(data)

            var ctx = document.getElementById("startFinishChart").getContext("2d");
            
            var dataset = {
            labels: data["level"],
            datasets: [{
                label: "Start",
                backgroundColor: "#A85055",
                data: data["startCount"]
            }, {
                label: "Finish",
                backgroundColor: "#932B4B",
                data: data["finishCount"]
            }]
            };

            var myBarChart = new Chart(ctx, {
            type: 'bar',
            data: dataset,
            options: {
                barValueSpacing: 20,
                scales: {
                yAxes: [{
                    ticks: {
                    min: 0,
                    stepSize: 1,
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Number of Player'
                    }
                }],
                xAxes:[{
                    scaleLabel: {
                        display: true,
                        labelString: 'Level'
                        }
                }]
                }
            }
            });
        }
    })).catch(function(error) {
        $('#startFinishChart').addClass('hide');
        $('#startFinishChartError').removeClass('hide');
        $("#startFinishChartError").text("Network Error: Internal Server Error")
    });
}
