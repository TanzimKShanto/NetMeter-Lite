import psutil
import threading
import json
import tkinter as tk
import win32gui
from optionwindow import open_options, wake_options
from taskbar import get_taskbar_color, get_taskbar_height, get_complementary_color
from main_classes import *
from res_path import resource_path


def update_speeds(window, label):
    kB = 1024
    mB = 1024*kB
    gB = 1024*mB
    keyb = [['Kb', 'Mb', 'Gb'], ['KB', 'MB', 'GB']]
    net_io = psutil.net_io_counters()
    last_speed_up = net_io.bytes_sent
    last_speed_down = net_io.bytes_recv
    def update_speed(last_speed_up, last_speed_down):

        if label.other_on.get():
            cpu_usage = psutil.cpu_percent(interval=0)
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent
            label.lab4.text.set(f'{cpu_usage}%\n{memory_usage}%')

        net_io = psutil.net_io_counters()
        cur_speed_up = net_io.bytes_sent
        cur_speed_down = net_io.bytes_recv
        interval = label.interval.get()/1000
        download_speed, upload_speed = (cur_speed_down - last_speed_down)*label.unit.get()/interval, (cur_speed_up - last_speed_up)*label.unit.get()/interval
        last_speed_down, last_speed_up = cur_speed_down, cur_speed_up

        # Convert download_speeds to kB/s or mB/s or gB for display
        if download_speed >= gB:
            download_speed/=gB
            did = 2
        elif download_speed >= mB:
            download_speed/=mB
            did = 1
        else:
            download_speed/=kB
            did = 0
        
        # Convert upload_speeds to kB/s or mB/s or gB for display
        if upload_speed >= gB:
            upload_speed/=gB
            uid = 2
        elif upload_speed >= mB:
            upload_speed/=mB
            uid = 1
        else:
            upload_speed/=kB
            uid = 0

        label.lab2.text.set(f"{upload_speed:.2f} {keyb[label.unit.get()%8][uid]}/s\n{download_speed:.2f} {keyb[label.unit.get()%8][did]}/s")

        window.after(label.interval.get(), update_speed, last_speed_up, last_speed_down)
    update_speed(last_speed_up, last_speed_down)

def send_back(hwnd):
     win32gui.SetWindowPos(
        hwnd, 
        win32con.HWND_BOTTOM,  
        0, 0, 0, 0,           
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
    )
# Keep the window always on top
def keep_on_top(widget):
    screen_width = widget.root.winfo_screenwidth()
    screen_height = widget.root.winfo_screenheight()
    mhwnd = win32gui.FindWindow("Progman", None)
    taskbar_handle = win32gui.FindWindow("Shell_TrayWnd", None)
    widget.check_top()
    def update_window():
        send_back(taskbar_handle)
        hwnd = win32gui.GetForegroundWindow()
        flag = True
        if hwnd and hwnd!=mhwnd:
            #print(hwnd, win32gui.GetWindowText(hwnd), win32gui.GetWindowRect(hwnd))
            rect = win32gui.GetWindowRect(hwnd)
            if rect[0] == 0 and rect[1] == 0 and rect[2] == screen_width and rect[3] == screen_height:
                   flag = False
        if not flag:
            widget.toogle_whole_transparent(flag)
        else:
            widget.toogle_whole_transparent(flag)
        widget.root.after(1000, update_window)
    update_window()

def load_config(json_file):
    with open(resource_path(json_file), "r") as f:
        data = json.load(f)
    return data['config'], data['skins']

def create_window():
    config, skins = load_config('config.json')
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    if config['new']:
        config['bg'] = get_taskbar_color()
    taskbar_color = config['bg']
    root.configure(bg=taskbar_color)
    root.attributes('-transparentcolor', taskbar_color)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    taskbar_height = get_taskbar_height()

    window_height = taskbar_height
    window_width = window_height*6
    
    if config['new']:
        config['x'] = int(screen_width*0.65)
        config['y'] = screen_height - window_height
        config['size'] = int(window_height*(8/30))
        config['color'] = get_complementary_color(taskbar_color)

    x_pos = config['x']
    y_pos = config['y']

    sz = f"{0}x{0}"
    pos = f"+{x_pos}+{y_pos}"
    root.geometry(sz+pos)

    tcc = toplevel_windows(root, sz+pos)
    cc = tcc.root
    cc.config(bg='white')
    tlast = toplevel_windows(root, sz+pos)
    last = tlast.root

    transparent = config['transparent']
    lock = config['lock']


    size = config['size']
    color = config['color']
    style = config['style']
    family = config['family']
    other_on = config['other_on']
    interval = config['interval']
    unit = config['unit']
    always_on_top = config['always_on_top']

    txt1 = config['txt1']
    txt2 = config['txt2']
    txt3 = config['txt3']
    txt4 = config['txt4']

    with open(resource_path('config.json'), 'r+') as f:
        data = json.load(f)
        config['new']=False
        data['config']=config
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


    fonts = font_hub(family, size, style, color, taskbar_color)

    lab1 = label_gen(root, fonts, txt1)
    lab2 = label_gen(root, fonts, txt2)
    lab3 = label_gen(root, fonts, txt3)
    lab4 = label_gen(root, fonts, txt4)

    #using Skin
    imlabel = Image_Label(cc, root, config['skin'], skins, (window_width, window_height), transparent, fonts)
    
    widget = widget_handle(root, cc, last, window_height, pos, imlabel, screen_height, screen_width, always_on_top)

    label = label_manager(lab1, lab2, lab3, lab4, other_on, interval, unit, widget)

    drag = make_window_draggable(last, root, cc, lock, fonts, label, imlabel)

    imlabel.register(widget, label)
    imlabel.toogle_transparent(x_pos)
    threading.Thread(target=keep_on_top, args=(widget,), daemon=True).start()

    threading.Thread(target=update_speeds, args=(root, label,), daemon=True).start()


    menu_open = tk.IntVar(value=0)
    def handle_menu(e):
        if not menu_open.get():
            menu_open.set(1)
            open_options(widget, drag, fonts, label, menu_open, imlabel)
        else:
            wake_options()
    widget.menu_bind(handle_menu)
    root.mainloop()

create_window()
