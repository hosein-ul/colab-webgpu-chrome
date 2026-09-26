#@title ⚡ [روش دوم] راه‌اندازی با Google Chrome Remote Desktop (Live Real-Time Logs)
#@markdown ### 📋 راهنمای اتصال ریموت دسکتاپ گوگل (تاخیر زیر ۳۰ میلی‌ثانیه و ۶۰ فریم):
#@markdown 1. در یک تب جدید در کامپیوتر خود به **[remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)** بروید.
#@markdown 2. دکمه‌های **Begin** ➔ **Next** ➔ **Authorize** را بزنید و کد لینوکس دبیان را کپی کنید.
#@markdown 3. ⚠️ کد یک‌بار مصرف و کوتاه‌عمر است؛ دقیقاً قبل از اجرای سلول آن را در `AUTH_COMMAND` پیست کنید.
AUTH_COMMAND = "" #@param {type:"string"}
PIN = 123456 #@param {type:"integer"}
TARGET_URL = "https://webgpureport.org" #@param {type:"string"}
CRD_USER = "colab" #@param {type:"string"}

import os, time, subprocess, re
from IPython.display import display, HTML

def sh(cmd):
    """اجرای دستور شل و برگرداندن نتیجه کامل (stdout/stderr/returncode)."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

raw_auth = AUTH_COMMAND.strip()
if not raw_auth:
    print("⚠️ فیلد AUTH_COMMAND خالی است!")
    print("👈 دریافت کد لینوکس: https://remotedesktop.google.com/headless")
    raw_auth = input("دستور احراز هویت را وارد کنید: ").strip()

if not raw_auth:
    raise ValueError("دستور احراز هویت الزامی است.")

def run_step(step_num, title, cmd):
    print(f"\n▶ [{step_num}/5] {title}...", flush=True)
    t0 = time.time()
    code = subprocess.run(cmd, shell=True).returncode
    dt = time.time() - t0
    status = "✔ انجام شد" if code == 0 else f"✖ خطا (کد {code})"
    print(f"  └─ {status} در {dt:.1f} ثانیه", flush=True)
    return code

# 1. گره‌های DRM/NVIDIA و درایور Vulkan
run_step(1, "پیکربندی گره‌های DRM، لودر Vulkan و درایور NVIDIA T4", """
mkdir -p /dev/dri /etc/vulkan/icd.d /usr/share/vulkan/icd.d /etc/apt/sources.list.d
mknod -m 666 /dev/dri/card0 c 226 0 2>/dev/null || true
mknod -m 666 /dev/dri/renderD128 c 226 128 2>/dev/null || true
mknod -m 666 /dev/nvidia-modeset c 195 254 2>/dev/null || true
chmod -R 666 /dev/dri /dev/nvidia* 2>/dev/null || true

rm -f /etc/apt/sources.list.d/lunarg-vulkan.list 2>/dev/null || true
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libvulkan1 vulkan-tools dbus-x11 xauth >/dev/null 2>&1

cat << 'EOF' > /etc/vulkan/icd.d/nvidia_icd.json
{
  "file_format_version": "1.0.0",
  "ICD": {
    "library_path": "libGLX_nvidia.so.0",
    "api_version": "1.3.275"
  }
}
EOF
cp /etc/vulkan/icd.d/nvidia_icd.json /usr/share/vulkan/icd.d/nvidia_icd.json
echo '/usr/lib64-nvidia' > /etc/ld.so.conf.d/nvidia.conf
ldconfig
/etc/init.d/dbus start >/dev/null 2>&1 || true
""")

# 2. ساخت کاربر اختصاصی
run_step(2, "ساخت کاربر اختصاصی و تنظیم دسترسی‌های سیستمی", f"""
mkdir -p /home/{CRD_USER}
id -u {CRD_USER} >/dev/null 2>&1 || useradd -m -s /bin/bash {CRD_USER} >/dev/null 2>&1
echo '{CRD_USER}:123456' | chpasswd
usermod -aG sudo,video,render {CRD_USER} >/dev/null 2>&1 || true
echo '{CRD_USER} ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/{CRD_USER}
""")

# 3. نصب XFCE4 + Chrome Remote Desktop
run_step(3, "نصب XFCE4 و Chrome Remote Desktop", """
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq xfce4 desktop-base xfce4-terminal >/dev/null 2>&1
DEBIAN_FRONTEND=noninteractive apt-get purge -y -qq xscreensaver >/dev/null 2>&1 || true
if [ ! -f /opt/google/chrome-remote-desktop/start-host ]; then
  wget -q -O /tmp/crd.deb https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
  dpkg -i /tmp/crd.deb >/dev/null 2>&1 || true
