# 🚀 Hardware-Accelerated WebGPU Google Chrome on Google Colab (Tesla T4)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WebGPU](https://img.shields.io/badge/WebGPU-Hardware%20Accelerated-green.svg)]()
[![NVIDIA T4](https://img.shields.io/badge/GPU-Tesla%20T4%20(15GB)-76B900.svg)]()

> 🌐 **Language / زبان:** [🇬🇧 English Documentation](#-english-documentation) | [🇮🇷 راهنمای جامع فارسی](#-راهنمای-جامع-فارسی-persian-guide)

---

## 📌 Direct Links / لینک‌های دسترسی مستقیم

* **Open Notebook in Google Colab:** [Launch on Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)
* **GitHub Repository:** [hosein-ul/colab-webgpu-chrome](https://github.com/hosein-ul/colab-webgpu-chrome)
* **Google Remote Desktop Setup:** [remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)
* **Google Remote Desktop Web Access:** [remotedesktop.google.com/access](https://remotedesktop.google.com/access)

---

# 🇬🇧 English Documentation

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

# 🇮🇷 راهنمای جامع فارسی (Persian Guide)

## 🌟 معرفی پروژه

این ریپازیتوری یک راه‌حل **جامع، خودکار و بهینه‌سازی شده** برای اجرای مرورگر رسمی **Google Chrome با شتاب کامل سخت‌افزاری WebGPU** روی کارت گرافیک **NVIDIA Tesla T4** در محیط ابری Google Colab است. با استفاده از این ابزار می‌توانید برنامه‌های سنگین وب۳، ماینینگ اثبات کار UniCred و شیدرهای سنگین ۳ بعدی را با بالاترین سرعت و هش‌ریت پردازش کنید.

---

## ⚡ مقایسه دو روش استریم نوت‌بوک

| قابلیت | روش اول: تک‌کلیک در مرورگر | روش دوم: ریموت دسکتاپ گوگل |
| :--- | :---: | :---: |
| **نحوه راه‌اندازی** | **فقط زدن دکمه Play (۱۰۰٪ تک‌کلیک)** | زدن Play همراه با کپی یک خط کد گوگل |
| **نیاز به اکانت؟** | **خیر (بدون نیاز به هیچ اکانت)** | بله (اکانت جیمیل گوگل) |
| **کیفیت و فریم‌ریت** | ۲۵ تا ۴۵ فریم بهینه‌شده | **۶۰ فریم بر ثانیه واقعی و پایدار** |
| **میزان تاخیر (Latency)** | ۶۰ تا ۱۲۰ میلی‌ثانیه | **زیر ۳۰ میلی‌ثانیه (حس کامپیوتر محلی)** |
| **لگ نشانگر موس** | رندر محلی کلاینت (`-cursor arrow`) | **صفر میلی‌ثانیه (Client-Side Rendering)** |
| **کپی و پیست** | مستقیم دوطرفه با `autocutsel` | **مستقیم و یکپارچه با سیستم‌عامل (`Ctrl+V`)** |
| **مناسب برای** | تست سریع، استفاده در موبایل و لپ‌تاپ | جلسات طولانی، بالاترین دقت و روانی |

---

## 🟢 راهنمای اجرای روش اول (تک‌کلیک و بدون اکانت)

این روش برای کاربرانی است که می‌خواهند بدون معطلی و در سریع‌ترین زمان ممکن به مرورگر دسترسی پیدا کنند:

1. نوت‌بوک را از طریق لینک **[Open in Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)** باز کنید.
2. از منوی بالای کولب مطمئن شوید کارت گرافیک فعال است:  
   `Runtime` ➔ `Change runtime type` ➔ انتخاب **T4 GPU** ➔ دکمه `Save`.
3. روی دکمه **Play (اجرا)** سلول اول کلیک کنید:  
   `🟢 [روش اول - پیشنهادی] راه‌اندازی ۱۰۰٪ تک‌کلیک مرورگر وب (1-Click Instant Stream)`
4. حدود ۴۵ ثانیه منتظر بمانید؛ یک کادر سبز رنگ با دکمه **«👉 ورود به مرورگر کروم ریموت»** نمایش داده می‌شود.
5. روی دکمه کلیک کنید تا مرورگر کروم مستقیماً در یک تب جدید برای شما باز شود!

---

## ⚡ راهنمای اجرای روش دوم (ریموت دسکتاپ گوگل ۶۰ فریم)

این روش برای کاربرانی است که خواهان تصویر کریستالی ۶۰ فریم و تاخیر ناچیز هستند:

1. در یک تب جدید به آدرس **[remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)** بروید.
2. دکمه‌های **Begin** ➔ **Next** ➔ **Authorize** را بزنید و کدی که برای سیستم لینوکس دبیان می‌دهد (که با `DISPLAY= /opt/google/...` شروع می‌شود) را کپی کنید.
3. کد را در فیلد `AUTH_COMMAND` سلول دوم نوت‌بوک پیست کرده و دکمه **Play** را بزنید:  
   `⚡ [روش دوم - پیشرفته ۶۰ فریم] راه‌اندازی با Google Chrome Remote Desktop (WebRTC)`
4. یک پین دلخواه ۶ رقمی (پیش‌فرض `123456`) تعیین کنید.
5. پس از آماده‌سازی، روی دکمه آبی رنگ یا لینک **[remotedesktop.google.com/access](https://remotedesktop.google.com/access)** کلیک کنید.
6. روی دستگاه **`colab-t4`** کلیک کرده و با وارد کردن پین وارد دسکتاپ فوق‌العاده روان شوید!

---

## 🦊 راهنمای ماینینگ UniCred و اتصال کیف پول

1. در داخل مرورگر کروم ریموت، صفحه UniCred به طور پیش‌فرض باز می‌شود: `https://unicred.fun/#mine`.
2. روی دکمه **Connect Wallet** کلیک کرده و کیف پول خود (مانند OKX Wallet) را وصل کنید.
3. با کلیک روی **Mine**، محاسبات اثبات کار با نرخ بیش از **۶۴۰ مگاهش بر ثانیه** روی کارت گرافیک تسلا T4 آغاز می‌شود.
4. سلول آخر نوت‌بوک (**Real-Time GPU Monitor**) را اجرا کنید تا مصرف وات، دما و لود لحظه‌ای گرافیک را به صورت زنده تماشا کنید.

---

## 🛠️ رفع محدودیت‌های کانتینر ابری کولب

کانتینرهای پیش‌فرض گوگل کولب نودهای دسترسی مستقیم به گرافیک را برای برنامه‌های رابط کاربری مسدود می‌کنند. این پروژه به صورت خودکار موارد زیر را اعمال می‌کند:

1. **ایجاد کرنل‌نودهای رندرینگ:** ایجاد `/dev/dri/card0`، `/dev/dri/renderD128` و `/dev/nvidia-modeset` با مجوز کامل `0666`.
2. **پیکربندی رسمی Vulkan ICD:** نگاشت درایور انویدیا `libGLX_nvidia.so.0` در آدرس‌های استاندارد و به‌روزرسانی `ldconfig`.
3. **پرچم‌های شتاب‌دهنده سخت‌افزاری کروم:** اجرای گوگل کروم با فلگ‌های:  
   `--enable-features=Vulkan,DefaultANGLEVulkan,VulkanFromANGLE,WebGPUService --use-vulkan=native --use-angle=vulkan --enable-unsafe-webgpu --enable-gpu-rasterization --enable-zero-copy`
4. **سازگاری کامل با POSIX sh:** جایگزینی تمام ریدایرکت‌های ناسازگار با استاندارد `> /dev/null 2>&1` برای جلوگیری از خطاهای شل `dash` در اوبونتو.

---

## 📊 مشخصات سخت‌افزاری تایید شده

* **کارت گرافیک:** NVIDIA Tesla T4 با ۱۵,۳۶۰ مگابایت حافظه VRAM
* **شناسایی در کروم:** `vendor: "nvidia"`, `architecture: "turing"`, `isFallbackAdapter: false`
* **نوع پروسه در سیستم:** پروسه اختصاصی `C+G` (محاسباتی و گرافیکی)
* **نرخ هش‌ریت ماینینگ:** ۶۴۰ تا ۶۵۰ مگاهش بر ثانیه ثابت روی الگوریتم Keccak-256
* **توان مصرفی GPU:** ۶۸ تا ۷۲ وات در زمان ماینینگ کامل

---

## 📜 لایسنس
این پروژه به صورت متن‌باز و تحت مجوز **MIT** منتشر شده است.
