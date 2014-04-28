from cx_Freeze import setup, Executable

#must include all file names
buildOptions = dict(include_files = ['data/maps/','data/maps/parkour/','data/images/','data/fonts/','data/music'])

setup(  
      name = "Parkour",
        version = "0.1",
        description = "My GUI application!",
        options = dict(build_exe = buildOptions),
        executables = [Executable("Main.py")])