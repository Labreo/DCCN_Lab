"""
Experiment 10: FLSM Subnetting and Static Routing Topology Generator
Designs 8 equal subnets (/27) across 4 Routers and 4 LANs with static routing.
Generates Cisco IOS configs and a clean topology diagram.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_configs():
    os.makedirs("/Users/sanjaywaradkar/DCCN_Lab/exp10", exist_ok=True)
    
    # R1 Config
    r1_cfg = """! Cisco Router R1 Configuration (FLSM 192.168.10.0/27)
enable
configure terminal
hostname R1

! LAN Interface (Subnet 1: 192.168.10.0/27)
interface GigabitEthernet0/0/0
 ip address 192.168.10.1 255.255.255.224
 description LAN-1 (HQ)
 no shutdown
exit

! WAN Interface to R2 (Subnet 5: 192.168.10.128/27)
interface GigabitEthernet0/0/1
 ip address 192.168.10.129 255.255.255.224
 description WAN-Link-R1-to-R2
 no shutdown
exit

! WAN Interface to R4 (Subnet 8: 192.168.10.224/27)
interface GigabitEthernet0/0/2
 ip address 192.168.10.226 255.255.255.224
 description WAN-Link-R1-to-R4
 no shutdown
exit

! Static Routes
! Route to LAN 2 (via R2)
ip route 192.168.10.32 255.255.255.224 192.168.10.130
! Route to LAN 3 (via R2)
ip route 192.168.10.64 255.255.255.224 192.168.10.130
! Route to LAN 4 (via R4)
ip route 192.168.10.96 255.255.255.224 192.168.10.225
! Route to WAN R2-R3 (via R2)
ip route 192.168.10.160 255.255.255.224 192.168.10.130
! Route to WAN R3-R4 (via R4)
ip route 192.168.10.192 255.255.255.224 192.168.10.225

end
write memory
"""

    # R2 Config
    r2_cfg = """! Cisco Router R2 Configuration (FLSM 192.168.10.0/27)
enable
configure terminal
hostname R2

! LAN Interface (Subnet 2: 192.168.10.32/27)
interface GigabitEthernet0/0/0
 ip address 192.168.10.33 255.255.255.224
 description LAN-2 (Branch-North)
 no shutdown
exit

! WAN Interface to R1 (Subnet 5: 192.168.10.128/27)
interface GigabitEthernet0/0/1
 ip address 192.168.10.130 255.255.255.224
 description WAN-Link-R2-to-R1
 no shutdown
exit

! WAN Interface to R3 (Subnet 6: 192.168.10.160/27)
interface GigabitEthernet0/0/2
 ip address 192.168.10.161 255.255.255.224
 description WAN-Link-R2-to-R3
 no shutdown
exit

! Static Routes
! Route to LAN 1 (via R1)
ip route 192.168.10.0 255.255.255.224 192.168.10.129
! Route to LAN 3 (via R3)
ip route 192.168.10.64 255.255.255.224 192.168.10.162
! Route to LAN 4 (via R3)
ip route 192.168.10.96 255.255.255.224 192.168.10.162
! Route to WAN R3-R4 (via R3)
ip route 192.168.10.192 255.255.255.224 192.168.10.162
! Route to WAN R4-R1 (via R1)
ip route 192.168.10.224 255.255.255.224 192.168.10.129

end
write memory
"""

    # R3 Config
    r3_cfg = """! Cisco Router R3 Configuration (FLSM 192.168.10.0/27)
enable
configure terminal
hostname R3

! LAN Interface (Subnet 3: 192.168.10.64/27)
interface GigabitEthernet0/0/0
 ip address 192.168.10.65 255.255.255.224
 description LAN-3 (Branch-East)
 no shutdown
exit

! WAN Interface to R2 (Subnet 6: 192.168.10.160/27)
interface GigabitEthernet0/0/1
 ip address 192.168.10.162 255.255.255.224
 description WAN-Link-R3-to-R2
 no shutdown
exit

! WAN Interface to R4 (Subnet 7: 192.168.10.192/27)
interface GigabitEthernet0/0/2
 ip address 192.168.10.193 255.255.255.224
 description WAN-Link-R3-to-R4
 no shutdown
exit

! Static Routes
! Route to LAN 1 (via R2)
ip route 192.168.10.0 255.255.255.224 192.168.10.161
! Route to LAN 2 (via R2)
ip route 192.168.10.32 255.255.255.224 192.168.10.161
! Route to LAN 4 (via R4)
ip route 192.168.10.96 255.255.255.224 192.168.10.194
! Route to WAN R1-R2 (via R2)
ip route 192.168.10.128 255.255.255.224 192.168.10.161
! Route to WAN R4-R1 (via R4)
ip route 192.168.10.224 255.255.255.224 192.168.10.194

end
write memory
"""

    # R4 Config
    r4_cfg = """! Cisco Router R4 Configuration (FLSM 192.168.10.0/27)
enable
configure terminal
hostname R4

! LAN Interface (Subnet 4: 192.168.10.96/27)
interface GigabitEthernet0/0/0
 ip address 192.168.10.97 255.255.255.224
 description LAN-4 (Branch-South)
 no shutdown
exit

! WAN Interface to R3 (Subnet 7: 192.168.10.192/27)
interface GigabitEthernet0/0/1
 ip address 192.168.10.194 255.255.255.224
 description WAN-Link-R4-to-R3
 no shutdown
exit

! WAN Interface to R1 (Subnet 8: 192.168.10.224/27)
interface GigabitEthernet0/0/2
 ip address 192.168.10.225 255.255.255.224
 description WAN-Link-R4-to-R1
 no shutdown
exit

