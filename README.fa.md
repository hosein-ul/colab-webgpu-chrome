# ⚡ پلتفرم ابری Google Chrome با شتاب کامل کارت گرافیک Tesla T4 (بدون VNC)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/modern-webrtc-stream/colab_chrome_stream.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WebGPU](https://img.shields.io/badge/WebGPU-Hardware%20Accelerated-green.svg)]()
[![NVIDIA T4](https://img.shields.io/badge/GPU-Tesla%20T4%20(15GB)-76B900.svg)]()

---

## 📌 لینک مستقیم نوت‌بوک در گوگل کولب

* **باز کردن مستقیم در Colab:** [اجرای `colab_chrome_stream.ipynb`](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/modern-webrtc-stream/colab_chrome_stream.ipynb)
* **برنچ فعال:** `modern-webrtc-stream`
* **سامانه ریموت دسکتاپ گوگل (روش دوم):** [remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)
* **پنل اتصال ریموت دسکتاپ:** [remotedesktop.google.com/access](https://remotedesktop.google.com/access)

---

## 🚀 ویژگی‌های کلیدی این معماری مدرن (حذف کامل VNC و دسکتاپ‌های سنگین)

روش‌های قدیمی VNC دارای تاخیر بالا، افت فریم و محیط‌های شلوغ دسکتاپ لینوکسی (مانند منوهای XFCE/GNOME) بودند. در این برنچ جدید، معماری بازطراحی کامل شد:

1. **نمایش اختصاصی خود پنجره گوگل کروم (بدون دسکتاپ):** دیگر هیچ نوار ابزار یا دسکتاپ اضافه لینوکسی لود نمی‌شود و شما مستقیماً با خود پنجره گوگل کروم تعامل دارید.
2. **شتاب سخت‌افزاری ۱۰۰٪ با Tesla T4:** نودهای کرنل لینوکس (`/dev/dri/card0` و `/dev/dri/renderD128`) و درایور Vulkan ICD رسمی انویدیا مستقیماً متصل شده و شتاب WebGPU و WebGL فعال است.
3. **تاخیر فوق‌العاده پایین (زیر ۵۰ میلی‌ثانیه):** پشتیبانی کامل از کلیک چپ، کلیک راست، اسکرول موس، درگ، تایپ کیبورد و کلیدهای میانبر.
4. **دو روش استریم نسل جدید:**
   - **روش اول (Chrome Ultra-Stream):** استریم مستقیم فریم‌های کامپوزیتور GPU از طریق وب‌سوکت و تانل امن کلودفلر، آماده اتصال در کمتر از ۲۰ ثانیه بدون نیاز به لاگین یا ساخت اکانت.
   - **روش دوم (Chrome Remote WebRTC):** استریم فوق‌روان ۶۰ فریم با پروتکل WebRTC و شبکه رله جهانی گوگل با تاخیر زیر ۳۰ میلی‌ثانیه.
5. **سلول اختصاصی تست و اعتبارسنجی:** بازرسی خودکار درایور انویدیا، وضعیت شتاب WebGPU، پروسه‌های فعال کروم و مانیتورینگ زنده توان پردازشی.

---

## ⚡ مقایسه دو روش موجود در نوت‌بوک

| ویژگی | روش اول: Chrome Ultra-Stream (مبتنی بر CDP WebSocket) | روش دوم: Chrome Remote WebRTC |
| :--- | :---: | :---: |
| **نوع استریم** | ارسال مستقیم فریم‌های GPU از طریق وب‌سوکت با کیفیت داینامیک | استریم ویدیویی ۶۰ فریم با پروتکل WebRTC و انکودر سخت‌افزاری H.264 |
| **دسکتاپ لینوکس** | ❌ **بدون دسکتاپ** (نمایش اختصاصی پنجره کروم در مرورگر) | ❌ **بدون دسکتاپ** (اجرای مستقیم کروم به صورت فول‌اسکرین) |
| **پروتکل ارتباطی** | TCP / WebSocket (۱۰۰٪ پایدار در تمام فایروال‌ها و NAT کولب) | WebRTC UDP/TCP با شبکه رله‌های اختصاصی گوگل |
| **تاخیر ورودی** | ۴۰ الی ۶۰ میلی‌ثانیه | **زیر ۳۰ میلی‌ثانیه (حس کامپیوتر محلی)** |
| **سرعت راه‌اندازی** | ⚡ **تک‌کلیک، زیر ۲۰ ثانیه (بدون نیاز به ثبت‌نام)** | تک‌کلیک همراه با پیست کردن کد اتصال گوگل |
| **شتاب سخت‌افزاری WebGPU** | **فعال (NVIDIA Tesla T4)** | **فعال (NVIDIA Tesla T4)** |
| **کنترل موس و کیبورد** | کامل (کلیک، درگ، اسکرول، کلیک راست، تایپ) | بومی سیستم‌عامل با کلیپ‌بورد دوطرفه |

---

## 🛠️ راهنمای سریع اجرا

1. وارد نوت‌بوک شوید: [لینک باز کردن در Google Colab](https://colab.research.google.com/github/hosein-ul/colab-webgpu-chrome/blob/modern-webrtc-stream/colab_chrome_stream.ipynb).
2. مطمئن شوید کارت گرافیک فعال است: `Runtime ➔ Change runtime type ➔ T4 GPU ➔ Save`.
3. سلول **روش اول** یا **روش دوم** را اجرا کنید.
4. سلول **تست و راستی‌آزمایی (سلول ۳)** را اجرا نمایید تا سلامت WebGPU و Tesla T4 تایید شود.
5. سلول **مانیتورینگ زنده (سلول ۴)** را برای مشاهده درصد استفاده کارت گرافیک اجرا نمایید.
