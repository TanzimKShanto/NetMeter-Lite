import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=NetMeter Lite',
    '--onedir',
    '--noconsole',
    '--add-data=skins;skins',
    '--add-data=config.json;.',
    '--add-data=setting.ico;.',
    '--add-data=setting.png;.',
    '--icon=netmeter.ico',
    '--upx-dir=E:/upx-4.2.4-win64/upx.exe',
    'main.py'
])
