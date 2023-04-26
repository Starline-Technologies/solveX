from PIL import Image
from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser,filedialog
import PIL.ImageGrab as ImageGrab
import cv2
import numpy as np
import pytesseract
from tkinter import ttk
from tkinter import messagebox
pytesseract.pytesseract.tesseract_cmd= r'c:/Program Files/Tesseract-OCR/tesseract.exe'


class Draw():
    def __init__(self,root):


        self.root =root
        self.root.title("AI Calculator")
#self.root.geometry("810x530")
        self.root.configure(background="white")
#self.root.resizable(0,0)
 
  
        self.pointer= "black"
        self.erase="white"


        text=Text(root)
        text.tag_configure("tag_name", justify='center', font=('arial',25),background='#292826',foreground='orange')

        text.insert("1.0", "SOLVE X")


        text.tag_add("tag_name", "1.0", "end")
        text.pack()
        

        self.pick_color = LabelFrame(self.root,text='Colors',font =('arial',15),bd=5,relief=RIDGE,bg="white")
        self.pick_color.place(x=0,y=40,width=90,height=185)

        colors = ['blue','red','green', 'orange','violet','black','yellow','purple','pink','gold','brown','indigo']
        i=j=0
        for color in colors:
            Button(self.pick_color,bg=color,bd=2,relief=RIDGE,width=3,command=lambda col=color:self.select_color(col)).grid(row=i,column=j)
            i+=1
            if i==6:
                i=0
                j=1


        self.eraser_btn= Button(self.root,text="Eraser",bd=4,bg='white',command=self.eraser,width=9,relief=RIDGE)
        self.eraser_btn.place(x=0,y=197)

        self.clear_screen= Button(self.root,text="Clear Screen",bd=4,bg='white',command= lambda : self.background.delete('all'),width=9,relief=RIDGE)
        self.clear_screen.place(x=0,y=227)

        self.save_btn= Button(self.root,text="Calculate",bd=4,bg='white',command=self.save_drawing,width=9,relief=RIDGE)
        self.save_btn.place(x=0,y=257)


        self.bg_btn= Button(self.root,text="Background",bd=4,bg='white',command=self.canvas_color,width=9,relief=RIDGE)
        self.bg_btn.place(x=0,y=287)



        self.pointer_frame= LabelFrame(self.root,text='size',bd=5,bg='white',font=('arial',15,'bold'),relief=RIDGE)
        self.pointer_frame.place(x=0,y=320,height=200,width=70)

        self.pointer_size =Scale(self.pointer_frame,orient=VERTICAL,from_ =48 , to =0, length=168)
        self.pointer_size.set(1)
        self.pointer_size.grid(row=0,column=1,padx=15)



        self.background = Canvas(self.root,bg='white',bd=5,relief=GROOVE,height=470,width=680)
        self.background.place(x=80,y=40)



        self.background.bind("<B1-Motion>",self.paint) 


    def paint(self,event):       
        x1,y1 = (event.x-2), (event.y-2)  
        x2,y2 = (event.x+2), (event.y+2)  

        self.background.create_oval(x1,y1,x2,y2,fill=self.pointer,outline=self.pointer,width=self.pointer_size.get())

  
    def select_color(self,col):
        self.pointer = col


    def eraser(self):
        self.pointer= self.erase

  
    def canvas_color(self):
        color=colorchooser.askcolor()
        self.background.configure(background=color[1])
        self.erase= color[1]


    def save_drawing(self):
        
        file_ss = 'math.jpg'
        x = self.root.winfo_rootx() + self.background.winfo_x()
        y = self.root.winfo_rooty() + self.background.winfo_y()
        x1 = x + self.background.winfo_width()
        y1 = y + self.background.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_ss)
            

            
            
        img = cv2.imread('math.jpg', cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        items = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = items[0] if len(items) == 2 else items[1]

        base = np.zeros(thresh.shape, dtype=np.uint8)
        base = cv2.bitwise_not(base)

        max_area = 0
        for i in range(len(contours)):
                x, y, w, h = cv2.boundingRect(contours[i])
                ratio = h / w
                area = cv2.contourArea(contours[i])
                cv2.drawContours(img, [contours[i]], 0, (255, 0, 0), 2)

                if 1 < ratio < 3:
                        max_area = max(area, max_area)
                        #print("area: " + str(area) + ", max area: " + str(max_area) + ", ratio: " + str(ratio))
                        # if 1000 < area < max_area / 2:
                        if 1000 < area < 40000:
                                mask = np.zeros(thresh.shape, dtype=np.uint8)
                                cv2.drawContours(mask, [contours[i]], -1, color=255, thickness=-1)
                                mean = cv2.mean(thresh, mask=mask)

                                segment = np.zeros((h, w), dtype=np.uint8)
                                segment[:h, :w] = thresh[y:y + h, x:x + w]

                                if mean[0] > 150:
                                        # white, invert
                                        segment = cv2.bitwise_not(segment)

                                base[y:y + h, x:x + w] = segment[:h, :w]
                                #cv2.imshow("base", base)

                                cv2.drawContours(img, [contours[i]], 0, (255, 0, 0), 2)

                                

        custom_config = r'-l eng --oem 3 --psm 6 -c tessedit_char_whitelist="0123456789()*/.><-" '
        text = pytesseract.image_to_string(base, config=custom_config)

           
        re= eval(text)
        print(text)
        print(eval(text))

        messagebox.showinfo("result", re)


if __name__ =="__main__":
    root = Tk()
    p= Draw(root)
    root.mainloop()
