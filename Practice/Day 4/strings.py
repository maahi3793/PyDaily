# The Chrono-Processor

raw_uptime_seconds = 8500
hours = raw_uptime_seconds // 3600
minutes = (raw_uptime_seconds % 3600) // 60
seconds = raw_uptime_seconds % 60

print(f"SERVER UPTIME DIAGNOSTIC:\n\tHours: {hours}\n\tMinutes: {minutes}\n\tSeconds: {seconds}")


# Strings

first_name = "grace"
last_name = "hopper"
department_code = 404
corporate_email = first_name + "." + last_name + str(department_code) + "@" + "cybernetics.com"
ui_line = "-" * 30

print(ui_line)
print(corporate_email)
print(ui_line)


# The Hexadecimal Decoder

raw_log = "X7-FAIL-0094-SYS"


status_code = raw_log[3:7]
error_id = raw_log[8:12]
system_flag = raw_log[-3:]

clean_report = status_code + ": " + error_id + " (" + system_flag + ")"
print(clean_report)


# The Bio-Metric Sanitizer

raw_scan = "   !!auth-granted-user_id:992A-zone:red!!   "
clean_scan = raw_scan.strip().replace("!","")
access_status = clean_scan[5:12]
user_id = clean_scan[21:25]
zone = clean_scan[-3:]
#[GRANTED] - User: 992a Accessing RED Zone
print(f"[{access_status.upper()}] - User: {user_id.lower()} Accessing {zone.upper()} Zone")


# The Network Handshake

ip_address = "192.168.0.15"
masked_address = ip_address.replace(".","*")
last_two_digits = ip_address[-2:]
border = "=" * 25
print(f"{border}\nMASKED IP: {masked_address}\nNODE ID: {last_two_digits}\n{border}")



# The Cryptographic String Master. Assignment 1 (There is a mistake in your question. Teh output you want is OMEGA but the raw intercept just has oMgA)

raw_intercept = "   *!vX-99_oMgA!* "
clean_intercept = raw_intercept.strip().replace("*!","").replace("!*","")

sector_code = clean_intercept[0:2].lower()
threat_level = clean_intercept[3:5]
protocol_name = clean_intercept[6:].upper()

decryption_key = ord(sector_code[0:1])

print(f"[DECRYPTION SUCCESSFUL]\n\tProtocol: {protocol_name}\n\tSector: {sector_code}\n\tThreat Level: {threat_level}\n\tEncryption Key: {decryption_key}")


# The Core Systems Integration

rover_designation = "  curiosity_mk4  "
base_solar_input = 850
battery_voltage = 12.4
comms_line = True

clean_name = rover_designation.strip().capitalize()[0:9]

battery_voltage += (base_solar_input + 45.5) / 3.2

battery_voltage = round(battery_voltage,2)
excess_energy = base_solar_input % 12
border_boot_sequence = "=" * 40


print(f"{border_boot_sequence}\nROVER BOOT SEQUENCE INITIATED...\n{border_boot_sequence}\n\tUnit: {clean_name}\n\tComms Status: {comms_line} (Type: {type(comms_line)})\n\tBattery Voltage: {battery_voltage}V\n\tExcess Energy Routed: {excess_energy} Units")


# The Corrupted Node

raw_node = "   >>sYs_fAiLuRe<<   "
clean_node = raw_node.strip().replace(">>","").replace("<<","").upper()
fault_code = ord(clean_node[0:1])

print(f"[NODE OFFLINE]\n\tStatus: {clean_node}\n\tFault Code: {fault_code}")


# The Quantum DNA Sequencer

raw_dna_scan = "G-C-A-T-C-G-T-A"
pure_sequence = raw_dna_scan[::-2]
first_codon = pure_sequence[0:4]
print(f"=== DNA SEQUENCER ONLINE ===\n\tRaw Scan: {raw_dna_scan}\n\tCorrected Sequence: {pure_sequence}\n\tPrimary Codon: {first_codon}")