import win32gui
import win32ui
import win32con

def get_taskbar_height():
    taskbar_handle = win32gui.FindWindow("Shell_TrayWnd", None)

    taskbar_rect = win32gui.GetWindowRect(taskbar_handle)

    return taskbar_rect[3] - taskbar_rect[1]

def get_taskbar_color(middle_x=None):
    taskbar_handle = win32gui.FindWindow("Shell_TrayWnd", None)

    taskbar_rect = win32gui.GetWindowRect(taskbar_handle)

    if middle_x is None:
        middle_x = int((taskbar_rect[0] + taskbar_rect[2]) * 0.65-5)
    middle_y = (taskbar_rect[1] + taskbar_rect[3]) // 2

    hwin = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hwin)
    window_dc = win32ui.CreateDCFromHandle(desktop_dc)
    memory_dc = window_dc.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(window_dc, 1, 1)

    memory_dc.SelectObject(bitmap)

    memory_dc.BitBlt((0, 0), (1, 1), window_dc, (middle_x, middle_y), win32con.SRCCOPY)

    bmp_info = bitmap.GetInfo()
    color_data = bitmap.GetBitmapBits(True)

    b = color_data[0]
    g = color_data[1]
    r = color_data[2]

    memory_dc.DeleteDC()
    win32gui.ReleaseDC(hwin, desktop_dc)
    win32gui.DeleteObject(bitmap.GetHandle())

    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def get_complementary_color(hex_color):
    hex_color = hex_color.lstrip('#')
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    comp_r = 255 - r
    comp_g = 255 - g
    comp_b = 255 - b
    
    complementary_color = f'#{comp_r:02X}{comp_g:02X}{comp_b:02X}'
    
    return complementary_color
