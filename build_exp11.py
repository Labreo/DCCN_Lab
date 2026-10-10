#!/usr/bin/env python3
"""
Experiment 11 Content Generator
VLSM Subnetting with Dynamic IP Addressing (DHCP)
"""

import os
from builder_helpers import (
    add_exp_header_block, add_heading_1, add_heading_2,
    add_paragraph, add_bullet, add_table_data, add_image_figure,
    add_screenshot_box, add_code_block
)

WORKSPACE_DIR = "/Users/sanjaywaradkar/DCCN_Lab"

def build_exp11_content(doc):
    add_exp_header_block(doc, "11", "01/10/2026")
    
    add_paragraph(doc, 
        "Design multiple subnets with suitable number of ports. Make a plan to assign Dynamic IP addressing across all subnets to explain the implementation of subnetting using Variable Length Subnet Masking (VLSM) using Cisco Packet Tracer.",
        bold_prefix="Aim: "
    )

    add_heading_1(doc, "Theory:")
    add_paragraph(doc,
        "Variable Length Subnet Masking (VLSM) is an advanced IP addressing technique that allows network engineers to divide an IP address space into subnets of varying sizes. While FLSM enforces an identical subnet mask across all subnets, VLSM permits different subnet masks for different subnets based on the specific host requirements of each segment. This concept—often referred to as 'subnetting a subnet'—prevents massive IPv4 address wastage, particularly on point-to-point router links where a /30 prefix (allocating exactly 2 usable host addresses) avoids wasting 28 or more addresses per WAN link compared to FLSM."
    )
    add_paragraph(doc,
        "Dynamic Host Configuration Protocol (DHCP) is a client-server network protocol designed to automate the assignment of IP addresses, subnet masks, default gateways, and DNS server parameters to IP hosts. Instead of manual static configuration, client computers dynamically lease an IP address from a centralized or router-based DHCP server upon network initialization."
    )
    add_paragraph(doc,
        "The DHCP address allocation exchange follows the four-step DORA process:\n"
        "1. DHCP DISCOVER: The client broadcasts an ICMP/UDP message (dest: 255.255.255.255, port 67) to locate available DHCP servers.\n"
        "2. DHCP OFFER: A listening DHCP server reserves an unassigned IP from its configured pool and unicasts/broadcasts an offer to the client with IP configuration options.\n"
        "3. DHCP REQUEST: The client officially requests the offered IP address and informs other potential DHCP servers that their offers were declined.\n"
        "4. DHCP ACKNOWLEDGE (ACK): The DHCP server finalizes the lease, registers the MAC-to-IP binding in its binding database, and sends an acknowledgment packet containing the lease duration.",
        bold_prefix="DHCP DORA Process:\n"
    )
    add_paragraph(doc,
        "When a DHCP server resides on a different network segment than the requesting client, an intermediate router must be configured with a DHCP Relay Agent using the Cisco IOS command 'ip helper-address <server-ip>'. This command converts client UDP broadcasts into directed unicast packets forwarded to the centralized DHCP server."
    )

    add_heading_1(doc, "REQUIREMENTS")
    add_bullet(doc, "3 Cisco 2911 / 1941 ISR Routers configured with Cisco IOS DHCP Server services", bold_prefix="Routers: ")
    add_bullet(doc, "3 Cisco Catalyst 2960 Layer-2 Switches", bold_prefix="Switches: ")
    add_bullet(doc, "Multiple End Devices (Host PCs, Laptops, DMZ Application Servers)", bold_prefix="Hosts: ")
    add_bullet(doc, "Copper Straight-Through Ethernet Cables and Serial WAN Cables", bold_prefix="Cabling: ")
    add_bullet(doc, "Cisco Packet Tracer (v8.2 or later) simulation software", bold_prefix="Software: ")

    add_heading_1(doc, "VLSM MATHEMATICAL DESIGN AND ADDRESSING PLAN")
    add_paragraph(doc,
        "A base address block of 192.168.1.0/24 (256 total IP addresses) is allocated for an enterprise network comprising four departmental LANs and three router-to-router WAN links. To prevent subnet collisions, subnets must be allocated in strictly descending order of host requirements (Largest Subnet First Rule)."
    )
    add_paragraph(doc,
        "1. Subnet A - Engineering Department (Needs 60 hosts):\n"
        "   Host bits h: 2^h - 2 >= 60 ==> 2^6 - 2 = 62 >= 60. Host bits = 6. Prefix: 32 - 6 = /26 (Mask: 255.255.255.192). Block size: 64.\n"
        "   Allocated: 192.168.1.0/26 (Usable: 192.168.1.1 - 192.168.1.62, Broadcast: 192.168.1.63)\n\n"
        "2. Subnet B - Sales & Marketing (Needs 28 hosts):\n"
        "   Host bits h: 2^h - 2 >= 28 ==> 2^5 - 2 = 30 >= 28. Host bits = 5. Prefix: 32 - 5 = /27 (Mask: 255.255.255.224). Block size: 32.\n"
        "   Allocated: 192.168.1.64/27 (Usable: 192.168.1.65 - 192.168.1.94, Broadcast: 192.168.1.95)\n\n"
        "3. Subnet C - HR & Admin Department (Needs 12 hosts):\n"
        "   Host bits h: 2^h - 2 >= 12 ==> 2^4 - 2 = 14 >= 12. Host bits = 4. Prefix: 32 - 4 = /28 (Mask: 255.255.255.240). Block size: 16.\n"
        "   Allocated: 192.168.1.96/28 (Usable: 192.168.1.97 - 192.168.1.110, Broadcast: 192.168.1.111)\n\n"
        "4. Subnet D - Server Farm & DMZ (Needs 6 hosts):\n"
        "   Host bits h: 2^h - 2 >= 6 ==> 2^3 - 2 = 6 >= 6. Host bits = 3. Prefix: 32 - 3 = /29 (Mask: 255.255.255.248). Block size: 8.\n"
        "   Allocated: 192.168.1.112/29 (Usable: 192.168.1.113 - 192.168.1.118, Broadcast: 192.168.1.119)\n\n"
        "5. Subnets E, F, G - Point-to-Point WAN Links (Needs 2 hosts each):\n"
        "   Host bits h: 2^h - 2 >= 2 ==> 2^2 - 2 = 2. Host bits = 2. Prefix: 32 - 2 = /30 (Mask: 255.255.255.252). Block size: 4.\n"
        "   WAN 1 (R1-R2): 192.168.1.120/30 (Usable: .121 - .122, Bcast: .123)\n"
        "   WAN 2 (R2-R3): 192.168.1.124/30 (Usable: .125 - .126, Bcast: .127)\n"
        "   WAN 3 (R3-R1): 192.168.1.128/30 (Usable: .129 - .130, Bcast: .131)",
        bold_prefix="Step-by-Step VLSM Derivations:\n"
    )

    headers_vlsm = ["Subnet Name", "Hosts", "Network ID", "Prefix / Mask", "Usable Host Range", "Broadcast", "DHCP Scope Pool"]
    rows_vlsm = [
        ["Engineering LAN", "60", "192.168.1.0", "/26 (.192)", "192.168.1.1 - 192.168.1.62", "192.168.1.63", "ENG_POOL (.11 - .62)"],
        ["Sales LAN", "28", "192.168.1.64", "/27 (.224)", "192.168.1.65 - 192.168.1.94", "192.168.1.95", "SALES_POOL (.71 - .94)"],
        ["HR & Admin LAN", "12", "192.168.1.96", "/28 (.240)", "192.168.1.97 - 192.168.1.110", "192.168.1.111", "HR_POOL (.101 - .110)"],
        ["Server Farm LAN", "6", "192.168.1.112", "/29 (.248)", "192.168.1.113 - 192.168.1.118", "192.168.1.119", "SERVER_POOL (.115 - .118)"],
        ["WAN 1 (R1-R2)", "2", "192.168.1.120", "/30 (.252)", "192.168.1.121 - 192.168.1.122", "192.168.1.123", "Static Assigned"],
        ["WAN 2 (R2-R3)", "2", "192.168.1.124", "/30 (.252)", "192.168.1.125 - 192.168.1.126", "192.168.1.127", "Static Assigned"],
        ["WAN 3 (R3-R1)", "2", "192.168.1.128", "/30 (.252)", "192.168.1.129 - 192.168.1.130", "192.168.1.131", "Static Assigned"],
    ]
    add_table_data(doc, headers_vlsm, rows_vlsm, col_widths=[1.2, 0.5, 0.9, 0.8, 1.3, 0.8, 1.5])

    add_heading_1(doc, "NETWORK TOPOLOGY ARCHITECTURE")
    add_paragraph(doc,
        "Figure 11.1 illustrates the VLSM network topology showing the three routers configured as local DHCP servers, connecting four distinct departmental subnets with their customized subnet masks."
    )
    add_image_figure(doc, 
        os.path.join(WORKSPACE_DIR, "exp11/vlsm_topology_diagram.png"), 
        "Figure 11.1: Experiment 11 VLSM Topology with Dynamic IP Addressing (DHCP Pools)"
    )

    add_heading_1(doc, "ROUTER DHCP SERVER AND INTERFACE CONFIGURATION")
    add_paragraph(doc,
        "Each router runs a local Cisco IOS DHCP Server daemon. Default gateways and static server IP addresses are explicitly excluded using 'ip dhcp excluded-address' to prevent duplicate IP collisions."
    )

    add_heading_2(doc, "Router R1 (DHCP Server for Engineering & Server Farm):")
    r1_dhcp_code = """R1> enable
R1# configure terminal
R1(config)# hostname R1
! Exclude default gateways from dynamic assignment
R1(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.10
R1(config)# ip dhcp excluded-address 192.168.1.113 192.168.1.114

! Configure DHCP Pool for Engineering LAN (/26)
R1(config)# ip dhcp pool ENG_POOL
R1(dhcp-config)# network 192.168.1.0 255.255.255.192
R1(dhcp-config)# default-router 192.168.1.1
R1(dhcp-config)# dns-server 8.8.8.8
R1(dhcp-config)# domain-name gec.ac.in
R1(dhcp-config)# lease 1 0 0
R1(dhcp-config)# exit

! Configure DHCP Pool for Server Farm (/29)
R1(config)# ip dhcp pool SERVER_POOL
R1(dhcp-config)# network 192.168.1.112 255.255.255.248
R1(dhcp-config)# default-router 192.168.1.113
R1(dhcp-config)# dns-server 8.8.8.8
R1(dhcp-config)# lease 7 0 0
R1(dhcp-config)# exit

! Interface IP Configuration
R1(config)# interface GigabitEthernet0/0/0
R1(config-if)# ip address 192.168.1.1 255.255.255.192
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)# interface GigabitEthernet0/0/1
R1(config-if)# ip address 192.168.1.113 255.255.255.248
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)# interface Serial0/1/0
R1(config-if)# ip address 192.168.1.121 255.255.255.252
R1(config-if)# clock rate 64000
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)# interface Serial0/1/1
R1(config-if)# ip address 192.168.1.130 255.255.255.252
R1(config-if)# no shutdown
R1(config-if)# exit
! Dynamic Routing Protocol (RIPv2 supporting VLSM)
R1(config)# router rip
R1(config-router)# version 2
R1(config-router)# no auto-summary
R1(config-router)# network 192.168.1.0
R1(config-router)# end
R1# write memory"""
    add_code_block(doc, r1_dhcp_code)

    add_heading_2(doc, "Router R2 & R3 DHCP Configuration:")
    r23_dhcp_code = """! Router R2 (DHCP Server for Sales LAN /27)
R2(config)# ip dhcp excluded-address 192.168.1.65 192.168.1.70
R2(config)# ip dhcp pool SALES_POOL
R2(dhcp-config)# network 192.168.1.64 255.255.255.224
R2(dhcp-config)# default-router 192.168.1.65
R2(dhcp-config)# dns-server 8.8.8.8
R2(dhcp-config)# exit
R2(config)# interface GigabitEthernet0/0/0
R2(config-if)# ip address 192.168.1.65 255.255.255.224
R2(config-if)# no shutdown

! Router R3 (DHCP Server for HR & Admin LAN /28)
R3(config)# ip dhcp excluded-address 192.168.1.97 192.168.1.100
R3(config)# ip dhcp pool HR_POOL
R3(dhcp-config)# network 192.168.1.96 255.255.255.240
R3(dhcp-config)# default-router 192.168.1.97
R3(dhcp-config)# dns-server 8.8.8.8
R3(dhcp-config)# exit
R3(config)# interface GigabitEthernet0/0/0
R3(config-if)# ip address 192.168.1.97 255.255.255.240
R3(config-if)# no shutdown"""
    add_code_block(doc, r23_dhcp_code)

    add_heading_1(doc, "PRACTICAL PROCEDURE")
    add_paragraph(doc, "1. Build the triangle router topology in Cisco Packet Tracer with 3 Cisco 2911 Routers and 3 Switches.")
    add_paragraph(doc, "2. Add client workstations (PCs and Laptops) to each LAN switch segment.")
    add_paragraph(doc, "3. Connect router Serial0/1/0 and Serial0/1/1 ports with Serial DCE cables to establish point-to-point /30 WAN links.")
    add_paragraph(doc, "4. Configure interface IP addresses and subnet masks corresponding to the VLSM allocation plan.")
    add_paragraph(doc, "5. Configure Cisco IOS DHCP server pools on each router, excluding default gateway IPs and defining network, default-router, and DNS parameters.")
    add_paragraph(doc, "6. Configure RIPv2 with 'version 2' and 'no auto-summary' across all routers so that variable subnet masks are propagated without classful auto-summarization.")
    add_paragraph(doc, "7. Open the Desktop tab on client PCs, select 'IP Configuration', and click the 'DHCP' radio button.")
    add_paragraph(doc, "8. Observe the DHCP DORA process in simulation mode and verify that the PC successfully receives an IP address, mask, default gateway, and DNS server.")
    add_paragraph(doc, "9. Execute 'show ip dhcp binding' on the routers to verify active client leases.")

    add_heading_1(doc, "OBSERVATIONS AND VERIFICATION")
    add_paragraph(doc,
        "Upon setting PC1 (Engineering Dept) to DHCP, it successfully requests and receives the IP address 192.168.1.11, Subnet Mask 255.255.255.192, and Default Gateway 192.168.1.1.",
        bold_prefix="Client DHCP Verification: "
    )

    dhcp_binding_out = """R1# show ip dhcp binding
IP address       Client-ID/              Lease expiration        Type
                 Hardware address
192.168.1.11     0060.7032.1801          Oct 02 2026 10:15 AM    Automatic
192.168.1.12     0060.7032.1802          Oct 02 2026 10:16 AM    Automatic
192.168.1.115    0001.9628.7410          Oct 08 2026 10:18 AM    Automatic

R1# show ip dhcp pool
Pool ENG_POOL :
 Utilization mark (high/low)    : 100 / 0
 Subnet size (total/usable)     : 62 / 52
 Leased addresses               : 2
 Excluded addresses             : 10
 Pending event                  : none"""
    add_code_block(doc, dhcp_binding_out)

    add_screenshot_box(doc, "Cisco Packet Tracer Screenshot: Client PC IP Configuration window showing DHCP request successful with IP 192.168.1.11 and Subnet Mask 255.255.255.192 (/26)")
    add_screenshot_box(doc, "Cisco Packet Tracer Screenshot: Router R1 executing 'show ip dhcp binding' displaying active client leases and MAC address associations")

    add_heading_1(doc, "PRECAUTIONS")
    add_bullet(doc, "Always use 'no auto-summary' in routing protocols when implementing VLSM; otherwise, routers will summarize subnets to Class C /24 boundaries and break routing.")
    add_bullet(doc, "Always exclude default gateway IP addresses before enabling DHCP pools to prevent IP address conflict errors on the LAN.")
    add_bullet(doc, "Ensure the 'default-router' IP matches the router's physical interface IP address on that specific subnet.")
    add_bullet(doc, "Allocate subnets in strictly descending order of host requirements to avoid overlapping address blocks.")

    add_heading_1(doc, "RESULT")
    add_paragraph(doc,
        "A multi-subnet internetwork was designed and implemented using Variable Length Subnet Masking (VLSM) across prefixes /26, /27, /28, /29, and /30. Dynamic IP addressing was realized using Cisco IOS DHCP Server pools, successfully leasing IP parameters to client workstations with zero IP address collisions and optimal IPv4 address utilization."
    )

    add_heading_1(doc, "Conclusion:")
    add_paragraph(doc,
        "VLSM design and Dynamic IP Addressing via DHCP was successfully studied and demonstrated using Cisco Packet Tracer."
    )

print("Exp 11 builder compiled successfully!")
