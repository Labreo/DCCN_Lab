/*
 * Experiment 08: 1's Complement Internet Checksum
 * Language: C (Standard C99)
 */

#include <stdio.h>

unsigned short ones_complement_add(unsigned short a, unsigned short b) {
    unsigned int sum = a + b;
    while (sum >> 8) {
        sum = (sum & 0xFF) + (sum >> 8); // Add carry back
    }
    return (unsigned short)(sum & 0xFF);
}

int main() {
    int n;
    unsigned short segments[20];

    printf("==================================================\n");
    printf("         INTERNET CHECKSUM (8-BIT) IN C           \n");
    printf("==================================================\n");
    printf("Enter number of 8-bit segments (e.g. 3): ");
    if (scanf("%d", &n) != 1 || n <= 0) n = 3;

    printf("Enter %d segments in hexadecimal (e.g., A9 39 C3): ", n);
    for (int i = 0; i < n; i++) {
        unsigned int val;
        if (scanf("%x", &val) != 1) val = 0;
        segments[i] = (unsigned short)(val & 0xFF);
    }

    // Sender: calculate checksum
    unsigned short sum = 0;
    for (int i = 0; i < n; i++) {
        sum = ones_complement_add(sum, segments[i]);
    }
    unsigned short checksum = (~sum) & 0xFF;

    printf("\n[SENDER SIDE]\n");
    printf("  Sum before complement : 0x%02X\n", sum);
    printf("  Calculated Checksum   : 0x%02X\n", checksum);

    // Receiver: verify
    printf("\n[RECEIVER SIDE]\n");
    unsigned short recv_sum = 0;
    for (int i = 0; i < n; i++) {
        recv_sum = ones_complement_add(recv_sum, segments[i]);
    }
    recv_sum = ones_complement_add(recv_sum, checksum);
    unsigned short result = (~recv_sum) & 0xFF;

    printf("  Sum with Checksum     : 0x%02X\n", recv_sum);
    printf("  Complemented Result   : 0x%02X\n", result);

    if (result == 0) {
        printf("  --> NO ERROR DETECTED! Data Accepted.\n");
    } else {
        printf("  --> ERROR DETECTED! Data Rejected.\n");
    }
    printf("==================================================\n");
    return 0;
}
