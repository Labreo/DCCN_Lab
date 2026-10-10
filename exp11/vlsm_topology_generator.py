"""
Experiment 11: VLSM Subnetting and Dynamic IP Addressing (DHCP) Generator
Designs variable length subnets (/26, /27, /28, /29, /30) with Cisco IOS DHCP servers.
Generates Cisco IOS configs and a clean topology diagram.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_configs():
    os.makedirs("/Users/sanjaywaradkar/DCCN_Lab/exp11", exist_ok=True)
    
    # R1 Config: Hosts LAN 1 (Engineering /26) and Server Farm (/29), acts as DHCP Server for both
    r1_cfg = """! Cisco Router R1 Configuration (VLSM + Dynamic IP Addressing via DHCP)
enable
configure terminal
hostname R1

! DHCP Excluded Addresses (Reserve Default Gateways and Static Servers)
ip dhcp excluded-address 192.168.1.1 192.168.1.10
ip dhcp excluded-address 192.168.1.113 192.168.1.114

! DHCP Pool 1: Engineering Department (60 hosts -> /26)
ip dhcp pool ENG_POOL
 network 192.168.1.0 255.255.255.192
 default-router 192.168.1.1
 dns-server 8.8.8.8
 domain-name eng.gec.ac.in
 lease 1 0 0
exit

! DHCP Pool 2: Server Farm (6 hosts -> /29)
ip dhcp pool SERVER_POOL
 network 192.168.1.112 255.255.255.248
 default-router 192.168.1.113
 dns-server 8.8.8.8
 domain-name servers.gec.ac.in
 lease 7 0 0
exit

! LAN Interfaces
interface GigabitEthernet0/0/0
 ip address 192.168.1.1 255.255.255.192
 description LAN-Engineering (/26)
 no shutdown
exit

interface GigabitEthernet0/0/1
 ip address 192.168.1.113 255.255.255.248
 description LAN-Server-Farm (/29)
 no shutdown
exit

! WAN Interfaces (/30 Point-to-Point)
interface Serial0/1/0
 ip address 192.168.1.121 255.255.255.252
 description WAN-to-R2 (/30)
 clock rate 64000
 no shutdown
exit

interface Serial0/1/1
 ip address 192.168.1.130 255.255.255.252
 description WAN-to-R3 (/30)
 no shutdown
exit

! Routing configuration
router rip
 version 2
 no auto-summary
 network 192.168.1.0
exit

end
write memory
"""

    # R2 Config: Hosts LAN 2 (Sales & Marketing /27)
    r2_cfg = """! Cisco Router R2 Configuration (VLSM + Dynamic IP Addressing via DHCP)
enable
configure terminal
hostname R2

! DHCP Excluded Addresses
ip dhcp excluded-address 192.168.1.65 192.168.1.70

! DHCP Pool: Sales & Marketing Department (28 hosts -> /27)
ip dhcp pool SALES_POOL
 network 192.168.1.64 255.255.255.224
 default-router 192.168.1.65
 dns-server 8.8.8.8
 domain-name sales.gec.ac.in
 lease 1 0 0
exit

! LAN Interface
interface GigabitEthernet0/0/0
 ip address 192.168.1.65 255.255.255.224
 description LAN-Sales (/27)
 no shutdown
exit

! WAN Interfaces (/30 Point-to-Point)
interface Serial0/1/0
 ip address 192.168.1.122 255.255.255.252
 description WAN-to-R1 (/30)
 no shutdown
exit

interface Serial0/1/1
 ip address 192.168.1.125 255.255.255.252
 description WAN-to-R3 (/30)
 clock rate 64000
 no shutdown
exit

! Routing configuration
router rip
 version 2
 no auto-summary
 network 192.168.1.0
exit

end
write memory
"""

    # R3 Config: Hosts LAN 3 (HR & Admin /28)
    r3_cfg = """! Cisco Router R3 Configuration (VLSM + Dynamic IP Addressing via DHCP)
enable
configure terminal
hostname R3

! DHCP Excluded Addresses
ip dhcp excluded-address 192.168.1.97 192.168.1.100

! DHCP Pool: Human Resources & Admin (12 hosts -> /28)
ip dhcp pool HR_POOL
 network 192.168.1.96 255.255.255.240
 default-router 192.168.1.97
 dns-server 8.8.8.8
 domain-name admin.gec.ac.in
 lease 1 0 0
exit

! LAN Interface
interface GigabitEthernet0/0/0
 ip address 192.168.1.97 255.255.255.240
 description LAN-HR-Admin (/28)
 no shutdown
exit

! WAN Interfaces (/30 Point-to-Point)
interface Serial0/1/0
 ip address 192.168.1.126 255.255.255.252
 description WAN-to-R2 (/30)
 no shutdown
exit

interface Serial0/1/1
 ip address 192.168.1.129 255.255.255.252
 description WAN-to-R1 (/30)
 clock rate 64000
 no shutdown
exit

! Routing configuration
router rip
 version 2
 no auto-summary
 network 192.168.1.0
exit

