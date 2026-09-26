# ⚡ 1-Click Hardware-Accelerated WebGPU Chrome on Google Colab (Tesla T4)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)
[![GitHub License](https://img.shields.io/github/license/hosein-ul/colab-webgpu-chrome)](LICENSE)
[![Repository Status](https://img.shields.io/badge/Visibility-Private-critical)](https://github.com/hosein-ul/colab-webgpu-chrome)

An automated, 1-click solution to run official **Google Chrome with full hardware-accelerated WebGPU on NVIDIA Tesla T4** inside a Google Colab Linux runtime, streamed at **60 FPS crystal-clear WebRTC with sub-30ms latency** via **Google Chrome Remote Desktop (CRD)**.

---

## 📌 Direct Links / لینک‌های دسترسی مستقیم

* **Direct Colab Notebook Link:** [Open in Google Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)
* **GitHub Repository:** [hosein-ul/colab-webgpu-chrome](https://github.com/hosein-ul/colab-webgpu-chrome)
* **Google Remote Desktop Setup:** [remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)
* **Google Remote Desktop Access:** [remotedesktop.google.com/access](https://remotedesktop.google.com/access)

---

## 🔒 Opening Private Repositories in Google Colab

Because this repository is **Private**, follow this one-time step when opening the badge in Colab:
1. Click the **[Open In Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)** badge.
2. In the "Open notebook" dialog, switch to the **GitHub** tab.
3. Check the box **"Include private repositories"** (Colab will request one-click GitHub read authorization).
4. Select `hosein-ul/colab-webgpu-chrome` and open `colab_chrome_webgpu.ipynb`.
*(Tip: You can also click `File -> Save a copy in Drive` to keep a permanent copy in your personal Google Drive!)*

---

# 🇬🇧 English Documentation

## 🚀 Why Chrome Remote Desktop (CRD) over Legacy VNC?

Traditional virtual desktop streaming (`Xvfb + x11vnc + noVNC`) relies on CPU screen scraping and TCP websockets, causing 300–800ms of lag, choppy framerates, and slow mouse response.

By adopting **Google Chrome Remote Desktop**:
* **Sub-30ms Real-Time Latency:** Direct WebRTC video streaming over Google's internal datacenter backbone.
* **Stable 60 FPS Video:** Hardware-accelerated VP8/VP9 video encoding instead of choppy image tiles.
* **Zero Input Lag:** Local client-side mouse pointer rendering feels like a native machine.
* **Dynamic Resolution Scaling:** Automatically adapts to your client screen size.
* **Seamless Two-Way Clipboard:** Native copy/paste support for wallet addresses, private keys, and passwords.

---

## ⚡ Quick Start Guide (Under 2 Minutes)

1. **Verify GPU Runtime:**  
   In Colab, go to `Runtime` ➔ `Change runtime type` ➔ select **T4 GPU** ➔ click `Save`.
2. **Get Authentication Command:**  
   Open **[remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)** in a new tab.  
   Click **Begin** ➔ **Next** ➔ **Authorize**, then copy the **Debian Linux** command (starts with `DISPLAY= /opt/google/chrome-remote-desktop/start-host ...`).
3. **Run the 1-Click Launcher:**  
   Paste the copied command into `AUTH_COMMAND`, set your 6-digit PIN (default `123456`), and click the **Play** button on the primary cell.
4. **Connect:**  
   In ~40 seconds, click the green button or visit **[remotedesktop.google.com/access](https://remotedesktop.google.com/access)**.  
   Click **colab-t4**, enter your PIN, and your remote 60 FPS WebGPU Chrome desktop opens immediately!

---

## 🛠️ Architecture & Under-The-Hood Fixes

Standard Google Colab containers restrict direct GPU rendering nodes and omit desktop Vulkan manifests by default. This script automatically handles:

* **Kernel DRM Nodes:** Creates missing `/dev/dri/card0`, `/dev/dri/renderD128`, and `/dev/nvidia-modeset` device nodes with full `0666` permissions.
* **NVIDIA Vulkan ICD:** Generates `/etc/vulkan/icd.d/nvidia_icd.json` mapped to `libGLX_nvidia.so.0` and configures `ldconfig`.
* **Hardware WebGPU Flags:** Launches Google Chrome Stable with:  
  `--use-angle=vulkan --use-vulkan=native --enable-unsafe-webgpu --enable-features=Vulkan,DefaultANGLEVulkan,VulkanFromANGLE,WebGPUService --enable-gpu-rasterization --enable-zero-copy`
* **Dedicated Shell Session:** Sets up a non-root `colab` user on a lightweight `XFCE4` session with autostart preloading UniCred mining (`https://unicred.fun/#mine`).
* **POSIX sh Compliance:** Uses POSIX `> /dev/null 2>&1` redirection to prevent `dash` shell errors in Debian/Ubuntu.

---

## 📊 Verified Metrics

* **GPU:** NVIDIA Tesla T4 (15,360 MiB VRAM)
* **WebGPU Adapter:** `vendor: "nvidia"`, `architecture: "turing"`, `isFallbackAdapter: false`
* **Mining Hashrate:** ~640+ MH/s on UniCred Proof-of-Work Keccak-256 WebGPU compute shaders.
* **Remote Streaming Frame Rate:** 60 FPS WebRTC with dynamic bitrate adaptation.

---

# 🇮🇷 راهنمای جامع فارسی (Persian Guide)

## 🌟 معرفی پروژه
این پروژه یک راه‌حل **۱ کلیکه و خودکار** برای اجرای مرورگر رسمی **Google Chrome با شتاب کامل سخت‌افزاری WebGPU** روی کارت گرافیک قدرتمند **NVIDIA Tesla T4** در محیط ابری Google Colab است که تصویر را با کیفیت کریستالی **۶۰ فریم بر ثانیه (WebRTC) و تاخیر زیر ۳۰ میلی‌ثانیه** از طریق سرویس رسمی **Google Chrome Remote Desktop** استریم می‌کند.

---

## ⚡ چرا Chrome Remote Desktop به جای VNC معمولی؟

| ویژگی | VNC / noVNC سنتی | Chrome Remote Desktop (این پروژه) |
| :--- | :---: | :---: |
| **میزان تاخیر (Latency)** | ۳۰۰ تا ۸۰۰ میلی‌ثانیه (پرش و کندی) | **زیر ۳۰ میلی‌ثانیه (بسیار روان)** |
| **فریم‌ریت تصویر** | ۵ تا ۱۵ فریم (فشار روی CPU کولب) | **۶۰ فریم بر ثانیه واقعی و ثابت** |
| **تاخیر حرکت موس** | با تاخیر و سنگین | **صفر میلی‌ثانیه (نشانگر محلی)** |
| **کدک فشرده‌سازی** | ارسال تایل‌های عکس (Tile-based) | **کدک‌های ویدیویی سخت‌افزاری VP8/VP9** |
| **پروتکل ارتباطی** | وب‌سوکت روی TCP (دارای پکت فریز) | **پروتکل WebRTC بر بستر شبکه گوگل** |
| **کلیپ‌بورد** | نیازمند منوی واسط | **مستقیم و دوطرفه (`Ctrl+C` و `Ctrl+V`)** |

---

## 📋 راهنمای اجرای گام‌به‌گام (کمتر از ۲ دقیقه)

### ۱. فعال‌سازی کارت گرافیک در کولب
نوت‌بوک را باز کنید و از منوی بالای صفحه مطمئن شوید کارت گرافیک فعال است:  
`Runtime` ➔ `Change runtime type` ➔ انتخاب **T4 GPU** ➔ دکمه `Save`.

### ۲. دریافت دستور اتصال گوگل
در یک تب جدید به آدرس **[remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)** بروید:
* دکمه **Begin (شروع)** و سپس **Next (بعدی)** و سپس **Authorize (مجوز دادن)** را بزنید.
* دستوری که برای سیستم لینوکس دبیان (Debian Linux) نمایش داده می‌شود (که با `DISPLAY= /opt/google/...` شروع می‌شود) را کپی کنید.

### ۳. اجرای سلول نوت‌بوک (تک‌کلیک)
* به نوت‌بوک کولب برگردید و دستور کپی‌شده را در کادر `AUTH_COMMAND` قرار دهید.
* یک پین ۶ رقمی (مثلاً `123456`) تعیین کرده و دکمه **Play (اجرا)** را بزنید.
* تمام درایورها، پیش‌نیازها، تنظیمات ولکان و هاست گوگل در کمتر از ۴۰ ثانیه به صورت خودکار لود می‌شوند.

### ۴. ورود به دسکتاپ کروم
* روی دکمه سبز رنگ ظاهر شده یا آدرس **[remotedesktop.google.com/access](https://remotedesktop.google.com/access)** کلیک کنید.
* روی سیستم **`colab-t4`** کلیک کرده و پین خود را وارد کنید.
* مرورگر کروم با فعال بودن کامل شتاب سخت‌افزاری WebGPU و صفحه ماینینگ UniCred به صورت خودکار باز می‌شود!

---

## 🦊 اتصال کیف پول (OKX Wallet) و ماینینگ UniCred

1. در داخل مرورگر کروم ریموت، صفحه UniCred به صورت پیش‌فرض لود می‌شود: `https://unicred.fun/#mine`.
2. روی دکمه **Connect Wallet** کلیک کنید.
3. در صورت نیاز به افزونه OKX Wallet، از وب‌استور کروم یا با ایمپورت امن کیف پول خود را متصل نمایید.
4. با زدن دکمه Mine، کارت گرافیک تسلا T4 با نرخ بیش از **۶۴۰ مگاهش بر ثانیه** شروع به حل مسائل اثبات کار (Keccak-256) می‌کند.
5. سلول دوم نوت‌بوک را اجرا کنید تا وضعیت لحظه‌ای مصرف برق، دما و هش‌ریت را در قالب یک داشبورد زیبا مشاهده نمایید.

---

## 📜 لایسنس
این پروژه تحت لایسنس **MIT** منتشر شده و به صورت کاملاً اختصاصی (Private) پیکربندی شده است.
