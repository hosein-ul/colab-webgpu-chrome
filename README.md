# 🚀 1-Click Hardware-Accelerated WebGPU Chrome on Google Colab (Tesla T4)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)

This repository provides an automated, 1-click solution to run official **Google Chrome with full hardware-accelerated WebGPU on NVIDIA Tesla T4** inside a Google Colab Linux runtime, streamed via low-latency interactive remote desktop (noVNC + Cloudflare Tunnel).

---

## ⚡ Quick Start (1-Click)

1. Click the **[Open In Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)** badge above.
2. In Colab menu, make sure **T4 GPU** is selected:  
   `Runtime` ➔ `Change runtime type` ➔ `T4 GPU` ➔ `Save`.
3. Click the **Play button** on the first cell (`🚀 1-Click Fast WebGPU Chrome Launcher`).
4. In ~50 seconds, a green **"ورود به مرورگر کروم ریموت"** button appears with your instant, secure tunnel link!

---

## 🛠️ Architecture & Under-the-Hood Fixes

Standard Google Colab containers restrict direct GPU rendering nodes and omit desktop Vulkan manifests by default. This script automatically:

* **Kernel DRM Nodes:** Creates missing `/dev/dri/card0`, `/dev/dri/renderD128`, and `/dev/nvidia-modeset` device nodes.
* **NVIDIA Vulkan ICD:** Generates `/etc/vulkan/icd.d/nvidia_icd.json` mapped to `libGLX_nvidia.so.0` and configures `ldconfig`.
* **Hardware WebGPU Flags:** Launches Google Chrome Stable with `--use-angle=vulkan --use-vulkan=native --enable-unsafe-webgpu` and hardware rasterization.
* **Low-Latency Streaming:** Pairs `Xvfb` (1280x720) with optimized `x11vnc` (-wait 5 -defer 5 -threads) and `noVNC` with JPEG/Tight compression.
* **Bidirectional Clipboard:** Bridges system and X11 clipboards via `autocutsel` for seamless `Ctrl+V` pasting.
* **Instant Tunnel:** Launches `cloudflared` to expose the interactive browser securely without opening ports or requiring accounts.

---

## 📊 Verified Metrics

* **GPU:** NVIDIA Tesla T4 (15,360 MiB VRAM)
* **WebGPU Adapter:** `vendor: "nvidia"`, `architecture: "turing"`, `isFallbackAdapter: false`
* **Mining Hashrate:** ~640+ MH/s on UniCred Proof-of-Work Keccak-256 WebGPU compute shaders.
* **Chrome Process:** Dedicated `C+G` (Compute + Graphics) process registered in `nvidia-smi`.

---

## 📜 License
MIT License
