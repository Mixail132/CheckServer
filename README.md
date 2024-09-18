# About
The project's app pings web hosts to ensure they are up.\
If not, an alarm occurs, and the power network is off.\
Then, the app sends the alarm message to specific Telegram and Viber users.

![graphic_description.png](static/graphic_description.png)
# Installation
- Git clone the project:\
```PS ... > git clone https://github.com/Mixail132/CheckServer.git```
- Create a virtual environment:\
```PS ... > python -m venv .venv```
- Activate the virtual environment:\
```PS ... > cd .venv/scripts/activate.bat```
- Install the project requirements:\
```(.venv) PS ... > pip install -r requirements.txt```
- Save the ```example_vars.ini``` file as ```vars.ini```:\
```(.venv) PS ... > cd app ; copy example_vars.ini vars.ini```
- Fill the ```vars.ini``` file with your data.
- Make sure you have set up at least one ```Telegram``` or ```Viber``` bot.
- If you haven't, create your ```Viber``` or ```Telegram``` bot.
- Run the tests:\
```(.venv) PS ... > python -m pytest -с .github\settings\pytest.ini```
- Run the script:
``` PS ... > CheckServer.exe```

# Folders
- .github - ```GitHub``` actions and linters settings;
- .temp   - linters and pytest cache files;
- .venv   - virtual environment components;
-  app    - the project's application files;
-  static - images and media files;
-  tests  - the project's tests.

# Files
- app/audit.py - the project's main actions
- app/builder.py - the ```CheckServer.exe``` file builder;
- app/CheckServer.exe - tha main output executable project's file;
- app/example_vars.ini - the project's configuration variables example;
- app/vars.ini - a user's configuration and secret variables;
- app/linter.py - the code checking with launching linters;
- app/logo.jpg - the ```Viber``` bot logo file;
- app/dirs.py - the relative path's to the project's folders;
- app/main.py - the project's main logic handler;
- app/telegram.py - ```Telegram``` bot logic and settings;
- app/viber.py  - ``Viner`` bot logic and settings;
- app/vars.py - the project's configuration file reading;
- static/ico.ico - the ```CheckServer.exe``` icon;
- requirements.txt - the project's Python modules.