/*
 * Experiment 05: Selective Repeat (SR) ARQ Protocol
 * Language: C (Standard C99)
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <stdbool.h>

int main() {
    int total_frames, window_size;
    srand(time(0));

    printf("==================================================\n");
    printf("     SELECTIVE REPEAT (SR) ARQ SIMULATION (C)     \n");
    printf("==================================================\n");
    printf("Enter total number of frames to send: ");
    if (scanf("%d", &total_frames) != 1 || total_frames <= 0) total_frames = 6;
    printf("Enter window size (Ws = Wr): ");
    if (scanf("%d", &window_size) != 1 || window_size <= 0) window_size = 3;

    bool acked[100] = {false};
    int base = 1;

    while (base <= total_frames) {
        printf("\n--- Transmitting Current Window [%d to %d] ---\n",
               base, (base + window_size - 1 < total_frames) ? base + window_size - 1 : total_frames);

        for (int i = base; i < base + window_size && i <= total_frames; i++) {
            if (!acked[i]) {
                printf("[SENDER]   Sending Frame %d...\n", i);
            }
        }

        // Simulate reception and ACKs
        for (int i = base; i < base + window_size && i <= total_frames; i++) {
            if (!acked[i]) {
                if (rand() % 3 == 0) {
                    printf("[NETWORK]  --> Frame %d was LOST!\n", i);
                } else {
                    printf("[RECEIVER] --> Frame %d received and buffered. Sending ACK %d.\n", i, i);
                    acked[i] = true;
                }
            }
        }

        // Handle timeouts for lost frames
        for (int i = base; i < base + window_size && i <= total_frames; i++) {
            if (!acked[i]) {
                printf("[TIMER]    --> Timeout for Frame %d! Resending ONLY Frame %d...\n", i, i);
                printf("[RECEIVER] --> Frame %d received and buffered. Sending ACK %d.\n", i, i);
                acked[i] = true;
            }
        }

        // Slide window
        while (base <= total_frames && acked[base]) {
            printf("[RECEIVER] --> Frame %d delivered in-order to Network Layer.\n", base);
            base++;
        }
        sleep(1);
    }

    printf("\n==================================================\n");
    printf("  All %d frames sent and delivered successfully!\n", total_frames);
    printf("==================================================\n");
    return 0;
}
