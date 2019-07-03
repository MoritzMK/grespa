var charts = {}

// Requests
function requestAuthorData(author_id, doc_year, side) {
    return $.ajax({
        type: 'GET',
        url: '/author/'.concat(author_id),
        data: {year: doc_year},
        success: (response) => {processData(response, side)} 
    });
}

function requestSearchData(search_string) {
    return $.ajax({
        type: 'GET',
        url: '/author/search/'.concat(search_string),
        success: (response) => {processSearchResult(response)} 
    });
}

// Data Processing
function processData(response, side) {
    console.info('Got response for side: '.concat(side));
    console.info(response);

    // clearSide(side);

    createCvyChart(response.data, side);
    createCiteCountChart(response.data, side)
    setImage(response.data.image_url, side);
    setGeneral(response.data, side);

    setMetrics(response.data, side);

    setCardsDisplay(side, false);
}

function processSearchResult(response) {
    console.info('Got response for search.');
    console.info(response);

    // clearSearchResults();

    for (author of response.data) {
        addSearchResult(author);
    }
}

// Clearing
function clearSearchResults() {
    $('#search-result-group').empty();
}

function clearSide(side) {
    if(side in charts) {
        for ([key,chart] of Object.entries(charts[side])) {
            chart.destroy();
        }
    }

    setCardsDisplay(side, true);
}

// Add data to view
function addSearchResult(author){
    var template = $('#search-result-template').html();

    template = template.replace('%image%', author.image_url);
    template = template.replace('%name%', author.name);
    template = template.replace('%org%', author.organization);
    template = template.replace('%desc%', author.description);
    template = template.replace('%id%', author.id);

    $('#search-result-group').append(template);
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


// Some other stuff
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

// Event handling
$('button').click(function(event) {
    if(event.target.id === 'btn-author-search') {
        console.info('Search button clicked');

        clearSearchResults();

        var search_string = $('#input-author-search').val();
        requestSearchData(search_string);
    }
    else {
        var side = getSide(event.target.id);
        console.info(side.concat(' button clicked'));
        clearSide(side);
        var user_id = $('#input-userid-'.concat(side)).val();
        var year = $('#input-docyear-'.concat(side)).val();
        requestAuthorData(user_id, year, side);
    }
});

$(".dropzone").on("dragenter", function(event) {
    event.preventDefault();
    $(event.currentTarget).addClass("bg-success");
}).on("dragover", function(event) {
    event.preventDefault(); 
    if(!$(event.currentTarget).hasClass("bg-success"))
        $(event.currentTarget).addClass("bg-success");
}).on("dragleave", function(event) {
    event.preventDefault();
    $(event.currentTarget).removeClass("bg-success");
}).on("drop", function(event) {
    event.preventDefault();
    $(event.currentTarget).removeClass("bg-success");
    id = event.originalEvent.dataTransfer.getData('id');
    $(event.currentTarget).find('.input-userid').val(id);
    clearSearchResults();
});

$('div').on("dragstart", function(event) {
    // event.preventDefault();
    id = $(event.target).find('.user-id').html();
    event.originalEvent.dataTransfer.setData('id', id);
})