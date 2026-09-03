/*
 * Experiment 05: Go-Back-N (GBN) ARQ Protocol
 * Language: C (Standard C99)
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

int main() {
    int total_frames, window_size;
    int base = 1, next_seq = 1;
    srand(time(0));

    printf("==================================================\n");
    printf("         GO-BACK-N (GBN) ARQ SIMULATION (C)       \n");
    printf("==================================================\n");
    printf("Enter total number of frames to send: ");
    if (scanf("%d", &total_frames) != 1 || total_frames <= 0) total_frames = 7;
    printf("Enter window size (N): ");
    if (scanf("%d", &window_size) != 1 || window_size <= 0) window_size = 3;

    while (base <= total_frames) {
        printf("\n--- Transmitting Current Window [%d to %d] ---\n", 
               base, (base + window_size - 1 < total_frames) ? base + window_size - 1 : total_frames);

        for (int i = base; i < base + window_size && i <= total_frames; i++) {
            printf("[SENDER]   Sending Frame %d...\n", i);
        }

        // Simulate channel transmission
        int lost_frame = -1;
        for (int i = base; i < base + window_size && i <= total_frames; i++) {
            if ((rand() % 4 == 0) && (lost_frame == -1)) {
                lost_frame = i;
                printf("[NETWORK]  --> Frame %d was LOST in transit!\n", i);
            }
        }

        if (lost_frame != -1) {
            printf("[RECEIVER] --> Discarding subsequent out-of-order frames.\n");
            printf("[TIMER]    --> Timeout expired for Frame %d!\n", lost_frame);
            printf("[SENDER]   --> GO-BACK-N: Retransmitting all frames starting from Frame %d...\n", lost_frame);
            base = lost_frame;
        } else {
            for (int i = base; i < base + window_size && i <= total_frames; i++) {
                printf("[RECEIVER] --> Frame %d accepted. Sending ACK %d.\n", i, i + 1);
            }
            printf("[SENDER]   --> All ACKs received for current window. Sliding window forward...\n");
            base += window_size;
        }
        sleep(1);
    }

    printf("\n==================================================\n");
    printf("  All %d frames sent and delivered successfully!\n", total_frames);
    printf("==================================================\n");
    return 0;
}
