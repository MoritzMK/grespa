var charts = {};
var author_data = {};
var theme = {};

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
    saveData(response.data, side);
    createCvyChart(response.data, side);
    setCitedChartData();
    setImage(response.data.image_url, side);
    setGeneral(response.data, side);

    setMetrics(response.data, side);

    setSpinnerVisibility(side, true);
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
    for ([key,chart] of Object.entries(charts)) {
        if(getSide(key) == side){
            chart.destroy();
        }
    }

    author_data[side] = {};

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

    saveChart(barChart, 'cvy-'.concat(side));
}

function createCiteCountChart(labels) {
    var ctx = document.getElementById('chart-citecount').getContext('2d');
    var barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            // datasets: [{
            //     data: values,
            //     backgroundColor: Object.values(theme),
            //     borderColor: Object.values(theme),
            //     borderWidth: 1
            // }]
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
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        min:  0,
                    }
                }],
            },
            // aspectRatio: 1,
            responsive: true,
            // legend: {
            //     display: false,
            // },
        }
    });

    saveChart(barChart, 'citecount');

    //equalizeChartAxis();
}

function setCitedChartData() {
    var datasets = [];
    var colors = Object.values(theme);
    for ([key,author] of Object.entries(author_data)) {
        dataset = {};
        dataset.label = author.name;
        dataset.data = [];
        dataset.data.push(author.cited);
        color = colors.shift();
        dataset.backgroundColor = color;
        dataset.borderColor = color;
        datasets.push(dataset);
    }

    if(!('citecount' in charts)){
        var labels = ['cited'];
        createCiteCountChart(labels);
    }

    var chart = charts['citecount'];
    chart.data.labels = labels;
    chart.data.datasets = datasets;

    chart.update();
    console.info('Updated chart.')
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
    document.getElementById('lbl-hindex-'.concat(side)).innerHTML = data.h_index;
    document.getElementById('lbl-gindex-'.concat(side)).innerHTML = data.g_index;
    document.getElementById('lbl-euclidean-'.concat(side)).innerHTML = Number.parseFloat(data.euclidean).toFixed(2);

}

// Some other stuff
function getSide(id) {
    var dummy = id.split('-');
    var side = dummy[dummy.length - 1].trim();
    return side;
}

function saveChart(chart, name) {
    charts[name] = chart;
}

function saveData(data, side) {
    author_data[side] = data
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

function setSpinnerVisibility(side, hide) {
    var div = $('#spinner-'.concat(side))[0];
    if (hide) {
      div.style.display = "none";
    } else {
      div.style.display = "block";
    }
  }

function getCurrentColors() {
    var style = getComputedStyle(document.body);
    theme = {};

    theme.primary = style.getPropertyValue('--primary');
    // theme.secondary = style.getPropertyValue('--secondary');
    theme.success = style.getPropertyValue('--success');
    theme.info = style.getPropertyValue('--info');
    theme.warning = style.getPropertyValue('--warning');
    theme.danger = style.getPropertyValue('--danger');
    theme.light = style.getPropertyValue('--light');
    theme.dark = style.getPropertyValue('--dark');
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
        setSpinnerVisibility(side, false);
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

getCurrentColors();
