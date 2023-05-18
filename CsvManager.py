import os
import csv

class Data_factor:
    def __init__(self,id,task,limit,value,state,person,progress,tag):
        self.id = id
        self.task = task
        self.limit = limit                if limit else "null"
        self.value = value                if value else "null"
        self.state = state    if state else "null"
        self.person = person                if person else "null"
        self.progress = progress                if progress else "null"
        self.tag = tag                if tag else "main"

class CsvManager:

    def __init__(self) -> None:
        
        self.folder_name = "csv_list"
        self.main_file = 'main.csv'

    def check_csv_file(self):
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)
            print("Make folder")
        file_path = self.folder_name + "/" + self.main_file
        if not os.path.isfile(file_path):
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # ヘッダー行を書き込み
                writer.writerow(['id','task','limit','value','state','person','progress','tag'])
                print("make main file")
        return file_path

    def load_data_from_csv(self,file_path):
        task_list = []
        with open(file_path, 'r',encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) # skip header row
            for row in reader:
                id = row[0]
                task = row[1]
                limit = row[2]
                value = row[3]
                state = row[4]
                person = row[5]
                progress = row[6]
                tag = row[7]
                data = Data_factor(id,task,limit,value,state,person,progress,tag)
                task_list.append(data)
        return task_list

    def add_data(self,file_path,task,limit,value,state,person,progress,tag):
        #新しいidを取得
        with open(file_path, 'r',encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            if len(reader) == 0:
                id = 1
            else:
                max_id = max([int(row['id']) for row in reader])
                id = max_id + 1

        with open(file_path, 'a', newline='\n',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # ヘッダー行を書き込む
            if csvfile.tell() == 0:
                writer.writerow(['id', 'task', 'limit', 'value', 'state', 'person', 'progress', 'tag'])
                csvfile.write('\n')
            # タスクの情報を新しい行に書き込む
            writer.writerow([str(id),task,limit,value,state,person,progress,tag])

    def Update_data(self, file_path,id,task,limit,value,state,person,progress,tag):
        # csvファイルを読み込む
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = list(reader)
        for i, row in enumerate(data):
            if row[0] == str(id):
                # 上書きする行のインデックスと上書きするデータ
                overwrite_data = [id,task,limit,value,state,person,progress,tag]

                # csvファイルを読み込む
                with open(file_path, "r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    data = list(reader)

                # 指定された行を上書きする 
                data[i] = overwrite_data
                # csvファイルに上書き保存する
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(data)
                break

    def delete_data(self, id, file_path):
        with open(file_path, 'r',encoding='utf-8') as f:
            f.seek(0)
            reader = csv.reader(f)
            rows = list(reader)

        for i, row in enumerate(rows):
            if row[0] == str(id):
                rows.pop(i)
                break

        with open(file_path, 'w', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

print("import csvManager!")



