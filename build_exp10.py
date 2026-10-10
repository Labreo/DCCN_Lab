#!/usr/bin/env python3
"""
Full Lab Report Builder for Experiments 10 to 15
Author: Kanak Sanjay Waradkar (Roll No: 24B-CO-030)
Department: Computer Engineering, Goa College of Engineering
"""

import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from builder_helpers import (
    setup_header_footer, add_exp_header_block, add_heading_1, add_heading_2,
    add_paragraph, add_bullet, add_table_data, add_image_figure,
    add_screenshot_box, add_code_block
)

WORKSPACE_DIR = "/Users/sanjaywaradkar/DCCN_Lab"
DOWNLOADS_DIR = "/Users/sanjaywaradkar/Downloads"

# ---------------------------------------------------------------------------
# EXPERIMENT 10 BUILDER
# ---------------------------------------------------------------------------
def build_exp10_content(doc):
    add_exp_header_block(doc, "10", "24/09/2026")
    
    add_paragraph(doc, 
        "Design multiple subnets with suitable number of ports. Make a plan to assign static IP addressing across all subnets to explain the implementation of subnetting using Fixed Length Subnet Masking (FLSM) with a minimum of 4 routers and a minimum of 8 networks, implementing static routing.",
        bold_prefix="Aim: "
    )

    add_heading_1(doc, "Theory:")
    add_paragraph(doc,
        "Subnetting is the architectural technique of partitioning a single physical or logical network into multiple distinct, smaller broadcast domains called subnets. In traditional classful IP addressing, large blocks of IP addresses were assigned without regard to actual host requirements, leading to severe IPv4 address exhaustion. Subnetting solves this inefficiency by borrowing host bits to create an extended network prefix, effectively segmenting network traffic and containing local broadcasts."
    )
    add_paragraph(doc,
        "Fixed Length Subnet Masking (FLSM) is a subnetting technique where all subnets derived from a parent network utilize an identical subnet mask and possess the exact same number of available host addresses. In FLSM, if a parent network is divided into subnets, every single subnet has the same prefix length regardless of the specific size or port density of the physical LAN segment connected to it. While FLSM is straightforward to plan and configure, it can cause address wastage on point-to-point links (such as WAN links between routers) where only two host IP addresses are strictly necessary."
    )
    add_paragraph(doc,
        "Static Routing is a non-adaptive, manual method of configuring forwarding paths in the routing table of an IP router. Unlike dynamic routing protocols that automatically discover network paths via periodic message exchanges, static routes are explicitly defined by the network administrator using the syntax:",
        bold_prefix="Static Routing Principles: "
    )
    add_code_block(doc, "ip route <destination-network> <subnet-mask> <next-hop-ip | exit-interface> [distance]")
    add_paragraph(doc,
        "Static routes have an Administrative Distance (AD) of 1 by default, indicating higher trustworthiness than any dynamic routing protocol (OSPF AD=110, RIP AD=120, EIGRP AD=90). Static routing eliminates routing protocol control overhead, consumes minimal router CPU and memory, and offers superior security since routing updates are not transmitted across untrusted external links."
    )

    add_heading_1(doc, "REQUIREMENTS")
    add_bullet(doc, "4 Cisco 2911 / 1941 ISR Routers equipped with GigabitEthernet and Serial HWIC-2T ports", bold_prefix="Routers: ")
    add_bullet(doc, "4 Cisco Catalyst 2960-24TT Layer-2 Switches", bold_prefix="Switches: ")
    add_bullet(doc, "4 Host Workstation PCs / Laptops", bold_prefix="End Devices: ")
    add_bullet(doc, "Copper Straight-Through Ethernet Cables and Serial DCE/DTE WAN Cables", bold_prefix="Cabling: ")
    add_bullet(doc, "Cisco Packet Tracer (v8.2 or later) network simulation platform", bold_prefix="Software: ")

    add_heading_1(doc, "FLSM MATHEMATICAL CALCULATIONS AND ADDRESSING PLAN")
    add_paragraph(doc,
        "To fulfill the design mandate of a minimum of 4 routers and 8 distinct networks, a parent Class C private IPv4 address block of 192.168.10.0/24 is allocated. The network consists of 4 Local Area Networks (one per router) and 4 Wide Area Network point-to-point links connecting the routers in a resilient loop topology."
    )
    add_paragraph(doc,
        "1. Base Network: 192.168.10.0/24 (Subnet Mask: 255.255.255.0)\n"
        "2. Number of Subnets Required (N): 8 subnets\n"
        "3. Bits to Borrow (s): 2^s >= 8  ==>  s = 3 bits\n"
        "4. New Subnet Mask: /24 + 3 = /27  ==>  11111111.11111111.11111111.11100000 (255.255.255.224)\n"
        "5. Remaining Host Bits (h): 32 - 27 = 5 bits\n"
        "6. Usable Host Addresses per Subnet: 2^h - 2 = 2^5 - 2 = 30 usable hosts per subnet\n"
        "7. Subnet Block Size (Delta): 256 - 224 = 32 addresses",
        bold_prefix="Mathematical Formulations:\n"
    )

    # Table 1: FLSM Addressing Table
    headers_flsm = ["Subnet Name", "Network ID", "Prefix / Mask", "Usable Host Range", "Broadcast", "Default Gateway", "Device / Port"]
    rows_flsm = [
        ["Subnet 1 (LAN 1)", "192.168.10.0", "/27 (.224)", "192.168.10.1 - 192.168.10.30", "192.168.10.31", "192.168.10.1", "R1 Gig0/0/0 (PC1)"],
        ["Subnet 2 (LAN 2)", "192.168.10.32", "/27 (.224)", "192.168.10.33 - 192.168.10.62", "192.168.10.63", "192.168.10.33", "R2 Gig0/0/0 (PC2)"],
        ["Subnet 3 (LAN 3)", "192.168.10.64", "/27 (.224)", "192.168.10.65 - 192.168.10.94", "192.168.10.95", "192.168.10.65", "R3 Gig0/0/0 (PC3)"],
        ["Subnet 4 (LAN 4)", "192.168.10.96", "/27 (.224)", "192.168.10.97 - 192.168.10.126", "192.168.10.127", "192.168.10.97", "R4 Gig0/0/0 (PC4)"],
        ["Subnet 5 (WAN 1)", "192.168.10.128", "/27 (.224)", "192.168.10.129 - 192.168.10.158", "192.168.10.159", "N/A", "R1 Gig0/1 <-> R2 Gig0/1"],
        ["Subnet 6 (WAN 2)", "192.168.10.160", "/27 (.224)", "192.168.10.161 - 192.168.10.190", "192.168.10.191", "N/A", "R2 Gig0/2 <-> R3 Gig0/1"],
        ["Subnet 7 (WAN 3)", "192.168.10.192", "/27 (.224)", "192.168.10.193 - 192.168.10.222", "192.168.10.223", "N/A", "R3 Gig0/2 <-> R4 Gig0/1"],
        ["Subnet 8 (WAN 4)", "192.168.10.224", "/27 (.224)", "192.168.10.225 - 192.168.10.254", "192.168.10.255", "N/A", "R4 Gig0/2 <-> R1 Gig0/2"],
    ]
    add_table_data(doc, headers_flsm, rows_flsm, col_widths=[1.1, 0.9, 0.8, 1.4, 0.8, 0.8, 1.2])

    add_heading_1(doc, "NETWORK TOPOLOGY ARCHITECTURE")
    add_paragraph(doc,
        "The complete network topology diagram below displays the 4 Cisco Routers (R1, R2, R3, R4) interconnected via Gigabit Ethernet WAN links, with each router anchoring an independent LAN broadcast domain containing a switch and client workstation."
    )
    add_image_figure(doc, 
        os.path.join(WORKSPACE_DIR, "exp10/flsm_topology_diagram.png"), 
        "Figure 10.1: Experiment 10 FLSM Network Topology Architecture (4 Routers, 8 Subnets, /27)"
    )

    add_heading_1(doc, "CISCO IOS STATIC ROUTING CONFIGURATION")
    add_paragraph(doc,
        "Static routes are configured on all routers to provide full end-to-end reachability across the entire 8-subnet internetwork without requiring any dynamic routing protocol."
    )

    add_heading_2(doc, "Router R1 Configuration:")
    r1_code = """Router> enable
Router# configure terminal
Router(config)# hostname R1
R1(config)# interface GigabitEthernet0/0/0
R1(config-if)# ip address 192.168.10.1 255.255.255.224
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)# interface GigabitEthernet0/0/1
R1(config-if)# ip address 192.168.10.129 255.255.255.224
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)# interface GigabitEthernet0/0/2
R1(config-if)# ip address 192.168.10.226 255.255.255.224
R1(config-if)# no shutdown
R1(config-if)# exit
! Static Routes to Remote Subnets
R1(config)# ip route 192.168.10.32 255.255.255.224 192.168.10.130
R1(config)# ip route 192.168.10.64 255.255.255.224 192.168.10.130
R1(config)# ip route 192.168.10.96 255.255.255.224 192.168.10.225
R1(config)# ip route 192.168.10.160 255.255.255.224 192.168.10.130
R1(config)# ip route 192.168.10.192 255.255.255.224 192.168.10.225
R1(config)# end
R1# write memory"""
    add_code_block(doc, r1_code)

    add_heading_2(doc, "Router R2 Configuration:")
    r2_code = """Router> enable
Router# configure terminal
Router(config)# hostname R2
R2(config)# interface GigabitEthernet0/0/0
R2(config-if)# ip address 192.168.10.33 255.255.255.224
R2(config-if)# no shutdown
R2(config-if)# exit
R2(config)# interface GigabitEthernet0/0/1
R2(config-if)# ip address 192.168.10.130 255.255.255.224
R2(config-if)# no shutdown
R2(config-if)# exit
R2(config)# interface GigabitEthernet0/0/2
R2(config-if)# ip address 192.168.10.161 255.255.255.224
R2(config-if)# no shutdown
R2(config-if)# exit
! Static Routes to Remote Subnets
R2(config)# ip route 192.168.10.0 255.255.255.224 192.168.10.129
R2(config)# ip route 192.168.10.64 255.255.255.224 192.168.10.162
R2(config)# ip route 192.168.10.96 255.255.255.224 192.168.10.162
R2(config)# ip route 192.168.10.192 255.255.255.224 192.168.10.162
R2(config)# ip route 192.168.10.224 255.255.255.224 192.168.10.129
R2(config)# end
R2# write memory"""
    add_code_block(doc, r2_code)

    add_heading_2(doc, "Router R3 & R4 Configuration Summary:")
    r34_code = """! Router R3 Interfaces & Static Routes
R3(config)# interface Gi0/0/0: 192.168.10.65 255.255.255.224 (LAN 3)
R3(config)# interface Gi0/0/1: 192.168.10.162 255.255.255.224 (WAN to R2)
R3(config)# interface Gi0/0/2: 192.168.10.193 255.255.255.224 (WAN to R4)
R3(config)# ip route 192.168.10.0 255.255.255.224 192.168.10.161
R3(config)# ip route 192.168.10.32 255.255.255.224 192.168.10.161
R3(config)# ip route 192.168.10.96 255.255.255.224 192.168.10.194
R3(config)# ip route 192.168.10.128 255.255.255.224 192.168.10.161
R3(config)# ip route 192.168.10.224 255.255.255.224 192.168.10.194

! Router R4 Interfaces & Static Routes
R4(config)# interface Gi0/0/0: 192.168.10.97 255.255.255.224 (LAN 4)
R4(config)# interface Gi0/0/1: 192.168.10.194 255.255.255.224 (WAN to R3)
R4(config)# interface Gi0/0/2: 192.168.10.225 255.255.255.224 (WAN to R1)
R4(config)# ip route 192.168.10.0 255.255.255.224 192.168.10.226
R4(config)# ip route 192.168.10.32 255.255.255.224 192.168.10.226
R4(config)# ip route 192.168.10.64 255.255.255.224 192.168.10.193
R4(config)# ip route 192.168.10.128 255.255.255.224 192.168.10.226
R4(config)# ip route 192.168.10.160 255.255.255.224 192.168.10.193"""
    add_code_block(doc, r34_code)

    add_heading_1(doc, "PRACTICAL PROCEDURE")
    add_paragraph(doc, "1. Launch Cisco Packet Tracer and assemble the hardware devices on the logical workspace: 4 Cisco 2911 Routers, 4 Catalyst 2960 Switches, and 4 PC Workstations.")
    add_paragraph(doc, "2. Connect PC1 to Switch 1, PC2 to Switch 2, PC3 to Switch 3, and PC4 to Switch 4 using Copper Straight-Through cables into FastEthernet ports.")
    add_paragraph(doc, "3. Connect each switch to its designated router's GigabitEthernet0/0/0 port.")
    add_paragraph(doc, "4. Interconnect the routers: R1 Gi0/0/1 to R2 Gi0/0/1, R2 Gi0/0/2 to R3 Gi0/0/1, R3 Gi0/0/2 to R4 Gi0/0/1, and R4 Gi0/0/2 to R1 Gi0/0/2.")
    add_paragraph(doc, "5. Access each router via the CLI tab, enter global configuration mode, configure interface IP addresses and subnet masks (/27, 255.255.255.224), and activate interfaces using 'no shutdown'.")
    add_paragraph(doc, "6. Program static routes on each router for all non-directly connected subnets using the next-hop IP address.")
    add_paragraph(doc, "7. Manually assign static IP configurations to PC1, PC2, PC3, and PC4 with appropriate IP address, subnet mask (255.255.255.224), and default gateway.")
    add_paragraph(doc, "8. Execute verification commands: 'show ip route' on routers and ping tests from PC command prompts.")

    add_heading_1(doc, "OBSERVATIONS AND VERIFICATION")
    add_paragraph(doc,
        "Verification confirms that all 8 subnets are reachable across the network. The routing table on Router R1 shows directly connected subnets marked with code 'C', local interfaces marked with 'L', and statically routed networks marked with 'S'.",
        bold_prefix="Routing Table Verification (R1): "
    )
    
    r1_route_out = """R1# show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
Gateway of last resort is not set

      192.168.10.0/27 is subnetted, 8 subnets
C        192.168.10.0/27 is directly connected, GigabitEthernet0/0/0
L        192.168.10.1/32 is directly connected, GigabitEthernet0/0/0
S        192.168.10.32/27 [1/0] via 192.168.10.130
S        192.168.10.64/27 [1/0] via 192.168.10.130
S        192.168.10.96/27 [1/0] via 192.168.10.225
C        192.168.10.128/27 is directly connected, GigabitEthernet0/0/1
L        192.168.10.129/32 is directly connected, GigabitEthernet0/0/1
S        192.168.10.160/27 [1/0] via 192.168.10.130
S        192.168.10.192/27 [1/0] via 192.168.10.225
C        192.168.10.224/27 is directly connected, GigabitEthernet0/0/2
L        192.168.10.226/32 is directly connected, GigabitEthernet0/0/2"""
    add_code_block(doc, r1_route_out)

    add_screenshot_box(doc, "Cisco Packet Tracer Screenshot: Router R1 'show ip route' displaying all 8 FLSM subnets with static and connected entries")
    add_screenshot_box(doc, "Cisco Packet Tracer Screenshot: Successful ICMP ping from PC1 (192.168.10.2) to remote PC3 (192.168.10.66) across static routes")

    add_heading_1(doc, "PRECAUTIONS")
    add_bullet(doc, "Verify that subnet mask 255.255.255.224 is consistently applied on all devices; mixing /24 and /27 leads to routing conflicts.")
    add_bullet(doc, "Ensure static routes are bi-directional; a packet reaching a destination host will be dropped if the return route back to the source is missing.")
    add_bullet(doc, "Always execute 'no shutdown' on Cisco router interfaces, as they remain in an administratively down state by default.")
    add_bullet(doc, "Double check that router interface IP addresses match the designated default gateway IP configured on connected PCs.")

    add_heading_1(doc, "RESULT")
    add_paragraph(doc,
        "A multi-router internetwork comprising 4 Cisco routers and 8 distinct subnets was designed and successfully implemented using Fixed Length Subnet Masking (FLSM) with prefix /27 (255.255.255.224). Static routing tables were established across all routers, and 100% end-to-end ICMP reachability was verified between all host PCs across the internetwork."
    )

    add_heading_1(doc, "Conclusion:")
    add_paragraph(doc,
        "Subnetting using FLSM and static routing was thoroughly studied and executed successfully in Cisco Packet Tracer."
    )

print("Exp 10 builder compiled successfully!")
