import os

ROOT_DIR = os.getcwd()

def generate_compiler_suite():
    print("🛠️  Injecting Cross-Compiler Suite for Debian 13 -> Windows/Linux...")
    
    base_path = os.path.join(ROOT_DIR, 'build_system')
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # 1. SETUP SCRIPT
    setup_sh = """#!/bin/bash
# Installs the Cross-Compiler toolchain on Debian 13
echo "🔧 Installing MinGW-w64 (Windows Compiler) and NASM (Assembler)..."
sudo apt-get update
sudo apt-get install -y build-essential mingw-w64 nasm make
echo "✅ Toolchain installed."
"""
    with open(os.path.join(base_path, 'install_toolchain.sh'), 'w') as f:
        f.write(setup_sh)
    os.chmod(os.path.join(base_path, 'install_toolchain.sh'), 0o755)

    # 2. MAKEFILE
    makefile = """
CC_LINUX = gcc
CC_WIN = x86_64-w64-mingw32-gcc
ASM = nasm
CFLAGS = -Wall -O2
WIN_GUI_FLAGS = -mwindows

all: linux_cli.elf windows_cli.exe windows_gui.exe

linux_cli.elf: core_logic.o wrapper_cli.c
\t$(CC_LINUX) $(CFLAGS) wrapper_cli.c core_logic.o -o bin/app_linux

windows_cli.exe: core_logic.obj wrapper_cli.c
\t$(CC_WIN) $(CFLAGS) wrapper_cli.c core_logic.obj -o bin/app_console.exe

windows_gui.exe: core_logic.obj wrapper_gui.c
\t$(CC_WIN) $(CFLAGS) $(WIN_GUI_FLAGS) wrapper_gui.c core_logic.obj -o bin/app_gui.exe

core_logic.o: core_logic.asm
\t$(ASM) -f elf64 core_logic.asm -o core_logic.o

core_logic.obj: core_logic.asm
\t$(ASM) -f win64 core_logic.asm -o core_logic.obj

clean:
\trm -f *.o *.obj bin/*
"""
    with open(os.path.join(base_path, 'Makefile'), 'w') as f:
        f.write(makefile)

    # 3. ASM CORE
    asm_code = """
global get_magic_number
section .text
get_magic_number:
    mov rax, 42
    ret
"""
    with open(os.path.join(base_path, 'core_logic.asm'), 'w') as f:
        f.write(asm_code)

    # 4. C CLI WRAPPER
    cli_code = """
#include <stdio.h>
extern int get_magic_number();
int main() {
    printf("FurryOS CLI Wrapper\\nMagic number from ASM: %d\\n", get_magic_number());
    return 0;
}
"""
    with open(os.path.join(base_path, 'wrapper_cli.c'), 'w') as f:
        f.write(cli_code)

    # 5. C GUI WRAPPER
    gui_code = """
#include <windows.h>
#include <stdio.h>
extern int get_magic_number();
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    char buffer[100];
    sprintf(buffer, "FurryOS Native GUI\\n\\nData from ASM Core: %d", get_magic_number());
    MessageBox(NULL, buffer, "FurryOS App", MB_OK | MB_ICONINFORMATION);
    return 0;
}
"""
    with open(os.path.join(base_path, 'wrapper_gui.c'), 'w') as f:
        f.write(gui_code)

    # Create bin directory
    if not os.path.exists(os.path.join(base_path, 'bin')):
        os.makedirs(os.path.join(base_path, 'bin'))
    
    print("✅ Compiler Suite Generated in '/build_system'")

if __name__ == "__main__":
    generate_compiler_suite()
