document.addEventListener('DOMContentLoaded', () => {
    // Initialize date
    // Check if element exists before updating to avoid errors if partial load
    if (document.getElementById('currentDate')) updateDate();

    // Initial fetch - default to what's selected
    const periodSelect = document.getElementById('periodSelect');
    const initialPeriod = periodSelect ? periodSelect.value : 'today';

    fetchDashboardMetrics(initialPeriod);
    fetchEnergyBalance('day', 7); // Balance chart defaults to last 7 days regardless of top filter
    fetchConsumptionBreakdown();
    fetchEVStatus();
    fetchInsights();

    // Auto-refresh every 30 seconds
    setInterval(() => {
        const currentPeriod = document.getElementById('periodSelect') ? document.getElementById('periodSelect').value : 'today';
        fetchDashboardMetrics(currentPeriod);
        fetchEVStatus();
    }, 30000);

    // Filter listener
    if (periodSelect) {
        periodSelect.addEventListener('change', (e) => {
            const period = e.target.value;
            fetchDashboardMetrics(period);
        });
    }
});

function updateDate() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const el = document.getElementById('currentDate');
    if (el) el.textContent = now.toLocaleDateString('en-US', options);
}

async function fetchDashboardMetrics(period = 'today') {
    try {
        const res = await fetch(`/api/dashboard?period=${period}`);
        const data = await res.json();

        if (data.success) {
            const m = data.metrics;
            // Update textual elements safely
            const setSafe = (id, val) => {
                const el = document.getElementById(id);
                if (el) el.textContent = val;
            };

            setSafe('solarProd', `${m.solar_production.toFixed(1)} kWh`);
            setSafe('totalCons', `${m.total_consumption.toFixed(1)} kWh`);
            setSafe('costSave', `$${m.cost_savings.toFixed(2)}`);
            setSafe('co2Offset', `${m.co2_offset.toFixed(1)} kg`);
        }
    } catch (err) {
        console.error('Error fetching dashboard metrics:', err);
    }
}

let balanceChart = null;

async function fetchEnergyBalance(period = 'day', days = 7) {
    try {
        const url = `/api/energy-balance?period=${period}&days=${days}`;
        const res = await fetch(url);
        const data = await res.json();

        if (data.success) {
            renderBalanceChart(data.data, period);
        }
    } catch (err) {
        console.error('Error fetching energy balance:', err);
    }
}

function renderBalanceChart(data, period) {
    const ctx = document.getElementById('energyBalanceChart').getContext('2d');

    const labels = data.map(item => {
        if (period === 'day') {
            // Format: YYYY-MM-DD -> short day
            const d = new Date(item.period);
            return d.toLocaleDateString('en-US', { weekday: 'short' });
        } else {
            // Hour
            const d = new Date(item.period);
            return d.getHours() + ':00';
        }
    });

    const solar = data.map(item => item.solar_production);
    const consumption = data.map(item => item.consumption);

    if (balanceChart) {
        balanceChart.destroy();
    }

    balanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Usage',
                    data: consumption,
                    backgroundColor: '#60a5fa', // Blue
                    borderRadius: 4,
                    barPercentage: 0.7,
                    categoryPercentage: 0.8
                },
                {
                    label: 'Solar',
                    data: solar,
                    backgroundColor: '#84cc16', // Green
                    borderRadius: 4,
                    barPercentage: 0.7,
                    categoryPercentage: 0.8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false // We built a custom legend in HTML
                },
                tooltip: {
                    backgroundColor: '#1f2937',
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        borderDash: [5, 5]
                    },
                    ticks: {
                        color: '#9ca3af',
                        font: { size: 11 }
                    },
                    border: { display: false }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#9ca3af',
                        font: { size: 11 }
                    },
                    border: { display: false }
                }
            }
        }
    });
}

let donutChart = null;