! Static Routes
! Route to LAN 1 (via R1)
ip route 192.168.10.0 255.255.255.224 192.168.10.226
! Route to LAN 2 (via R1)
ip route 192.168.10.32 255.255.255.224 192.168.10.226
! Route to LAN 3 (via R3)
ip route 192.168.10.64 255.255.255.224 192.168.10.193
! Route to WAN R1-R2 (via R1)
ip route 192.168.10.128 255.255.255.224 192.168.10.226
! Route to WAN R2-R3 (via R3)
ip route 192.168.10.160 255.255.255.224 192.168.10.193

end
write memory
"""

    with open("/Users/sanjaywaradkar/DCCN_Lab/exp10/R1_config.txt", "w") as f:
        f.write(r1_cfg)
    with open("/Users/sanjaywaradkar/DCCN_Lab/exp10/R2_config.txt", "w") as f:
        f.write(r2_cfg)
    with open("/Users/sanjaywaradkar/DCCN_Lab/exp10/R3_config.txt", "w") as f:
        f.write(r3_cfg)
    with open("/Users/sanjaywaradkar/DCCN_Lab/exp10/R4_config.txt", "w") as f:
        f.write(r4_cfg)
    print("FLSM configuration files written successfully!")

def draw_topology():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis("off")
    
    # Coordinates
    # R1: (2, 6), R2: (8, 6), R3: (8, 2), R4: (2, 2)
    # LAN1: (0, 7.5), LAN2: (10, 7.5), LAN3: (10, 0.5), LAN4: (0, 0.5)
    
    # Draw WAN links
    ax.plot([2, 8], [6, 6], color="#2563EB", lw=3, zorder=1) # R1-R2
    ax.plot([8, 8], [6, 2], color="#2563EB", lw=3, zorder=1) # R2-R3
    ax.plot([8, 2], [2, 2], color="#2563EB", lw=3, zorder=1) # R3-R4
    ax.plot([2, 2], [2, 6], color="#2563EB", lw=3, zorder=1) # R4-R1
    
    # Draw LAN links
    ax.plot([2, 0.5], [6, 7.5], color="#059669", lw=2.5, ls="--", zorder=1)
    ax.plot([8, 9.5], [6, 7.5], color="#059669", lw=2.5, ls="--", zorder=1)
    ax.plot([8, 9.5], [2, 0.5], color="#059669", lw=2.5, ls="--", zorder=1)
    ax.plot([2, 0.5], [2, 0.5], color="#059669", lw=2.5, ls="--", zorder=1)
    
    # Link labels (WAN subnets)
    ax.text(5, 6.25, "WAN 1 (Subnet 5: 192.168.10.128/27)\n.129 <---> .130", 
            ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#1E3A8A",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#93C5FD"))
    ax.text(8.2, 4, "WAN 2 (Subnet 6: 192.168.10.160/27)\n.161 <---> .162", 
            ha="left", va="center", fontsize=8.5, fontweight="bold", color="#1E3A8A",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#93C5FD"))
    ax.text(5, 1.75, "WAN 3 (Subnet 7: 192.168.10.192/27)\n.194 <---> .193", 
            ha="center", va="top", fontsize=8.5, fontweight="bold", color="#1E3A8A",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#93C5FD"))
    ax.text(1.8, 4, "WAN 4 (Subnet 8: 192.168.10.224/27)\n.226 <---> .225", 
            ha="right", va="center", fontsize=8.5, fontweight="bold", color="#1E3A8A",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#93C5FD"))
    
    # Routers
    routers = [
        ("Router R1", (2, 6), "#1E40AF"),
        ("Router R2", (8, 6), "#1E40AF"),
        ("Router R3", (8, 2), "#1E40AF"),
        ("Router R4", (2, 2), "#1E40AF"),
    ]
    for name, (x, y), col in routers:
        circle = plt.Circle((x, y), 0.55, color=col, ec="#1E293B", lw=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, name, ha="center", va="center", color="white", fontsize=9, fontweight="bold", zorder=4)

    # LAN Hubs / End stations
    lans = [
        ("LAN 1 (Subnet 1: 192.168.10.0/27)\nGW: 192.168.10.1 (Gig0/0)\nPC1: 192.168.10.2", (0.5, 7.5), "#065F46"),
        ("LAN 2 (Subnet 2: 192.168.10.32/27)\nGW: 192.168.10.33 (Gig0/0)\nPC2: 192.168.10.34", (9.5, 7.5), "#065F46"),
        ("LAN 3 (Subnet 3: 192.168.10.64/27)\nGW: 192.168.10.65 (Gig0/0)\nPC3: 192.168.10.66", (9.5, 0.5), "#065F46"),
        ("LAN 4 (Subnet 4: 192.168.10.96/27)\nGW: 192.168.10.97 (Gig0/0)\nPC4: 192.168.10.98", (0.5, 0.5), "#065F46"),
    ]
    for text, (x, y), col in lans:
        box = patches.FancyBboxPatch((x-1.3, y-0.6), 2.6, 1.2, boxstyle="round,pad=0.2",
                                    facecolor="#ECFDF5", edgecolor=col, lw=2, zorder=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha="center", va="center", color="#064E3B", fontsize=8, fontweight="bold", zorder=4)

    plt.title("EXPERIMENT 10: FLSM TOPOLOGY ARCHITECTURE (8 Subnets, 4 Routers, /27 Static Routing)", 
              fontsize=12, fontweight="bold", pad=20, color="#0F172A")
    plt.tight_layout()
    plt.savefig("/Users/sanjaywaradkar/DCCN_Lab/exp10/flsm_topology_diagram.png", dpi=300)
    plt.close()
    print("Topology diagram saved to exp10/flsm_topology_diagram.png")

if __name__ == "__main__":
    generate_configs()
    draw_topology()
