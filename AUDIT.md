# 🧾 گزارش Audit کامل پروژه `chrome-colab`

**مخزن بررسی‌شده:** `https://github.com/rodigers/chrome-colab`
**فایل‌ها:** `colab_chrome_webgpu.ipynb` (۴ سلول)، `README.md`
**روش بررسی:** خواندن مستقیم کد (parse واقعی فایل `.ipynb` و کامپایل هر سلول)، مقایسه با مخزن بالادستی (`hosein-ul/colab-chrome-webgpu`)، بررسی سورس واقعی KasmVNC و اسکریپت‌های Chrome Remote Desktop، و بررسی مستندات رسمی.

> ⚠️ این نسخه از نوتبوک **اصلاح‌شده** در همین مخزن قرار گرفته است. نسخه‌ی اصلی برای مقایسه در `_audit/colab_chrome_webgpu.original.ipynb` نگه داشته شده است.

---

## خلاصه اجرایی

هر دو روش به‌دلیل ترکیب چند باگ «محیط غیرتعاملی» (non-interactive) و «مسیر خانه‌ی کاربر» (HOME) شکست می‌خورند:

| روش | علت ریشه‌ای (Critical) | علت‌های ثانویه |
| :--- | :--- | :--- |
| **روش ۱ (KasmVNC)** | اجرای `vncserver` در حالت غیرتعاملی، در حالی که `command_line.prompt` پیش‌فرض `true` است → `vncserver` سعی می‌کند برای ساخت کاربر و **انتخاب Desktop Environment** تعاملی Prompt کند و در کولب هنگ/خطا می‌دهد. | ۱) `sudo -u colab` متغیر `HOME` را تغییر نمی‌دهد → `vncserver` از `/root/.vnc` می‌خواند و xstartup و کانفیگ کاربر نادیده گرفته می‌شود. ۲) ساخت رمز با `echo -e` زیر `/bin/sh=dash` قابل اتکا نیست → کاربر ساخته نمی‌شود. ۳) KasmVNC خوانا بودن گواهی SSL را حتی با `require_ssl:false` اجبار می‌کند. |
| **روش ۲ (Chrome Remote Desktop)** | اجرای سرویس هاست: در کولب **systemd وجود ندارد** و مکانیزم استاندارد CRD (سرویس user) در دسترس نیست؛ در کد اصلی خطا با `\|\| true` قورت داده می‌شود و فقط با `ps` چک می‌شود. | ۱) تحویل PIN به `start-host` فقط از طریق stdin انجام می‌شود در حالی که نسخه‌های جدید `--pin` می‌خواهند. ۲) وابستگی‌های CRD اگر `dpkg -i` شکست بخورد صریح نصب نمی‌شوند. ۳) فایل سشن متعلق به root می‌ماند. |

---

## روش ۱ — KasmVNC

### 🔴 ۱-۱ (Critical) عدم غیرفعال‌سازی Prompt تعاملی
در سورس واقعی `vncserver` (KasmVNC) این مراحل **بدون قید و شرط** اجرا می‌شوند:

```perl
# unix/vncserver/vncserver
DisableLegacyVncAuth();
AllowXProgramsToConnectToXvnc();
EnsureAtLeastOneKasmUserExists();   # اگر کاربر با دسترسی write نباشد → Prompt
ConfigureDeToRun();                 # اگر DE انتخاب نشده باشد → Prompt انتخاب XFCE/GNOME...
StartXvncOrExit();
```

- `EnsureAtLeastOneKasmUserExists()` اگر کاربری با دسترسی write نباشد، با `PromptingAllowed()` (که از `command_line.prompt` می‌آید و **پیش‌فرض `true`** است) وارد مسیر تعاملی می‌شود.
- `ConfigureDeToRun()` روی اولین اجرا (نبودِ `~/.vnc/.de-was-selected`) تابع `SelectDe()` را صدا می‌زند که یک UI متنی تعاملی است.
- در سلول کولب این دستور با `subprocess.run(..., shell=True)` و **بدون tty** اجرا می‌شود؛ نتیجه: هنگ یا خطای «Failed to execute …» و بالا نیامدن سرور.