async function fetchConsumptionBreakdown() {
    try {
        const res = await fetch('/api/consumption-breakdown');
        const data = await res.json();

        if (data.success) {
            renderDonutChart(data.breakdown);
        }
    } catch (err) {
        console.error('Error fetching breakdown:', err);
    }
}

function renderDonutChart(breakdown) {
    const ctx = document.getElementById('consumptionChart').getContext('2d');

    // Capitalize keys for labels
    const labels = Object.keys(breakdown).map(k => {
        // Simple mapping for better labels
        const map = {
            'ev_charging': 'EV Charging',
            'hvac': 'HVAC',
            'appliances': 'Appliances',
            'lighting': 'Lighting'
        };
        return map[k] || k.replace(/_/g, ' ');
    });
    const values = Object.values(breakdown);

    if (donutChart) {
        donutChart.destroy();
    }

    donutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    '#818cf8', // Indigo for EV
                    '#f472b6', // Pink for HVAC
                    '#fbbf24', // Amber for Appliances
                    '#9ca3af'  // Gray for Lighting
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        pointStyle: 'circle',
                        color: '#4b5563',
                        boxWidth: 8,
                        padding: 20,
                        font: { size: 12 }
                    }
                }
            }
        }
    });
}

async function fetchEVStatus() {
    try {
        const res = await fetch('/api/ev-charging');
        const data = await res.json();

        if (data.success) {
            const ev = data.ev_charging;
            const pct = Math.round(data.percentage);

            const batteryLevel = document.getElementById('batteryLevel');
            if (batteryLevel) batteryLevel.style.width = `${pct}%`;

            const batteryText = document.getElementById('batteryText');
            if (batteryText) batteryText.textContent = `${pct}%`;

            const evPower = document.getElementById('evPower');
            if (evPower) evPower.textContent = `${ev.charging_power} kW`;

            const evTime = document.getElementById('evTimeEstimate');
            // Convert hours to nicely formatted string if needed, or just keep rough hours
            const mins = Math.round(ev.time_to_complete * 60);
            if (evTime) evTime.textContent = `Est. completion: ${mins} mins`;

            const evCost = document.getElementById('evCost');
            if (evCost) evCost.textContent = `Session cost: $${ev.cost_estimate.toFixed(2)}`;

            // Toggle Status Badge
            const badge = document.getElementById('evStatusBadge');
            if (badge) {
                if (pct >= 100) {
                    badge.textContent = 'Complete';
                    badge.style.background = '#dcfce7';
                    badge.style.color = '#166534';
                } else {
                    badge.textContent = 'Active';
                    badge.style.background = '#dcfce7'; // Keep green background as per image
                    badge.style.color = '#166534';
                }
            }
        }
    } catch (err) {
        console.error('Error fetching EV status:', err);
    }
}

async function fetchInsights() {
    try {
        const res = await fetch('/api/insights');
        const data = await res.json();

        if (data.success) {
            const container = document.getElementById('insightsList');
            if (!container) return;

            container.innerHTML = '';

            data.insights.forEach(insight => {
                const div = document.createElement('div');
                div.className = `insight-item ${insight.type}`;

                // Determine icon based on insight type or title
                let iconClass = 'fa-regular fa-lightbulb';
                if (insight.type === 'positive') iconClass = 'fa-solid fa-temperature-arrow-down';
                if (insight.type === 'warning') iconClass = 'fa-regular fa-clock';

                div.innerHTML = `
                    <div class="insight-icon"><i class="${iconClass}"></i></div>
                    <div class="insight-content">
                        <h4>${insight.title}</h4>
                        <p>${insight.message}</p>
                    </div>
                `;
                container.appendChild(div);
            });

            if (data.insights.length === 0) {
                container.innerHTML = `
                    <div class="insight-item">
                        <div class="insight-content"><p>No interactions required at the moment.</p></div>
                    </div>`;
            }
        }
    } catch (err) {
        console.error('Error fetching insights:', err);
    }
}
