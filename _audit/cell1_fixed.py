#@title 🟢 [روش اول] راه‌اندازی ۱۰۰٪ تک‌کلیک با KasmVNC مدرن (Live Real-Time Logs)
#@markdown ### 🌐 تنظیمات آدرس، رزولوشن و حساب کاربری:
#@markdown آدرس سایت/دپ مورد نظر، رزولوشن دسکتاپ و نام کاربری/رمز ورود را تعیین کنید:
TARGET_URL = "https://webgpureport.org" #@param {type:"string"}
RESOLUTION = "1280x720" #@param ["1280x720", "1366x768", "1600x900", "1920x1080"]
VNC_USER = "colab" #@param {type:"string"}
VNC_PASS = "123456" #@param {type:"string"}

import os, time, subprocess, re, shutil
from IPython.display import display, HTML

def sh(cmd):
    """اجرای دستور شل و برگرداندن نتیجه کامل (stdout/stderr/returncode)."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def run_step(step_num, title, cmd, show_output=False):
    print(f"\n▶ [{step_num}/6] {title}...", flush=True)
    t0 = time.time()
    if show_output:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in iter(proc.stdout.readline, ''):
            l = line.strip()
            if l: print(f"  │ {l[:110]}", flush=True)
        proc.wait()
        code = proc.returncode
    else:
        code = subprocess.run(cmd, shell=True).returncode
    dt = time.time() - t0
    status = "✔ انجام شد" if code == 0 else f"✖ خطا (کد {code})"
    print(f"  └─ {status} در {dt:.1f} ثانیه", flush=True)
    return code

# 1. گره‌های DRM/NVIDIA، لودر Vulkan و نسخه‌ی ICD انویدیا
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

# 2. ساخت کاربر اختصاصی و تنظیم مجوزها
run_step(2, "ساخت کاربر اختصاصی و تنظیم مجوزهای سیستم", f"""
mkdir -p /home/{VNC_USER}
id -u {VNC_USER} >/dev/null 2>&1 || useradd -m -s /bin/bash {VNC_USER} >/dev/null 2>&1
echo '{VNC_USER}:{VNC_PASS}' | chpasswd
usermod -aG sudo,video,render {VNC_USER} >/dev/null 2>&1 || true
echo '{VNC_USER} ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/{VNC_USER}
""")

# 3. نصب Google Chrome
if not os.path.exists("/usr/bin/google-chrome"):
    run_step(3, "دانلود و نصب Google Chrome Stable", """
    wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    dpkg -i /tmp/chrome.deb >/dev/null 2>&1 || apt-get install -fy -qq >/dev/null 2>&1
    rm -f /tmp/chrome.deb
    """)
else:
    print("\n▶ [3/6] بررسی مرورگر: Google Chrome از قبل نصب است.", flush=True)

# 4. نصب KasmVNC 1.5.0 و XFCE4
res = sh("lsb_release -cs")
distro = res.stdout.strip() if res.stdout.strip() in ["jammy", "noble", "focal"] else "jammy"
kasm_deb = f"/tmp/kasmvnc_{distro}.deb"

if not os.path.exists("/usr/bin/vncserver") or not os.path.exists("/usr/share/kasmvnc"):
    run_step(4, f"نصب KasmVNC 1.5.0 ({distro}) و محیط XFCE4", f"""
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq xfce4 xfce4-terminal desktop-base xauth ssl-cert >/dev/null 2>&1
    make-ssl-cert generate-default-snakeoil --force-overwrite >/dev/null 2>&1 || true
    wget -q -O {kasm_deb} https://github.com/kasmtech/KasmVNC/releases/download/v1.5.0/kasmvncserver_{distro}_1.5.0_amd64.deb
    dpkg -i {kasm_deb} >/dev/null 2>&1 || apt-get install -fy -qq >/dev/null 2>&1
    rm -f {kasm_deb}
    """)
else:
    print("\n▶ [4/6] بررسی KasmVNC: پکیج‌ها از قبل نصب هستند.", flush=True)

# --- کانفیگ KasmVNC -------------------------------------------------------
# 🔧 اصلاح ۱ (علت اصلی خطای روش اول): command_line.prompt=false
# بدون این تنظیم، vncserver روی اجرای اول در حالت غیرتعاملی برای «انتخاب
# Desktop Environment» و «ساخت کاربر» Prompt می‌کند و در کولب هنگ/خطا می‌خورد.
os.makedirs(f"/home/{VNC_USER}/.vnc", exist_ok=True)
os.makedirs("/etc/kasmvnc", exist_ok=True)
kasm_yaml = f"""
command_line:
  prompt: false
