# ⚡ Hardware-Accelerated WebGPU Google Chrome on Google Colab (Tesla T4)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WebGPU](https://img.shields.io/badge/WebGPU-Hardware%20Accelerated-green.svg)]()
[![NVIDIA T4](https://img.shields.io/badge/GPU-Tesla%20T4%20(15GB)-76B900.svg)]()
[![Language: Persian](https://img.shields.io/badge/Language-فارسی-blue.svg)](README.fa.md)

> 📖 **Read in other languages:** [🇮🇷 راهنمای فارسی (Persian Guide)](README.fa.md)

---

## 📌 Direct Links

* **Open Notebook in Google Colab:** [Launch on Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)
* **GitHub Repository:** [hosein-ul/colab-webgpu-chrome](https://github.com/hosein-ul/colab-webgpu-chrome)
* **Google Remote Desktop Setup:** [remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)
* **Google Remote Desktop Web Access:** [remotedesktop.google.com/access](https://remotedesktop.google.com/access)

---

## 📖 Overview

Google Colab provides access to enterprise **NVIDIA Tesla T4 GPUs (15,360 MiB VRAM)**, but standard Colab Docker containers restrict direct GPU rendering nodes and lack desktop Vulkan manifests by default. Furthermore, running headless browsers for heavy Web3 computational tasks (such as Proof-of-Work WebGPU NFT mining or 3D WebGL/WebGPU shaders) requires an interactive visual environment to connect browser wallets (e.g., OKX Wallet, MetaMask).

This repository provides an automated, turn-key solution that:
1. **Unlocks Native Hardware WebGPU:** Configures missing kernel DRM nodes (`/dev/dri/card0`, `/dev/dri/renderD128`, `/dev/nvidia-modeset`) and builds official NVIDIA Vulkan ICD manifests mapped to `libGLX_nvidia.so.0`.
2. **Offers Two Remote Streaming Engines:**
   * **Method 1 (1-Click Instant Stream):** In-browser low-latency noVNC streaming with zero configuration, zero accounts, and zero token copying.
   * **Method 2 (60 FPS WebRTC):** Ultra-fast, crystal-clear Google Chrome Remote Desktop (CRD) with sub-30ms latency, native client cursor, and dynamic resolution scaling.

---

## ⚡ Comparison of Both Methods

| Feature | Method 1: 1-Click Browser Stream | Method 2: Google Chrome Remote Desktop |
| :--- | :---: | :---: |
| **Setup Complexity** | **1-Click (Play button only)** | 1-Click with Google Auth code |
| **Account Required?** | **None** | Google Account |
| **Streaming Protocol** | WebSocket (noVNC / Cloudflare) | **WebRTC over Google Backbone** |
| **Frame Rate** | 25–45 FPS (Adaptive) | **60 FPS Constant** |
| **Latency** | 60–120ms (Tuned Low-Latency) | **Sub-30ms (Feels like local PC)** |
| **Cursor Lag** | Local client cursor (`-cursor arrow`) | **Zero Input Lag (Client-rendered)** |
| **Clipboard** | Bidirectional (`autocutsel`) | **Native OS Clipboard (`Ctrl+C / Ctrl+V`)** |
| **Best For** | Instant testing, mobile, quick minting | High-framerate, extended sessions, precision |

---

## 🟢 Method 1: 1-Click Instant In-Browser Stream

Recommended when you want the fastest, zero-friction experience without visiting any other website:

1. Click the **[Open In Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)** badge.
2. In Colab, verify that GPU is enabled: `Runtime` ➔ `Change runtime type` ➔ **T4 GPU** ➔ `Save`.
3. Click the **Play button** on the first cell:  
   `🟢 [روش اول - پیشنهادی] راه‌اندازی ۱۰۰٪ تک‌کلیک مرورگر وب (1-Click Instant Stream)`.
4. Wait ~45 seconds. A green button titled **"👉 ورود به مرورگر کروم ریموت"** will appear.
5. Click it to open your remote WebGPU Chrome desktop directly inside a new browser tab!

---

## ⚡ Method 2: Google Chrome Remote Desktop (60 FPS WebRTC)

Recommended when you want the ultimate smoothness, zero latency, and 60 FPS performance:

1. Open **[remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)** in a new tab.
2. Click **Begin** ➔ **Next** ➔ **Authorize**, then copy the **Debian Linux** command (starts with `DISPLAY= /opt/google/chrome-remote-desktop/start-host ...`).
3. In Colab, paste the command into `AUTH_COMMAND` in the second cell:  
   `⚡ [روش دوم - پیشرفته ۶۰ فریم] راه‌اندازی با Google Chrome Remote Desktop (WebRTC)`.
4. Set your 6-digit PIN (default `123456`) and click **Play**.
5. Once started, click the blue button or visit **[remotedesktop.google.com/access](https://remotedesktop.google.com/access)**.
6. Click **colab-t4**, enter your PIN, and your 60 FPS WebGPU desktop is live!

---

## 🦊 Web3 & UniCred PoW Mining Setup

Both methods launch Google Chrome with all hardware WebGPU flags enabled and preload UniCred mining (`https://unicred.fun/#mine`):

1. Click **Connect Wallet** on the UniCred page.
2. Connect your wallet (e.g. OKX Wallet).
3. Click **Mine** to start the Proof-of-Work Keccak-256 compute shaders.
4. Run the **Real-Time GPU Monitor** cell in Colab to view live GPU utilization (%), VRAM, temperature, and wattage!

---

## 🛠️ Linux Kernel & Vulkan Architecture

Standard Colab runtimes do not expose DRM device nodes to userland browsers. This script automatically handles:

```
[Google Colab Container]
       │
       ├─► DRM Nodes: mknod /dev/dri/card0 (226, 0) + /dev/dri/renderD128 (226, 128)
       ├─► ModeSet:   mknod /dev/nvidia-modeset (195, 254)
       ├─► Vulkan:    /etc/vulkan/icd.d/nvidia_icd.json ──► libGLX_nvidia.so.0
       └─► Chrome:    --enable-features=Vulkan,DefaultANGLEVulkan,VulkanFromANGLE,WebGPUService
                      --use-vulkan=native --use-angle=vulkan --enable-unsafe-webgpu
```

---

## 📊 Verified Hardware Benchmarks

* **GPU:** NVIDIA Tesla T4 (Turing TU104, 15,360 MiB VRAM)
* **WebGPU Adapter:** `vendor: "nvidia"`, `architecture: "turing"`, `isFallbackAdapter: false`
* **Process Type in nvidia-smi:** Dedicated `C+G` (Compute + Graphics) Chrome GPU process
* **Mining Hashrate:** ~640+ MH/s sustained Keccak-256 WebGPU compute shaders
* **Power Draw:** 68–72 W under full mining load

---

## 📜 License
MIT License.
