import itertools
import pyautogui
import typing
import sys
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

APP_NAME = "OpenAppGrid"
NUM_COLS = 10
NUM_ROWS = 4
APP_TITLE_LINEBREAK_CHAR_FREQ = 20

ICON_FOLDER = "C:\\repos\\OpenAppDeck\\icons\\"
app_title_to_icon_filename = {
    "" : "WE.png",
    "7-Zip" : "7Z.png",
    "Adobe Acrobat Pro (64-bit)" : "AA.png",
    "Adobe Photoshop 2023" : "APS.png",
    "Anaconda Prompt (miniconda3)" : "Conda.png",
    "Driver4VR - 5.7.7.3" : "D4VR.png",
    "Deluge" : "Deluge.png",
    "Docker Desktop" : "Docker.png",
    "f.lux: Smaller adjustments, better for color accuracy" : "F.lux.png",
    "Google Chrome" : "GC.png",
    "Kdenlive" : "KL.png",
    "Logitech Capture" : "LC.png",
    "LosslessCut" : "LLC.png",
    "Logi Options+" : "LO.png",
    "Microsoft Edge" : "ME.png",
    "Microsoft 365 (Office)" : "MO.png",
    "Excel" : "MOE.png",
    "OneNote" : "MON.png",
    "PowerPoint" : "MOP.png",
    "Microsoft Teams" : "MOT.png",
    "Word" : "MOW.png",
    "Paint" : "MSP.png",
    "Microsoft Store" : "MSS.png",
    "Movies & TV" : "MTV.png",
    "Mouse without Borders 2.2.1.0327 - Settings" : "MWB.png",
    "Nebula for Windows" : "Nebula.png",
    "Notepad" : "NP.png",
    "NVIDIA Control Panel" : "NS.png",
    "OBS" : "OBS.png",
    "opentrack-2023.3.0 :: default.ini" : "OT.png",
    "PDF Annotator" : "PDFA.png",
    "Photos" : "Photos.png",
    "tiff" : "Photos.png",
    "png" : "Photos.png",
    "jpg" : "Photos.png",
    "svg" : "Photos.png",
    "webp" : "Photos.png",
    "gif" : "Photos.png",
    "PhoenixHeadTracker 3.0.3.5" : "PHT.png",
    "PowerToys Settings" : "PT.png",
    "Proton VPN" : "PVPN.png",
    "spacedesk Driver Console Application" : "SDDC.png",
    "Settings" : "Settings.png",
    "Steam" : "Steam.png",
    "Headset Window" : "SVR.png",
    "SteamVR Status" : "SVR.png",
    "vrmonitor" : "SVR.png",
    "ShareX 16.1" : "SX.png",
    "Task Manager": "TM.png",
    "TreeSize Free": "TSF.png",
    "VLC media player" : "VLC.png",
    "Microsoft Visual Studio" : "VS.png",
    "Visual Studio Code" : "VSC.png",
    "Media Player" : "WMP.png",
    # "WinRAR" : "WR.png", no way to distinguish with Windows Explorer
    "root" : "WSL.png",
    "Administrator" : "WT.png",  # Windows Terminal 
    "Zoom" : "Zoom.png",
}


app_title_blacklist = [
    "",
    "SylphyHornPlus",
    "Select C:\\repos\\OpenAppDeck\\venv\\Scripts\\python.exe",
    "C:\\repos\\OpenAppDeck\\venv\\Scripts\\python.exe",
    "Settings",
    "Program Manager",
    "Windows Input Experience",
    "PowerToys.PowerLauncher",
    "OpenAppDeck",
    "PopupHost",
    "vrmonitor",
    "ZPToolBarParentWnd"
    
]
keys = [list("1234567890"), 
        list("qwfpbjluy'"),
        list("arstgmneio"),
        list("zxcdvkh,./")]
assert len(keys) == NUM_ROWS
assert len(keys[0]) == NUM_COLS
keys_flat = list(itertools.chain(*keys))


def replace_bad_unicode(app_title:str) -> str:
    return app_title.encode("ascii", "ignore").decode()  # for example \u200b


