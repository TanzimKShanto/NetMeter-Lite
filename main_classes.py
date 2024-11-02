import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from taskbar import get_taskbar_height
from taskbar import *
import json
from res_path import resource_path

class make_window_draggable:
    def __init__(self, window, last, cc, lock, fonts, label, imlabel):
        self.window = window
        self.last = last
        self.cc = cc
        self.lock = tk.BooleanVar(value=lock)
        self.toogle_lock()
        self.fonts = fonts
        self.label = label
        self.imlabel = imlabel
    def toogle_lock(self):
        if self.lock.get():
            self.unbind()
        else:
            self.bind()
    def bind(self):
        self.window.bind("<Button-1>", self.on_press)
        self.window.bind("<B1-Motion>", self.on_drag)
    def unbind(self):
        self.window.unbind("<Button-1>")
        self.window.unbind("<B1-Motion>")
    def on_press(self, event):
        self.window.x = event.x
        self.window.y = event.y
    def on_drag(self, event):
        x = self.window.winfo_pointerx() - self.window.x
        y = self.window.winfo_pointery() - self.window.y
        if self.imlabel.transparent.get():
            self.fonts.bg=get_taskbar_color(x-2)
            self.label.handle_bg()
        self.window.geometry(f"+{x}+{y}")
        self.cc.geometry(f"+{x}+{y}")
        self.last.geometry(f"+{x}+{y}")
        with open(resource_path('config.json'), 'r+') as f:
            data = json.load(f)
            data['config']['x']=x
            data['config']['y']=y
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

class Image_Label:
    def __init__(self, root, master, skin_no, skin, sz, transparent, fonts):
        self.root = root
        self.master = master
        self.label = None
        self.sz = sz
        self.fonts = fonts
        self.skin_no = tk.IntVar(value=skin_no)
        self.skin = skin
        self.hbg = tk.StringVar(value=skin[skin_no]['color'])
        self.load_img()
        self.transparent = tk.BooleanVar(value=transparent)
        self.widget = None
    def register(self, widget, label):
        self.widget = widget
        self.label_manager = label
        self.widget.resize()
    def toogle_transparent(self, x_pos=None):
        if self.widget is not None:
            self.widget.resize()
        if self.transparent.get():
            self.remove_img()
            self.fonts.bg = get_taskbar_color(x_pos if x_pos else self.master.winfo_x() - 2)
            self.label_manager.handle_bg()
        else:
            self.fonts.color.set(self.skin[self.skin_no.get()]['color'])
            self.label_manager.handle_color()
            self.fonts.bg = self.skin[self.skin_no.get()]['bg']
            self.label_manager.handle_bg()
            self.add_img()
    def create_label(self):
        self.label = tk.Label(self.root, image=self.photo_img, bg='white', highlightthickness=1, highlightbackground=self.hbg.get())
        self.label.pack(fill='both', expand=True)
    def load_img(self):
        self.hbg.set(self.skin[self.skin_no.get()]['color'])
        self.source_img = Image.open(resource_path(self.skin[self.skin_no.get()]['path']))
        self.og_img = self.source_img.resize(self.sz, Image.Resampling.LANCZOS)
        self.photo_img = ImageTk.PhotoImage(self.og_img)
    def add_skin(self):
        self.load_img()
        if self.transparent.get():
            self.transparent.set(False)
        self.toogle_transparent()
    def resize_img(self, sz):
        width , height = sz
        width*=(60/height)
        self.cropped_image = self.source_img.crop((max(0,480-width), 0, 480, 60))
        #print(self.cropped_image.size, 'x')
        self.sz = sz
        self.og_img = self.cropped_image.resize(self.sz, Image.Resampling.LANCZOS)
        #print(self.og_img.size, 'y')
        self.photo_img = ImageTk.PhotoImage(self.og_img)
    def add_img(self):
        if self.label is None:
            self.create_label()
        else:
            self.label.config(image=self.photo_img)
            self.label.image = self.photo_img
            self.label.config(highlightbackground=self.hbg.get())
    def remove_img(self):
        if self.label is not None:
            self.label.config(image='')
            self.label.config(highlightbackground='white')

class font_hub:
    def __init__(self, family, size, style, color, bg):
        self.family = tk.StringVar(value=family)
        self.size = tk.IntVar(value=size)
        self.style = tk.StringVar(value=style)
        self.color = tk.StringVar(value=color)
        self.bg = bg
        

