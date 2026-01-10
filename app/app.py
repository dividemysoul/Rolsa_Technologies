"""
Energy Dashboard API
This is the entry point that exposes all our logic via HTTP endpoints
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime, timedelta

# Import our services and models
from .services.data_generator import EnergyDataGenerator
from .services.calculator import EnergyCalculator
from . import config

# Initialise Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to access this API

# Initialize our services
data_generator = EnergyDataGenerator()
calculator = EnergyCalculator()

# === GLOBAL DATA STORE ===
# In a real app, this would be a database
# For learning, we'll store in memory
historical_readings = []

def initialize_data():
    """Generate initial historical data on startup"""
    global historical_readings
    print("🔄 Generating historical data...")
    historical_readings = data_generator.generate_historical_data(
        days=config.HISTORICAL_DAYS
    )
    print(f"✅ Generated {len(historical_readings)} readings")

# Generate data when the app starts
initialize_data()


# ============================================================================
# API ENDPOINTS - This is how the frontend talks to our backend
# ============================================================================

@app.route('/')
def index():
    """Serve the landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard application"""
    return render_template('dashboard.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint - is the API alive?
    
    Test with: http://localhost:5000/api/health
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Energy Dashboard API is running! ⚡'
    })


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_metrics():
    """
    Get current dashboard metrics
    
    Returns the main metrics for the dashboard cards:
    - Total Consumption
    - Solar Production  
    - Cost Savings
    - CO2 Offset
    
    Test with: http://localhost:5000/api/dashboard
    
    Query Parameters:
        period: 'today', 'week', 'month', 'all' (default: 'today')
    """
    # Get the time period from query parameters
    period = request.args.get('period', 'today')
    
    # Filter readings based on period
    now = datetime.now()
    if period == 'today':
        # Get today's readings
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        filtered_readings = [
            r for r in historical_readings 
            if r.timestamp >= start_time
        ]
    elif period == 'week':
        start_time = now - timedelta(days=7)
        filtered_readings = [
            r for r in historical_readings 
            if r.timestamp >= start_time
        ]
    elif period == 'month':
        start_time = now - timedelta(days=30)
        filtered_readings = [
            r for r in historical_readings 
            if r.timestamp >= start_time
        ]
    else:  # 'all'
        filtered_readings = historical_readings
    
    # Add current reading
    current_reading = data_generator.generate_current_reading()
    filtered_readings.append(current_reading)
    
    # Calculate metrics
    metrics = calculator.calculate_dashboard_metrics(filtered_readings)
    
    return jsonify({
        'success': True,
        'period': period,
        'metrics': metrics.to_dict(),
        'readings_count': len(filtered_readings)
    })


@app.route('/api/energy-balance', methods=['GET'])
def get_energy_balance():
    """
    Get energy balance data for charts
    
    Returns aggregated data for the Energy Balance bar chart
    
    Test with: http://localhost:5000/api/energy-balance?period=day&days=7
    
    Query Parameters:
        period: 'hour', 'day', 'week' (default: 'day')
        days: number of days to include (default: 7)
    """
    period = request.args.get('period', 'day')
    days = int(request.args.get('days', 7))
    
    # Get readings for the specified time range
    now = datetime.now()
    start_time = now - timedelta(days=days)
    
    filtered_readings = [
        r for r in historical_readings 
        if r.timestamp >= start_time
    ]
    
    # Aggregate by period
    aggregated_data = calculator.aggregate_by_period(filtered_readings, period)
    
    return jsonify({
        'success': True,
        'period': period,
        'days': days,
        'data': aggregated_data
    })


@app.route('/api/consumption-breakdown', methods=['GET'])
def get_consumption_breakdown():
    """
    Get consumption breakdown by category
    
    Returns percentage breakdown for the donut chart
    
    Test with: http://localhost:5000/api/consumption-breakdown
    """
    breakdown = calculator.calculate_consumption_breakdown()
    
    return jsonify({
        'success': True,
        'breakdown': breakdown.to_dict()
    })


@app.route('/api/ev-charging', methods=['GET'])
def get_ev_charging_status():
    """
    Get EV charging status
    
    Returns current EV charging metrics
    
    Test with: http://localhost:5000/api/ev-charging
    """
    ev_status = calculator.calculate_ev_charging_status()
    
    return jsonify({
        'success': True,
        'ev_charging': ev_status.to_dict(),
        'percentage': ev_status.get_percentage()
    })


@app.route('/api/current-reading', methods=['GET'])
def get_current_reading():
    """
    Get the current real-time energy reading
    
    Test with: http://localhost:5000/api/current-reading
    """
    reading = data_generator.generate_current_reading()
    
    return jsonify({
        'success': True,
        'reading': reading.to_dict()
    })


@app.route('/api/insights', methods=['GET'])
def get_energy_insights():
    """
    Get energy insights and recommendations
    
    This analyses patterns and provides smart suggestions
    
    Test with: http://localhost:5000/api/insights
    """
    # Get today's readings
    now = datetime.now()
    start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_readings = [
        r for r in historical_readings 
        if r.timestamp >= start_time
    ]
    
    # Calculate some insights
    if today_readings:
        avg_solar = sum(r.solar_production for r in today_readings) / len(today_readings)
        avg_consumption = sum(r.consumption for r in today_readings) / len(today_readings)
        
        # Generate insights based on data
        insights = []
        
        if avg_solar > avg_consumption:
            insights.append({
                'type': 'positive',
                'title': 'Optimised Usage',
                'message': f'Your solar panels are generating more than you consume! Average excess: {(avg_solar - avg_consumption):.2f} kW'
            })
        
        if avg_consumption > config.PEAK_CONSUMPTION * 0.8:
            insights.append({
                'type': 'warning',
                'title': 'High Usage',
                'message': 'Your consumption is approaching peak capacity. Consider scheduling high-power tasks during solar peak hours.'
            })
    else:
        insights = [
            {
                'type': 'info',
                'title': 'No Data',
                'message': 'Not enough data to generate insights yet.'
            }
        ]
    
    return jsonify({
        'success': True,
        'insights': insights
    })


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested API endpoint does not exist.'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': str(error)
    }), 500


# ============================================================================
# MAIN - Run the application
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🌞 ENERGY DASHBOARD API 🌞")
    print("=" * 60)
    print("\n📡 API Endpoints:")
    print("  - GET /api/health")
    print("  - GET /api/dashboard?period=today")
    print("  - GET /api/energy-balance?period=day&days=7")
    print("  - GET /api/consumption-breakdown")
    print("  - GET /api/ev-charging")
    print("  - GET /api/current-reading")
    print("  - GET /api/insights")
    print("\n🚀 Starting server on http://localhost:5000")
    print("=" * 60)
    print()
    
    # Run the Flask development server
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=5000,
        debug=True  # Enable debug mode for development
    )
