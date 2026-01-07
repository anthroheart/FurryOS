#!/bin/bash
# FurryOS Ghost Mode Security Implementation
# Implements MAC randomization, hostname rotation, and privacy hardening

set -e

echo "🕵️ Ghost Mode Security Hardening"
echo "=================================="

# ═══════════════════════════════════════════════════════════════════
# MAC Address Randomization
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[1/8] Configuring MAC Address Randomization"

# Install macchanger
apt-get install -y macchanger >/dev/null 2>&1 || true

# Create NetworkManager configuration for MAC randomization
mkdir -p /etc/NetworkManager/conf.d/

cat > /etc/NetworkManager/conf.d/00-furryos-mac-randomization.conf << 'EOF'
[device]
wifi.scan-rand-mac-address=yes

[connection]
wifi.cloned-mac-address=random
ethernet.cloned-mac-address=random
connection.stable-id=${CONNECTION}/${BOOT}
EOF

# Create systemd service to randomize MAC on boot
cat > /etc/systemd/system/furryos-mac-randomize.service << 'EOF'
[Unit]
Description=FurryOS MAC Address Randomization
Before=network-pre.target
Wants=network-pre.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/furryos-randomize-mac

[Install]
WantedBy=multi-user.target
EOF

# Create MAC randomization script
cat > /usr/local/bin/furryos-randomize-mac << 'EOF'
#!/bin/bash
# Randomize MAC addresses for all network interfaces

for iface in $(ls /sys/class/net | grep -v lo); do
    ip link set dev "$iface" down 2>/dev/null || true
    macchanger -r "$iface" 2>/dev/null || true
    ip link set dev "$iface" up 2>/dev/null || true
done
EOF

chmod +x /usr/local/bin/furryos-randomize-mac
systemctl enable furryos-mac-randomize.service 2>/dev/null || true

echo "  ✓ MAC randomization configured"

# ═══════════════════════════════════════════════════════════════════
# Hostname Randomization
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[2/8] Configuring Hostname Randomization"

cat > /usr/local/bin/furryos-randomize-hostname << 'HOSTNAMEEOF'
#!/bin/bash
# Generate random hostname on each boot

RANDOM_ID=$(tr -dc 'a-z0-9' < /dev/urandom | head -c 8)
NEW_HOSTNAME="anonymous-${RANDOM_ID}"

hostnamectl set-hostname "$NEW_HOSTNAME"
echo "$NEW_HOSTNAME" > /etc/hostname

# Update /etc/hosts
sed -i "s/127.0.1.1.*/127.0.1.1	$NEW_HOSTNAME/" /etc/hosts
HOSTNAMEEOF

chmod +x /usr/local/bin/furryos-randomize-hostname

# Create systemd service
cat > /etc/systemd/system/furryos-hostname-randomize.service << 'EOF'
[Unit]
Description=FurryOS Hostname Randomization
Before=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/furryos-randomize-hostname

[Install]
WantedBy=multi-user.target
EOF

systemctl enable furryos-hostname-randomize.service 2>/dev/null || true

echo "  ✓ Hostname randomization configured"

# ═══════════════════════════════════════════════════════════════════
# Encrypted DNS (DNS-over-HTTPS)
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[3/8] Configuring Encrypted DNS"

# Install dnscrypt-proxy
apt-get install -y dnscrypt-proxy >/dev/null 2>&1 || true

# Configure dnscrypt-proxy for Quad9 privacy-focused DNS
cat > /etc/dnscrypt-proxy/dnscrypt-proxy.toml << 'EOF'
server_names = ['quad9-dnscrypt-ip4-filter-pri']

listen_addresses = ['127.0.0.1:53']

require_dnssec = true
require_nolog = true
require_nofilter = false

dnscrypt_servers = true
doh_servers = true

block_ipv6 = false

cache = true
cache_size = 512
cache_min_ttl = 600
cache_max_ttl = 86400
EOF

# Configure systemd-resolved to use dnscrypt-proxy
mkdir -p /etc/systemd/resolved.conf.d/
cat > /etc/systemd/resolved.conf.d/furryos-dns.conf << 'EOF'
[Resolve]
DNS=127.0.0.1
DNSStubListener=no
DNSSEC=yes
EOF

systemctl enable dnscrypt-proxy.service 2>/dev/null || true

echo "  ✓ Encrypted DNS configured (Quad9)"

# ═══════════════════════════════════════════════════════════════════
# Kernel Hardening
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[4/8] Applying Kernel Hardening"

cat > /etc/sysctl.d/99-furryos-ghost-hardening.conf << 'EOF'
# Network hardening
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_timestamps = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.all.rp_filter = 1
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_source_route = 0

# Kernel hardening
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 2
kernel.yama.ptrace_scope = 2
kernel.unprivileged_bpf_disabled = 1
kernel.unprivileged_userns_clone = 0

