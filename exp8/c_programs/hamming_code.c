/*
 * Experiment 08: Hamming Code (7,4) Error Detection & Correction
 * Language: C (Standard C99)
 */

#include <stdio.h>

int main() {
    int data[4];
    int code[8];

    printf("==================================================\n");
    printf("           HAMMING CODE (7,4) SIMULATION (C)      \n");
    printf("==================================================\n");
    printf("Enter 4 data bits (space separated, e.g. 1 0 1 1): ");
    if (scanf("%d %d %d %d", &data[0], &data[1], &data[2], &data[3]) != 4) {
        data[0] = 1; data[1] = 0; data[2] = 1; data[3] = 1;
        printf("Defaulting to 1 0 1 1\n");
    }

    // Positions: 1 (p1), 2 (p2), 3 (d1), 4 (p3), 5 (d2), 6 (d3), 7 (d4)
    code[3] = data[0];
    code[5] = data[1];
    code[6] = data[2];
    code[7] = data[3];

    // Even Parity calculations
    code[1] = code[3] ^ code[5] ^ code[7]; // p1: checks 1, 3, 5, 7
    code[2] = code[3] ^ code[6] ^ code[7]; // p2: checks 2, 3, 6, 7
    code[4] = code[5] ^ code[6] ^ code[7]; // p3: checks 4, 5, 6, 7

    printf("\n[SENDER SIDE]\n");
    printf("  Parity bits: p1=%d, p2=%d, p3=%d\n", code[1], code[2], code[4]);
    printf("  Transmitted Codeword (1 to 7): %d%d%d%d%d%d%d\n",
           code[1], code[2], code[3], code[4], code[5], code[6], code[7]);

    printf("\n[RECEIVER SIDE]\n");
    int recv[8];
    printf("Enter 7-bit received codeword (separated by spaces): ");
    for (int i = 1; i <= 7; i++) {
        if (scanf("%d", &recv[i]) != 1) recv[i] = code[i];
    }

    int c1 = recv[1] ^ recv[3] ^ recv[5] ^ recv[7];
    int c2 = recv[2] ^ recv[3] ^ recv[6] ^ recv[7];
    int c3 = recv[4] ^ recv[5] ^ recv[6] ^ recv[7];
    int syndrome = c3 * 4 + c2 * 2 + c1;

    if (syndrome == 0) {
        printf("  --> Syndrome is 0: NO ERROR DETECTED!\n");
        printf("  --> Extracted Data: %d%d%d%d\n", recv[3], recv[5], recv[6], recv[7]);
    } else {
        printf("  --> ERROR DETECTED at bit position: %d\n", syndrome);
        recv[syndrome] = 1 - recv[syndrome]; // Invert / correct bit
        printf("  --> Corrected Codeword: %d%d%d%d%d%d%d\n",
               recv[1], recv[2], recv[3], recv[4], recv[5], recv[6], recv[7]);
        printf("  --> Extracted Corrected Data: %d%d%d%d\n",
               recv[3], recv[5], recv[6], recv[7]);
    }
    printf("==================================================\n");
    return 0;
}
