import telnetlib
import time

# Telnet 目標設備資訊
HOST = "192.168.50.1"
USERNAME = "admin"
PASSWORD = "admin"
PROMPT = b':~$ '  # 根據設備的實際提示符調整

# 要執行的 Shell 腳本內容
script_content = """#!/bin/sh
setconsole /dev/pts/0
while true; do
    wl -i wl1 dfs_status
    wl -i wl1 radar_status
    wl -i wl1 chanspec
    echo "--------------------------------"
    sleep 2
done
"""

try:
    # 建立 Telnet 連線
    with telnetlib.Telnet(HOST, timeout=5) as tn:
        print(f"正在連接到 {HOST} ...")

        # 登入
        tn.read_until(b'login: ', timeout=3)
        tn.write(USERNAME.encode('ascii') + b"\n")
        tn.read_until(b'Password: ', timeout=3)
        tn.write(PASSWORD.encode('ascii') + b"\n")

        # 確保成功登入
        tn.read_until(PROMPT, timeout=5)
        print(f"成功登入 {HOST}")

        # **建立並寫入腳本**
        print("正在創建 test.sh 腳本...")
        tn.write(b"cat > /tmp/test.sh <<EOF\n")
        for line in script_content.split("\n"):
            tn.write(line.encode("ascii") + b"\n")
        tn.write(b"EOF\n")
        tn.write(b"chmod +x /tmp/test.sh\n")  # 賦予執行權限

        # **等待命令執行完畢**
        time.sleep(1)
        output = tn.read_very_eager().decode("ascii")
        print("創建腳本輸出:\n", output)

        # **執行 `test.sh` 腳本，並持續監聽輸出**
        print("開始執行 test.sh，按 Ctrl+C 手動停止...")
        tn.write(b"/tmp/test.sh\n")  # 直接在前台執行

        # **持續即時接收輸出**
        while True:
            output = tn.read_very_eager().decode("ascii")
            if output:
                print(output, end="")  # 即時輸出到終端
            time.sleep(0.5)  # 降低 CPU 負載，避免過度輪詢

except KeyboardInterrupt:
    print("\n手動停止執行，關閉 Telnet 連線...")
    # Since 'tn' is defined inside the 'with' block, we don't need to manually close it.
    print("連線已關閉。")
except Exception as e:
    print(f"發生錯誤: {e}")