def intersperse_linebreak(text: str, char_freq: int) -> str:
    # https://stackoverflow.com/a/1772997
    text_with_linebreaks = ""
    for i in range(len(text)):
        text_with_linebreaks += text[i]
        if i % char_freq == 0 and i != 0:
            text_with_linebreaks += "\n" 
    return text_with_linebreaks


def get_next_valid_app_info_title(iter_running_apps: typing.Iterable[tuple]) -> str:
    app_info = None
    title = ""
    try:
        while title in app_title_blacklist:
            app_info = next(iter_running_apps)
            if app_info is not None:
                title = app_info.title
    except StopIteration as e:
        title = ""
    return title

def get_button_callback(my_app_title: str):  # https://stackoverflow.com/a/63198062
    def wrapper(app_title=my_app_title):
        print(app_title) # this is returned to hotkey.py
        app.destroy() # close tkinter app
    return wrapper


def keypress(event):
    print(key_to_app_title[event.char]) # this is returned to hotkey.py
    app.destroy() # close tkinter app

# tkinter setup
app = Tk()
app.title(APP_NAME)
app.geometry(str(app.winfo_screenwidth()) + "x" + str(app.winfo_screenheight()) + "+0+0")
app.resizable(False, False)
app.configure(bg="black")


label_frame = []
app_title_label = []
app_icon = []  # need a global variable for each Image to avoid garbage collection in function
button = []

running_apps = iter(pyautogui.getAllWindows())

key_to_app_title = {}

# create grid for label frames with label and button inside
for i in range(NUM_ROWS):
    label_frame.append([])
    app_title_label.append([])
    app_icon.append([])
    button.append([])
    
    for j in range(NUM_COLS):
        label_frame[i].append(
            LabelFrame(
                app,
                text=keys[i][j],
                fg="gray",
                bg="black",
            )
        )

        app_title = replace_bad_unicode(get_next_valid_app_info_title(running_apps))
        key_to_app_title[keys[i][j]] = app_title

        app_title_label[i].append(
            Label(
                label_frame[i][j],
                text=intersperse_linebreak(app_title, APP_TITLE_LINEBREAK_CHAR_FREQ),
                anchor=CENTER,
                fg="black",
                bg="grey"
            )
        )
        app_title_label[i][j].pack(side=TOP)
        
        full_app_title = app_title
        found = False
        if not (found:= app_title in app_title_to_icon_filename):
            app_title = full_app_title.split("-")[-1].strip()  # try splitting on last minus sign
        if not (found:= app_title in app_title_to_icon_filename):
            app_title = full_app_title.split("|")[-1].strip()  # try splitting by last | sign, (MSTeams)
        if not (found:= app_title in app_title_to_icon_filename):
            app_title = full_app_title.split(":")[0].strip()  # try splitting first : sign, (Administrator: (Admin) Windows Powershell))
        if not (found:= app_title in app_title_to_icon_filename):
            app_title = full_app_title.split("@")[0].strip()  # try splitting first @ sign, (root@<machine>: current directory)
        if not (found:= app_title in app_title_to_icon_filename):
            app_title = full_app_title.split(".")[-1]  # try splitting on last . (image formats in Photos app)
        if not (found:= app_title in app_title_to_icon_filename):
            app_title = full_app_title.split(" ")[0]  # try splitting on first space (OBS)
        if not (found:= app_title in app_title_to_icon_filename):
            app_title = ""  # Unknown, assume its a Windows Explorer Folder 
        
        app_icon[i].append(Image.open(ICON_FOLDER + app_title_to_icon_filename[app_title]))
        app_icon[i][j] = app_icon[i][j].resize((200, 200), Image.LANCZOS)
        app_icon[i][j] = ImageTk.PhotoImage(app_icon[i][j], master=app)

        button[i].append(
            Button(
                label_frame[i][j],
                text="CLICK ME",
                image=app_icon[i][j],
                command=get_button_callback(app_title),
                # bg="black"
            )
        )
        button[i][j].pack(side=BOTTOM)

        label_frame[i][j].grid(row=i, column=j)

        app.columnconfigure(j, weight=1)
    app.rowconfigure(i, weight=1)

# bind keys
for key in keys_flat:  # flatten keys
    if key_to_app_title[key] != "":
        app.bind_all(key, keypress)

app.lift()  # bring in front of all other windows 
app.mainloop()
