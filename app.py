import time
import win32gui
import uiautomation as auto
import regex as re

def script(duration):
    start_time = time.time()
    timeout = start_time + 60*duration
    application = None
    app_dict = {}
    while time.time() < timeout:
        time.sleep(3)
        window = win32gui.GetForegroundWindow()
        win_name = win32gui.GetWindowText(window)
        if "Google Chrome" in win_name:
            chromeControl = auto.ControlFromHandle(window)
            edit = chromeControl.DocumentControl()
            url = edit.GetValuePattern().Value
            base_url = re.search(r"https:\/\/(?:www\.)?([^\/]*)", url)
            if base_url:
                base_url = base_url.group(1)
            if application == base_url:
                continue
            elapsed_time = time.time() - start_time
            # print(application)
            # print("You spent " + str(elapsed_time) + " on the above application")
            if application not in app_dict:
                app_dict[application] =  elapsed_time
            app_dict[application] +=  elapsed_time
            application = base_url
            start_time = time.time()
        else:
            if application == win_name:
                continue
            elapsed_time = time.time() - start_time
            # print(application)
            # print("You spent " + str(elapsed_time) + " on the above application")
            if application not in app_dict:
                app_dict[application] =  elapsed_time
            app_dict[application] +=  elapsed_time
            application = win_name
            start_time = time.time()
    elapsed_time = time.time() - start_time
    if application not in app_dict:
        app_dict[application] =  elapsed_time
    app_dict[application] +=  elapsed_time
    print(app_dict)

duration = float(input("How long would you like me to track your activity (in minutes)? "))
script(duration)