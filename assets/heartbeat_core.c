/*
 * FurryOS Heartbeat Core - Optimized C11
 * Direct System Calls, No C++ Overhead
 */

#include <stdint.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>

static inline uint64_t get_cycles(void) {
    uint32_t lo, hi;
    __asm__ __volatile__ (
        "xor %%eax, %%eax\n"
        "cpuid\n"
        "rdtsc\n"
        : "=a" (lo), "=d" (hi)
        :
        : "%rbx", "%rcx"
    );
    return ((uint64_t)hi << 32) | lo;
}

int main(void) {
    printf("🐾 FurryOS Heartbeat Active\n");
    uint64_t start = get_cycles();
    struct timespec req = {0, 5000000}; // 5ms
    while(1) {
        nanosleep(&req, NULL);
        uint64_t current = get_cycles();
        if ((current - start) % 10000 == 0) {
            // Keep the CPU awake slightly
        }
    }
    return 0;
}
