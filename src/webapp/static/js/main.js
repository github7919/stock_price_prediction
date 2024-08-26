document.addEventListener('DOMContentLoaded', function() {
    const predictionForm = document.getElementById('prediction-form');
    const analysisForm = document.getElementById('analysis-form');

    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePredictionSubmit);
    }

    if (analysisForm) {
        analysisForm.addEventListener('submit', handleAnalysisSubmit);
    }
});

async function handlePredictionSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const response = await fetch('/predict', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    displayPredictionResults(data);
}

async function handleAnalysisSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const response = await fetch('/analysis', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    displayAnalysisResults(data);
}

function displayPredictionResults(data) {
    const resultsDiv = document.getElementById('prediction-results');
    resultsDiv.style.display = 'block';

    // Create and update the chart
    const ctx = document.getElementById('prediction-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Predicted Price',
                data: data.predictions,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Populate the table
    const tableBody = document.getElementById('prediction-table-body');
    tableBody.innerHTML = '';
    for (let i = 0; i < data.dates.length; i++) {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = data.dates[i];
        row.insertCell(1).textContent = data.predictions[i].toFixed(2);
    }
}

function displayAnalysisResults(data) {
    const resultsDiv = document.getElementById('analysis-results');
    resultsDiv.style.display = 'block';

    // Create and update the chart
    const ctx = document.getElementById('analysis-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Closing Price',
                data: data.closing_prices,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Populate summary statistics
    const summaryStats = document.getElementById('summary-stats');
    summaryStats.innerHTML = `
        <tr><td>Mean</td><td>${data.summary.mean.toFixed(2)}</td></tr>
        <tr><td>Median</td><td>${data.summary.median.toFixed(2)}</td></tr>
        <tr><td>Standard Deviation</td><td>${data.summary.std.toFixed(2)}</td></tr>
        <tr><td>Min</td><td>${data.summary.min.toFixed(2)}</td></tr>
        <tr><td>Max</td><td>${data.summary.max.toFixed(2)}</td></tr>
    `;

    // Populate technical indicators
    const technicalIndicators = document.getElementById('technical-indicators');
    technicalIndicators.innerHTML = `
        <tr><td>SMA (50 days)</td><td>${data.indicators.sma_50.toFixed(2)}</td></tr>
        <tr><td>EMA (20 days)</td><td>${data.indicators.ema_20.toFixed(2)}</td></tr>
        <tr><td>RSI (14 days)</td><td>${data.indicators.rsi_14.toFixed(2)}</td></tr>
        <tr><td>MACD</td><td>${data.indicators.macd.toFixed(2)}</td></tr>
    `;
}