fi
# 🔧 اصلاح: نصب صریح وابستگی‌های CRD (به‌جای اتکا به --fix-broken)
DEBIAN_FRONTEND=noninteractive apt-get install -fy -qq >/dev/null 2>&1 || true
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-psutil xserver-xorg-core xbase-clients x11-utils x11-xserver-utils dbus-x11 >/dev/null 2>&1 || true
rm -f /tmp/crd.deb
""")

# فایل سشن CRD (باید در HOME کاربر و قابل‌اجرا باشد)
crd_session = """export DESKTOP_SESSION=xfce
export XDG_CURRENT_DESKTOP=XFCE
export XDG_CONFIG_DIRS=/etc/xdg/xdg-xfce:/etc/xdg
exec /usr/bin/xfce4-session
"""
with open(f"/home/{CRD_USER}/.chrome-remote-desktop-session", "w") as f: f.write(crd_session)
sh(f"cp /home/{CRD_USER}/.chrome-remote-desktop-session /etc/chrome-remote-desktop-session")
sh(f"chmod +x /home/{CRD_USER}/.chrome-remote-desktop-session")
sh(f"usermod -aG chrome-remote-desktop {CRD_USER} >/dev/null 2>&1 || true")

# 4. نصب Chrome و اسکریپت اجرای خودکار با شتاب Dawn/WebGPU
run_step(4, "نصب Google Chrome و تنظیم اجرای خودکار WebGPU", f"""
if [ ! -f /usr/bin/google-chrome ]; then
  wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -i /tmp/chrome.deb >/dev/null 2>&1 || apt-get install -fy -qq >/dev/null 2>&1
  rm -f /tmp/chrome.deb
fi
mkdir -p /home/{CRD_USER}/.config/autostart /home/{CRD_USER}/Desktop
cat << 'EOF' > /home/{CRD_USER}/launch_chrome.sh
#!/bin/bash
export VK_ICD_FILENAMES=/etc/vulkan/icd.d/nvidia_icd.json
google-chrome-stable \\
  --no-sandbox \\
  --disable-gpu-sandbox \\
  --enable-unsafe-webgpu \\
  --enable-features=Vulkan,DefaultANGLEVulkan,VulkanFromANGLE,WebGPUService \\
  --use-angle=vulkan \\
  --enable-dawn-features=allow_unsafe_apis,disable_adapter_blocklist \\
  --disable-dawn-features=disallow_unsafe_apis \\
  --ignore-gpu-blocklist \\
  --disable-dev-shm-usage \\
  --enable-gpu-rasterization \\
  --enable-zero-copy \\
  --start-maximized \\
  "{TARGET_URL}" &