class label_gen:
    def __init__(self, master, fonts, txt):
        self.master = master
        self.fonts = fonts
        self.text = tk.StringVar(value=txt)
        self.mtext = tk.StringVar(value=txt)
        self.source = tk.StringVar(value=txt)
        self.txt1 , self.txt2 = map(lambda e: tk.StringVar(value=e), txt.split('\n'))
        self.frame = tk.Frame(master, height=30)
        self.frame.pack_propagate(0)
        self.frame.pack(side='left')
        self.label = tk.Label(self.frame, textvariable=self.text, background=self.fonts.bg, justify='right', anchor='w', foreground=fonts.color.get())
        self.label.pack(side='right', fill='both', expand=True)
        self.restruct()
    def restruct(self, flag = False):
        tx1 , tx2 = self.mtext.get().split('\n')
        my_font = self.my_font()
        width = max(my_font.measure(tx1), my_font.measure(tx2)) + 4
        height = my_font.metrics('linespace')*2+3
        self.frame.config(width=width+30*flag, height=height)
        self.label.config(font=(self.fonts.family.get(), self.fonts.size.get(), self.fonts.style.get()), foreground=self.fonts.color.get())
        return width
    def my_font(self):
        weight = 'normal'
        slant = 'roman'
        style = self.fonts.style.get()
        if 'bold' in style:
            weight = 'bold'
        if 'italic' in style:
            slant = 'italic'
        return font.Font(family=self.fonts.family.get(), size=self.fonts.size.get(), weight=weight, slant=slant)
    def update_color(self):
        self.label.config(foreground=self.fonts.color.get())
    def update_bg(self):
        self.label.config(background=self.fonts.bg)
        self.master.attributes('-transparentcolor', self.fonts.bg)
    def toogle_other_on(self, flag):
        if flag:
            self.mtext.set(self.source.get())
            self.text.set(self.mtext.get())
        else:
            self.mtext.set('\n')
            self.text.set('\n')
    def manage_text(self):
        self.mtext.set(self.source.get())
        self.text.set(self.source.get())
    def set_source(self):
        self.source.set(self.txt1.get()+'\n'+self.txt2.get())


class label_manager:
    def __init__(self, lab1, lab2, lab3, lab4, other_on, interval, unit, widget):
        self.lab1 = lab1
        self.lab2 = lab2
        self.lab3 = lab3
        self.lab4 = lab4
        self.other_on = tk.BooleanVar(value=other_on)
        self.interval = tk.IntVar(value=interval)
        self.unit = tk.IntVar(value=unit)
        self.widget = widget
        self.manage_other()
    def handle_style(self, event = None):
        my_font = self.lab1.my_font()
        self.widget.height.set(my_font.metrics('linespace')*2+3)
        self.widget.width.set(self.lab1.restruct()+self.lab2.restruct()+self.lab3.restruct()+self.lab4.restruct(True))
        self.widget.resize()
    def handle_color(self):
        self.lab1.update_color()
        self.lab2.update_color()
        self.lab3.update_color()
        self.lab4.update_color()
    def handle_bg(self):
        self.lab1.update_bg()
        self.lab2.update_bg()
        self.lab3.update_bg()
        self.lab4.update_bg()
    def manage_other(self):
        self.lab3.toogle_other_on(self.other_on.get())
        self.lab4.toogle_other_on(self.other_on.get())
        self.handle_style()
    def manage_text(self, event):
        self.lab1.set_source()
        self.lab3.set_source()
        self.lab1.manage_text()
        if self.other_on.get():
            self.lab3.manage_text()
        self.handle_style()


    
class toplevel_windows:
    def __init__(self, master, pos):
        self.root = tk.Toplevel(master)
        self.pos = pos
        self.root.overrideredirect(True)
        self.root.config(bg='')
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparent', 'white')
        self.root.geometry(self.pos)



class widget_handle:
    def __init__(self, root, cc, last, height, pos, imlabel, screenh, screenw, always_on_top):
        self.root = root
        self.cc = cc
        self.last = last
        self.pos = pos
        self.imlabel = imlabel
        self.taskbar_height = get_taskbar_height()
        self.height = tk.IntVar(value=height)
        self.width = tk.IntVar()
        self.screenh = screenh
        self.screenw = screenw
        self.flag = 1
        self.always_on_top = tk.BooleanVar(value=always_on_top)
        self.last.bind('<Escape>', lambda e: self.root.destroy())
    def resize(self):
        extra = not self.imlabel.transparent.get()
        sz = f"{self.width.get()+30*extra}x{self.height.get()}"
        #print(sz)
        self.root.geometry(sz)
        self.cc.geometry(sz)
        self.last.geometry(sz)
        self.imlabel.resize_img((self.width.get()+30*extra, self.height.get()))
        if not self.imlabel.transparent.get():
            self.imlabel.add_img()
    def reset_size(self):
        self.height.set(self.taskbar_height)
        self.resize()
    def reset_pos(self):
        self.pos = f"+{int(self.screenw*0.65)}+{self.screenh-self.height.get()}"

        with open(resource_path('config.json'), 'r+') as f:
            data = json.load(f)
            data['config']['x'] = int(self.screenw*0.65)
            data['config']['y'] = self.screenh-self.height.get()
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        self.root.geometry(self.pos)
        self.cc.geometry(self.pos)
        self.last.geometry(self.pos)
    def keep_on_top(self):
        self.cc.attributes('-topmost', True)
        self.root.attributes('-topmost', True)
        self.last.attributes('-topmost', True)
    def check_top(self, flag=None):
        if flag==False:
            self.cc.attributes('-topmost', flag)
            self.root.attributes('-topmost', flag)
            self.last.attributes('-topmost', flag)
        else:
            self.cc.attributes('-topmost', self.always_on_top.get())
            self.root.attributes('-topmost', self.always_on_top.get())
            self.last.attributes('-topmost', self.always_on_top.get())
    def menu_bind(self, menu):
        self.root.bind('<Button-3>', menu)
        self.cc.bind('<Button-3>', menu)
        self.last.bind('<Button-3>', menu)
    def toogle_whole_transparent(self, flag):
        if self.flag!=flag:
            self.flag^=1
            self.check_top(flag)
            self.cc.wm_attributes('-alpha', self.flag)
            self.root.wm_attributes('-alpha', self.flag)