network:
  protocol: http
  interface: 0.0.0.0
  websocket_port: 8443
  use_ipv4: true
  use_ipv6: false
  ssl:
    require_ssl: false
    pem_certificate: /home/{VNC_USER}/.vnc/self.pem
    pem_key: /home/{VNC_USER}/.vnc/self.pem
"""
with open("/etc/kasmvnc/kasmvnc.yaml", "w") as f: f.write(kasm_yaml)
with open(f"/home/{VNC_USER}/.vnc/kasmvnc.yaml", "w") as f: f.write(kasm_yaml)

# --- xstartup: فقط XFCE را با DBus بالا می‌آورد؛ Chrome از autostart اجرا
#     می‌شود تا داخل نشست XFCE و با DBUS_SESSION_BUS_ADDRESS صحیح اجرا شود
#     (این کار خطاهای غیرمهلک dbus در لاگ Chrome را حذف می‌کند).
xstartup = """#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export VK_ICD_FILENAMES=/etc/vulkan/icd.d/nvidia_icd.json
export DESKTOP_SESSION=xfce
export XDG_CURRENT_DESKTOP=XFCE
exec dbus-launch --exit-with-session startxfce4
"""
with open(f"/home/{VNC_USER}/.vnc/xstartup", "w") as f: f.write(xstartup)

# --- اجرای خودکار Chrome داخل نشست XFCE (با DBus سالم) ---------------------
launch_chrome = f"""#!/bin/bash
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
"""
os.makedirs(f"/home/{VNC_USER}/.config/autostart", exist_ok=True)
with open(f"/home/{VNC_USER}/launch_chrome.sh", "w") as f: f.write(launch_chrome)
chrome_desktop = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=WebGPU Google Chrome
Exec=/home/{VNC_USER}/launch_chrome.sh
Icon=google-chrome
Terminal=false
"""
with open(f"/home/{VNC_USER}/.config/autostart/webgpu-chrome.desktop", "w") as f: f.write(chrome_desktop)
subprocess.run(f"chmod +x /home/{VNC_USER}/launch_chrome.sh", shell=True)

# --- گواهی اختصاصی کاربر + رمز KasmVNC ------------------------------------
# 🔧 اصلاح ۲: گواهی self-signed اختصاصی کاربر (چون KasmVNC خوانا بودن cert را
# حتی در حالت require_ssl=false نیز اجبار می‌کند و گواهی snakeoil سیستم برای
# کاربر قابل خواندن نیست).
# 🔧 اصلاح ۳: استفاده از printf به‌جای echo -e (echo -e زیر /bin/sh=dash
# قابل اتکا نیست و باعث ناموفق ماندن ساخت کاربر/رمز می‌شد).
# 🔧 اصلاح ۴: استفاده از su - به‌جای sudo -u تا HOME درست روی /home/<user>
# تنظیم شود (sudo به‌طور پیش‌فرض HOME را عوض نمی‌کند و vncserver از /root/.vnc
# می‌خواند؛ یعنی xstartup و کانفیگ کاربر نادیده گرفته می‌شد).
sh(f"su - {VNC_USER} -c 'openssl req -x509 -newkey rsa:2048 -keyout ~/.vnc/self.pem -out ~/.vnc/self.pem -days 3650 -nodes -subj /CN=colab 2>/dev/null'")
sh(f"chmod +x /home/{VNC_USER}/.vnc/xstartup")
sh(f"printf '{VNC_PASS}\\n{VNC_PASS}\\n' | su - {VNC_USER} -c 'kasmvncpasswd -u {VNC_USER} -wo'")
sh(f"chown -R {VNC_USER}:{VNC_USER} /home/{VNC_USER}")
print("  ✔ گواهی self-signed، xstartup و رمز KasmVNC آماده شد.", flush=True)

# 5. تونل Cloudflare
if not os.path.exists("/usr/local/bin/cloudflared"):
    run_step(5, "دانلود باینری تونل Cloudflare", """
    wget -q -O /usr/local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    chmod +x /usr/local/bin/cloudflared
    """)
else:
    print("\n▶ [5/6] بررسی تونل: Cloudflared آماده است.", flush=True)

