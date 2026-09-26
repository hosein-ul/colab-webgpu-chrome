# 🚀 اجرای مرورگر Google Chrome با شتاب سخت‌افزاری WebGPU روی کارت گرافیک NVIDIA Tesla T4 در Google Colab

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
* **پنل دریافت کد احراز هویت گوگل:** [remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)
* **پنل ورود به ریموت دسکتاپ:** [remotedesktop.google.com/access](https://remotedesktop.google.com/access)

---

## 🌟 معرفی پروژه

این ریپازیتوری یک راه‌حل **جامع، خودکار و بهینه‌سازی شده** برای اجرای مرورگر رسمی **Google Chrome با شتاب کامل سخت‌افزاری WebGPU** روی کارت گرافیک **NVIDIA Tesla T4** در محیط ابری Google Colab است. با استفاده از این ابزار می‌توانید برنامه‌های سنگین وب۳، ماینینگ اثبات کار UniCred و شیدرهای سنگین ۳ بعدی را با بالاترین سرعت و بدون کوچک‌ترین گلوگاه پردازش کنید.

---

## ⚡ مقایسه دو روش استریم نوت‌بوک

| قابلیت | روش اول: تک‌کلیک در مرورگر (noVNC) | روش دوم: ریموت دسکتاپ گوگل (CRD) |
| :--- | :---: | :---: |
| **نحوه راه‌اندازی** | **فقط زدن دکمه Play (۱۰۰٪ تک‌کلیک)** | زدن Play همراه با کپی یک خط کد گوگل |
| **نیاز به اکانت؟** | **خیر (بدون نیاز به هیچ اکانت)** | بله (اکانت جیمیل گوگل) |
| **کیفیت و فریم‌ریت** | ۲۵ تا ۴۵ فریم بهینه‌شده | **۶۰ فریم بر ثانیه واقعی و ثابت** |
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
