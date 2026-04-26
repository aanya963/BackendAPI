import time
import requests
from queue_manager import pop_log   # ✅ correct import

def process_logs():
    while True:
        print("\n🔄 [WORKER] Checking queue...")

        log = pop_log()

        if log:
            print("🚀 [WORKER] Processing log:", log)

            try:
                res = requests.post(
                    "http://localhost:5124/api/Logs",
                    json=log
                )
                print("📡 [WORKER] Sent to .NET, status:", res.status_code)
            except Exception as e:
                print("❌ [WORKER] Error:", e)

        time.sleep(2)

if __name__ == "__main__":
    process_logs()