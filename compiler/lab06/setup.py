import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_exe_options = {"packages": ["os", "sys"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "win32gui"
print(base)
setup(name="小型编译器",
      version="1.0",
      description="小型编译器",
      options={"build_exe": build_exe_options},
      executables=[Executable("main_ui.py", base=base,
                              targetName='compiler.exe',
                              icon='images/app.ico'
                              )
                   ])
