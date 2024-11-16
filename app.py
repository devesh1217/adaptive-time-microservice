from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_green_time(vehicles, base_green_time=30, max_limit_per_side=90, min_green_time=5):
    total_vehicles = sum(vehicles.values())
    
    if total_vehicles == 0:
        return {side: 0 for side in vehicles}
    
    adaptive_max_green_time = base_green_time + (total_vehicles * 0.5)
    adaptive_max_green_time = min(adaptive_max_green_time, max_limit_per_side * len(vehicles))
    
    green_times = {}
    for side, count in vehicles.items():
        proportion_of_traffic = count / total_vehicles
        green_time = proportion_of_traffic * adaptive_max_green_time
        
        if green_time < min_green_time:
            green_time = min_green_time
        elif green_time > max_limit_per_side:
            green_time = max_limit_per_side
        
        green_times[side] = round(green_time, 2)
    
    return green_times

@app.route('/green-time', methods=['POST'])
def get_green_time():
    data = request.get_json()
    vehicles = data.get('vehicles', {})
    base_green_time = data.get('base_green_time', 30)
    max_limit_per_side = data.get('max_limit_per_side', 90)
    min_green_time = data.get('min_green_time', 5)
    
    green_times = calculate_green_time(vehicles, base_green_time, max_limit_per_side, min_green_time)
    
    return jsonify(green_times)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
