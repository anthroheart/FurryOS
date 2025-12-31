; ==============================================================================
; FURRYOS - heartbeat_core Monitoring Loop (x86_64 Assembly)
; ==============================================================================
; High-performance monitoring loop with nanosecond precision
; Uses RDTSC for cycle-accurate timing
; Optimized register usage and cache alignment
; ==============================================================================

section .data
    align 64
    monitor_state: times 8 dq 0    ; 64-byte aligned state

section .text
    global asm_monitor_loop
    global asm_get_cycles
    global asm_measure_latency

; ==============================================================================
; Get CPU cycle count (RDTSC)
; Returns: RAX = cycle count
; ==============================================================================
asm_get_cycles:
    push rbx
    push rcx
    push rdx
    
    xor eax, eax
    cpuid                   ; Serialize
    rdtsc                   ; Read timestamp counter
    shl rdx, 32
    or rax, rdx            ; Combine into 64-bit
    
    pop rdx
    pop rcx
    pop rbx
    ret

; ==============================================================================
; Measure operation latency
; Args: RDI = function pointer to measure
; Returns: RAX = cycles elapsed
; ==============================================================================
asm_measure_latency:
    push rbx
    push r12
    push r13
    
    mov r12, rdi           ; Save function pointer
    
    ; Get start cycles
    xor eax, eax
    cpuid
    rdtsc
    shl rdx, 32
    or rax, rdx
    mov r13, rax           ; r13 = start_cycles
    
    ; Call measured function
    call r12
    
    ; Get end cycles
    rdtsc
    shl rdx, 32
    or rax, rdx            ; rax = end_cycles
    
    ; Calculate delta
    sub rax, r13           ; rax = end - start
    
    pop r13
    pop r12
    pop rbx
    ret

; ==============================================================================
; Main monitoring loop (optimized hot path)
; Args: 
;   RDI = iterations (uint64_t)
;   RSI = callback function pointer (void (*)(uint64_t cycles))
; ==============================================================================
asm_monitor_loop:
    push rbp
    mov rbp, rsp
    push rbx
    push r12
    push r13
    push r14
    push r15
    
    mov r14, rdi           ; r14 = iterations
    mov r15, rsi           ; r15 = callback
    xor r12, r12           ; r12 = counter
    
    ; Align stack for calls
    and rsp, -16
    
.loop:
    ; === HOT PATH START ===
    
    ; Prefetch next cache line
    lea rax, [monitor_state + 64]
    prefetcht0 [rax]
    
    ; Get timestamp (start)
    xor eax, eax
    cpuid
    rdtsc
    shl rdx, 32
    or rax, rdx
    mov r13, rax           ; r13 = start_cycles
    
    ; === MONITORED OPERATION ===
    ; (Your monitoring logic here - keeping minimal for performance)
    ; Example: memory fence + cache flush
    mfence
    clflush [monitor_state]
    mfence
    
    ; Get timestamp (end)
    rdtsc
    shl rdx, 32
    or rax, rdx            ; rax = end_cycles
    
    ; Calculate latency
    sub rax, r13           ; rax = latency in cycles
    
    ; === HOT PATH END ===
    
    ; Call callback with latency
    mov rdi, rax
    call r15
    
    ; Increment and check loop
    inc r12
    cmp r12, r14
    jl .loop
    
    ; Cleanup
    mov rsp, rbp
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    pop rbp
    ret

; ==============================================================================
; Fast memory copy with cache optimization
; Args:
;   RDI = dest
;   RSI = src
;   RDX = size (bytes)
; ==============================================================================
    global asm_fast_memcpy
asm_fast_memcpy:
    mov rcx, rdx
    shr rcx, 3             ; rcx = qwords
    rep movsq              ; Fast 64-bit copy
    
    mov rcx, rdx
    and rcx, 7             ; Remaining bytes
    rep movsb
    ret

; ==============================================================================
; Cache-aligned zero memory
; Args:
;   RDI = address
;   RSI = size (bytes)
; ==============================================================================
    global asm_zero_memory
asm_zero_memory:
    xor rax, rax
    mov rcx, rsi
    shr rcx, 3             ; qwords
    rep stosq
    
    mov rcx, rsi
    and rcx, 7
    rep stosb
    ret
