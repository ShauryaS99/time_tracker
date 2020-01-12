import time
import win32gui
import uiautomation as auto
import regex as re
import matplotlib.pyplot as plt

def script(duration):
    start_time = time.time()
    timeout = start_time + 60*duration
    application = None
    app_dict = {}
    #Run Script for Desired Duration
    while time.time() < timeout:
        try:
            time.sleep(3)
            window = win32gui.GetForegroundWindow()
            win_name = win32gui.GetWindowText(window)
            #Handles Chrome Activities
            if "Google Chrome" in win_name:
                chromeControl = auto.ControlFromHandle(window)
                edit = chromeControl.DocumentControl()
                url = edit.GetValuePattern().Value
                base_url = re.search(r"https:\/\/(?:www\.)?([^\/]*)", url)
                if base_url:
                    base_url = base_url.group(1)
                if application == base_url:
                    continue
                #Update Time & Application Name
                elapsed_time = time.time() - start_time
                if application not in app_dict:
                    app_dict[application] =  elapsed_time
                app_dict[application] +=  elapsed_time
                application = base_url
                start_time = time.time()
            #Handles Other Applications
            else:
                if application == win_name:
                    continue
                elapsed_time = time.time() - start_time
                if application not in app_dict:
                    app_dict[application] =  elapsed_time
                app_dict[application] +=  elapsed_time
                application = win_name
                start_time = time.time()
        except:
            continue
    #Finalizes Application Dictionary
    elapsed_time = time.time() - start_time
    if application not in app_dict:
        app_dict[application] =  elapsed_time
    app_dict[application] +=  elapsed_time
    visualize(app_dict)
def visualize(app_dict):
    #Pie Chart for Time Tracker
    del app_dict[None]
    print(app_dict)
    plt.figure(figsize=(5,5))
    labels = list(app_dict.keys())
    values = list(app_dict.values())
    plt.title("Time Tracker for " + str(duration) + " Minutes")
    plt.pie(values, labels = labels, autopct="%.1f%%")
    plt.show()
def sanitize_input(question):
    #Sanitize Input
    options = ["mins", "hours"]
    duration = 'f'
    value = 'f'
    while True:
        try:
            prompt = input(question)
            prompt_mins = re.search(r"([0-9]+)\s?(mins)", prompt)
            if prompt_mins:
                duration = int(prompt_mins.group(1))
                value = prompt_mins.group(2)
            else:
                prompt_hours = re.search(r"([0-9]+)\s?(hours)", prompt)
                if prompt_hours:
                    duration = int(prompt_hours.group(1)) * 60
                    value = prompt_hours.group(2) 
            mins = int(duration)
        except ValueError:
            print("Please give your response as [XX mins/ hours] ")
            continue
        if value not in options:
            print("hey give your response as [XX mins/ hours] ")
            continue
        else:
            break
    return mins
#Ask User for Duration
duration = sanitize_input("How long would you like me to track your activity [mins/ hours]? ")
script(duration)