**شاهد:** مستندات رسمی KasmVNC — `command_line.prompt` پیش‌فرض `true` است.

**اصلاح اعمال‌شده:** افزودن به `kasmvnc.yaml` (هم در `/etc/kasmvnc` و هم در `~/.vnc`):
```yaml
command_line:
  prompt: false
```
به‌همراه ساخت مطمئن کاربر با دسترسی write (بخش ۱-۳).

### 🔴 ۱-۲ (Critical) `HOME` اشتباه با `sudo -u`
```python
subprocess.run("sudo -u colab vncserver :1 ... -disableBasicAuth", shell=True)
```
بر اساس `man sudoers`: «By default, sudo does not modify HOME». چون نوتبوک کولب با کاربر `root` اجرا می‌شود، `sudo -u colab` مقدار `HOME` را روی `/root` نگه می‌دارد. پس:
- کانفیگ `~/.vnc/kasmvnc.yaml` و `xstartup`ای که در `/home/colab/.vnc/` ساخته‌اید خوانده **نمی‌شود**،
- و `vncserver` سراغ `/root/.vnc/` می‌رود (پس نه Chrome اجرا می‌شود، نه WebGPU).

**اصلاح اعمال‌شده:** استفاده از `su - colab -c '...'` (login shell که `HOME` را درست تنظیم می‌کند) در همه‌ی جاهایی که کاربر اجرا می‌شود (`kasmvncpasswd`، `vncserver`، `vncserver -kill`، ساخت گواهی).

### 🟠 ۱-۳ (High) ساخت رمز به‌روش غیرقابل‌اتکا
```python
subprocess.run("echo -e '123456\\n123456\\n' | sudo -u colab kasmvncpasswd -u colab -wo ...", shell=True)
```
- `subprocess.run(shell=True)` روی اوبونتو از `/bin/sh` (که `dash` است) استفاده می‌کند، و `echo -e` در dash رفتار تضمینی ندارد.
- در سورس `kasmpasswd.c`، خود KasmVNC برای پایپ کردن رمز `echo -e "password\npassword\n"` را پیشنهاد می‌دهد؛ اما مطمئن‌ترین راه `printf` است.
- اگر این مرحله ناموفق بماند، کاربری با دسترسی write ساخته نمی‌شود و باگ ۱-۱ فعال می‌شود (Prompt).

**اصلاح اعمال‌شده:**
```python
sh("printf 'PASS\\nPASS\\n' | su - colab -c 'kasmvncpasswd -u colab -wo'")
```

### 🟠 ۱-۴ (High) گواهی SSL
`StartXvncOrExit()` تابع `CheckSslCertReadable()` را صدا می‌زند که در صورت غیرقابل‌خواندن بودن cert، **`exit 1`** می‌کند — حتی وقتی `require_ssl: false` است. گواهی `snakeoil` سیستم (`/etc/ssl/private/ssl-cert-snakeoil.key` با مالکیت `root:ssl-cert`) تنها در صورت عضویت کاربر در گروه `ssl-cert` خوانا است که شکننده است.

**اصلاح اعمال‌شده:** ساخت گواهی self-signed اختصاصی کاربر در `~/.vnc/self.pem` و اشاره‌ی کانفیگ به آن.

