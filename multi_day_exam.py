from tkinter import Tk, LabelFrame, Button, Label, Entry, Listbox, Scrollbar, messagebox, END, SINGLE, ttk, Toplevel, Menu
from datetime import datetime, date, timedelta
import os
from utils import JSON_PATH, TIME_FORMAT, load_data, save_data, calculate_end_time

def Settonsofday():
    # 全局配置
    base_title = "考试时间录入"
    # 全局变量
    is_saved = True
    data = load_data()  # 存储结构: {日期: [考试信息列表]}
    current_date = None
    date_listbox = None
    time_tree = None
    add_time_btn = None
    setofdayWindow = None
    
    def update_title():
        nonlocal is_saved
        if is_saved:
            setofdayWindow.title(base_title)
        else:
            setofdayWindow.title(f"{base_title}-有未保存的考试！")
    
    def refresh_date_list():
        nonlocal date_listbox, data
        date_listbox.delete(0, END)
        for date_item in sorted(data.keys()):
            date_listbox.insert(END, date_item)
    
    def on_date_select(event):
        nonlocal current_date, date_listbox, add_time_btn, time_tree, data
        selected = date_listbox.curselection()
        if not selected:
            current_date = None
            add_time_btn.config(state="disabled")
            return

        current_date = date_listbox.get(selected[0])
        add_time_btn.config(state="normal")
    
        # 刷新表格
        for item in time_tree.get_children():
            time_tree.delete(item)
        for exam in data.get(current_date, []):
            time_tree.insert("", END, values=(exam["subject"], exam["start_time"], exam["duration"]))
    
    def add_date():
        nonlocal data, is_saved
        top = Toplevel(setofdayWindow)
        top.title("选择日期")
        top.grid_columnconfigure(0, weight=1)
    
        Label(top, text="请选择考试日期：").grid(row=0, column=0, pady=10, padx=10, sticky="n")

        cal = Entry(top, width=12)
        seetoday = str(date.today())
        cal.insert(0, seetoday)
        cal.grid(row=1, column=0, pady=10)
    
        def confirm():
            nonlocal is_saved
            date_str = cal.get()
            if date_str not in data:
                data[date_str] = []
                refresh_date_list()
                is_saved = False
                update_title()
            else:
                messagebox.showwarning("提示", f"日期 {date_str} 已存在")
            top.destroy()
    
        Button(top, text="确认", command=confirm).grid(row=2, column=0, pady=10)
    
    def add_time():
        nonlocal current_date, data, is_saved
        if not current_date:
            return
    
        top = Toplevel(setofdayWindow)
        top.title("添加考试时间")

        top.grid_columnconfigure(1, weight=1)
    
        # 科目输入
        Label(top, text="考试科目：").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        subject_entry = Entry(top)
        subject_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        subject_entry.insert(0, "数学")
    
        # 开始时间
        Label(top, text="开始时间：").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        time_entry = Entry(top)
        time_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        time_entry.insert(0, "09:00")
        Label(top, text="(HH:MM)", font=("TkDefaultFont", 8)).grid(row=1, column=2, padx=5, sticky="w")
    
        # 时长
        Label(top, text="时长(分钟)：").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        duration_entry = Entry(top)
        duration_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        duration_entry.insert(0, "120")
    
        def confirm():
            nonlocal is_saved
            subject = subject_entry.get().strip()
            start_time = time_entry.get().strip()
            duration_str = duration_entry.get().strip()
        
            if not all([subject, start_time, duration_str]):
                messagebox.showerror("错误", "请填写所有字段")
                return
            try:
                datetime.strptime(start_time, TIME_FORMAT)
                duration = int(duration_str)
                if duration <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("错误", "时间格式错误或时长需为正整数")
                return
            
            current_exams = data[current_date]
            has_conflict = False
        
            for exam in current_exams:
                if exam["start_time"] == start_time:
                    messagebox.showwarning(parent=setofdayWindow, title="提示", message=f"时间设置冲突！{start_time} 的考试时段已经被分配给其他科目")
                    has_conflict = True
                    break
        
            if not has_conflict:
                data[current_date].append({
                    "subject": subject,
                    "start_time": start_time,
                    "duration": duration
                })
                on_date_select(None)
                is_saved = False
                update_title()
            top.destroy()
    
        Button(top, text="确认", command=confirm).grid(row=3, column=0, columnspan=2, pady=20)
    
    def delete_date():
        nonlocal date_listbox, data, is_saved
        selected = date_listbox.curselection()
        if not selected:
            messagebox.showinfo(parent=setofdayWindow, title="提示", message="请先选中要删除的日期")
            return
        
        selected_date = date_listbox.get(selected[0])
        
        if messagebox.askyesno(parent=setofdayWindow, title="确认删除", message=f"确定要删除 {selected_date} 及该日期下的所有考试吗？"):
            if selected_date in data:
                del data[selected_date]
                refresh_date_list()
                for item in time_tree.get_children():
                    time_tree.delete(item)
                is_saved = False
                update_title()
    
    def change_date():
        nonlocal date_listbox, data, is_saved
        selected = date_listbox.curselection()
        if not selected:
            messagebox.showinfo(parent=setofdayWindow, title="提示", message="请先选中要修改的日期")
            return
        
        selected_date = date_listbox.get(selected[0])
        
        if selected_date in data:
            top = Toplevel(setofdayWindow)
            top.title("修改考试日期")
            top.grid_columnconfigure(0, weight=1)
        
            Label(top, text="请修改考试日期：").grid(row=0, column=0, pady=10, padx=10, sticky="n")

            cal = Entry(top, width=12)
            cal.insert(0, selected_date)
            cal.grid(row=1, column=0, pady=10)
        
            def confirm():
                nonlocal is_saved
                date_item = cal.get()
                if date_item in data:
                    messagebox.showwarning("提示", f"日期 {date_item} 已经存在")                
                else:
                    data[date_item] = data[selected_date]
                    del data[selected_date]
                    refresh_date_list()
                    is_saved = False
                    update_title()
                top.destroy()
                
            Button(top, text="确认", command=confirm).grid(row=2, column=0, pady=10)
            
            is_saved = False
            update_title()
    
    def delete_exam():
        nonlocal time_tree, current_date, data, is_saved
        selected_item = time_tree.selection()
        if not selected_item or not current_date:
            messagebox.showinfo("提示", "请先选中要删除的考试")
            return
        
        item_values = time_tree.item(selected_item[0], "values")
        exam_subject = item_values[0]
        exam_time = item_values[1]
        
        if messagebox.askyesno("确认删除", f"确定要删除 {exam_subject}（{exam_time}）吗？"):
            current_exams = data[current_date]
            for i, exam in enumerate(current_exams):
                if exam["subject"] == exam_subject and exam["start_time"] == exam_time:
                    del current_exams[i]
                    break
            on_date_select(None)
            is_saved = False
            update_title()
    
    def modify_exam():
        nonlocal time_tree, current_date, data, is_saved
        selected_item = time_tree.selection()
        if not selected_item or not current_date:
            messagebox.showinfo(parent=setofdayWindow, title="提示", message="请先选中要修改的考试")
            return
    
        item_values = time_tree.item(selected_item[0], "values")
        old_subject = item_values[0]
        old_start_time = item_values[1]
        old_duration = item_values[2]

        top = Toplevel(setofdayWindow)
        top.title("修改考试信息")
        top.grid_columnconfigure(1, weight=1)
    
        Label(top, text="考试科目：").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        subject_entry = Entry(top)
        subject_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        subject_entry.insert(0, old_subject)
    
        Label(top, text="开始时间：").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        time_entry = Entry(top)
        time_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        time_entry.insert(0, old_start_time)
        Label(top, text="(HH:MM)", font=("TkDefaultFont", 8)).grid(row=1, column=2, padx=5, sticky="w")
    
        Label(top, text="时长(分钟)：").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        duration_entry = Entry(top)
        duration_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        duration_entry.insert(0, old_duration)
        
        def confirm_modify():
            nonlocal is_saved
            new_subject = subject_entry.get().strip()
            new_start_time = time_entry.get().strip()
            new_duration_str = duration_entry.get().strip()
        
            if not all([new_subject, new_start_time, new_duration_str]):
                messagebox.showerror(parent=setofdayWindow, title="错误", message="请填写所有字段")
                return
            try:
                datetime.strptime(new_start_time, TIME_FORMAT)
                new_duration = int(new_duration_str)
                if new_duration <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(parent=setofdayWindow, title="错误", message="时间格式错误或时长需为正整数")
                return
        
            current_exams = data[current_date]
            has_conflict = False
            for exam in current_exams:
                if (exam["start_time"] == new_start_time and 
                    not (exam["subject"] == old_subject and exam["start_time"] == old_start_time)):
                    messagebox.showwarning(parent=setofdayWindow, title="提示", message=f"时间冲突！{new_start_time} 已被其他科目占用")
                    has_conflict = True
                    break
            if has_conflict:
                return
        
            for i, exam in enumerate(current_exams):
                if exam["subject"] == old_subject and exam["start_time"] == old_start_time:
                    current_exams[i] = {
                        "subject": new_subject,
                        "start_time": new_start_time,
                        "duration": new_duration
                    }
                    break
        
            on_date_select(None)
            is_saved = False
            update_title()
            top.destroy()
            
        Button(top, text="确认修改", command=confirm_modify).grid(row=3, column=0, columnspan=2, pady=20)
    
    def on_closing():
        nonlocal is_saved, data, setofdayWindow
        if not is_saved and data:
            result = messagebox.askyesnocancel(parent=setofdayWindow, title="提示", message="有未保存的考试信息，是否保存后再关闭？")
            if result is None:
                return
            elif result:
                global_save_data()
        setofdayWindow.destroy()
    
    def global_save_data():
        nonlocal data, is_saved
        if save_data(data):
            is_saved = True
            update_title()
    
    # 创建主窗口
    setofdayWindow = Tk()
    setofdayWindow.title(base_title)
    update_title()
    setofdayWindow.grid_rowconfigure(1, weight=1)
    setofdayWindow.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 左侧日期列表区域
    setofdayWindow.grid_columnconfigure(0, minsize=200)
    Label(setofdayWindow, text="考试日期列表", font=("TkDefaultFont", 12)).grid(row=0, column=0, sticky="nw")
    
    # 日期列表（带滚动条）
    date_frame = LabelFrame(setofdayWindow)
    date_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    date_frame.grid_rowconfigure(0, weight=1)
    date_frame.grid_columnconfigure(0, weight=1)

    date_scroll = Scrollbar(date_frame)
    date_scroll.grid(row=0, column=1, sticky="ns")
    date_listbox = Listbox(
        date_frame, selectmode=SINGLE, yscrollcommand=date_scroll.set, height=15
    )
    date_listbox.grid(row=0, column=0, sticky="nsew")
    date_scroll.config(command=date_listbox.yview)
    date_listbox.bind('<<ListboxSelect>>', on_date_select)
    
    # 日期菜单
    date_menu = Menu(date_listbox, tearoff=0)
    date_menu.add_command(label="删除日期", command=delete_date)
    date_menu.add_command(label="修改日期", command=change_date)
    
    def show_date_menu(event):
        if date_listbox.curselection():
            date_menu.post(event.x_root, event.y_root)
    
    date_listbox.bind("<Button-3>", show_date_menu)
    
    # 添加日期按钮
    Button(setofdayWindow, text="+ 添加日期", command=add_date).grid(
        row=2, column=0, padx=10, pady=10, sticky="ew"
    )
    
    # 右侧单科时间区域
    setofdayWindow.grid_columnconfigure(1, weight=1)
    Label(setofdayWindow, text="单科考试时间", font=("TkDefaultFont", 12)).grid(
        row=0, column=1, sticky="nw"
    )
    
    # 单科时间表格
    tree_frame = LabelFrame(setofdayWindow)
    tree_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    columns = ("科目", "开始时间", "时长(分钟)")
    time_tree = ttk.Treeview(
        tree_frame, columns=columns, show="headings", height=10
    )
    for col in columns:
        time_tree.heading(col, text=col)
        time_tree.column(col, width=150)
    time_tree.grid(row=0, column=0, sticky="nsew")
    
    # 考试菜单
    exam_menu = Menu(time_tree, tearoff=0)
    exam_menu.add_command(label="删除考试", command=delete_exam)
    exam_menu.add_command(label="修改考试", command=modify_exam)
    
    def show_exam_menu(event):
        if time_tree.selection():
            exam_menu.post(event.x_root, event.y_root)
    
    time_tree.bind("<Button-3>", show_exam_menu)
    
    # 添加单科时间按钮
    add_time_btn = Button(setofdayWindow, text="+ 添加单科时间", command=add_time, state="disabled")
    add_time_btn.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    
    # 保存按钮
    Button(setofdayWindow, text="保存", command=global_save_data).grid(row=2, column=1, padx=10, pady=10, sticky="e")
    
    # 初始化
    refresh_date_list()
    
    setofdayWindow.mainloop()

