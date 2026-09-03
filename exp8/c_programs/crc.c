/*
 * Experiment 08: Cyclic Redundancy Check (CRC)
 * Language: C (Standard C99)
 */

#include <stdio.h>
#include <string.h>

void xor_op(char *a, char *b, int len) {
    for (int i = 0; i < len; i++) {
        a[i] = (a[i] == b[i]) ? '0' : '1';
    }
}

void modulo2_divide(char *dividend, char *divisor, char *remainder) {
    int m = strlen(dividend);
    int n = strlen(divisor);
    char tmp[100];
    strncpy(tmp, dividend, n);
    tmp[n] = '\0';

    int pick = n;
    while (pick <= m) {
        if (tmp[0] == '1') {
            xor_op(tmp, divisor, n);
        }
        if (pick < m) {
            for (int i = 0; i < n - 1; i++) tmp[i] = tmp[i + 1];
            tmp[n - 1] = dividend[pick];
            tmp[n] = '\0';
        }
        pick++;
    }
    strncpy(remainder, tmp + 1, n - 1);
    remainder[n - 1] = '\0';
}

int main() {
    char data[100], gen[50], appended[150], crc[50], codeword[150], received[150];

    printf("==================================================\n");
    printf("        CYCLIC REDUNDANCY CHECK (CRC) IN C        \n");
    printf("==================================================\n");
    printf("Enter data bits (e.g., 100100): ");
    if (scanf("%s", data) != 1) strcpy(data, "100100");

    printf("Enter generator polynomial (e.g., 1101): ");
    if (scanf("%s", gen) != 1) strcpy(gen, "1101");

    int r = strlen(gen) - 1;
    strcpy(appended, data);
    for (int i = 0; i < r; i++) strcat(appended, "0");

    modulo2_divide(appended, gen, crc);
    strcpy(codeword, data);
    strcat(codeword, crc);

    printf("\n[SENDER SIDE]\n");
    printf("  Appended Data      : %s\n", appended);
    printf("  CRC Checksum       : %s\n", crc);
    printf("  Transmitted Codeword: %s\n", codeword);

    printf("\n[RECEIVER SIDE]\n");
    printf("Enter received codeword (press Enter to use %s): ", codeword);
    scanf("%s", received);

    char rem[50];
    modulo2_divide(received, gen, rem);
    printf("  Syndrome Remainder : %s\n", rem);

    int err = 0;
    for (int i = 0; i < strlen(rem); i++) {
        if (rem[i] != '0') err = 1;
    }

    if (!err) {
        printf("  --> NO ERROR DETECTED! Packet Accepted.\n");
    } else {
        printf("  --> ERROR DETECTED! Packet Rejected.\n");
    }
    printf("==================================================\n");
    return 0;
}
