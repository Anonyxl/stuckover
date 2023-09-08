import customtkinter as custk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import shutil
import threading
import gc

mainWindow = custk.CTk()
custk.set_appearance_mode("dark")
custk.set_default_color_theme("dark-blue")

mainWindow.geometry('1200x800')
mainWindow.title('PhotoSorter 1.0')

mainFrame = custk.CTkScrollableFrame(mainWindow, width=930, height=770)
mainFrame.place(x=1190, y=10, anchor='ne')


def sourceFolderButton_event():
    global sourceFolderPathsList
    global sourceFolderPath
    try:
        sourceFolderPath = filedialog.askdirectory()

        valid_extensions = [".png", ".jpg"]
        files = os.listdir(sourceFolderPath)
        sourceFolderPathsList = [file for file in files if os.path.splitext(file)[1].lower() in valid_extensions]
    except: passe
    

sourceFolderButton_Image = ImageTk.PhotoImage(image=Image.open('mainFiles\\icons\\folder_icon.png').resize((40,40)))
sourceFolderButton = custk.CTkButton(mainWindow, width=225, image=sourceFolderButton_Image, fg_color='#101010', hover_color='#121212', border_width=0, text='hlavní složka', font=('Arial', 15), command=sourceFolderButton_event)
sourceFolderButton.place(x=7, y=745)

checkY = 0
forImgNameCounter = 0
actualIndexOfPath = -1
bindProfile_list = []
img_obj = 0


def rightWayImage(event):
    global img_obj
    if img_obj != 0:
        img_obj.imageLabel.destroy()
        # img_obj.image.close()
        del img_obj
    
    gc.collect()


    global actualIndexOfPath
    if actualIndexOfPath < len(sourceFolderPathsList)-1:
        actualIndexOfPath += 1


    img_obj = soImage(f'{sourceFolderPath}/{sourceFolderPathsList[actualIndexOfPath]}')



def leftWayImage(event):
    global img_obj
    if img_obj != 0:
        img_obj.imageLabel.destroy()
        # img_obj.image.close()
        del img_obj.cu_image
        del img_obj
    
    gc.collect()


    global actualIndexOfPath
    if actualIndexOfPath < len(sourceFolderPathsList)-1:
        actualIndexOfPath -= 1


    img_obj = soImage(f'{sourceFolderPath}/{sourceFolderPathsList[actualIndexOfPath]}')


mainWindow.bind('<Right>', rightWayImage)
mainWindow.bind('<Left>', leftWayImage)

class soImage():
    def __init__(self, image_path):
        self.image_path = image_path
        self.checkRotate = 0
        self.angle = 0
        
        self.imageLabel = custk.CTkLabel(mainFrame, text='')
        self.imageLabel.pack()
        
        self.load_image()

        mainWindow.bind(",", self.rotate_left)  # Bind klávesy pro rotaci doleva
        mainWindow.bind(".", self.rotate_right)  # Bind klávesy pro rotaci doprava
 
    def load_image(self):
        self.image = Image.open(fp=self.image_path)
        self.getSizeHeight()
        self.cu_image = custk.CTkImage(dark_image=self.image, size=(self.width, self.height))
        self.imageLabel.configure(image=self.cu_image)

        

    
    def getSizeHeight(self):
        width, height = self.image.size
        if width > height:
            if self.checkRotate == 1:
                tmp = width
                width = height
                height = tmp

                width = width*(770/height)
                height = height*(770/height)
            else:
                height = height*(920/width)
                width = width*(920/width)  

        elif height > width:
            width = width*(770/height)
            height = height*(770/height)
        self.width = width
        self.height = height
        self.checkRotate = 0    

    def rotate_left(self, event):
        self.angle = 90
        self.rotateImg()

    def rotate_right(self, event):
        self.angle = -90
        self.rotateImg()

    def rotateImg(self):
        self.checkRotate = 1
        self.getSizeHeight()
        self.image = self.image.rotate(self.angle, expand=True)
        self.cu_image.configure(dark_image=self.image, size=(self.width, self.height))


class plusFunc():
    def __init__(self, keyBind):
        self.button = custk.CTkButton(mainWindow, width=220, height=27, corner_radius=4, text=keyBind, fg_color='transparent', bg_color='transparent', text_color='#580FF0', border_width=2, border_color='#580FF0', hover=False)
        if checkY == 1:
            self.button.place(x=7, y=50)
        else:
            self.button.place(x=7, y=20+30*checkY)
        self.keyBind = keyBind
        self.location = ''

        mainWindow.bind(self.keyBind, self.keyBind_event)
    
    def keyBind_event(self, event):
        global forImgNameCounter
        def keyBind_eventTHREADdef():
            if self.location == '':
                self.location = filedialog.askdirectory()
            else:
                shutil.copyfile(f'{sourceFolderPath}/{sourceFolderPathsList[actualIndexOfPath]}', f'{self.location}/{sourceFolderPathsList[actualIndexOfPath][:-3]}_{forImgNameCounter}.{sourceFolderPathsList[actualIndexOfPath][-3:]}')
                sourceFolderPathsList.remove(sourceFolderPathsList[actualIndexOfPath])   
        forImgNameCounter += 1
        t1 = threading.Thread(target=keyBind_eventTHREADdef)
        t1.start()
        

def make_bindProfile(key=None):
    if bindProfile_list[0] :
        bindProfile_list.append(key)

 
def plusFuncButton_event():
    toplevelMessage = custk.CTkToplevel(mainWindow)
    toplevelMessage.geometry('350x100')
    toplevelMessage.title('WindowForBind')
    toplevelMessage.attributes('-topmost', 1)
    toplevelMessage.focus_force()

    label = custk.CTkLabel(toplevelMessage, text='Stiskněte libovolnou klávesu pro přiřazení k "bindu"')
    label.pack(anchor='center')

    def key_press(event):
        key = event.keysym
        toplevelMessage.destroy()
        global checkY
        checkY += 1
        plusFunc(key)

    toplevelMessage.bind('<Key>', key_press)


plusFuncButton = custk.CTkButton(mainWindow, width=223, height=30, corner_radius=13, border_width=0, text='přidat bind', text_color='black', font=('Arial', 20), fg_color='#6e2ff2', hover_color='#5F18F1', command= plusFuncButton_event)
plusFuncButton.place(x=7, y=10)


def auto_make(keyBind):
    pass



mainWindow.mainloop()




