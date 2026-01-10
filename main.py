from tkinter import Tk, Label, Button, Entry
from datetime import datetime

root = Tk()
root.title("ExamCountdown")

# 创建界面元素
title1 = Label(text="请输入有关此次考试的信息", font=("TkDefaultFont", 32))
title1.grid(row=0, column=0, sticky="N", columnspan=2)

tip1 = Label(text="请输入此次考试的科目", font=("TkDefaultFont", 16))
tip1.grid(row=1, column=0, sticky="W")
EntrySub = Entry(font=("TkDefaultFont", 16), width=20)
EntrySub.grid(row=1, column=1, sticky="W")

tip2 = Label(text="请输入此次考试以分钟计算的时长", font=("TkDefaultFont", 16))
tip2.grid(row=2, column=0, sticky="W")
EntryMinutes = Entry(font=("TkDefaultFont", 16), width=20)
EntryMinutes.grid(row=2, column=1, sticky="W")
EntryMinutes.insert(0, "120")

tip3 = Label(text="请输入此次考试的开始时间", font=("TkDefaultFont", 16))
tip3.grid(row=3, column=0, sticky="W")
EntryStartTime = Entry(font=("TkDefaultFont", 16), width=20)
EntryStartTime.grid(row=3, column=1, sticky="W")

now = datetime.now().strftime("%H:%M")
EntryStartTime.insert(0, now)

# 懒加载函数

def lazy_load_single_exam():
    """懒加载单场考试模块并执行"""
    # 先获取输入值
    start_time_input = EntryStartTime.get()
    minutes_input = EntryMinutes.get()
    subject_input = EntrySub.get()
    
    # 再销毁窗口并加载模块
    from single_exam import ExamStart
    root.destroy()  # 关闭主窗口
    ExamStart(
        start_time_input=start_time_input,
        minutes_input=minutes_input,
        subject_input=subject_input
    )

def lazy_load_multi_day_set():
    """懒加载多日考试设置模块并执行"""
    from multi_day_exam import Settonsofday
    root.destroy()  # 关闭主窗口
    Settonsofday()

def lazy_load_multi_day_start():
    """懒加载多日考试开始模块并执行"""
    from multi_day_exam import stratToomanyDays
    root.destroy()  # 关闭主窗口
    stratToomanyDays()

# 创建按钮
ButtonOfExit = Button(text="退出", command=root.destroy, width=20)
ButtonOfExit.grid(row=4, column=0, sticky="E")

ButtonOfStart = Button(text="开始考试", command=lazy_load_single_exam, width=20)
ButtonOfStart.grid(row=4, column=1, sticky="E")

ButtonOfMakelist = Button(text="设定多日或多次考试", command=lazy_load_multi_day_set, width=20)
ButtonOfMakelist.grid(row=5, column=0, sticky="E", pady=10)

ButtonOfReadlist = Button(text="读取多日或多次考试并开始", command=lazy_load_multi_day_start, width=20)
ButtonOfReadlist.grid(row=5, column=1, sticky="E", pady=10)

# 设置窗口位置
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
windowX = int(((screen_width - window_width) / 2) - 200)
windowY = int(((screen_height - window_height) / 2) + 80)
root.geometry(f"+{windowX}+{windowY}")

# 开始主循环
root.mainloop()