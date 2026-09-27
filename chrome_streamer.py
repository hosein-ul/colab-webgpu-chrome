import asyncio
import json
import time
import os
import argparse
from aiohttp import web, ClientSession

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ Chrome Ultra-Stream (GPU Accelerated)</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: #090d16;
            color: #e6edf3;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
            user-select: none;
        }
        #navbar {
            background: #161b22;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid #30363d;
            z-index: 10;
        }
        .nav-btn {
            background: #21262d;
            border: 1px solid #363b42;
            color: #c9d1d9;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }
        .nav-btn:hover { background: #30363d; color: #58a6ff; }
        #urlInput {
            flex: 1;
            background: #0d1117;
            border: 1px solid #30363d;
            padding: 7px 14px;
            border-radius: 6px;
            color: #58a6ff;
            font-size: 14px;
            outline: none;
            user-select: text;
        }
        #urlInput:focus { border-color: #1f6feb; box-shadow: 0 0 0 2px rgba(31,111,235,0.3); }
        #stats {
            display: flex;
            gap: 12px;
            font-size: 12px;
            font-family: monospace;
            background: #0d1117;
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid #30363d;
            color: #00e676;
        }
        #viewport-container {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #000;
            position: relative;
            overflow: hidden;
        }
        #screenCanvas {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            cursor: default;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }
        #statusOverlay {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(13, 17, 23, 0.9);
            border: 1px solid #30363d;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 13px;
            color: #58a6ff;
            pointer-events: none;
            transition: opacity 0.5s;
        }
    </style>
</head>
<body>
    <div id="navbar">
        <button class="nav-btn" id="backBtn" title="Back">◀</button>
        <button class="nav-btn" id="reloadBtn" title="Reload">🔄</button>
        <input type="text" id="urlInput" placeholder="https://webgpureport.org">
        <button class="nav-btn" id="goBtn">Go ➔</button>
        <div id="stats">
            <span>FPS: <b id="fpsVal">0</b></span>
            <span>Latency: <b id="latVal">0</b>ms</span>
            <span>GPU: <b style="color:#64ffda;">Tesla T4 (WebGPU)</b></span>
        </div>
        <button class="nav-btn" id="fullscreenBtn" title="Fullscreen">⛶</button>
    </div>
    <div id="viewport-container">
        <canvas id="screenCanvas"></canvas>
        <div id="statusOverlay">Connecting to Chrome...</div>
    </div>

    <script>
        const canvas = document.getElementById('screenCanvas');
        const ctx = canvas.getContext('2d');
        const urlInput = document.getElementById('urlInput');
        const fpsVal = document.getElementById('fpsVal');
        const latVal = document.getElementById('latVal');
        const statusOverlay = document.getElementById('statusOverlay');
        let ws, frameCount = 0;

        function getCoords(e) {
            const r = canvas.getBoundingClientRect();
            return {
                x: Math.round((e.clientX - r.left) * (canvas.width / r.width)),
                y: Math.round((e.clientY - r.top) * (canvas.height / r.height))
            };
        }

        function connect() {
            const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(proto + '//' + location.host + '/ws');

            ws.onopen = () => {
                statusOverlay.textContent = '🟢 Connected to GPU Chrome';
                setTimeout(() => { statusOverlay.style.opacity = '0'; }, 2000);
            };

            ws.onmessage = (event) => {
                if (typeof event.data === 'string') {
                    const msg = JSON.parse(event.data);
                    if (msg.type === 'error') {
                        statusOverlay.style.opacity = '1';
                        statusOverlay.style.background = 'rgba(180, 20, 20, 0.9)';
                        statusOverlay.textContent = '❌ ' + msg.message;
                    } else if (msg.type === 'frame') {
                        const img = new Image();
                        img.onload = () => {
                            if (canvas.width !== img.width || canvas.height !== img.height) {
                                canvas.width = img.width;
                                canvas.height = img.height;
                            }
                            ctx.drawImage(img, 0, 0);
                            frameCount++;
                            statusOverlay.style.opacity = '0';
                        };
                        img.src = 'data:image/jpeg;base64,' + msg.data;
                        if (msg.currentUrl && document.activeElement !== urlInput) {
                            urlInput.value = msg.currentUrl;
                        }
                    } else if (msg.type === 'pong') {
                        latVal.textContent = Math.round(performance.now() - msg.t);
                    }
                }
            };

            ws.onclose = () => {
                statusOverlay.style.opacity = '1';
                statusOverlay.style.background = 'rgba(13, 17, 23, 0.9)';
                statusOverlay.textContent = '🔴 Disconnected. Reconnecting...';
                setTimeout(connect, 1500);
            };
        }

        setInterval(() => {
            fpsVal.textContent = frameCount;
            frameCount = 0;
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: 'ping', t: performance.now() }));
            }
        }, 1000);

        function sendInput(payload) {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify(payload));
            }
        }

        canvas.addEventListener('mousemove', (e) => {
            const pos = getCoords(e);
            sendInput({ type: 'mouse', event: 'mouseMoved', x: pos.x, y: pos.y });
        });

        canvas.addEventListener('mousedown', (e) => {
            e.preventDefault();
            const pos = getCoords(e);
            const btn = e.button === 2 ? 'right' : e.button === 1 ? 'middle' : 'left';
            sendInput({ type: 'mouse', event: 'mousePressed', x: pos.x, y: pos.y, button: btn, clickCount: 1 });
        });

        canvas.addEventListener('mouseup', (e) => {
            const pos = getCoords(e);
            const btn = e.button === 2 ? 'right' : e.button === 1 ? 'middle' : 'left';
            sendInput({ type: 'mouse', event: 'mouseReleased', x: pos.x, y: pos.y, button: btn });
        });

        canvas.addEventListener('contextmenu', (e) => e.preventDefault());

        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const pos = getCoords(e);
            sendInput({ type: 'wheel', x: pos.x, y: pos.y, deltaX: e.deltaX, deltaY: e.deltaY });
        }, { passive: false });

        window.addEventListener('keydown', (e) => {
            if (document.activeElement === urlInput) return;
            sendInput({
                type: 'key',
                event: 'rawKeyDown',
                key: e.key,
                code: e.code,
                windowsVirtualKeyCode: e.keyCode,
                text: e.key.length === 1 ? e.key : ''
            });
        });

        window.addEventListener('keyup', (e) => {
            if (document.activeElement === urlInput) return;
            sendInput({
                type: 'key',
                event: 'keyUp',
                key: e.key,
                code: e.code,
                windowsVirtualKeyCode: e.keyCode
            });
        });

        function navigate() {
            let u = urlInput.value.trim();
            if (!u.startsWith('http://') && !u.startsWith('https://')) u = 'https://' + u;
            sendInput({ type: 'navigate', url: u });
        }
        document.getElementById('goBtn').onclick = navigate;
        urlInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') navigate(); });
        document.getElementById('reloadBtn').onclick = () => sendInput({ type: 'reload' });
        document.getElementById('backBtn').onclick = () => sendInput({ type: 'history', delta: -1 });
        document.getElementById('fullscreenBtn').onclick = () => {
            if (!document.fullscreenElement) document.documentElement.requestFullscreen();
            else document.exitFullscreen();
        };

        connect();
    </script>
