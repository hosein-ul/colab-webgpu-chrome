# 🚀 پلتفرم جامع اجرای Google Chrome با شتاب سخت‌افزاری WebGPU روی NVIDIA Tesla T4 در Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WebGPU](https://img.shields.io/badge/WebGPU-فعال%20سخت‌افزاری-green.svg)]()
[![NVIDIA T4](https://img.shields.io/badge/کارت%20گرافیک-تسلا%20T4%20(۱۵GB)-76B900.svg)]()
[![Language: English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)

> 📖 **مطالعه به زبان‌های دیگر:** [🇬🇧 English Documentation](README.md)

---

## 📌 لینک‌های دسترسی مستقیم

* **اجرای مستقیم در گوگل کولب:** [باز کردن در Google Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)
* **ریپازیتوری گیت‌هاب:** [hosein-ul/colab-webgpu-chrome](https://github.com/hosein-ul/colab-webgpu-chrome)
* **پنل دریافت کد احراز هویت گوگل (روش دوم):** [remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)
* **پنل ورود به ریموت دسکتاپ گوگل:** [remotedesktop.google.com/access](https://remotedesktop.google.com/access)

---

## 🌟 معرفی پروژه

این پلتفرم یک راه‌حل **همه‌منظوره، خودکار و با کارایی فوق‌العاده بالا** برای اجرای مرورگر رسمی **Google Chrome با شتاب کامل سخت‌افزاری WebGPU** روی پردازنده گرافیکی قدرتمند **NVIDIA Tesla T4 (با ۱۵ گیگابایت VRAM)** در بستر ابری Google Colab است.

### 🎯 کاربردهای اصلی (بدون محدودیت به یک پروژه خاص):
* **پردازش موازی و شیدرهای محاسباتی WebGPU:** اجرای محاسبات سنگین ریاضی و الگوریتم‌های شیدر درون مرورگر (مانند Keccak-256، Argon2، Blake3، کتابخانه‌های رمزنگاری و لایه‌های پردازش موازی).
* **رندرینگ سه‌بعدی و گرافیک وب (3D WebGL / WebGPU):** اجرای کدهای پیچیده WebGL و انیمیشن‌های سنگین جهت رندرینگ و شبیه‌سازی‌های بلادرنگ.
* **پردازش هوش مصنوعی درون مرورگر (In-Browser AI):** اجرای مدل‌های یادگیری ماشین مبتنی بر WebGPU با کتابخانه‌هایی نظیر ONNX Runtime Web، Transformers.js یا WebLLM.
* **نمایش زنده و ریل‌تایم وضعیت مراحل (Live Step-by-Step Logging):** کلیه مراحل نصب با تایمر دقیق ثانیه‌ای و لاگ لحظه‌ای نمایش داده می‌شوند تا کاربر دقیقاً از وضعیت اجرای سیستم آگاه باشد.

---

## ⚡ مقایسه دو موتور ریموت استریم نوت‌بوک

| قابلیت | روش اول: موتور مدرن KasmVNC 1.5.0 | روش دوم: ریموت دسکتاپ گوگل (CRD) |
| :--- | :---: | :---: |
| **نحوه راه‌اندازی** | **فقط زدن دکمه Play (۱۰۰٪ تک‌کلیک)** | زدن Play همراه با کپی یک خط کد گوگل |
| **نیاز به اکانت؟** | **خیر (بدون نیاز به هیچ اکانت یا کد)** | بله (اکانت جیمیل گوگل) |
| **تکنولوژی فشرده‌سازی** | **فشرده‌سازی داینامیک WebP (حجم تا ۸۰٪ کمتر)** | **کدک سخت‌افزاری VP8/VP9** |
| **کیفیت و فریم‌ریت** | تا ۶۰ فریم بر ثانیه تطبیق‌پذیر | **۶۰ فریم بر ثانیه واقعی و پایدار** |
| **میزان تاخیر (Latency)** | ۴۰ تا ۸۰ میلی‌ثانیه | **زیر ۳۰ میلی‌ثانیه (حس کامپیوتر محلی)** |
| **لگ نشانگر موس** | **رندر محلی کلاینت (صفر میلی‌ثانیه تاخیر)** | **صفر میلی‌ثانیه (Client-Side Rendering)** |
| **کپی و پیست** | مستقیم دوطرفه | **مستقیم و یکپارچه با سیستم‌عامل (`Ctrl+V`)** |
| **مناسب برای** | دسترسی سریع ۱ کلیکه، موبایل، لپ‌تاپ | کارهای فوق‌العاده حساس و طولانی |

---

## 🟢 راهنمای اجرای روش اول (KasmVNC تک‌کلیک و بدون اکانت)

این روش سریع‌ترین و ساده‌ترین مسیر برای شروع کار است؛ بدون نیاز به ورود به اکانت یا کپی کردن کدهای دستوری:

1. نوت‌بوک را از طریق لینک **[Open in Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/main/colab_chrome_webgpu.ipynb)** باز کنید.
2. از منوی بالای کولب مطمئن شوید کارت گرافیک فعال است:  
   `Runtime` ➔ `Change runtime type` ➔ انتخاب **T4 GPU** ➔ دکمه `Save`.
3. در صورت تمایل آدرس مورد نظر خود را در فیلد `TARGET_URL` وارد کنید (پیش‌فرض `https://google.com` است).
4. روی دکمه **Play (اجرا)** سلول اول کلیک کنید:  
   `🟢 [روش اول] راه‌اندازی ۱۰۰٪ تک‌کلیک با KasmVNC مدرن (Live Real-Time Logs)`
5. مراحل ۶ گانه با لاگ زنده و تایمر ثانیه‌ای اجرا می‌شوند (حدود ۴۵ ثانیه).
6. یک کادر سبز رنگ با دکمه **«👉 ورود به مرورگر ابری (KasmVNC)»** نمایش داده می‌شود؛ روی آن کلیک کنید تا دسکتاپ مدرن بدون لگ موس باز شود!

---

## ⚡ راهنمای اجرای روش دوم (ریموت دسکتاپ گوگل ۶۰ فریم)

این روش برای کاربرانی است که خواهان تصویر کریستالی ۶۰ فریم و تاخیر ناچیز WebRTC هستند:

1. در یک تب جدید به آدرس **[remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)** بروید.
2. دکمه‌های **Begin** ➔ **Next** ➔ **Authorize** را بزنید و کدی که برای سیستم لینوکس دبیان می‌دهد (که با `DISPLAY= /opt/google/...` شروع می‌شود) را کپی کنید.
3. کد را در فیلد `AUTH_COMMAND` سلول دوم نوت‌بوک پیست کرده و دکمه **Play** را بزنید:  
   `⚡ [روش دوم] راه‌اندازی با Google Chrome Remote Desktop (Live Real-Time Logs)`
4. یک پین دلخواه ۶ رقمی (پیش‌فرض `123456`) تعیین کرده و آدرس `TARGET_URL` را مشخص کنید.
5. پس از تکمیل مراحل، روی دکمه آبی رنگ یا لینک **[remotedesktop.google.com/access](https://remotedesktop.google.com/access)** کلیک کنید.
6. روی دستگاه **`colab-t4`** کلیک کرده و با وارد کردن پین وارد دسکتاپ فوق‌العاده روان شوید!

---

## 🌐 اجرای پروژه‌های وب۳، برنامه‌های محاسباتی و اتصال ولت

در هر دو روش، مرورگر Google Chrome رسمی با دسترسی کامل به Chrome Web Store لود می‌شود:

1. **نصب آسان هرگونه کیف پول:** به راحتی افزونه‌های OKX Wallet، MetaMask، Phantom یا Rabby را از کروم وب‌استور نصب کنید.
2. **شتاب سخت‌افزاری کامل شیدرهای WebGPU:** تمام فلگ‌های شتاب‌دهنده گرافیکی از جمله `--enable-unsafe-webgpu` و `--use-vulkan=native` فعال هستند.
3. **بررسی سلامت و بنچمارک سخت‌افزار:** سلول سوم نوت‌بوک (**GPU Diagnostics**) را اجرا کنید تا وضعیت درایورها، درصد لود پردازشی GPU، حافظه VRAM و دمای کارت گرافیک تسلا T4 را رصد نمایید.

---

## 🛠️ معماری کرنل لینوکس و رفع محدودیت‌های کانتینر

کانتینرهای ابری کولب به طور پیش‌فرض نودهای مستقیم به GPU را به مرورگر متصل نمی‌کنند. این اسکریپت اقدامات زیر را به صورت سیستمی پیاده‌سازی می‌کند:

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

## 📊 مشخصات سخت‌افزاری تایید شده

* **کارت گرافیک:** NVIDIA Tesla T4 با ۱۵,۳۶۰ مگابایت حافظه اختصاصی VRAM
* **شناسایی در مرورگر کروم:** `vendor: "nvidia"`, `architecture: "turing"`, `isFallbackAdapter: false`
* **نوع پروسه در سیستم:** پروسه اختصاصی `C+G` (Compute + Graphics)
* **نرخ هش‌ریت شیدرهای محاسباتی (مانند Keccak-256):** بیش از ۶۴۰ مگاهش بر ثانیه پایدار
* **توان مصرفی GPU:** ۶۸ تا ۷۲ وات زیر فشار کامل پردازشی

---

## 📜 لایسنس
این پروژه به صورت متن‌باز و تحت مجوز **MIT** منتشر شده است.
