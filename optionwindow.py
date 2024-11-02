import tkinter as tk
from tkinter import ttk, colorchooser, font
from PIL import Image, ImageTk
import json
from res_path import resource_path

def wake_options():
    if options.winfo_viewable():  # If it's not minimized
        options.iconify()  # Hide the window
    else:
        options.deiconify()

class handle_lframe:
    def __init__(self, master, text, row, col, colsp, padx, pady, sticky):
        self.lframe=tk.LabelFrame(master, text=text, font=('Verdana', 10, 'bold'), background = 'white')
        self.lframe.grid(row=row, column=col, columnspan=colsp, padx=padx, pady=pady, sticky=sticky)

class handle_radio:
    def __init__(self, master, text, tvar, value, row, col, padx, pady, sticky, command=None):
        self.radiob = ttk.Radiobutton(master, text=text, variable=tvar, value=value, takefocus=False, command=command)
        self.radiob.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)

def load_config(json_file):
    with open(resource_path(json_file), "r") as f:
        data = json.load(f)
    return data['skins']

def open_options(widget, drag, fonts, label, menu_open, imlabel):

    def handle_color():
        selected_color = colorchooser.askcolor()[1]
        if selected_color:
            fonts.color.set(selected_color)
            label.handle_color()
            cur_color_label.config(background=fonts.color.get())

    global options
    options = tk.Toplevel(widget.root)
    options.title('Option Setting')
    options.iconbitmap(resource_path('setting.ico'))
    options.wm_iconphoto(True, ImageTk.PhotoImage(Image.open(resource_path('setting.png'))))
    options_width = 600
    options_height = 575
    options.geometry(f'{options_width}x{options_height}+{(widget.screenw-options_width)//2}+{(widget.screenh-options_height)//2}')

    style = ttk.Style()
    style.configure('TFrame', background = 'white')
    style.configure('O.TLabel',font=('Verdana', 10), background = 'white')
    style.configure('TEntry', font=('Verdana', 10))
    style.configure('TButton', font=('Verdana', 10))
    style.configure('TRadiobutton', font=('Verdana', 10), background = 'white')
    style.configure('TCheckbutton', font=('Verdana', 10), background = 'white')
    style.configure('TCombobox', selectbackground='white', selectforeground='black', insertcolor = 'white')

    notebook = ttk.Notebook(options, padding=15, takefocus=False)
    notebook.pack(expand=True, fill='both')

    taskbar_setting_frame = ttk.Frame(notebook)
    notebook.add(taskbar_setting_frame, text='Taskbar Window Setting')

    font_frame = handle_lframe(taskbar_setting_frame, 'Color and Font', 0, 0, 2, 10, 10, 'we')

    size_label = ttk.Label(font_frame.lframe,text='Font Size:', style='O.TLabel')
    size_label.grid(row=0, column=0, padx=10, sticky='w')

    size_spinbox = tk.Spinbox(font_frame.lframe, from_=6, to= 12, font=("Verdana", 12), borderwidth=1, relief='solid', state='readonly', textvariable=fonts.size, width=5, command=label.handle_style)
    size_spinbox.grid(row=0, column=1, padx=2, pady= 10, sticky='w')

    size_reset = ttk.Button(font_frame.lframe, text='Reset Size', takefocus=False, command=lambda: fonts.size.set(8) or label.handle_style())
    size_reset.grid(row=0, column=2, columnspan=3, padx=10, pady= 10, sticky='w')

    color_label = ttk.Label(font_frame.lframe, text='Current Color:', style='O.TLabel')
    color_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    cur_color_label = tk.Label(font_frame.lframe, background=fonts.color.get(), width=2, borderwidth=1, relief="solid")
    cur_color_label.grid(row=1, column=1, padx=2, pady=10, sticky='w')


    change_color = ttk.Button(font_frame.lframe, text='Change Color', takefocus=False, command=handle_color)
    change_color.grid(row=1, column=2, columnspan=3, padx=10, pady=10, sticky='w')

    styel_label = ttk.Label(font_frame.lframe, text='Choose Style:', style='O.TLabel')
    styel_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    style_radio = ttk.Frame(font_frame.lframe)
    style_radio.grid(row=2, column=1, columnspan=4, sticky='w')

    normal_style = handle_radio(style_radio, 'Normal', fonts.style, 'normal', 2, 1, (0,5), 10, 'w', label.handle_style)
    bold_style = handle_radio(style_radio, 'Bold', fonts.style, 'bold', 2, 2, 5, 10, 'w', label.handle_style)
    italic_style = handle_radio(style_radio, 'Italic', fonts.style, 'italic', 2, 3, 5, 10, 'w', label.handle_style)
    bold_italic_style = handle_radio(style_radio, 'Bold Italic', fonts.style, 'bold italic', 2, 4, 5, 10, 'w', label.handle_style)

    choose_font = ttk.Label(font_frame.lframe, text='Choose Font:', style='O.TLabel')
    choose_font.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    font_combo = ttk.Combobox(font_frame.lframe, values=sorted(list(font.families())), textvariable=fonts.family, takefocus=False)
    font_combo.grid(row=3, column=1, columnspan=2,padx=10, pady=10, sticky='w')
    font_combo.bind("<<ComboboxSelected>>", label.handle_style)

    reset_font = ttk.Button(font_frame.lframe, text='Reset Font', takefocus=False, command=lambda: fonts.family.set('Verdana') or label.handle_style())
    reset_font.grid(row=3, column=3, padx=10, pady=10, sticky='w')

    widget_frame = handle_lframe(taskbar_setting_frame, 'Widget Settings', 1, 0, 1, 10, (0, 10), 'nsew')

    transparent_bg = ttk.Checkbutton(widget_frame.lframe, text='Transparent Background', variable=imlabel.transparent, takefocus=False, command=lambda: imlabel.toogle_transparent() or cur_color_label.config(background=fonts.color.get()))
    transparent_bg.grid(row=0, column=0, columnspan=2, padx=(10,0), pady=10, sticky='w')

    show_cm = ttk.Checkbutton(widget_frame.lframe, text='Show CPU and Memory Status', variable=label.other_on, takefocus=False, command=label.manage_other)
    show_cm.grid(row=1, column=0, columnspan=3, padx=10, pady=10,sticky='w')

    lock_position = ttk.Checkbutton(widget_frame.lframe, text='Lock Position', variable=drag.lock, takefocus=False, command=drag.toogle_lock)
    lock_position.grid(row=2, column=0, padx=(10,0), pady=10, sticky='w')

    reset_pos = ttk.Button(widget_frame.lframe, text='Reset Position', takefocus=False, command=widget.reset_pos)
    reset_pos.grid(row=2, column=1, columnspan=2, padx=10, pady= 10, sticky='w')

    refresh_label = ttk.Label(widget_frame.lframe, text='Refresh Rate', style='O.TLabel')
    refresh_label.grid(row=3, column=0, padx=(10, 0), pady=10, sticky='w')

    rr_holder = ttk.Frame(widget_frame.lframe)
    rr_holder.grid(row=3, column=1, columnspan=4, padx=0, pady=0, sticky='w')


    refresh_rates = [500, 1000, 1500, 2000]
    for i, rr in enumerate(refresh_rates):
        radio_button = handle_radio(rr_holder, str(rr/1000)+'s', label.interval, rr, 3, i, 5, 10, 'w')
    

    display_text = ttk.Frame(widget_frame.lframe)
    display_text.grid(row=4, column=0, columnspan=4, sticky='w')

    display_texts = ['Upload:', 'CPU:', 'Download:', 'Memory:']
    display_var = [label.lab1.txt1, label.lab3.txt1, label.lab1.txt2, label.lab3.txt2]
    for i, rr in enumerate(display_texts):
        lab = ttk.Label(display_text, text=rr, style='O.TLabel')
        lab.grid(row=i//2, column=(i%2)*3, padx=10, pady=5, sticky='w')
        entry = ttk.Entry(display_text, textvariable=display_var[i], width=8, takefocus=False)
        entry.grid(row=i//2, column=(i%2)*3+1, padx=5, pady=5, sticky='w')
        entry.bind("<KeyRelease>", label.manage_text)


    always_on_top = ttk.Checkbutton(widget_frame.lframe, text='Always Keep on Top', variable=widget.always_on_top, takefocus=False, command=widget.check_top)
    always_on_top.grid(row=5, column=0, columnspan=3, padx=(10,0), pady=10, sticky='w')

    unit_setting_frame = handle_lframe(taskbar_setting_frame, 'Unit Settings', 1, 1, 1, 10, (0, 10), 'nsew')

    unit_label = ttk.Label(unit_setting_frame.lframe, text='Netspeed unit:', style='O.TLabel')
    unit_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 5), sticky='w')

    nbyte = handle_radio(unit_setting_frame.lframe,'B (Byte)', label.unit, 1, 1, 0, 10, 0, 'w')
    nbyte = handle_radio(unit_setting_frame.lframe, 'b (bit)', label.unit, 8, 2, 0, 10, 5, 'w')

    taskbar_setting_frame.grid_columnconfigure(0, weight=1)
    taskbar_setting_frame.grid_columnconfigure(1, weight=1)

    taskbar_setting_frame.grid_rowconfigure(0, weight=0)
    taskbar_setting_frame.grid_rowconfigure(1, weight=1)

    Change_skin_frame = ttk.Frame(notebook)
    notebook.add(Change_skin_frame, text='Change Skin')
    
    choose_skin = tk.LabelFrame(Change_skin_frame, text='Choose Skin', font=(fonts.family.get(), 10, 'bold'), background='white')
    choose_skin.pack(expand=True, fill='both', padx=10, pady=10)

    skins = load_config('config.json')
    rbs = [None]*len(skins)
    for i in range(len(skins)):
        rbs[i] = tk.PhotoImage(file=resource_path(skins[i]['path']))
        x = ttk.Radiobutton(choose_skin, image=rbs[i], variable=imlabel.skin_no, value=i, takefocus=False, command=lambda: imlabel.add_skin() or cur_color_label.config(background=fonts.color.get()))
        x.pack(padx=10, pady=10)
        x.image = rbs[i]

    def option_destroy():
        with open(resource_path('config.json'), "r+") as f:
            data = json.load(f)
            config = data['config']

            config['size']=fonts.size.get()
            config['color']=fonts.color.get()
            config['style']=fonts.style.get()
            config['family']=fonts.family.get()
            config['other_on']=label.other_on.get()
            config['interval']=label.interval.get()
            config['unit']=label.unit.get()
            config['transparent']=imlabel.transparent.get()
            config['lock']=drag.lock.get()
            config['skin']=imlabel.skin_no.get()
            config['always_on_top']=widget.always_on_top.get()
            config['txt1']=label.lab1.txt1.get()+'\n'+label.lab1.txt2.get()
            config['txt3']=label.lab3.txt1.get()+'\n'+label.lab3.txt2.get()

            data['config']=config
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        menu_open.set(0)
        options.destroy()


    options.protocol('WM_DELETE_WINDOW', option_destroy)