end
write memory
"""

    with open("/Users/sanjaywaradkar/DCCN_Lab/exp11/R1_vlsm_dhcp.txt", "w") as f:
        f.write(r1_cfg)
    with open("/Users/sanjaywaradkar/DCCN_Lab/exp11/R2_vlsm_dhcp.txt", "w") as f:
        f.write(r2_cfg)
    with open("/Users/sanjaywaradkar/DCCN_Lab/exp11/R3_vlsm_dhcp.txt", "w") as f:
        f.write(r3_cfg)
    print("VLSM + DHCP configuration files written successfully!")

def draw_topology():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis("off")
    
    # Triangle Router topology
    # R1: (5, 6.5), R2: (2, 2.5), R3: (8, 2.5)
    
    # WAN Links
    ax.plot([5, 2], [6.5, 2.5], color="#DC2626", lw=3, zorder=1) # R1-R2
    ax.plot([2, 8], [2.5, 2.5], color="#DC2626", lw=3, zorder=1) # R2-R3
    ax.plot([8, 5], [2.5, 6.5], color="#DC2626", lw=3, zorder=1) # R3-R1
    
    # WAN Labels
    ax.text(3.1, 4.8, "WAN 1: 192.168.1.120/30\n(Se0/1/0 .121 <-> .122)",
            ha="center", va="center", fontsize=8, fontweight="bold", color="#991B1B",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FEF2F2", edgecolor="#FCA5A5"))
    ax.text(5, 2.1, "WAN 2: 192.168.1.124/30\n(.125 <-> .126)",
            ha="center", va="top", fontsize=8, fontweight="bold", color="#991B1B",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FEF2F2", edgecolor="#FCA5A5"))
    ax.text(6.9, 4.8, "WAN 3: 192.168.1.128/30\n(.130 <-> .129)",
            ha="center", va="center", fontsize=8, fontweight="bold", color="#991B1B",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FEF2F2", edgecolor="#FCA5A5"))

    # LAN Links
    ax.plot([5, 1.5], [6.5, 7.8], color="#2563EB", lw=2, ls="--", zorder=1) # R1 to LAN Eng
    ax.plot([5, 8.5], [6.5, 7.8], color="#7C3AED", lw=2, ls="--", zorder=1) # R1 to Server Farm
    ax.plot([2, 0.5], [2.5, 0.5], color="#059669", lw=2, ls="--", zorder=1) # R2 to LAN Sales
    ax.plot([8, 9.5], [2.5, 0.5], color="#D97706", lw=2, ls="--", zorder=1) # R3 to LAN HR

    # Routers
    routers = [
        ("Router R1\n(DHCP Server 1)", (5, 6.5), "#1E3A8A"),
        ("Router R2\n(DHCP Server 2)", (2, 2.5), "#1E3A8A"),
        ("Router R3\n(DHCP Server 3)", (8, 2.5), "#1E3A8A"),
    ]
    for name, (x, y), col in routers:
        circle = plt.Circle((x, y), 0.65, color=col, ec="#0F172A", lw=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, name, ha="center", va="center", color="white", fontsize=8.5, fontweight="bold", zorder=4)

    # LAN Subnets
    subnets = [
        ("LAN 1: Engineering Department\nRequirement: 60 Hosts\nAllocated: 192.168.1.0/26 (Mask .192)\nDHCP Scope: .11 - .62 | GW: .1", 
         (1.5, 7.8), "#1D4ED8", "#EFF6FF", "#BFDBFE"),
        ("LAN 4: Server Farm & DMZ\nRequirement: 6 Hosts\nAllocated: 192.168.1.112/29 (Mask .248)\nDHCP Scope: .115 - .118 | GW: .113", 
         (8.5, 7.8), "#6D28D9", "#F5F3FF", "#DDD6FE"),
        ("LAN 2: Sales & Marketing\nRequirement: 28 Hosts\nAllocated: 192.168.1.64/27 (Mask .224)\nDHCP Scope: .71 - .94 | GW: .65", 
         (0.5, 0.5), "#047857", "#ECFDF5", "#A7F3D0"),
        ("LAN 3: Human Resources & Admin\nRequirement: 12 Hosts\nAllocated: 192.168.1.96/28 (Mask .240)\nDHCP Scope: .101 - .110 | GW: .97", 
         (9.5, 0.5), "#B45309", "#FFFBEB", "#FDE68A"),
    ]

    for text, (x, y), border_col, bg_col, edge_col in subnets:
        box = patches.FancyBboxPatch((x-1.8, y-0.65), 3.6, 1.3, boxstyle="round,pad=0.2",
                                    facecolor=bg_col, edgecolor=border_col, lw=2, zorder=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha="center", va="center", color="#0F172A", fontsize=7.5, fontweight="bold", zorder=4)

    plt.title("EXPERIMENT 11: VLSM TOPOLOGY WITH DYNAMIC IP ADDRESSING (DHCP)", 
              fontsize=12, fontweight="bold", pad=20, color="#0F172A")
    plt.tight_layout()
    plt.savefig("/Users/sanjaywaradkar/DCCN_Lab/exp11/vlsm_topology_diagram.png", dpi=300)
    plt.close()
    print("VLSM Topology diagram saved to exp11/vlsm_topology_diagram.png")

if __name__ == "__main__":
    generate_configs()
    draw_topology()
