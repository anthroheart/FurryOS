# 🐾 FurryOS: Sovereign Universe Overview

### A Biological Framework for Operating System Architecture

> **"Don't just install an OS. Grow one."**

---

## 🌍 The Concept

FurryOS is not a standard Linux distribution. It is a **Declarative Framework** (a "Genome") that allows you to build a custom, sovereign operating system based on **Debian 13 (Trixie)**.

Instead of downloading a pre-made ISO that someone else configured, you define the "DNA" of the system in a YAML file. Our builder tool (the "Ribosome") reads that DNA and compiles a bootable Hybrid ISO tailored exactly to your needs.

### 🛑 The Problem: "Linux Pain Points"

We built this because modern Linux has introduced too many "papercuts" that frustrate users:

- **Python Pain:** `pip install` is blocked by "EXTERNALLY-MANAGED" errors.
- **Pathing Pain:** Filenames with spaces or trailing slashes causing script errors.
- **Driver Pain:** Guessing which NVIDIA/WiFi firmware you need.
- **Privacy Pain:** Telemetry and tracking baked into the kernel.

### ✅ The Solution: The "Omniscient" Builder

FurryOS fixes these issues **during the build process**. The builder enforces strict rules (the "Taxonomy") to ensure the resulting OS is clean, functional, and devoid of the usual headaches.

---

## 🧬 The Taxonomy (How It Works)

We organize the OS like a living organism. This structure is defined in `GENOME.yaml`.

| Rank        | Meaning                   | Example                                              |
| :---------- | :------------------------ | :--------------------------------------------------- |
| **Kingdom** | The Target Hardware       | `Desktop`, `Server`, `Raspberry Pi`                  |
| **Phylum**  | The Foundation            | `Debian 13`, `Kernel 6.12+`                          |
| **Genus**   | The Core Organs (Modules) | `Heartbeat` (C++ Orchestrator), `Vault` (Encryption) |
| **Species** | **YOU** (The User Config) | Your username, your timezone, your software choices. |

---

## 🎮 The 4 Experience Levels (The "Order")

FurryOS respects your skill level. You choose your "Order" in the config, and the installer adapts to you:

1.  **👵 Granny Mode (Beginner)**

    - **Philosophy:** "Just make it work."
    - **Action:** Fully automated. No questions asked. Encrypts disk, installs updates, sets up WiFi.

2.  **🎮 Gamer Mode (Intermediate)**

    - **Philosophy:** "I want performance."
    - **Action:** Guided setup. Asks about NVIDIA/AMD drivers, installs Steam/Proton/Lutris automatically.

3.  **💻 Hacker Mode (Advanced)**

    - **Philosophy:** "Don't touch my config."
    - **Action:** You control the partitioning, the init system, and the packages. The safety rails are off.

4.  **👻 Ghost Mode (Paranoid)**
    - **Philosophy:** "I was never here."
    - **Action:** Privacy extreme. MAC address randomization, telemetry blocking, and detached header encryption.

---

## 🛠️ For Developers: The "Ribosome" Compiler

If you are contributing to the build tools, your job is to create the **Compiler** (in Python/Bash/C++) that connects the YAML to the Kernel.

**The Compiler's Job:**

1.  **Parse** the `GENOME.yaml` and `USER_CONFIG.yaml`.
2.  **Hydrate** the workspace by pulling the Debian 13 Kernel (`vmlinuz`) and Body (`filesystem.squashfs`).
3.  **Compile** the custom C++ modules (Heartbeat, Healer).
4.  **Inject** the specific "Pain Point" fixes (deleting PEP 668 flags, renaming files).
5.  **Master** the final Hybrid ISO using `xorriso`.

_See `COMPILER_SPEC.md` for the technical requirements._

---

## 👤 For Users: Getting Started

1.  **Download the Framework:** Clone this repo.
2.  **Add the Core:** Place your preferred Debian kernel files in the `/kernel/` folder (or let the builder download them).
3.  **Edit your DNA:** Open `USER_CONFIG.yaml` and choose your profile (e.g., "Gamer").
4.  **Build:** Run the launcher script.
    ```bash
    sudo python3 launcher.py
    ```
5.  **Boot:** Flash the resulting `furryos.iso` to a USB stick. You will see the **Orange Pulsing Border** indicating you are in Live Mode.

---

## ⚓ Provenance & Trust

- **Anchored:** This architecture is timestamped to **Bitcoin Block 929481**.
- **Source:** All assets are verified against [anthroheart.com](https://anthroheart.com).
- **License:** MIT. This is a Sovereign Universe—you own your OS.