# 6. استارت سرور KasmVNC و ایجاد تونل
print("\n▶ [6/6] استارت سرور KasmVNC و ایجاد لینک ارتباطی زنده...", flush=True)
sh(f"su - {VNC_USER} -c 'vncserver -kill :1'")
sh("pkill -9 -f 'cloudflared' >/dev/null 2>&1 || true")
sh("rm -rf /tmp/.X1-lock /tmp/.X11-unix/X1")
time.sleep(1)

# 🔧 اصلاح ۴ (ادامه): اجرای vncserver با HOME صحیح کاربر
vnc_proc = sh(f"su - {VNC_USER} -c 'vncserver :1 -geometry {RESOLUTION} -depth 24 -disableBasicAuth'")

# بررسی پورت باز شده (8443 پیش‌فرض، یا 8444 برای websocket_port=auto)
vnc_port = None
for _ in range(15):
    time.sleep(1)
    chk = sh("ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null")
    if ":8443" in chk.stdout:
        vnc_port = 8443
        break
    elif ":8444" in chk.stdout:
        vnc_port = 8444
        break

if not vnc_port:
    print("❌ خطا: سرور VNC روی پورت 8443/8444 فعال نشد!")
    print("خروجی vncserver:", vnc_proc.stdout)
    if vnc_proc.stderr: print("خطای vncserver:", vnc_proc.stderr)
    print("\nآخرین خطوط لاگ VNC:")
    print(sh(f"cat /home/{VNC_USER}/.vnc/*.log 2>/dev/null | tail -n 30").stdout)
    raise RuntimeError("VNC Server failed to bind to port.")

print(f"  ✔ سرور KasmVNC روی پورت داخلی {vnc_port} با موفقیت مستقر شد.", flush=True)

# استارت تونل روی پورت تایید شده با پروتکل HTTP خالص (بدون خطای 502)
log_file = "/tmp/cloudflared.log"
if os.path.exists(log_file): os.remove(log_file)
cloudflared_bin = "/usr/local/bin/cloudflared" if os.path.exists("/usr/local/bin/cloudflared") else (shutil.which("cloudflared") or "cloudflared")
subprocess.Popen([cloudflared_bin, "tunnel", "--no-autoupdate", "--url", f"http://127.0.0.1:{vnc_port}", "--logfile", log_file])

tunnel_url = None
for _ in range(30):
    time.sleep(1)
    if os.path.exists(log_file):
        with open(log_file) as f:
            m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", f.read())
            if m:
                tunnel_url = m.group(0)
                break

if tunnel_url:
    print("\n" + "═"*65)
    print("🎉 محیط ابری با موفقیت لود شد! (شتاب سخت‌افزاری Tesla T4 فعال است)")
    print(f"🎯 پورت لوکال متصل‌شده: {vnc_port} | مقصد: {TARGET_URL}")
    print("═"*65)
    display(HTML(f'''
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 24px; border-radius: 12px; color: #fff; font-family: sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,0.3); text-align: center; margin: 15px 0;">
            <h2 style="margin: 0 0 10px 0; color: #00e676;">⚡ دسکتاپ KasmVNC آماده اتصال است!</h2>
            <p style="font-size: 15px; margin-bottom: 20px; opacity: 0.95;">
                ارتباط بدون خطای 502 برقرار شد. برای ورود به محیط روی دکمه زیر کلیک کنید:
            </p>
            <a href="{tunnel_url}" target="_blank" style="padding: 14px 34px; background: #00e676; color: #000; font-weight: bold; font-size: 18px; text-decoration: none; border-radius: 8px; display: inline-block; box-shadow: 0 4px 15px rgba(0,230,118,0.4);">
                👉 ورود به مرورگر ابری (KasmVNC)
            </a>
            <p style="margin-top: 15px; font-size: 13px; opacity: 0.8;">
                لینک مستقیم: <a href="{tunnel_url}" target="_blank" style="color: #64ffda;">{tunnel_url}</a>
            </p>
            <p style="margin-top: 8px; font-size: 12px; opacity: 0.7;">
                (نام کاربری: <b>{VNC_USER}</b> | رمز عبور: <b>{VNC_PASS}</b> در صورت درخواست لاگین)
            </p>
        </div>
    '''))
else:
    print("❌ خطا در ایجاد آدرس تونل Cloudflare.")
    print(sh("tail -n 30 /tmp/cloudflared.log 2>/dev/null").stdout)
