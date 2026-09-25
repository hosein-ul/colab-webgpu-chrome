# ⚡ 60 FPS Hardware-Accelerated WebGPU Chrome on Google Colab (Tesla T4)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)
[![GitHub License](https://img.shields.io/github/license/hosein-ul/colab-webgpu-chrome)](LICENSE)

An automated solution to run official **Google Chrome with full hardware-accelerated WebGPU on NVIDIA Tesla T4** inside a Google Colab Linux runtime, streamed at **60 FPS crystal-clear WebRTC with sub-30ms latency** via **Google Chrome Remote Desktop (CRD)**.

---

## 🚀 Why Chrome Remote Desktop (CRD) instead of Legacy VNC?

Traditional VNC / noVNC setups rely on software frame polling (`x11vnc`), CPU tile compression, and TCP websockets which suffer from high latency (300–800ms) and sluggish input lag.

By migrating to **Chrome Remote Desktop**:
* **Sub-30ms Real-Time Latency:** Direct WebRTC streaming over Google's internal low-latency backbone.
* **Stable 60 FPS Video:** Hardware-accelerated VP8/VP9 video encoding instead of choppy image tiles.
* **Zero Input Lag:** Local client-side mouse pointer rendering feels like a native local machine.
* **Adaptive Dynamic Resolution:** Automatically matches your client monitor dimensions and scale.
* **Seamless Two-Way Clipboard:** Native copy/paste support for wallet addresses, passwords, and text.

---

## ⚡ Quick Start Guide (Takes ~2 Minutes)

### 1. Open the Notebook
Click the **[Open In Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)** badge.

### 2. Verify GPU Runtime
Ensure **T4 GPU** is selected:  
`Runtime` ➔ `Change runtime type` ➔ `T4 GPU` ➔ `Save`.

### 3. Step 1: Install Drivers & Remote Desktop (~45s)
Click **Play** on the first cell:  
`⚡ [1/2] پیکربندی سخت‌افزاری تسلا T4، درایورهای Vulkan و پکیج‌های ریموت دسکتاپ`

### 4. Step 2: Authenticate & Connect
1. In another browser tab, open [remotedesktop.google.com/headless](https://remotedesktop.google.com/headless).
2. Click **Begin** ➔ **Next** ➔ **Authorize**.
3. Copy the command for **Debian Linux** (starts with `DISPLAY= /opt/google/chrome-remote-desktop/start-host ...`).
4. Paste it into the `AUTH_COMMAND` field of cell **[2]** in Colab, choose a 6-digit PIN (e.g. `123456`), and click **Play**.
5. Open [remotedesktop.google.com/access](https://remotedesktop.google.com/access).
6. Click on **colab-t4**, enter your PIN, and enjoy 60 FPS remote WebGPU Chrome!

---

## 🛠️ Architecture & Under-the-Hood Fixes

Standard Google Colab containers restrict direct GPU rendering nodes and omit desktop Vulkan manifests by default. This script automatically:

* **Kernel DRM Nodes:** Creates missing `/dev/dri/card0`, `/dev/dri/renderD128`, and `/dev/nvidia-modeset` device nodes with full non-root permissions.
* **NVIDIA Vulkan ICD:** Generates `/etc/vulkan/icd.d/nvidia_icd.json` mapped to `libGLX_nvidia.so.0` and configures `ldconfig`.
* **Hardware WebGPU Flags:** Launches Google Chrome Stable with `--use-angle=vulkan --use-vulkan=native --enable-unsafe-webgpu` and hardware rasterization.
* **Native Desktop Shell:** Configures a dedicated non-root user (`colab`) on a lightweight `XFCE4` session with automatic Chrome WebGPU autostart.
* **Fallback Web Mode:** Also includes a standalone in-browser noVNC + Cloudflare Quick Tunnel cell for testing without a Google account.

---

## 📊 Verified Metrics

* **GPU:** NVIDIA Tesla T4 (15,360 MiB VRAM)
* **WebGPU Adapter:** `vendor: "nvidia"`, `architecture: "turing"`, `isFallbackAdapter: false`
* **Mining Hashrate:** ~640+ MH/s on UniCred Proof-of-Work Keccak-256 WebGPU compute shaders.
* **Remote Streaming Frame Rate:** 60 FPS WebRTC with dynamic bitrate adaptation.

---

## 📜 License
MIT License
