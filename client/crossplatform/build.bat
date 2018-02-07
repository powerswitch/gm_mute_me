call pyrcc5 icons.qrc -o muteme/icons_rc.py
call pyinstaller --noupx --noconsole -n MuteMe -F muteme\gui.py
