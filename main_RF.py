import os
import re
import logging
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

class RouterTestApp:
    def __init__(self, root):
        self.root = root
        self.driver = None
        self.log_text = None
        self.channel_options = ["自動","100", "104", "108", "112", "116", "120", "124", "128", "132", "136", "140", "144", "149", "153", "157", "161", "165"]
        self.dut_url = "http://192.168.50.1/Main_Login.asp"
        self.dut_url_wifi = "http://192.168.50.1/Advanced_Wireless_Content.asp"
        self.esg_url = "http://192.168.50.18/display"
        self.wave_url = "http://192.168.50.14/remote_fp.html"
        self.http_username = "admin"
        self.http_password = "admin"
        self.setup_logging()
        self.setup_gui()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s - %(levelname)s] - %(message)s")
        self.logger = logging.getLogger()

    def print_msg(self, msg):
        self.logger.info(msg)
        if self.log_text:
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, msg + "\n")
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
            self.root.update()

    def start_driver(self):
        if not self.driver:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()

    def countdown(self, seconds):
        def tick(i):
            self.print_msg(f"倒數: {i}秒")
            if i > 1:
                self.root.after(1000, tick, i-1)
        tick(seconds)

    # ...將原本的 login, get_dfs_channel, change_channel, reboot_router, wait_for_completion, open_esg_web, open_wave_web, start_test 等函式都改成 self.xxx() 並將 driver, print_msg 換成 self.driver, self.print_msg...

    def setup_gui(self):
        self.root.title("路由器測試工具")
        progress_bar = ttk.Progressbar(self.root, length=300, mode="indeterminate")
        progress_bar.pack(pady=20)
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TLabel", font=("Helvetica", 12), background="#2c3e50", foreground="white")
        style.configure("TButtonStartTest", font=("Helvetica", 12, "bold"), foreground="green")
        frame = ttk.Frame(self.root, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        login_btn = ttk.Button(frame, text="登入路由器", command=lambda: threading.Thread(target=self.login).start())
        login_btn.pack(fill=tk.X, pady=10)
        get_channel_btn = ttk.Button(frame, text="獲取當前控制頻道", command=lambda: threading.Thread(target=self.get_dfs_channel).start())
        get_channel_btn.pack(fill=tk.X, pady=10)
        channel_label = ttk.Label(frame, text="選擇 WiFi 頻道:")
        channel_label.pack(pady=5)
        self.channel_var = tk.StringVar()
        channel_dropdown = ttk.Combobox(frame, textvariable=self.channel_var, values=self.channel_options, state="readonly")
        channel_dropdown.pack(fill=tk.X, pady=5)
        change_channel_btn = ttk.Button(frame, text="更改頻道", command=lambda: threading.Thread(target=self.change_channel, args=(self.channel_var.get(),)).start())
        change_channel_btn.pack(fill=tk.X, pady=5)
        reboot_btn = ttk.Button(frame, text="重新開機路由器", command=lambda: threading.Thread(target=self.reboot_router).start())
        reboot_btn.pack(fill=tk.X, pady=5)
        esg_btn = ttk.Button(frame, text="E4438C", command=lambda: threading.Thread(target=self.open_esg_web, args=(self.channel_var.get(),)).start())
        esg_btn.pack(fill=tk.X, pady=5)
        wave_btn = ttk.Button(frame, text="33220A", command=lambda: threading.Thread(target=self.open_wave_web).start())
        wave_btn.pack(fill=tk.X, pady=5)
        start_test_btn = ttk.Button(frame, text="開始測試", command=lambda: threading.Thread(target=self.start_test, args=(self.channel_var.get(),)).start())
        start_test_btn.pack(fill=tk.X, pady=5)
        self.log_text = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state='disabled', bg="#000000", fg="#39ff14", font=("Courier New", 12)
        )
        self.log_text.pack(fill=tk.X, pady=5)
        self.log_text.configure(bg="black", fg="#39ff14")

    # ...其餘函式請依照原本邏輯搬進類別，並將 driver, print_msg 換成 self.driver, self.print_msg...

    def on_close(self):
        if self.driver:
            self.driver.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RouterTestApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()