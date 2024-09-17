# About
The project's app checks a series of web servers to ensure they are up.\
If not, an alarm occurs, and the power supply breaker is turned off.\
Then, the app sends the alarm message to specific Telegram and Viber users.

# Installation
1. Git clone the project.
2. Create a virtual environment.
3. Install the project's requirements.
4. Save the ```example_vars.ini``` file as ```vars.ini```.
5. Fill the ```vars.ini``` file with your data.
6. Make sure you have set up at least one ```Telegram``` or ```Viber``` bot.
7. If you haven't, create your ```Viber``` or ```Telegram``` bot.
8. Run the tests.
9. Run ```CheckServer.exe```

# Folders
- .github - ```GitHub``` actions and linters settings;
- .temp   - linters and pytest cache files;
- .venv   - virtual environment components;
-  app    - the project's application files;
-  static - images and media files;
-  tests  - the project's tests.

# Filess
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