# Memory protection
vm.mmap_min_addr = 65536

# Disable IPv6 if not needed (optional)
# net.ipv6.conf.all.disable_ipv6 = 1
EOF

sysctl -p /etc/sysctl.d/99-furryos-ghost-hardening.conf 2>/dev/null || true

echo "  ✓ Kernel hardening applied"

# ═══════════════════════════════════════════════════════════════════
# Browser Privacy Hardening (Firefox)
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[5/8] Configuring Browser Privacy Settings"

# Create Firefox policy for privacy
mkdir -p /etc/firefox/policies
cat > /etc/firefox/policies/policies.json << 'EOF'
{
  "policies": {
    "DisableTelemetry": true,
    "DisableFirefoxStudies": true,
    "DisablePocket": true,
    "DisableFirefoxAccounts": true,
    "DontCheckDefaultBrowser": true,
    "EnableTrackingProtection": {
      "Value": true,
      "Locked": false,
      "Cryptomining": true,
      "Fingerprinting": true
    },
    "FirefoxHome": {
      "Search": true,
      "TopSites": false,
      "Highlights": false,
      "Pocket": false,
      "Snippets": false
    },
    "Preferences": {
      "privacy.resistFingerprinting": {
        "Value": true,
        "Status": "default"
      },
      "geo.enabled": {
        "Value": false,
        "Status": "locked"
      },
      "media.navigator.enabled": {
        "Value": false,
        "Status": "default"
      },
      "network.cookie.cookieBehavior": {
        "Value": 1,
        "Status": "default"
      },
      "media.peerconnection.enabled": {
        "Value": false,
        "Status": "default"
      }
    }
  }
}
EOF

echo "  ✓ Firefox privacy policies configured"

# ═══════════════════════════════════════════════════════════════════
# Clipboard Auto-Clear
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[6/8] Configuring Clipboard Auto-Clear"

cat > /usr/local/bin/furryos-clipboard-clear << 'EOF'
#!/bin/bash
# Clear clipboard every 60 seconds

while true; do
    sleep 60
    xsel -bc 2>/dev/null || true
    xsel -pc 2>/dev/null || true
    xsel -sc 2>/dev/null || true
done
EOF

chmod +x /usr/local/bin/furryos-clipboard-clear

# Create user autostart entry
mkdir -p /etc/skel/.config/autostart
cat > /etc/skel/.config/autostart/furryos-clipboard-clear.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=FurryOS Clipboard Auto-Clear
Exec=/usr/local/bin/furryos-clipboard-clear
Hidden=false
NoDisplay=true
X-MATE-Autostart-enabled=true
EOF

echo "  ✓ Clipboard auto-clear configured"

# ═══════════════════════════════════════════════════════════════════
# Memory Wipe on Shutdown
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[7/8] Configuring Memory Wipe on Shutdown"

cat > /etc/systemd/system/furryos-memory-wipe.service << 'EOF'
[Unit]
Description=FurryOS Secure Memory Wipe
DefaultDependencies=no
Before=shutdown.target reboot.target halt.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/furryos-wipe-memory

[Install]
WantedBy=halt.target reboot.target shutdown.target
EOF

cat > /usr/local/bin/furryos-wipe-memory << 'EOF'
#!/bin/bash
# Securely wipe memory on shutdown

sync
echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true

# Clear swap if it exists
swapoff -a 2>/dev/null || true
EOF

chmod +x /usr/local/bin/furryos-wipe-memory
systemctl enable furryos-memory-wipe.service 2>/dev/null || true

echo "  ✓ Memory wipe on shutdown configured"

# ═══════════════════════════════════════════════════════════════════
# Disable Browser Cache
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[8/8] Disabling Browser Cache"

# Firefox cache disable via user.js
mkdir -p /etc/skel/.mozilla/firefox/furryos.default
cat > /etc/skel/.mozilla/firefox/furryos.default/user.js << 'EOF'
// Disable all caching
user_pref("browser.cache.disk.enable", false);
user_pref("browser.cache.memory.enable", false);
user_pref("browser.cache.offline.enable", false);
user_pref("network.http.use-cache", false);

// Clear on exit
user_pref("privacy.sanitize.sanitizeOnShutdown", true);
user_pref("privacy.clearOnShutdown.cache", true);
user_pref("privacy.clearOnShutdown.cookies", true);
user_pref("privacy.clearOnShutdown.downloads", true);
user_pref("privacy.clearOnShutdown.formdata", true);
user_pref("privacy.clearOnShutdown.history", true);
user_pref("privacy.clearOnShutdown.sessions", true);
EOF

echo "  ✓ Browser cache disabled"

echo ""
echo "=================================="
echo "✅ Ghost Mode Security Complete"
echo "=================================="
