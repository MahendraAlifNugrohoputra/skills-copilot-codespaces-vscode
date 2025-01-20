import random
import numpy as np
import matplotlib.pyplot as plt

# Assumed Variables
num_quay_cranes = 5
num_rtgc = 10
num_internal_trucks = 20
num_external_trucks = 50
container_yard_capacity = 1000
working_hours = 24
arrival_rate_ships = 5  # ships per day
arrival_rate_external_trucks = 100  # trucks per day
ship_name = "Sinar Sunda"
container_dwell_time_mean = 3  # days
container_dwell_time_std = 1  # days
operational_delays_mean = 1  # hour
operational_delays_std = 0.5  # hours
initial_num_containers = 500

# Target average productivity values
target_crane_productivity = 20  # containers per hour
target_rtgc_productivity = 13  # containers per hour

# Dynamic Variables
num_containers = initial_num_containers
queue_length_ships = 0
queue_length_trucks = 0
operational_delays = 0
weather_conditions = "Clear"
labor_availability = 100  # percentage

# Productivity Rates (Dynamic)
crane_productivity_rates = [0] * num_quay_cranes  # containers per hour for each crane
rtgc_productivity_rates = [0] * num_rtgc  # containers per hour for each RTGC
truck_turn_time = 1  # hour

# Store productivity rates for visualization
crane_productivity_history = [[] for _ in range(num_quay_cranes)]
rtgc_productivity_history = [[] for _ in range(num_rtgc)]

# Simulation Logic
def simulate_day():
    global num_containers, queue_length_ships, queue_length_trucks
    
    # Simulate ship arrivals
    for _ in range(arrival_rate_ships):
        queue_length_ships += 1
    
    # Simulate external truck arrivals
    for _ in range(arrival_rate_external_trucks):
        queue_length_trucks += 1
    
    # Process ships (Stevedoring)
    daily_containers_handled_by_cranes = [0] * num_quay_cranes
    for i in range(num_quay_cranes):
        if queue_length_ships > 0:
            queue_length_ships -= 1
            # Randomize the number of containers handled by each crane using normal distribution
            containers_handled = max(0, np.random.normal(target_crane_productivity * working_hours, 5 * working_hours))  # mean=target_crane_productivity * working_hours, std=5 * working_hours
            daily_containers_handled_by_cranes[i] = containers_handled
    
    # Update crane productivity rates
    for i in range(num_quay_cranes):
        if daily_containers_handled_by_cranes[i] > 0:
            crane_productivity_rates[i] = daily_containers_handled_by_cranes[i] / working_hours
        else:
            crane_productivity_rates[i] = 0  # Ensure a value is recorded even if no containers are handled
        crane_productivity_history[i].append(crane_productivity_rates[i])
    
    # Process trucks (Cargodoring)
    daily_containers_handled_by_rtgc = [0] * num_rtgc
    for i in range(num_rtgc):
        if queue_length_trucks > 0:
            queue_length_trucks -= 1
            # Randomize the number of containers handled by each RTGC using normal distribution
            containers_handled = max(0, np.random.normal(target_rtgc_productivity * working_hours, 3 * working_hours))  # mean=target_rtgc_productivity * working_hours, std=3 * working_hours
            daily_containers_handled_by_rtgc[i] = containers_handled
    
    # Update RTGC productivity rates
    for i in range(num_rtgc):
        if daily_containers_handled_by_rtgc[i] > 0:
            rtgc_productivity_rates[i] = daily_containers_handled_by_rtgc[i] / working_hours
        else:
            rtgc_productivity_rates[i] = 0  # Ensure a value is recorded even if no containers are handled
        rtgc_productivity_history[i].append(rtgc_productivity_rates[i])

    # Update container dwell time
    dwell_time = max(0, np.random.normal(container_dwell_time_mean, container_dwell_time_std))
    num_containers = max(0, num_containers - (num_containers / dwell_time))

    # Simulate operational delays
    operational_delays = max(0, np.random.normal(operational_delays_mean, operational_delays_std))

# Run simulation for a month
for day in range(30):
    simulate_day()
    print(f"Day {day+1}: Containers in yard: {num_containers}, Ship queue: {queue_length_ships}, Truck queue: {queue_length_trucks}")
    for i in range(num_quay_cranes):
        print(f"Crane {i+1} productivity: {crane_productivity_rates[i]} containers/hour")
    for i in range(num_rtgc):
        print(f"RTGC {i+1} productivity: {rtgc_productivity_rates[i]} containers/hour")

# Visualization
days = list(range(1, 31))

plt.figure(figsize=(14, 7))

# Plot crane productivity rates
for i in range(num_quay_cranes):
    plt.plot(days, crane_productivity_history[i], label=f'Crane {i+1} Productivity')

plt.xlabel('Day')
plt.ylabel('Productivity (containers/hour)')
plt.title(f'Crane Productivity Over Time for Ship: {ship_name}')
plt.legend()
plt.grid(True)
plt.show()

# Plot RTGC productivity rates
plt.figure(figsize=(14, 7))
for i in range(num_rtgc):
    plt.plot(days, rtgc_productivity_history[i], label=f'RTGC {i+1} Productivity')

plt.xlabel('Day')
plt.ylabel('Productivity (containers/hour)')
plt.title(f'RTGC Productivity Over Time for Ship: {ship_name}')
plt.legend()
plt.grid(True)
plt.show()