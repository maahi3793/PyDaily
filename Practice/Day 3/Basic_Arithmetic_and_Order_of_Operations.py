# The Server Override - DAY 1 and DAY 2 revision

operator_code_name = '"Alpha"'
server_ID = 14369
server_temperature_baseline = 35.5
is_manual_override_engaged = True

server_temperature_baseline = server_temperature_baseline + 12.0

print(f"Override Initiated by: {operator_code_name}\n\tServer ID Type: {type(server_ID)}\n\tManual Override: {is_manual_override_engaged}\n\tCurrent Temp: {server_temperature_baseline}C")


# Assignment from PyDaily - The Logistics Calculator

total_eggs = 77
carton_capacity = 12
full_cartons = total_eggs // carton_capacity

leftover_eggs = total_eggs % carton_capacity

print(f"Daily Logistics Report:\n\tCartons Packed: {full_cartons}\n\tEggs Remaining: {leftover_eggs}")


# Orbital Trajectory - PEMDAS

velocity_a = 5
velocity_b = 3
distance_x = 12
distance_y = 4
gravity_dampener = 2

trajectory_vector = ((velocity_a + velocity_b) * (distance_x - distance_y) // gravity_dampener)

print(f"Calculated Trajectory Vector: {trajectory_vector}")


# The Cryptographic Cipher - Modulo

raw_signal = 98765
encryption_cycle = 13
signal_shift = 4

decrypted_key = (signal_shift + raw_signal) % encryption_cycle

print(f"Decrypting Signal...\n\tFinal Key: {decrypted_key}")


# The Cybernetic Foundry - Final boss 1

total_titanium_plates_arrived = 850
plates_required_per_drone = 12
assembly_time_in_hours = 1.5
power_surge_limit = True

fully_manufactured_drones = total_titanium_plates_arrived // plates_required_per_drone
remaining_plates = total_titanium_plates_arrived % plates_required_per_drone
total_time_required = fully_manufactured_drones * assembly_time_in_hours

efficiency_score = (((total_titanium_plates_arrived + remaining_plates) * plates_required_per_drone) / assembly_time_in_hours)

print(f"DRONE FOUNDRY PRODUCTION DASHBOARD\n\tFully Build Drone Yield: {fully_manufactured_drones}\n\tLeftover Titanium Scrap: {remaining_plates}\n\tTotal Assembly Time (in hours): {total_time_required}\n\tEfficiency Score: [{efficiency_score}]")


# Ledger Audit

trading_balance = 100.50
trading_balance += 25.20
trading_balance -= 0.10
trading_balance *= 1.05

certified_balance = round(trading_balance,2)
print(f"=== SECURE LEDGER AUDIT ===\n\tFinal Certified Balance: ${certified_balance}\n===========================")