</body>
</html>"""

CONFIG = {
    'cdp_port': 9222,
    'width': 1280,
    'height': 720,
    'quality': 80
}

async def get_cdp_target():
    port = CONFIG['cdp_port']
    async with ClientSession() as s:
        for _ in range(40):
            try:
                async with s.get(f'http://127.0.0.1:{port}/json/list', timeout=2) as resp:
                    tabs = await resp.json()
                    for t in tabs:
                        if t.get('type') == 'page' and 'webSocketDebuggerUrl' in t:
                            return t['webSocketDebuggerUrl']
                # If no active tab found, open a new one
                async with s.put(f'http://127.0.0.1:{port}/json/new', timeout=2) as resp:
                    new_tab = await resp.json()
                    if 'webSocketDebuggerUrl' in new_tab:
                        return new_tab['webSocketDebuggerUrl']
            except Exception:
                await asyncio.sleep(0.5)
    raise RuntimeError('Could not find or create active Chrome tab.')

async def index(request):
    return web.Response(text=INDEX_HTML, content_type='text/html')

async def websocket_handler(request):
    ws_client = web.WebSocketResponse(heartbeat=15.0)
    await ws_client.prepare(request)
    
    try:
        target_ws_url = await get_cdp_target()
    except Exception as e:
        await ws_client.send_str(json.dumps({'type': 'error', 'message': str(e)}))
        await ws_client.close()
        return ws_client

    async with ClientSession() as session:
        async with session.ws_connect(target_ws_url) as cdp_ws:
            await cdp_ws.send_json({'id': 1, 'method': 'Page.enable'})
            await cdp_ws.send_json({
                'id': 2,
                'method': 'Page.startScreencast',
                'params': {
                    'format': 'jpeg',
                    'quality': CONFIG['quality'],
                    'maxWidth': CONFIG['width'],
                    'maxHeight': CONFIG['height'],
                    'everyNthFrame': 1
                }
            })
            # Trigger immediate screenshot so frame 1 appears instantly without waiting for page event
            await cdp_ws.send_json({
                'id': 50,
                'method': 'Page.captureScreenshot',
                'params': {
                    'format': 'jpeg',
                    'quality': CONFIG['quality']
                }
            })

            ack_id = 100
            async def cdp_to_client():
                nonlocal ack_id
                try:
                    async for msg in cdp_ws:
                        if msg.type == web.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            if data.get('id') == 50 and 'result' in data:
                                await ws_client.send_str(json.dumps({
                                    'type': 'frame',
                                    'data': data['result']['data'],
                                    'currentUrl': ''
                                }))
                            elif data.get('method') == 'Page.screencastFrame':
                                p = data['params']
                                await ws_client.send_str(json.dumps({
                                    'type': 'frame',
                                    'data': p['data'],
                                    'currentUrl': p.get('metadata', {}).get('url', '')
                                }))
                                ack_id += 1
                                await cdp_ws.send_json({
                                    'id': ack_id,
                                    'method': 'Page.screencastFrameAck',
                                    'params': {'sessionId': p['sessionId']}
                                })
                except Exception as e:
                    print(f"cdp_to_client error: {e}")

            async def keepalive():
                while not ws_client.closed:
                    await asyncio.sleep(2)
                    try:
                        await cdp_ws.send_json({
                            'id': 50,
                            'method': 'Page.captureScreenshot',
                            'params': {'format': 'jpeg', 'quality': CONFIG['quality']}
                        })
                    except Exception:
                        break

            async def client_to_cdp():
                try:
                    async for msg in ws_client:
                        if msg.type == web.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            t = data.get('type')
                            if t == 'mouse':
                                await cdp_ws.send_json({
                                    'id': 10,
                                    'method': 'Input.dispatchMouseEvent',
                                    'params': {
                                        'type': data['event'],
                                        'x': data['x'],
                                        'y': data['y'],
                                        'button': data.get('button', 'left'),
                                        'clickCount': data.get('clickCount', 1)
                                    }
                                })
                            elif t == 'wheel':
                                await cdp_ws.send_json({
                                    'id': 11,
                                    'method': 'Input.dispatchMouseEvent',
                                    'params': {
                                        'type': 'mouseWheel',
                                        'x': data['x'],
                                        'y': data['y'],
                                        'deltaX': data['deltaX'],
                                        'deltaY': data['deltaY']
                                    }
                                })
                            elif t == 'key':
                                await cdp_ws.send_json({
                                    'id': 12,
                                    'method': 'Input.dispatchKeyEvent',
                                    'params': {
                                        'type': data['event'],
                                        'key': data.get('key', ''),
                                        'code': data.get('code', ''),
                                        'windowsVirtualKeyCode': data.get('windowsVirtualKeyCode', 0),
                                        'text': data.get('text', '')
                                    }
                                })
                            elif t == 'navigate':
                                await cdp_ws.send_json({
                                    'id': 13,
                                    'method': 'Page.navigate',
                                    'params': {'url': data['url']}
                                })
                            elif t == 'reload':
                                await cdp_ws.send_json({'id': 14, 'method': 'Page.reload'})
                            elif t == 'ping':
                                await ws_client.send_str(json.dumps({'type': 'pong', 't': data.get('t', 0)}))
                except Exception:
                    pass

            await asyncio.gather(cdp_to_client(), client_to_cdp(), keepalive())
    return ws_client

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--cdp-port', type=int, default=9222)
    parser.add_argument('--width', type=int, default=1280)
    parser.add_argument('--height', type=int, default=720)
    parser.add_argument('--quality', type=int, default=80)
    args = parser.parse_args()

    CONFIG['cdp_port'] = args.cdp_port
    CONFIG['width'] = args.width
    CONFIG['height'] = args.height
    CONFIG['quality'] = args.quality

    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/ws', websocket_handler)
    print(f"Starting Chrome Streamer on http://127.0.0.1:{args.port} (CDP on {args.cdp_port})...")
    web.run_app(app, host='127.0.0.1', port=args.port)

if __name__ == '__main__':
    main()
