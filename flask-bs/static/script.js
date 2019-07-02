var charts = {}

function requestData(author_id, side) {
    return $.ajax({
        type: 'GET',
        url: '/author/'.concat(author_id),
        success: (response) => {processData(response, side)} 
    });
}

function processData(response, side) {
    console.info('Got response for side: '.concat(side))
    console.info(response);

    clearSide(side);

    createChart(response.data, side)
}

function getSide(id) {
    var dummy = id.split('-');
    var side = dummy[dummy.length - 1].trim();
    return side;
}

function saveChart(chart, side) {
    if (!(side in charts)) {
        charts[side] = [];
    }

    charts[side].push(chart);
}

function clearSide(side) {
    if(side in charts) {
        for (chart of charts[side]) {
            chart.destroy();
        }
    }
}

function createChart(data, side) {
    var ctx = document.getElementById('chart-cpy-'.concat(side)).getContext('2d');
    var barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data.cite_year_values),
            datasets: [{
                label: 'Cites per year',
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
                        beginAtZero: true
                    }
                }]
            },
            aspectRatio: 1.7
        }
    });

    saveChart(barChart, side)
}

// $(() => {
//     $('button#btn-search').bind('click', ()  => {
//         requestData($('#input-search').val());
//     });
// });

$(() => {
    $('button').click(function(event) {
        // this.append wouldn't work
        // $(this).append(' Clicked');
        
        var side = getSide(event.target.id);
        console.info(side.concat(' button clicked'));
        requestData($('#input-search-'.concat(side)).val(), side);
    });
});