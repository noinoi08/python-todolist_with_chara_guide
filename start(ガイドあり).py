import tkinter as tk
from tkinter import ttk
from CsvManager import CsvManager
from tkinter import messagebox
import State_to_value
import Guide

class GUI:
    def __init__(self,master):
        self.master = master
        self.row_count = 0
        self.csvM = CsvManager()
        self.file_path = self.csvM.check_csv_file()
        self.task_list = self.csvM.load_data_from_csv(self.file_path)
        self.mode_select=["追加","編集","削除","未選択"]
        self.color_set = ["lightcyan","white","paleturquoise"]
        self.state_set = ["","検討中","進行中","テスト中","完了"]
        self.color_count = 0
        self.value_star = ["","★","★★","★★★"]
        self.edit_flag = False
        self.selected_node = ""
        self.canvas = None

    def create_window(self):
        # id,task,limit,value,state,person,progress,tag
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill="both",expand=True)
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(4,weight=1)

        L_title_Edit = tk.Label(self.frame, text="Editor")
        L_title_Edit.grid(row=self.row_count, column=0,columnspan=9, padx=5, pady=5,sticky = tk.EW)

        self.row_count += 1
        # ラベルを作成
        L_task = tk.Label(self.frame, text="task")
        L_limit = tk.Label(self.frame, text="limit")
        L_value = tk.Label(self.frame, text="value")
        L_state = tk.Label(self.frame, text="state")
        L_person = tk.Label(self.frame, text="person")
        L_progress = tk.Label(self.frame, text="progress")
        L_tag = tk.Label(self.frame, text="tag")

        # ラベルを横に並べるための配置設定
        L_task.grid(row=self.row_count, column=0)
        L_limit.grid(row=self.row_count, column=1)
        L_value.grid(row=self.row_count, column=2)
        L_state.grid(row=self.row_count, column=3)
        L_person.grid(row=self.row_count, column=4)
        #L_progress.grid(row=self.row_count, column=5)
        L_tag.grid(row=self.row_count, column=6)

        self.progress_button = tk.Button(self.frame,text = "progress", command=self.progress_circles)
        self.progress_button.grid(row=self.row_count, column=5)

        self.button_text = "何する？"
        self.B_action = tk.Button(self.frame,text = self.button_text, command=lambda: self.button_manager(self.button_text))
        self.B_action.grid(row=self.row_count,column=7,columnspan=2,sticky="ew")

        self.row_count += 1

        # Entryの作成
        self.E_task_edit = tk.Entry(self.frame)
        self.E_task_edit.grid(row=self.row_count, column=0, sticky="ew")

        self.E_limit_edit = tk.Entry(self.frame,width=12)
        self.E_limit_edit.grid(row=self.row_count, column=1, sticky="ew")

        self.CB_value_select = ttk.Combobox(self.frame,textvariable=tk.IntVar(),width=6,values=self.value_star,state="readonly")
        self.CB_value_select.grid(row=self.row_count,column=2)

        self.CB_state_select = ttk.Combobox(self.frame,textvariable=tk.IntVar(),width=10,values=self.state_set,state="readonly")
        self.CB_state_select.grid(row=self.row_count,column=3, sticky="ew")

        self.person_entry = tk.Entry(self.frame)
        self.person_entry.grid(row=self.row_count, column=4, sticky="ew")

        self.progress_entry = tk.Entry(self.frame,width=10)
        self.progress_entry.grid(row=self.row_count, column=5, sticky="ew")
        
        self.tag_entry = tk.Entry(self.frame,width=6)
        self.tag_entry.grid(row=self.row_count, column=6, sticky="ew")

        self.CB_mode_select = ttk.Combobox(self.frame,textvariable=tk.IntVar(),width=6,values=self.mode_select,state="readonly")
        self.CB_mode_select.grid(row=self.row_count,column=7)
        self.CB_mode_select.set(self.mode_select[3])
        self.CB_mode_select.bind("<<ComboboxSelected>>", lambda event: self.update_button_text())

        self.row_count += 1

        L_title = tk.Label(self.frame, text="Task List")
        L_title.grid(row=self.row_count, column=0,columnspan=9, padx=5, pady=5,sticky = tk.EW)

        self.row_count += 1

        self.task_infomation()

        self.canvas = Guide.guide_animation(self.master)
        self.canvas.create_canvas(self.master)

    def task_infomation(self):

        # Treeviewウィジェットの作成
        self.tree = ttk.Treeview(self.frame)
        self.tree["columns"] = ('id','limit','value','state','person','progress','tag')
        
        self.tree.tag_configure("indigo",background="#e5e5ff") # mainツリー
        self.tree.tag_configure("white",background="white")
        self.tree.tag_configure("paleturquoise",background="#afeeee")
        self.tree.tag_configure("gray",background="#8b968d")  # 完了
        self.tree.tag_configure("green",background="#e5ffe5") # 進行中
        self.tree.tag_configure("yellow",background="#ffffcc") # 検討中
        self.tree.tag_configure("red",background="#ffe0ff") # テスト中
        self.tree.tag_configure('big_font', font=('Arial', 12))

        # 列の設定
        self.tree.column("id", width=10, anchor="center")
        self.tree.column("limit", width=50, anchor="center")
        self.tree.column("value", width=10, anchor="center")
        self.tree.column("state", width=10, anchor="center")        
        self.tree.column("person", width=100, anchor="center")
        self.tree.column("progress", width=100, anchor="w")
        self.tree.column("tag", width=10, anchor="center")

        # ヘッダーの設定
        self.tree.heading("id", text="id")
        self.tree.heading("limit", text="Limit")
        self.tree.heading("value", text="Value",command=lambda: self.sort_tree_value(self.selected_node))
        self.tree.heading("state", text="State",command=lambda: self.sort_tree("state",self.selected_node))
        self.tree.heading("person", text="Person")
        self.tree.heading("progress", text="Progress")
        self.tree.heading("tag", text="Tag")

        has_empty_parent = any(item.tag == "main" for item in self.task_list)

        if has_empty_parent:
            main_indices = [index for index, item in enumerate(self.task_list) if item.tag == 'main']
            for index in main_indices:
                task = self.task_list[index]
                color = self.throw_state_color(task.state)
                if task.state == "進行中":
                    flag = True
                else:
                    flag = False
                parent = self.tree.insert('', 'end', text=task.task,tags=color)
                self.tree.item(parent,open=flag, values=(task.id, task.limit, task.value, task.state, task.person, task.progress, task.tag))
                self.build_tree(self.tree, parent, self.task_list[index].id, self.task_list)
                self.sort_tree("state",parent)
        else:
            print("ルートノードが見つかりません")

        # Treeviewウィジェットの配置
        self.tree.grid(row=self.row_count, column=0, columnspan=8, sticky="nsew")
        
        # スクロールバーの作成.
        self.tree_scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        # Treeviewとスクロールバーを関連付ける
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=self.row_count, column=8, sticky='ns')

        # ツリーの要素クリック時のイベントハンドラをバインド
        self.tree.bind("<<TreeviewSelect>>", self.handle_treeview_click)

    def build_tree(self, tree, parent_node, parent_id, data):
        children = [task for task in data if parent_id == task.tag]
        for child in children:
            state = child.state
            color = self.throw_state_color(state)
            if state == "進行中":
                flag = True
            else:
                flag = False
            child_node = tree.insert(parent_node, 'end', text=child.task,tags = color)
            self.tree.item(child_node,open = flag, values=(child.id, child.limit, child.value, child.state, child.person, child.progress, child.tag))
            has_parent = any(item.tag == child.id for item in data)
            if has_parent:
                self.build_tree(tree, child_node, child.id, data)
            if flag == True:
                self.sort_tree("state",child_node)

    def button_manager(self,text):
        if text == "編集":
            self.edit_task()
        elif text == "削除":
            self.delete_task()
        elif text == "追加":
            self.add_new_task()
        else:
            self.canvas.conversation_text("ボックスからボタンの作業を選んでね")
            return
        
    def add_new_task(self):

        task = self.E_task_edit.get()
        if not task:
            self.canvas.conversation_text("追加するときはタスクを入力してね")
            return
        limit = self.E_limit_edit.get() if self.E_limit_edit.get() else "null"
        value = self.CB_value_select.get() if self.CB_value_select.get() else "null"
        state = self.CB_state_select.get() if self.CB_state_select.get() else "null"
        person = self.person_entry.get() if self.person_entry.get() else "null"
        progress = self.progress_entry.get() if self.progress_entry.get() else "null"
        tag = self.tag_entry.get() if self.tag_entry.get() else "main"
        self.csvM.add_data(self.file_path,task,limit,value,state,person,progress,tag)

        self.reload_info()
        self.default_entry_box()
        self.canvas.conversation_text("タスクを追加したよ")

    def edit_task(self):

        task = self.E_task_edit.get()
        if not task:
            self.canvas.conversation_text("編集するときはタスクを入力してね")
            return
        id = self.edit_id_value
        limit = self.E_limit_edit.get() if self.E_limit_edit.get() else "null"
        value = self.CB_value_select.get() if self.CB_value_select.get() else "null"
        state = self.CB_state_select.get() if self.CB_state_select.get() else "null"
        person = self.person_entry.get() if self.person_entry.get() else "null"
        progress = self.progress_entry.get() if self.progress_entry.get() else "null"
        tag = self.tag_entry.get() if self.tag_entry.get() else "main"
        self.csvM.Update_data(self.file_path,id,task,limit,value,state,person,progress,tag)

        self.reload_info()
        self.default_entry_box()
        if state == "完了":
            text = "このタスクは終了！\nお疲れさま"
        else:
            text = "編集完了！"
        self.canvas.conversation_text(text)

    def delete_task(self):
        task = self.E_task_edit.get()
        if not task:
            self.canvas.conversation_text("削除するならタスクを選んでからボタンを押してね")
            return
        
        answer = messagebox.askyesno('Alert!', '本当に消しますか？')
        if not answer:
            return

        id = self.edit_id_value
        
        self.csvM.delete_data(id, self.file_path)

        self.reload_info()
        self.default_entry_box()
        self.canvas.conversation_text("削除完了！")

    def handle_treeview_click(self,event):
        item = self.tree.focus()
        tags = self.tree.item(item, 'tags')
        item_values = self.tree.item(item)['values']
        value_text = self.tree.item(item)['text']
        self.selected_node = item   #親ツリーの選択.
        children_count = str(len(self.tree.get_children(item)))
        if not children_count == "0":
            text = value_text +"\n" + children_count +"個の子タスクがあるよ"
        else:
            text = value_text
        self.canvas.conversation_text(text)


        if not self.edit_flag:
            self.tag_entry.delete(0, tk.END)
            parent_id = self.tree.item(item)['values'][0]
            self.tag_entry.insert(tk.END, parent_id)
            return

        self.default_entry_box()
        
        self.edit_id_value = item_values[0]
        limit_value = item_values[1]
        value_value = item_values[2]
        state_value = item_values[3]
        self.state_set = ["","検討中","進行中","テスト中","完了"]
        if state_value in self.state_set:
            index = self.state_set.index(state_value)
        else:
            index = 0
        if value_value in self.value_star:
            value_index = self.value_star.index(value_value)
        else:
            value_index = 0
        person_value = item_values[4]
        progress_value = item_values[5]
        tag_value = item_values[6]

        self.E_task_edit.insert(tk.END, value_text)
        self.E_limit_edit.insert(tk.END, limit_value)
        self.CB_value_select.set(self.value_star[value_index])
        self.CB_state_select.set(self.state_set[index])
        self.person_entry.insert(tk.END, person_value)
        self.progress_entry.insert(tk.END, progress_value)
        self.tag_entry.insert(tk.END, tag_value)
    
    # 並び替えの関数
    def sort_tree(self,column,parent):
        items = [(State_to_value.state_sort(self.tree.set(child, column)), child) for child in self.tree.get_children(parent)]
        items.sort(key=lambda x: x[0])
        for index, (_, child) in enumerate(items):
            self.tree.move(child, parent, index)
        if self.canvas:
            self.canvas.conversation_text("stateで並び替えたよ")
    
    def sort_tree_value(self,parent):
        items = [(State_to_value.value_sort(self.tree.set(child, "value")), child) for child in self.tree.get_children(parent)]
        items.sort(key=lambda x: x[0])
        for index, (_, child) in enumerate(items):
            self.tree.move(child, parent, index)
        self.canvas.conversation_text("valueで並び替えたよ")

    def update_button_text(self):
        self.default_entry_box()
        self.button_text = self.CB_mode_select.get()
        self.B_action["text"] = self.button_text
        if self.button_text == "追加":
            self.edit_flag = False
        else:
            self.edit_flag = True
        self.canvas.conversation_text(self.button_text + "のボタンに切り替えたよ")
    
    def default_entry_box(self):
        self.E_task_edit.delete(0, tk.END)
        self.E_limit_edit.delete(0, tk.END)
        self.CB_value_select.set(self.value_star[0])
        self.CB_state_select.set(self.state_set[0])
        self.person_entry.delete(0, tk.END)
        self.progress_entry.delete(0, tk.END)
        self.tag_entry.delete(0, tk.END)

    def reload_info(self):
        self.tree.destroy()
        self.task_list = []
        self.task_list = self.csvM.load_data_from_csv(self.file_path)
        self.task_infomation()

    def throw_state_color(self,state):
        item = self.state_set
        if state == item[2]:
            return "green"
        elif state == item[1]:
            return "yellow"
        elif state == item[3]:
            return "red"
        else:
            return "white"
        
    def progress_circles(self):
        parent = self.selected_node
        items = [(self.tree.set(child,"state"), child) for child in self.tree.get_children(parent)]
        if not items:
            self.canvas.conversation_text("このタスクでは進捗状況の丸を作れないよ")
            return
        progression = State_to_value.progress_count(items)
        self.progress_entry.delete(0, tk.END)
        self.progress_entry.insert(tk.END,progression)
        self.canvas.conversation_text("まる、まる、まる！")


# この関数がないと、treeviewの色が反映されない可能性があります.
def fixed_map(option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
        elm[:2] != ('!disabled', '!selected')]

root = tk.Tk()

#Style修正用.
style = ttk.Style()  
style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
style.map("Treeview", background=[("selected", "gray")])
root.title = "test"
gui = GUI(root)
gui.create_window()

# canvas = tk.Canvas(root, width=400, height=100)
# canvas.pack()

root.geometry("1200x600")

root.mainloop()