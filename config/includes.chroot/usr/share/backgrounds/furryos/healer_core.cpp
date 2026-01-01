
#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <chrono>
#include <vector>
#include <thread>
// Minimal Healer logic to keep file small
int main(int argc, char* argv[]) {
    if (argc < 2) return 1;
    while(true) {
        pid_t pid = fork();
        if (pid == 0) { execvp(argv[1], &argv[1]); exit(1); }
        else { int s; waitpid(pid, &s, 0); std::this_thread::sleep_for(std::chrono::seconds(1)); }
    }
    return 0;
}
