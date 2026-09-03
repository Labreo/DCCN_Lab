/*
 * Experiment 07: Bit Stuffing and De-stuffing (HDLC)
 * Language: C (Standard C99)
 */

#include <stdio.h>
#include <string.h>

void bit_stuffing(char *input, char *stuffed) {
    int count = 0, j = 0;
    for (int i = 0; i < strlen(input); i++) {
        stuffed[j++] = input[i];
        if (input[i] == '1') {
            count++;
            if (count == 5) {
                stuffed[j++] = '0'; // Stuff '0'
                count = 0;
            }
        } else {
            count = 0;
        }
    }
    stuffed[j] = '\0';
}

void bit_destuffing(char *stuffed, char *destuffed) {
    int count = 0, j = 0;
    for (int i = 0; i < strlen(stuffed); i++) {
        destuffed[j++] = stuffed[i];
        if (stuffed[i] == '1') {
            count++;
            if (count == 5) {
                if (i + 1 < strlen(stuffed) && stuffed[i + 1] == '0') {
                    i++; // Skip the stuffed '0'
                }
                count = 0;
            }
        } else {
            count = 0;
        }
    }
    destuffed[j] = '\0';
}

int main() {
    char input[200], stuffed[300], destuffed[200];
    char flag[] = "01111110";

    printf("==================================================\n");
    printf("   EXPERIMENT 07: BIT STUFFING & DE-STUFFING (C)  \n");
    printf("==================================================\n");
    printf("Enter binary bit string (e.g., 01111110111110): ");
    if (scanf("%s", input) != 1) {
        strcpy(input, "01111110111110");
        printf("Using default: %s\n", input);
    }

    bit_stuffing(input, stuffed);
    printf("\n[SENDER] Original Bit String : %s\n", input);
    printf("[SENDER] After Bit Stuffing  : %s\n", stuffed);
    printf("[SENDER] Transmitted Frame   : %s%s%s\n", flag, stuffed, flag);

    bit_destuffing(stuffed, destuffed);
    printf("\n[RECEIVER] De-stuffed String : %s\n", destuffed);

    float payload = strlen(input);
    float total = strlen(stuffed) + 2 * strlen(flag);
    float efficiency = (payload / total) * 100.0;

    printf("\n[EFFICIENCY ANALYSIS]\n");
    printf("  Payload Bits     : %.0f\n", payload);
    printf("  Total Frame Bits : %.0f\n", total);
    printf("  Efficiency (η)   : %.2f%%\n", efficiency);
    printf("==================================================\n");

    return 0;
}
