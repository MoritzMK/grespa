var charts = {}

function requestData(author_id, doc_year, side) {
    return $.ajax({
        type: 'GET',
        url: '/author/'.concat(author_id),
        data: {year: doc_year},
        success: (response) => {processData(response, side)} 
    });
}

function processData(response, side) {
    console.info('Got response for side: '.concat(side))
    console.info(response);

    clearSide(side);

    createCvyChart(response.data, side);
    createCiteCountChart(response.data, side)
    setImage(response.data.image_url, side);
    setGeneral(response.data, side);

    setMetrics(response.data, side);


    setCardsDisplay(side, false);
}

function getSide(id) {
    var dummy = id.split('-');
    var side = dummy[dummy.length - 1].trim();
    return side;
}

function saveChart(chart, name, side) {
    if (!(side in charts)) {
        charts[side] = {};
    }

    charts[side][name] = chart;
}

function clearSide(side) {
    if(side in charts) {
        for ([key,chart] of Object.entries(charts[side])) {
            chart.destroy();
        }
    }

    // document.getElementById('avatar-'.concat(side)).style.display = 'none';

    setCardsDisplay(side, true);
}

function setCardsDisplay(side, hide) {
    var cards = document.getElementById('col-'.concat(side)).getElementsByClassName('card-hide');

    for (card of cards) {
        if(hide){
            card.style.display = 'none';
        }
        else{
            card.style.display = 'flex';
        }
    }
}

function createCvyChart(data, side) {
    var ctx = document.getElementById('chart-cpy-'.concat(side)).getContext('2d');
    var barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data.cite_year_values),
            datasets: [{
                data: Object.values(data.cite_year_values),
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                    }
                }],
                xAxes: [{
                    gridLines: {
                        color: "rgba(0, 0, 0, 0)",
                    }
                }],
            },
            aspectRatio: 1.7,
            responsive: true,
            legend: {
                display: false,
            },
        }
    });

    saveChart(barChart, 'cvy', side);
}

function createCiteCountChart(data, side) {
    var ctx = document.getElementById('chart-citecount-'.concat(side)).getContext('2d');
    var barChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: ['Cited'],
            datasets: [{
                data: [data.cited],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    gridLines: {
                        color: "rgba(0, 0, 0, 0)",
                    },
                    ticks: {
                        beginAtZero: true,
                        min:  0,
                    }
                }],
            },
            // aspectRatio: 1,
            responsive: true,
            legend: {
                display: false,
            },
        }
    });

    saveChart(barChart, 'citecount', side);

    //equalizeChartAxis();
}

function equalizeChartAxis(){
    var max = 0;
    for ([key, side] of Object.entries(charts)) {
        chart = side['citecount'];
        if (chart === undefined){
            continue;
        }
        max = Math.max([max, chart.options.scales.xAxes[0].ticks.max]);
    }
    
    for ([key, side] of Object.entries(charts)) {
        chart = side['citecount'];
        if (chart === undefined){
            continue;
        }
        chart.options.scales.xAxes[0].ticks.max = max;
        chart.update();
        console.info('Updated chart.')
    }
}

function setImage(link, side) {
    var image = document.getElementById('avatar-'.concat(side));
    image.src = link;
    image.style.display = 'inline-block';
}

function setGeneral(data, side) {
    document.getElementById('lbl-name-'.concat(side)).innerHTML = data.name;
    document.getElementById('lbl-description-'.concat(side)).innerHTML = data.description;
    document.getElementById('lbl-fos-'.concat(side)).innerHTML = data.fields_of_study;
}

function setMetrics(data, side) {
    document.getElementById('lbl-cited-'.concat(side)).innerHTML = data.cited;
    document.getElementById('lbl-hindex-'.concat(side)).innerHTML = data.hindex;

}

$(() => {
    $('button').click(function(event) {
        // this.append wouldn't work
        // $(this).append(' Clicked');
        
        var side = getSide(event.target.id);
        console.info(side.concat(' button clicked'));
        var user_id = $('#input-userid-'.concat(side)).val();
        var year = $('#input-docyear-'.concat(side)).val();
        requestData(user_id, year, side);
    });
});