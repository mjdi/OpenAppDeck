# OpenAppDeck
Visual App Icon Grid (inspired by Vimium + Elgato Stream Deck) task switcher enhancement middleware for PowerToys Run
- more easily switch between up to 40 open windows with a 4x10 app grid layout which intuitively compliments your keyboard!
- Note: Currently maps to number row + Colemak DH layout (easily changed in app.py or later in the config files when I refactor the code)
- default hotkey to open OpenAppDeck is `win+backspace` (as this was easy on my split ergonomic keyboard)
  - I would also suggest changing it to `alt+space` (PowerToysRun's default hotkey) in `hotkey.py`
  
## Video Demo

https://github.com/user-attachments/assets/fb4f480e-a128-45df-abae-7f0573657c22

## Comparison with Windows TaskView
### OpenAppDeck 😎😎😎
![OpenAppDeck](https://github.com/user-attachments/assets/c4fd4cb6-191c-4673-97dd-6c1f019e6ba9)

##                                      ...VS...

### Windows Task View 🤮🤮🤮
![WindowsTaskView](https://github.com/user-attachments/assets/21b37b1c-dd8c-41c3-8886-66c451d699eb)


## Non-Python requirements
PowerToys (up to date is best)
https://apps.microsoft.com/detail/xp89dcgq3k6vld?launch=true&mode=full&hl=en-us&gl=ca&ocid=bingwebsearch

## Installation and Running
```
git clone https://github.com/mjdi/OpenAppDeck.git
cd OpenAppDeck
virtualenv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
python hotkey.py
```

## Why does it require Admin privileges?
As shown in the demo, hotkey.py will ask for admin privileges in order to swap to/away from other admin windows

## ToDo:
- get `hotkey.py` to run at startup and auto-minimize the python/cmd window that appears
- move all hardcoded values to a config file (to avoid committing them every time they change)
- improve the rendering speed (perhaps use smaller images/icons), improve window title extraction logic
- improve text formatting and user interface, test with more types of apps, downloading more icons to fill gaps
- disable remaining buttons that don't have an associated app, find/fix more bugs that are created/discoverd later
- figure out a way to disambiguate Windows Explorer windows (default image since they are ambiguously titled after directory)
