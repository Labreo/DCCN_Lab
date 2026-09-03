/*
 * Experiment 07: Character / Byte Stuffing and De-stuffing
 * Language: C (Standard C99)
 */

#include <stdio.h>
#include <string.h>

int main() {
    char input[200], stuffed[400], destuffed[200];
    char flag = 'F'; // Flag byte
    char esc = 'E';  // Escape byte

    printf("==================================================\n");
    printf("   EXPERIMENT 07: CHARACTER STUFFING & DE-STUFF (C)\n");
    printf("==================================================\n");
    printf("Delimiters: FLAG = 'F', ESC = 'E'\n");
    printf("Enter character sequence (e.g., AFEBF): ");
    if (scanf("%s", input) != 1) {
        strcpy(input, "AFEBF");
    }

    // Sender: Stuffing
    int j = 0;
    stuffed[j++] = flag;
    for (int i = 0; i < strlen(input); i++) {
        if (input[i] == flag) {
            stuffed[j++] = esc;
            stuffed[j++] = flag;
        } else if (input[i] == esc) {
            stuffed[j++] = esc;
            stuffed[j++] = esc;
        } else {
            stuffed[j++] = input[i];
        }
    }
    stuffed[j++] = flag;
    stuffed[j] = '\0';

    printf("\n[SENDER] Original Characters : %s\n", input);
    printf("[SENDER] Transmitted Frame   : %s\n", stuffed);

    // Receiver: De-stuffing
    int k = 0;
    for (int i = 1; i < strlen(stuffed) - 1; i++) {
        if (stuffed[i] == esc) {
            i++; // Next char is literal
            destuffed[k++] = stuffed[i];
        } else {
            destuffed[k++] = stuffed[i];
        }
    }
    destuffed[k] = '\0';

    printf("\n[RECEIVER] Recovered String  : %s\n", destuffed);

    float payload = strlen(input);
    float total = strlen(stuffed);
    float efficiency = (payload / total) * 100.0;

    printf("\n[EFFICIENCY ANALYSIS]\n");
    printf("  Payload Chars   : %.0f\n", payload);
    printf("  Total Chars     : %.0f\n", total);
    printf("  Efficiency (η)  : %.2f%%\n", efficiency);
    printf("==================================================\n");

    return 0;
}
