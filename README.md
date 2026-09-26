# ⚡ Universal Hardware-Accelerated WebGPU Google Chrome on Google Colab (Tesla T4)

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
* **Google Remote Desktop Setup (Method 2):** [remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)
* **Google Remote Desktop Access Panel:** [remotedesktop.google.com/access](https://remotedesktop.google.com/access)

---

## 📖 Overview

Google Colab provides free access to high-performance **NVIDIA Tesla T4 GPUs (15,360 MiB VRAM)**, but default Colab containers restrict direct GPU rendering nodes and lack desktop Vulkan manifests. Standard headless browsers cannot handle interactive Web3 tasks that require browser wallet authorization (e.g., OKX Wallet, MetaMask, Phantom) or intensive WebGPU compute shaders.

This repository provides a universal, production-grade cloud solution:
1. **Unlocks Full Hardware WebGPU:** Binds kernel DRM nodes (`/dev/dri/card0`, `/dev/dri/renderD128`, `/dev/nvidia-modeset`) and installs official NVIDIA Vulkan ICD manifests mapped to `libGLX_nvidia.so.0`.
2. **Universal Web3 & Graphics Workloads:** Built for any high-compute task — WebGPU compute shaders (Keccak-256, Argon2, Blake3), WebGL 3D rendering, browser extensions (OKX, MetaMask), AI model inference in browser, and interactive graphics.
3. **Real-Time Step-by-Step Logging:** Displays live progress timers, command stdout, and validation checks directly in Colab output instead of hanging silently.
4. **Two Modern Remote Streaming Engines:**
   * **Method 1 (KasmVNC 1.5.0):** 100% 1-Click web-native streaming with lossy **WebP compression**, client-side cursor rendering (zero mouse lag), and dynamic framerates up to 60 FPS — zero setup, zero accounts, no token copying!
   * **Method 2 (Google Chrome Remote Desktop):** Ultra-fast 60 FPS WebRTC streaming over Google's internal datacenter backbone with sub-30ms latency.

---

## ⚡ Comparison of Streaming Engines

| Feature | Method 1: Modern KasmVNC 1.5.0 | Method 2: Google Chrome Remote Desktop |
| :--- | :---: | :---: |
| **Setup Complexity** | **1-Click (Play button only)** | 1-Click with Google Auth code |
| **Account Required?** | **None (Zero registration)** | Google Account |
| **Compression Engine** | **Dynamic WebP (up to 80% lighter)** | **Hardware VP8/VP9 Video** |
| **Frame Rate** | Up to 60 FPS (Adaptive) | **60 FPS Constant** |
| **Latency** | 40–80ms (Ultra-Low) | **Sub-30ms (Feels like local PC)** |
| **Cursor Response** | **Client-Side Rendered (0ms input lag)** | **Zero Input Lag (Client-rendered)** |
| **Clipboard** | Bidirectional Web Clipboard | **Native OS Clipboard (`Ctrl+C / Ctrl+V`)** |
| **Best For** | Instant 1-click launch, mobile, laptops | Extended sessions, maximum framerate |

---

## 🟢 Method 1: 1-Click Modern KasmVNC Stream (WebP)

Recommended when you want the fastest, zero-friction launch without visiting external sites:

1. Click the **[Open In Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)** badge.
2. In Colab, verify GPU runtime: `Runtime` ➔ `Change runtime type` ➔ **T4 GPU** ➔ `Save`.
3. Set your desired `TARGET_URL` (or leave default `https://google.com`).
4. Click the **Play button** on the first cell:  
   `🟢 [روش اول] راه‌اندازی ۱۰۰٪ تک‌کلیک با KasmVNC مدرن (Live Real-Time Logs)`.
5. Watch the real-time step timer (steps 1 to 6 complete in ~45 seconds).
6. A green button titled **"👉 ورود به مرورگر ابری (KasmVNC)"** appears. Click it to open your desktop directly in your browser!

---

## ⚡ Method 2: Google Chrome Remote Desktop (60 FPS WebRTC)

Recommended when you want crystal-clear 60 FPS video streaming with sub-30ms latency:

1. Open **[remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)** in a new tab.
2. Click **Begin** ➔ **Next** ➔ **Authorize**, then copy the **Debian Linux** command (starts with `DISPLAY= /opt/google/chrome-remote-desktop/start-host ...`).
3. In Colab, paste the command into `AUTH_COMMAND` in the second cell:  
   `⚡ [روش دوم] راه‌اندازی با Google Chrome Remote Desktop (Live Real-Time Logs)`.
4. Enter your 6-digit PIN (default `123456`), set `TARGET_URL`, and click **Play**.
5. Once initialized, click the blue button or visit **[remotedesktop.google.com/access](https://remotedesktop.google.com/access)**.
6. Click **colab-t4**, enter your PIN, and enjoy fluid 60 FPS desktop streaming!

---

## 🌐 High-Performance Web3 & Compute Workloads

This platform is completely agnostic and supports any decentralized compute task:

1. **Custom Target URL:** Set the `TARGET_URL` parameter in Colab before running, or navigate manually inside Chrome to any dApp.
2. **Install Any Wallet Extension:** Google Chrome has full WebStore access — install MetaMask, OKX Wallet, Phantom, Coinbase Wallet, etc., with one click.
3. **Heavy GPU/CPU Compute Tasks:**
   * **Compute Shaders:** Parallel WebGPU computing (e.g., Keccak-256, Argon2, matrix multiplication).
   * **Generative Graphics:** Heavy procedural WebGL/WebGPU generative art algorithms.
   * **AI In-Browser Inference:** WebGPU-accelerated models (ONNX Runtime Web, Transformers.js, WebLLM).
4. **Hardware Diagnostics:** Run the dedicated **GPU Diagnostics** cell to inspect live GPU compute utilization (%), VRAM, and temperature.

---

## 🛠️ Linux Kernel & Vulkan Architecture

Colab Docker runtimes do not expose DRM device nodes to userland browsers. This script automatically handles:

```
[Google Colab Container]
       │
       ├─► DRM Nodes: mknod /dev/dri/card0 (226, 0) + /dev/dri/renderD128 (226, 128)
       ├─► ModeSet:   mknod /dev/nvidia-modeset (195, 254)
       ├─► Vulkan:    /etc/vulkan/icd.d/nvidia_icd.json ──► libGLX_nvidia.so.0
       └─► Chrome:    --enable-features=Vulkan,DefaultANGLEVulkan,VulkanFromANGLE,WebGPUService
                      --use-angle=vulkan --enable-unsafe-webgpu
```

---

## 📊 Verified Hardware Benchmarks

* **GPU:** NVIDIA Tesla T4 (Turing TU104, 15,360 MiB VRAM)
* **WebGPU Adapter:** `vendor: "nvidia"`, `architecture: "turing"`, `isFallbackAdapter: false`
* **Process Type in nvidia-smi:** Dedicated `C+G` (Compute + Graphics) Chrome GPU process
* **Shader Compute Throughput:** Full hardware utilization via native Vulkan ICD backend

---

## 📜 License
MIT License.
