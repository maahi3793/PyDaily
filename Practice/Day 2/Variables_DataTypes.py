# Day 1 Test

print(f"\"Diagnostics\" \\ Start \n\tErrors: {10 - 10} \n\tStatus: 'Optimal'")


# Day 2 Variables

agent_name = "Maheedhar"
clearance_level = 5
department = "MI-6"

print(f"Alert: Agent {agent_name} from the {department} department has logged in with level {clearance_level} clearance.")


# Boss Health Assignment

boss_health = 100
attack_damage = 35
print(f"Boss Appears with {boss_health} HP")

boss_health = boss_health - attack_damage

print(f"You strike for {attack_damage} damage. The boss now has {boss_health} HP left")


# Inventory 

item_name = "Dragon Scale"
item_quantity = 3
item_rarity = "Epic"

item_quantity = item_quantity + 1

print(f"Inventory Updated:\n\tItem: [{item_rarity}] {item_name}\n\tTotal in Pouch: {item_quantity}")


# RPG Merchant

player_gold = 100
potion_price = 20
potions_bought = 3

total_cost = potion_price * potions_bought

player_gold = player_gold - total_cost

print(f"=== TRANSACTION LOG ===\nPurchased: {potions_bought} Health Potions\nCost: {total_cost}G\nRemaining Balance: {player_gold}G\n=======================")



# The Core Diagnostic

system_name = "Apollo"
active_cores = 8
core_temp = 85.5
is_stable = True


print(f"[{system_name}] Diagnostic\n\tTemp: {core_temp} | Cores: {active_cores}\n\tStability: {is_stable} (Data Type: {type(is_stable)})")


# The Deep Space Transmission

rover_name = "Ananta"
samples_collected = 17
distance_covered_in_kms = 0.85
comms_active = True

samples_collected = samples_collected + 5
distance_covered_in_kms = distance_covered_in_kms + 0.25

print(f"\'{rover_name}\'\n\tLog Stored at: C:\\rover\\logs\\data\n\tTotal Samples Collected Today: {samples_collected}\n\tTotal Distance Covered Today: {distance_covered_in_kms} KMS\n\tCommunication Systems Active: {comms_active} (Data Type: {type(comms_active)})")