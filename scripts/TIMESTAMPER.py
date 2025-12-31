import socket
import struct
import time
from datetime import datetime, timezone

def get_ntp_time_with_telemetry(server='time.google.com'):
    """Get time from NTP server with detailed telemetry"""
    NTP_PACKET_FORMAT = "!12I"
    NTP_DELTA = 2208988800  # 1970-01-01 00:00:00
    NTP_QUERY = b'\x1b' + 47 * b'\0'
    
    telemetry = {
        'server_hostname': server,
        'server_ip': None,
        'response_time_ms': None,
        'stratum': None,
        'precision': None,
        'root_delay': None,
        'success': False,
        'error': None
    }
    
    try:
        # Resolve server IP
        telemetry['server_ip'] = socket.gethostbyname(server)
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            
            # Measure response time
            start_time = time.time()
            s.sendto(NTP_QUERY, (server, 123))
            msg, address = s.recvfrom(1024)
            end_time = time.time()
            
            telemetry['response_time_ms'] = (end_time - start_time) * 1000
        
        unpacked = struct.unpack(NTP_PACKET_FORMAT, msg[0:struct.calcsize(NTP_PACKET_FORMAT)])
        
        # Extract NTP packet details
        leap_indicator = (msg[0] >> 6) & 0x3
        version = (msg[0] >> 3) & 0x7
        mode = msg[0] & 0x7
        telemetry['stratum'] = msg[1]
        telemetry['precision'] = struct.unpack('!b', bytes([msg[2]]))[0]
        telemetry['root_delay'] = unpacked[1] / 2**16
        
        ntp_time = unpacked[10] + float(unpacked[11]) / 2**32
        epoch_time = ntp_time - NTP_DELTA
        
        telemetry['success'] = True
        telemetry['leap_indicator'] = leap_indicator
        telemetry['version'] = version
        telemetry['mode'] = mode
        
        return epoch_time, telemetry
    except Exception as e:
        telemetry['error'] = str(e)
        print(f"NTP query failed: {e}")
        print("Falling back to system time...")
        return time.time(), telemetry

# Get time from NTP server
ntp_server = 'time.google.com'
epoch_timestamp, telemetry = get_ntp_time_with_telemetry(ntp_server)

# Create datetime object in UTC
dt_utc = datetime.fromtimestamp(epoch_timestamp, tz=timezone.utc)

# Build telemetry section
telemetry_section = f"""=== NTP SERVER TELEMETRY ===
Server Hostname: {telemetry['server_hostname']}
Server IP Address: {telemetry['server_ip'] if telemetry['server_ip'] else 'N/A'}
Query Success: {'Yes' if telemetry['success'] else 'No (using system time)'}
Response Time: {f"{telemetry['response_time_ms']:.2f} ms" if telemetry['response_time_ms'] else 'N/A'}
"""

if telemetry['success']:
    telemetry_section += f"""Stratum Level: {telemetry['stratum']} (distance from reference clock)
Precision: {telemetry['precision']} (log2 seconds)
Root Delay: {telemetry['root_delay']:.6f} seconds
NTP Version: {telemetry.get('version', 'N/A')}
Leap Indicator: {telemetry.get('leap_indicator', 'N/A')}
"""
else:
    telemetry_section += f"Error Details: {telemetry['error']}\n"

# Prepare full timestamp data
timestamp_data = f"""TIMESTAMP ARCHIVE FILE
Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
Query Time: {datetime.now(timezone.utc).isoformat()}

{telemetry_section}
=== EPOCH FORMATS ===
Unix Epoch (seconds): {int(epoch_timestamp)}
Unix Epoch (milliseconds): {int(epoch_timestamp * 1000)}
Unix Epoch (microseconds): {int(epoch_timestamp * 1000000)}
Precise Epoch: {epoch_timestamp:.6f}

=== HUMAN READABLE FORMATS ===
ISO 8601 Format: {dt_utc.isoformat()}
RFC 2822 Format: {dt_utc.strftime('%a, %d %b %Y %H:%M:%S +0000')}
Standard Format: {dt_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}
Long Format: {dt_utc.strftime('%A, %B %d, %Y at %H:%M:%S UTC')}
Compact Format: {dt_utc.strftime('%Y%m%d_%H%M%S')}

=== COMPONENT BREAKDOWN ===
Year: {dt_utc.year}
Month: {dt_utc.month:02d} ({dt_utc.strftime('%B')})
Day: {dt_utc.day:02d} ({dt_utc.strftime('%A')})
Hour: {dt_utc.hour:02d}
Minute: {dt_utc.minute:02d}
Second: {dt_utc.second:02d}
Microsecond: {dt_utc.microsecond}
"""

# Write to file
filename = 'TIMESTAMP.txt'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(timestamp_data)

print(f"✓ SUCCESS: Timestamp file written!")
print(f"✓ File: {filename}")
print(f"✓ Location: Current working directory")
print(f"\n--- Telemetry Summary ---")
print(f"Server: {telemetry['server_hostname']} ({telemetry['server_ip']})")
print(f"Response Time: {telemetry['response_time_ms']:.2f} ms" if telemetry['response_time_ms'] else "N/A")
print(f"Stratum: {telemetry['stratum']}" if telemetry.get('stratum') else "N/A")