def stratToomanyDays():
    if not os.path.exists(JSON_PATH):
        messagebox.showerror("错误", f"未找到考试日程文件 {JSON_PATH}")
        return

    try:
        exam_data = load_data()
    except Exception as e:
        messagebox.showerror("错误", f"读取文件失败: {str(e)}")
        return

    if not exam_data:
        messagebox.showinfo("提示", "考试日程为空")
        return

    display_window = Tk()
    display_window.title("多日考试倒计时")
    display_window.grid_rowconfigure(1, weight=1)
    display_window.grid_columnconfigure(0, weight=1)

    Label(display_window, text="所有考试日程", font=("TkDefaultFont", 25)).grid(row=2, column=0, pady=10, sticky="nsew")
    
    # 添加样式设置
    style = ttk.Style()
    style.configure("Treeview", font=("TkDefaultFont", 20, "bold"), rowheight=30)
    style.configure("Treeview.Heading", font=("TkDefaultFont", 21, "bold"))

    columns = ("日期", "科目", "开始时间", "结束时间", "时长(分钟)")
    tree = ttk.Treeview(display_window, columns=columns, show="headings")
    for i, col in enumerate(columns):
        tree.heading(col, text=col)
        if i == 0:
            tree.column(col, width=180, anchor="center")
        else:
            tree.column(col, width=150, anchor="center")
    tree.grid(row=3, column=0, padx=10, pady=10)

    all_exams = []
    for exam_date, exams in exam_data.items():
        for exam in exams:
            start_time = exam["start_time"]
            duration = exam["duration"]
            end_time = calculate_end_time(start_time, duration)

            all_exams.append({
                "date": exam_date,
                "subject": exam["subject"],
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration
            })
            
            tree.insert("", END, values=(
                exam_date,
                exam["subject"],
                start_time,
                end_time,
                duration
            ))

    countdown_label = Label(display_window, text="", font=("TkDefaultFont", 64))
    countdown_label.grid(row=0, column=0, pady=10, sticky="nsew")
    status_label = Label(display_window, text="", font=("TkDefaultFont", 32))
    status_label.grid(row=1, column=0, pady=10, sticky="nsew")
    current_exam_index = -1
    today_str = str(date.today())
    today_exams = []

    if today_str in exam_data:
        for exam in exam_data[today_str]:
            try:
                start_dt = datetime.strptime(f"{today_str} {exam['start_time']}", "%Y-%m-%d %H:%M")
                today_exams.append({
                    "start_dt": start_dt,
                    "subject": exam["subject"],
                    "duration": exam["duration"],
                    "start_time": exam["start_time"]
                })
            except:
                continue

        today_exams.sort(key=lambda x: x["start_dt"])

        now = datetime.now()
        for i, exam in enumerate(today_exams):
            if exam["start_dt"] > now:
                current_exam_index = i
                break

        if current_exam_index == -1:
            for i, exam in enumerate(today_exams):
                end_dt = exam["start_dt"] + timedelta(minutes=exam["duration"])
                if now < end_dt:
                    current_exam_index = i
                    break

    def update_countdown():
        nonlocal current_exam_index
        now = datetime.now()
        
        if not today_exams:
            status_label.config(text=f"今天({today_str})没有考试")
            countdown_label.config(text="")
            display_window.after(1000, update_countdown)
            return

        if current_exam_index < 0 or current_exam_index >= len(today_exams):
            status_label.config(text=f"今天({today_str})所有考试已结束")
            countdown_label.config(text="")
            display_window.after(5000, display_window.destroy)
            return

        current_exam = today_exams[current_exam_index]
        start_dt = current_exam["start_dt"]
        end_dt = start_dt + timedelta(minutes=current_exam["duration"])
        
        if now < start_dt:
            remaining = start_dt - now
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown_label.config(text=f"距离考试开始还有: {hours}时{minutes}分{seconds}秒")
            display_window.after(1000, update_countdown)
            status_label.config(text=f"即将开始的考试: {current_exam['subject']} ({today_str} {current_exam['start_time']})")

        elif now < end_dt:
            remaining = end_dt - now
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown_label.config(text=f"考试进行中\n剩余: {hours}时{minutes}分{seconds}秒")
            display_window.after(1000, update_countdown)
            status_label.config(text=f"当前考试: {current_exam['subject']} ({today_str} {current_exam['start_time']})")
        else:
            countdown_label.config(text="本场考试已结束")
            current_exam_index += 1
            display_window.after(3000, update_countdown)

    update_countdown()
    # 窗口最大化
    display_window.state('zoomed')
    display_window.mainloop()