/*
 * Experiment 05: Stop-and-Wait ARQ Protocol
 * Language: C (Standard C99)
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

int main() {
    int total_frames, i = 1;
    int seq_num = 0;
    srand(time(0));

    printf("==================================================\n");
    printf("        STOP-AND-WAIT ARQ SIMULATION (C)          \n");
    printf("==================================================\n");
    printf("Enter the total number of frames to send: ");
    if (scanf("%d", &total_frames) != 1 || total_frames <= 0) {
        total_frames = 4;
        printf("Defaulting to 4 frames.\n");
    }

    while (i <= total_frames) {
        printf("\n[SENDER]   Sending Frame %d (Seq No = %d)...\n", i, seq_num);
        sleep(1);

        int r = rand() % 4; // 0: Frame lost, 1: ACK lost, 2 or 3: Success

        if (r == 0) {
            printf("[NETWORK]  --> Frame %d was LOST in transit!\n", i);
            printf("[TIMER]    --> Timeout! No ACK received for Frame %d.\n", i);
            printf("[SENDER]   --> Retransmitting Frame %d (Seq No = %d)...\n", i, seq_num);
        } else if (r == 1) {
            printf("[RECEIVER] --> Frame %d received successfully.\n", i);
            printf("[RECEIVER] --> Sending ACK %d...\n", 1 - seq_num);
            printf("[NETWORK]  --> ACK %d was LOST in transit!\n", 1 - seq_num);
            printf("[TIMER]    --> Timeout expired at sender waiting for ACK!\n");
            printf("[SENDER]   --> Retransmitting Frame %d (Seq No = %d)...\n", i, seq_num);
            printf("[RECEIVER] --> Duplicate Frame detected. Discarded. Resending ACK %d...\n", 1 - seq_num);
            printf("[SENDER]   --> ACK %d received successfully.\n", 1 - seq_num);
            seq_num = 1 - seq_num;
            i++;
        } else {
            printf("[RECEIVER] --> Frame %d received successfully.\n", i);
            printf("[RECEIVER] --> Sending ACK %d...\n", 1 - seq_num);
            printf("[SENDER]   --> ACK %d received successfully before timeout.\n", 1 - seq_num);
            seq_num = 1 - seq_num;
            i++;
        }
    }

    printf("\n==================================================\n");
    printf("  All %d frames transmitted and acknowledged!\n", total_frames);
    printf("==================================================\n");
    return 0;
}
