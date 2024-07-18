import time
import pyuac
import keyboard as kb
import pyperclip as pc
import subprocess as sp

PYTHON_EXE_ABSOLUTE_LOCATION = "C:\\repos\\OpenAppDeck\\venv\\Scripts\\python.exe"
OPEN_APP_DECK_PYTHON_FILENAME = "C:\\repos\\OpenAppDeck\\app.py"
OPEN_APP_DECK_HOTKEY = 'windows+backspace'
POWER_TOYS_RUN_HOTKEY = 'alt+space'
POWER_TOYS_WINDOW_WALKER_DIRECT_ACTIVATION_COMMAND = 'shift+comma'  # <
MIN_SLEEP_DELAY_FOR_POWER_TOYS_RUN_AFTER_PASTE = 0.3
SLEEP_DELAY_FOR_POWER_TOYS_RUN_AFTER_PASTE_FACTOR = 0.025 # has to be long enough s, so should be proportional to length of title, 1.5ms per char
A_REALLY_LARGE_NUMBER_FOR_INDEFINITE_RUNTIME = 1000000

def main():
    def on_app_hotkey():
        try:
            command = f'{PYTHON_EXE_ABSOLUTE_LOCATION} {OPEN_APP_DECK_PYTHON_FILENAME}'
            open_app_deck_process = sp.Popen(
                command,
                shell=True,
                stdout=sp.PIPE,
                stderr=sp.STDOUT,
                text=True
            )

            # get app title from stdout of the Open App Deck subprocess
            app_title = ""
            while True:  # https://stackoverflow.com/a/14837673
                inchar = open_app_deck_process.stdout.read(1)
                if inchar == "\n" and app_title == "":
                    break
                try:
                    if inchar: #neither empty string nor None
                        app_title += inchar
                    else:
                        break
                except AttributeError as e:
                    print(e)

            if app_title == "":
                raise Exception(f"Empty {app_title=}")
            else:
                # use PowerToysRun to enact app switch
                stored_clipboard = pc.paste() # save currently copied clipboard
                kb.send(POWER_TOYS_RUN_HOTKEY)
                kb.send(POWER_TOYS_WINDOW_WALKER_DIRECT_ACTIVATION_COMMAND)
                pc.copy(app_title) 
                kb.send("ctrl+v") # faster to paste than use kb.write to emulate typing char by char
                sleep_delay = MIN_SLEEP_DELAY_FOR_POWER_TOYS_RUN_AFTER_PASTE + SLEEP_DELAY_FOR_POWER_TOYS_RUN_AFTER_PASTE_FACTOR * len(app_title)
                time.sleep(sleep_delay)
                kb.send("enter")
                pc.copy(stored_clipboard) # restore whatever was previously copied        
        except Exception as e:
            print(e)

    kb.add_hotkey(OPEN_APP_DECK_HOTKEY, on_app_hotkey, suppress=False)  # we don't want to supress Windows key

    time.sleep(A_REALLY_LARGE_NUMBER_FOR_INDEFINITE_RUNTIME)

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:        
        main()  # Already an admin here.