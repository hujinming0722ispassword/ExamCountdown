import json
import os
from datetime import datetime, date, timedelta
from tkinter import messagebox

# 共享常量
JSON_PATH = "exam_schedule.json"
TIME_FORMAT = "%H:%M"

# 共享函数
def load_data():
    """加载已有数据"""
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    """保存数据到JSON"""
    if not data:
        messagebox.showwarning(title="提示", message="暂无数据可保存")
        return

    try:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo(title="考试文件已经被保存至程序所在目录", message=f"已保存到 {JSON_PATH}")
        return True
    except Exception as e:
        messagebox.showerror("错误", f"保存失败：{str(e)}")
        return False

def calculate_end_time(start_time, duration):
    """计算结束时间"""
    start_dt = datetime.strptime(start_time, TIME_FORMAT)
    end_dt = start_dt + timedelta(minutes=duration)
    return end_dt.strftime(TIME_FORMAT)