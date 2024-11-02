import sys
import os

def resource_path(relative_path):
    app_data_path = os.path.join(os.getenv('APPDATA'), 'NetMeterLite')
    if os.path.exists(app_data_path):
        return os.path.join(app_data_path, relative_path)
    else:
        return os.path.join(relative_path)