### 🟡 سایر موارد روش ۱
- تعیین‌کننده‌ی توزیع (`jammy/noble/focal`) درست است و asset `kasmvncserver_jammy_1.5.0_amd64.deb` واقعاً موجود است (بررسی شد).
- پرچم `-disableBasicAuth` معتبر است و به `Xvnc` پاس داده می‌شود (تأییدشده در issues رسمی KasmVNC #120 و #259)، **اما** نیازمندی «حداقل یک کاربر Kasm» را حذف نمی‌کند.
- تشخیص پورت با `ss`/`netstat` منطقی است (پیش‌فرض `websocket_port: auto` = `8443 + display`؛ برای `:1` می‌شود `8444`).
- `desktop.gpu.hw3d` روی پیش‌فرض `false` است؛ برای شتاب DRI3 می‌توان `true` کرد (اختیاری و وابسته به محیط).

---

## روش ۲ — Chrome Remote Desktop

### 🔴 ۲-۱ (Critical) استارت‌نشدن واقعی هاست در نبود systemd
```python
runner_script = "...\n/opt/google/chrome-remote-desktop/chrome-remote-desktop --start || true\n"
...
check = subprocess.run("ps aux | grep ... chrome-remote-desktop", ...)
```
- محیط کولب **systemd ندارد**؛ سرویس استاندارد CRD (`chrome-remote-desktop.service` / user unit) در دسترس نیست و خطای رایج `Failed to start chrome-remote-desktop.service: Unit ... not found` رخ می‌دهد.
- کد اصلی خطا را با `|| true` می‌پوشاند و فقط با `grep` روی `ps` بررسی می‌کند، بنابراین کاربر متوجه‌ی ریشه‌ی خطا نمی‌شود.

**اصلاح اعمال‌شده:** اسکریپت اجرا حالا (الف) سرویس systemd را در صورت وجود امتحان می‌کند، (ب) دیمن را مستقیماً با `/opt/google/chrome-remote-desktop/chrome-remote-desktop --start` بالا می‌آورد، (ج) با `pgrep` و در صورت شکست با چاپ `host.log` خطا را شفاف نشان می‌دهد.

### 🔴 ۲-۲ (High) تحویل PIN به `start-host`
پین فقط از طریق stdin پایپ می‌شد: `printf '{PIN}\n{PIN}\n' | start-host ...`. بعضی نسخه‌های `start-host` به‌جای Prompt، پرچم `--pin` می‌خواهند.

**اصلاح اعمال‌شده:** تشخیص خودکار پشتیبانی `--pin` از خروجی `start-host --help` و انتخاب مسیر مناسب؛ در غیر این صورت همان stdin.

### 🟠 ۲-۳ (Medium) وابستگی‌ها و مالکیت فایل سشن
- اگر `dpkg -i` بابت وابستگی‌های ناقص شکست بخورد، نصب به `apt-get install -fy` سپرده می‌شد که ممکن است بی‌صدا شکست بخورد.
- فایل `~/.chrome-remote-desktop-session` توسط root ساخته می‌شد و مالکیت/مجوز آن برای کاربر تضمین نبود.

**اصلاح اعمال‌شده:** نصب صریح `python3-psutil xserver-xorg-core xbase-clients x11-utils x11-xserver-utils dbus-x11` + `chown` صریح به کاربر + افزودن کاربر به گروه `chrome-remote-desktop`.

### 🟡 سایر موارد روش ۲
- `su - colab -c ...` در این روش از قبل `HOME` را درست تنظیم می‌کند (برخلاف روش ۱).
- کد تأیید OAuth یک‌بارمصرف و کوتاه‌عمر است (در README/سلول توضیح داده شده).

---

## یافته‌های تکمیلی (خارج از دو باگ اصلی) — پیشنهادی

1. **لینک‌های README به مخزن اشتباه اشاره می‌کنند:** همه‌ی badgeها و «Open in Colab» به `hosein-ul/colab-webgpu-chrome` اشاره دارند، نه این مخزن (`rodigers/chrome-colab`). در نتیجه اجرای ۱-کلیک، نسخه‌ی upstream را باز می‌کند نه نسخه‌ی شما.
2. **`README.fa.md` وجود ندارد** ولی در badge و متن به آن لینک داده شده است.
3. **فایل `LICENSE` وجود ندارد** در حالی که README می‌گوید MIT.
4. **سلول مانیتور GPU** یک assignment تکراری `status_str` دارد و ۱۰۰٪ CPU را با `clear_output` در حلقه‌ی بی‌پایان مصرف می‌کند (بهینه‌سازی جزئی).
5. **امنیت:** رمز ثابت `123456`، فعال‌بودن `NOPASSWD:ALL` برای کاربر، و `-disableBasicAuth` روی تونل عمومی Cloudflare یعنی هر کسی که لینک `trycloudflare` را داشته باشد به دسکتاپ دسترسی دارد. توصیه: حذف `-disableBasicAuth` و استفاده از رمز قوی، یا محدودسازی.
6. **سازگاری با TOS کولب:** نسخه‌های قدیمی حاوی کلماتی مثل «mining/PoW» بودند؛ نسخه‌ی فعلی پاک‌سازی شده است.
7. فایل `.ipynb` بدون newline انتهایی است (جزئی).

---

## چه چیزهایی اصلاح شد

- ✅ افزودن `command_line.prompt: false` (روش ۱) — **علت اصلی**
- ✅ جایگزینی `sudo -u` با `su -` برای تصحیح `HOME` (روش ۱)
- ✅ جایگزینی `echo -e` با `printf` برای ساخت رمز (روش ۱)
- ✅ گواهی self-signed اختصاصی کاربر (روش ۱)
- ✅ استارت مستقیم دیمن CRD مستقل از systemd + لاگ شفاف (روش ۲) — **علت اصلی**
- ✅ تشخیص خودکار `--pin` در `start-host` (روش ۲)
- ✅ نصب صریح وابستگی‌های CRD و تصحیح مالکیت فایل سشن (روش ۲)
- ✅ کامپایل موفق هر سه سلول کد تأیید شد و خروجی رشته‌های تولیدی (xstartup/runner/kasmvnc.yaml) بازبینی شد.

## تست پیشنهادی

1. نوتبوک را در Colab با ران‌تایم **T4 GPU** باز کنید.
2. سلول روش اول را اجرا کنید؛ باید تا ~۱–۲ دقیقه به دکمه‌ی سبز KasmVNC برسد. اگر نشد، خروجی «آخرین خطوط لاگ VNC» را بفرستید.
3. برای روش دوم، کد تازه‌ی `headless` را بلافاصله در `AUTH_COMMAND` پیست کنید و اجرا کنید.
4. اگر خطایی ماند، متن دقیق خطا را بفرستید تا ریشه‌یابی عمیق‌تر انجام شود (MCP کولب نیز نصب و متصل است و می‌توان اجرا را گام‌به‌گام رصد کرد).

## اجرای واقعی روی کولب (e2e) ✅

روش اول روی یک ران‌تایم واقعی **Tesla T4 (15360 MiB, driver 580.82.07)** اجرا و تأیید شد:

- `Xvnc :1` روی پورت `8443` با فلگ‌های `-drinode /dev/dri/renderD128`، `-disableBasicAuth` و cert اختصاصی بالا آمد.
- Chrome با پرچم‌های Vulkan/Dawn اجرا شد و پروسهٔ `chrome --type=gpu-process --use-angle=vulkan` در `nvidia-smi --query-compute-apps` دیده شد → **استفادهٔ واقعی از GPU تسلا T4 تأیید شد**.
- تونل Cloudflare ساخته شد و کلاینت KasmVNC از آن سرو شد (`HTTP 200`).
- یک نکتهٔ جزئی (خطاهای غیرمهلک `dbus` در لاگ Chrome) نیز برطرف شد: Chrome حالا از داخل `~/.config/autostart` نشست XFCE اجرا می‌شود تا `DBUS_SESSION_BUS_ADDRESS` صحیح را ارث ببرد.

## محدودیت بررسی

روش اول پس از اصلاح، به‌صورت واقعی روی T4 اجرا و تأیید شد (بخش بالا). روش دوم ذاتاً نیازمند کد OAuth یک‌بارمصرف حساب گوگل کاربر است و به‌صورت تعاملی توسط خود کاربر نهایی می‌شود؛ تمام پیش‌نیازهای آن (نصب XFCE/CRD، فایل سشن، اسکریپت اجرا) آماده‌سازی شده است.