EOF
chmod +x /home/{CRD_USER}/launch_chrome.sh
cat << 'EOF' > /home/{CRD_USER}/.config/autostart/webgpu-chrome.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=WebGPU Google Chrome
Exec=/home/{CRD_USER}/launch_chrome.sh
Icon=google-chrome
Terminal=false
EOF
cp /home/{CRD_USER}/.config/autostart/webgpu-chrome.desktop /home/{CRD_USER}/Desktop/
chmod +x /home/{CRD_USER}/Desktop/webgpu-chrome.desktop
chown -R {CRD_USER}:{CRD_USER} /home/{CRD_USER}
""")

# 5. ثبت هاست (start-host) و اجرای سرویس ریموت دسکتاپ
print("\n▶ [5/5] ثبت و راه‌اندازی هاست ریموت دسکتاپ گوگل با اکانت شما...", flush=True)
clean_cmd = re.sub(r'^DISPLAY=\s*', '', raw_auth)
clean_cmd = re.sub(r'--pin=\S+', '', clean_cmd).strip()

# 🔧 اصلاح: تشخیص پشتیبانی از --pin در start-host برای تحویل مطمئن پین
help_txt = sh("/opt/google/chrome-remote-desktop/start-host --help 2>&1").stdout
if "--pin" in help_txt:
    register_cmd = f"{clean_cmd} --pin={PIN}"
    print("  ℹ از --pin برای ثبت هاست استفاده می‌شود.")
else:
    register_cmd = f"printf '{PIN}\\n{PIN}\\n' | {clean_cmd}"
    print("  ℹ پین از طریق stdin به start-host داده می‌شود.")

runner_script = f"""#!/bin/bash
set -x
pkill -f 'chrome-remote-desktop' 2>/dev/null || true
{register_cmd}
sleep 2
# 🔧 اصلاح: اجرای دیمن CRD به‌صورت مستقیم (مستقل از systemd که در کولب وجود ندارد)
if command -v systemctl >/dev/null 2>&1; then
  systemctl --user start chrome-remote-desktop 2>/dev/null || true
fi
/opt/google/chrome-remote-desktop/chrome-remote-desktop --start || true
sleep 5
pgrep -af 'chrome-remote-desktop' || true
"""
with open("/tmp/start_crd.sh", "w") as f: f.write(runner_script)
sh(f"chmod +x /tmp/start_crd.sh && chown {CRD_USER}:{CRD_USER} /tmp/start_crd.sh")

# 🔧 اصلاح: اجرای start-host با HOME صحیح کاربر (su -)
res = sh(f"su - {CRD_USER} -c /tmp/start_crd.sh")
time.sleep(3)
check = sh("ps aux | grep -v grep | grep -E 'chrome-remote-desktop(-host)?'")

print("\n" + "═"*65)
if "chrome-remote-desktop" in check.stdout:
    print("🎉 سرویس Google Chrome Remote Desktop با موفقیت استارت شد!")
    print(f"🔑 پین اتصال: {PIN}")
    print(f"🖥 نام دستگاه: colab-t4")
    print("═"*65)
    display(HTML(f'''
        <div style="background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%); padding: 24px; border-radius: 12px; color: #fff; font-family: sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,0.3); text-align: center; margin: 15px 0;">
            <h2 style="margin: 0 0 10px 0; color: #64ffda;">🚀 دسکتاپ ابری ۶۰ فریم آماده اتصال است!</h2>
            <p style="font-size: 15px; margin-bottom: 20px; opacity: 0.95;">
                دستگاه در پنل ریموت گوگل ثبت شد. روی دکمه زیر کلیک کرده و پین <b>{PIN}</b> را وارد کنید:
            </p>
            <a href="https://remotedesktop.google.com/access" target="_blank" style="padding: 14px 34px; background: #00e676; color: #000; font-weight: bold; font-size: 18px; text-decoration: none; border-radius: 8px; display: inline-block; box-shadow: 0 4px 15px rgba(0,230,118,0.4);">
                👉 ورود به Chrome Remote Desktop
            </a>
            <p style="margin-top: 15px; font-size: 13px; opacity: 0.8;">
                آدرس مستقیم: <a href="https://remotedesktop.google.com/access" target="_blank" style="color: #64ffda;">https://remotedesktop.google.com/access</a>
            </p>
        </div>
    '''))
else:
    print("⚠️ هاست ریموت دسکتاپ بالا نیامد. خروجی ثبت:")
    print(res.stdout[-3000:])
    if res.stderr: print("خطاها:", res.stderr[-1500:])
    print("── لاگ هاست (host.log) ──")
    print(sh(f"cat /home/{CRD_USER}/.config/chrome-remote-desktop/host.log 2>/dev/null | tail -n 40").stdout)
    print("═"*65)
    print("نکات: ۱) کد تأیید گوگل یک‌بار مصرف است؛ دقیقاً قبل از اجرای سلول آن را بگیرید.")
    print("      ۲) در کولب systemd وجود ندارد؛ این اسکریپت دیمن را مستقیم اجرا می‌کند.")
    print("      ۳) اگر نشانگر «Section: prompt» دیدید، پین را دوباره با مقدار PIN تنظیم کنید.")
