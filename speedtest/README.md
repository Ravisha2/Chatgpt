# Simple Speed Test

A small speed tester that measures **download speed, upload speed, ping and jitter**.
It saves each result with a label like "Bedroom", so you can compare rooms and find Wi‑Fi weak spots.

## Two ways to use it

### 1. Test your internet speed (easiest)
Double-click `index.html` to open it in your browser, then press **Start test**.
It uses Cloudflare's free public speed-test servers, the same ones behind speed.cloudflare.com.

### 2. Test your Wi‑Fi on its own (needs Python 3)
This shows whether slowness comes from your **Wi‑Fi** or from your **internet plan**.

**Windows shortcut:** double-click **`Start Speed Test (Windows).bat`**. It starts the server and opens the test page for you, so you can skip step 1.

1. On a computer connected to the router (with a cable if possible), open a terminal in this folder and run:
   ```
   python3 server.py
   ```
   On Windows, use `py server.py` if `python3` isn't recognised.
2. It prints two addresses. On your phone or laptop, connected to the same Wi‑Fi, open the
   **"phone / other device"** address, for example `http://192.168.1.20:8080`.
3. Choose **Local network only** under "Test against", then press **Start test**.
4. Walk around and test in each room.

If Windows asks whether to allow Python through the firewall, allow it on **private networks**. Otherwise other devices can't connect.
Press `Ctrl+C` in the terminal to stop the server.

## Reading the results
| | Good | Okay | Poor |
|---|---|---|---|
| Download | 25+ Mbps | 10–25 Mbps | under 10 Mbps |
| Upload | 5+ Mbps | 3–5 Mbps | under 3 Mbps |
| Ping | under 50 ms | 50–150 ms | over 150 ms |

If the speed is slow **next to the router too**, the problem is your internet plan or provider.
If it is only slow **far from the router**, the problem is Wi‑Fi coverage: move the router, switch to 5 GHz, or add a mesh system.

## Notes
- An internet test uses roughly 50–500 MB of data, depending on your speed. Keep that in mind on mobile data.
- Results are saved only in your browser. Nothing is sent anywhere else.
- Each test runs ping first, then download and upload for 8 seconds each over 4 parallel connections.
  The first 1.5 seconds of each phase are ignored while connections speed up.
