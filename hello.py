import random
import simpy

# Parameter
RANDOM_SEED = 42
NUM_VEHICLES = 10  # Jumlah kendaraan
PROCESSING_TIME = 5  # Waktu pemrosesan setiap kendaraan (dalam menit)

def vehicle(env, name, terminal):
    """Proses kendaraan di terminal."""
    arrival_time = env.now
    print(f"{name} tiba di terminal pada {arrival_time:.1f} menit.")
    
    with terminal.request() as request:
        yield request  # Menunggu giliran
        wait_time = env.now - arrival_time
        print(f"{name} menunggu selama {wait_time:.1f} menit.")
        
        yield env.timeout(PROCESSING_TIME)  # Proses kendaraan
        print(f"{name} selesai diproses pada {env.now:.1f} menit.")

def setup(env, num_vehicles, terminal):
    """Mengatur kedatangan kendaraan."""
    for i in range(num_vehicles):
        yield env.timeout(random.expovariate(1 / 2))  # Kedatangan kendaraan setiap 2 menit
        env.process(vehicle(env, f'Kendaraan {i+1}', terminal))

# Simulasi
random.seed(RANDOM_SEED)  # Untuk reproducibility
env = simpy.Environment()
terminal = simpy.Resource(env, capacity=1)  # Kapasitas terminal
env.process(setup(env, NUM_VEHICLES, terminal))
env.run()