
import tkinter as tk
from PIL import Image, ImageTk
import random

class guide_animation:
    def __init__(self,master) -> None:
        self.master = master
        self.guide_flag = False
        self.guide_text = "Hello!! Hello!!"
        self.draw_flag = False
        self.text_count = 0
        self.textX = 150
        self.textY = 100
        self.current_image_index = 0 #瞬き用変数.
        self.blink_interval_base = 5000
        self.animation_flag = False
        self.reaction_list = ["どうしたの？","ん？何？","疲れたの？","ちょっと休憩する？","眠くなってきちゃった","ん？おはよー"]
        self.reaction_list_head = ["ん？急にどうしたの？","頭撫でるの楽しい？","子ども扱いしないで？","撫でられるの悪くないけど...","気が晴れた？","満足した？"]
        # 画像リサイズ用変数.
        new_width = 400 
        new_height = 300
        try:
            self.image_base = Image.open("img/ガイドちゃん_body.png").resize((new_width, new_height), Image.LANCZOS)
            self.image_mouth = [
                Image.open("img/ガイドちゃん_mouth_0.png").resize((new_width, new_height), Image.LANCZOS),
                Image.open("img/ガイドちゃん_mouth_1.png").resize((new_width, new_height), Image.LANCZOS),
                Image.open("img/ガイドちゃん_mouth_2.png").resize((new_width, new_height), Image.LANCZOS),
                Image.open("img/ガイドちゃん_mouth_3.png").resize((new_width, new_height), Image.LANCZOS)
            ]
            self.image_eye = [
                Image.open("img/ガイドちゃん_eye_0.png").resize((new_width, new_height), Image.LANCZOS),
                Image.open("img/ガイドちゃん_eye_1.png").resize((new_width, new_height), Image.LANCZOS),
                Image.open("img/ガイドちゃん_eye_2.png").resize((new_width, new_height), Image.LANCZOS),
                Image.open("img/ガイドちゃん_eye_3.png").resize((new_width, new_height), Image.LANCZOS)
            ]
            image_eye1 = self.image_eye[1]
            image_eye2 = self.image_eye[2]
            self.image_eye.append(image_eye2)  # 2番目の要素を追加
            self.image_eye.append(image_eye1)  # 3番目の要素を追加
            self.guide_flag = True
        except IOError as error:
            print(error)
            print("ガイド機能がOFFになりました。")

    def create_canvas(self,master):
        if not self.guide_flag:
            return

        self.canvas = tk.Canvas(master, width=1200, height=200,background="white")
        self.canvas.pack(expand=True,fill=tk.BOTH)
        self.imgX = int(self.canvas.cget("width")) - 300
        self.imgY = 0


        self.create_guide()

        boxX = 100
        boxY = 50
        box_width = 800
        box_height = 100
        text = "ごきげんよう"+ "\n" +"作業を確認しよう"
        self.conversation_box(self.canvas, boxX,boxY,box_width,box_height)
        self.conversation_text(text)

        self.canvas.bind("<Button-1>", lambda event: self.on_canvas_click(event,text))

    def create_guide(self):

        ##範囲確認用の四角.
        # areaX = self.imgX + 130 #+130
        # areaY = self.imgY + 100 #+75
        # check_square = self.canvas.create_rectangle(areaX, areaY, areaX +130, areaY +100, fill="white")
        # check_square1 = self.canvas.create_rectangle(areaX, areaY - 75, areaX +130, areaY, fill="white")

        self.photo = ImageTk.PhotoImage(self.image_base)
        self.mouse_close = ImageTk.PhotoImage(self.image_mouth[3])
        
        self.img_guide = self.canvas.create_image(self.imgX, self.imgY, image=self.photo, anchor=tk.NW, tags="image")  # 新しい座標で画像を作成

        self.img_mouth_close = self.canvas.create_image(self.imgX, self.imgY, image=self.mouse_close, anchor=tk.NW, tags="mouse_close")
        
        self.current_image = ImageTk.PhotoImage(self.image_eye[0])
        self.canvas.create_image(self.imgX, self.imgY, image=self.current_image,anchor=tk.NW, tags="eye")

        self.guide_blick()

    def guide_kuchipaku(self):
        if self.animation_flag:
            return
        self.animation_flag = True
        self.mouse = ImageTk.PhotoImage(self.image_mouth[1])

        self.canvas.delete("mouth_close")
        self.img_mouth_action = self.canvas.create_image(self.imgX, self.imgY, image=self.mouse, anchor=tk.NW, tags="mouse")
        self.canvas.after(1000, self.guide_kuchipaku_end)

    def guide_kuchipaku_end(self):
        self.canvas.delete("mouse")
        self.img_mouth_close = self.canvas.create_image(self.imgX, self.imgY, image=self.mouse_close, anchor=tk.NW, tags="mouse_close")
        self.animation_flag = False

    def guide_blick(self):
        self.canvas.delete("eye")  # キャンバスをクリア

        # 現在の画像を表示
        self.current_image = ImageTk.PhotoImage(self.image_eye[self.current_image_index])
        self.canvas.create_image(self.imgX, self.imgY, image=self.current_image,anchor=tk.NW, tags="eye")

        # 次の瞬きまでの間隔（ミリ秒）
        if self.current_image_index == 0:
            # 1000から2000までの整数を生成します
            random_integer = random.randint(0, 2000)
            blink_interval = self.blink_interval_base + random_integer
        else:
            blink_interval = 50
        # 画像の切り替え
        self.current_image_index = (self.current_image_index + 1) % len(self.image_eye)

        self.canvas.after(blink_interval, self.guide_blick)
        

    def conversation_text(self, text):
        self.canvas.delete("text")
        text = self.canvas.create_text(self.textX, self.textY, text=text, font=("Arial", 20), fill="black",anchor="w",tags ="text")
        self.guide_kuchipaku()

    def conversation_box(self, canvas, boxX,boxY,box_width,box_height):
        offset = 10
        x1 = boxX
        x2 = boxX + box_width
        x5 = boxX - offset
        x6 = boxX + box_width + offset

        circleX_left = boxX
        circleX_right = boxX + box_width 

        y1 = boxY
        y2 = boxY + box_height
        y5 = boxY + offset
        y6 = boxY + box_height - offset

        circleY_top = boxY + offset
        circleY_bottom = boxY + box_height - offset

        radius = 10
        circle_color = "brown"

        canvas.create_rectangle(x1, y1, x2, y2, fill="gray")

        canvas.create_rectangle(x5, y5, x6, y6, fill="gray")

        # 黒色の四角形を描画
        x1, y1 = x1 , y1 + offset
        x2, y2 = x2 , y2 - offset
        canvas.create_rectangle(x1, y1, x2, y2, fill="white")

        # 白い丸を描画（四隅）
        radius = 10
        canvas.create_oval(circleX_left-radius, circleY_top-radius, circleX_left+radius, circleY_top+radius, fill=circle_color)  # 左上の丸
        canvas.create_oval(circleX_right-radius, circleY_top-radius, circleX_right+radius, circleY_top+radius, fill=circle_color)  # 右上の丸
        canvas.create_oval(circleX_left-radius, circleY_bottom-radius, circleX_left+radius, circleY_bottom+radius, fill=circle_color)  # 左下の丸
        canvas.create_oval(circleX_right-radius, circleY_bottom-radius, circleX_right+radius, circleY_bottom+radius, fill=circle_color)  # 右下の丸


    def on_canvas_click(self, event, text):
        # print("クリックした座標:", event.x, event.y)
        minX = self.imgX + 130
        maxX = self.imgX + 260
        minY = self.imgY + 100
        maxY = self.imgY + 300

        if event.x >= minX and event.x <= maxX:
            if event.y >= minY and event.y <= maxY:
                text = self.reaction_list[self.text_count]
                self.text_count = (self.text_count + 1) % len(self.reaction_list)

            elif event.y >= minY-75 and event.y <= maxY-100:
                text = self.reaction_list_head[self.text_count]
                self.text_count = (self.text_count + 1) % len(self.reaction_list_head)
            
            else:
                return
        else:
            return
        
        self.conversation_text(text)


if __name__ == "__main__": # ファイルを直接実行時に起動します.
    root = tk.Tk()
    canvas = guide_animation(root)
    canvas.create_canvas(root)
    
    root.mainloop()