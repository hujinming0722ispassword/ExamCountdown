from tkinter import Tk, Label, messagebox
from datetime import datetime, date, timedelta

def ExamStart(start_time_input, minutes_input, subject_input):
    if ":" not in start_time_input:
        messagebox.showerror("错误", "您需要输入正确的时间格式,冒号应该为英文冒号，请在输入时切换为英文输入法以规避此问题。")
        return
    
    subject_text = f"本场考试的科目是{subject_input}" if subject_input else "未输入考试科目"
    
    startTimeALL = datetime.strptime(start_time_input, "%H:%M")
    time_interval1 = timedelta(minutes=int(minutes_input))
    end = startTimeALL + time_interval1
    startTime = startTimeALL.time()
    endTime = end.time()
    
    def count_down(REMSEC):
        minutes = REMSEC // 60
        secs = REMSEC % 60
        timeLABEL.config(text=f"考试时间还有{minutes}:{secs}")

        if REMSEC > 0:
            countDownWindow.after(1000, count_down, REMSEC - 1)
        else:
            timeLABEL.config(text="考试结束！")

    Testseconds = int(time_interval1.total_seconds())

    countDownWindow = Tk()
    now = datetime.now()
    countDownWindow.title("ExamCountdown")

    if now.time() < startTime:
        today = now.date()
        
        timeLABEL = Label(countDownWindow, text=f"考试将在{start_time_input}开始", font=("TkDefaultFont", 64))
        timeLABEL.grid(row=0, column=0, sticky="nsew")
        start_datetime = datetime.combine(today, startTime)
        current_datetime = now
        wait_seconds = (start_datetime - current_datetime).total_seconds()
        countDownWindow.after(int(wait_seconds * 1000), count_down, Testseconds)
        subjectlabel = Label(countDownWindow, text=f"{subject_text}", font=("TkDefaultFont", 64))
        subjectlabel.grid(row=1, column=0)
        countDownWindow.grid_columnconfigure(0, weight=1)
        countDownWindow.grid_rowconfigure(0, weight=1)
        countDownWindow.grid_rowconfigure(1, weight=1)
    elif now.time() == startTime or now.time() > startTime < endTime:
        timeLABEL = Label(countDownWindow, text="考试结束！", font=("TkDefaultFont", 64))
        timeLABEL.grid(row=0, column=0)
        current_time = datetime.combine(now.date(), now.time())
        end_datetime = datetime.combine(now.date(), endTime)
        remaining = int((end_datetime - current_time).total_seconds())
        REMSEC = remaining if remaining > 0 else 0
        subjectlabel = Label(countDownWindow, text=f"{subject_text}", font=("TkDefaultFont", 64))
        count_down(REMSEC)
        timeLABEL.grid(row=0, column=0)
        subjectlabel.grid(row=1, column=0)
        countDownWindow.grid_columnconfigure(0, weight=1)
        countDownWindow.grid_rowconfigure(0, weight=1)
        countDownWindow.grid_rowconfigure(1, weight=1)

    # 窗口最大化
    countDownWindow.state('zoomed')

    countDownWindow.mainloop()