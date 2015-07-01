import subprocess
import os


def try_import(module):
    try:
        module
        return True
    except ImportError:
        print("\nImport: {} UNSUCCESSFUL!!".format(module))
        return False


def fix_gtk_import():
    """
    function prompts user to fix import issue and if yes
    calls shell command to install PyGtk
    :return: None
    """
    while True:
        attempt_install = input("\nWould you like to attempt to install PyGtk? (y/n) ")
        if attempt_install == "y":
            subprocess.call("sudo apt-get install python3-gi", shell=True)
            break
        elif attempt_install == "n":
            break
        else:
            print("Invalid input, please use (y/n)")

def check_files():
    program_files = ("themer.py", "main.py", "make.py", "help", "welcome",
                     "README.md", "icons/button.png", "icons/popup.png",
                     "icons/panel.png")

    for i in program_files:
        if not os.path.isfile(i):
            print("\n{} system file is not found, re-clone for repo and try again\n".format(i))
            return False
    return True

if __name__ == '__main__':
    if not try_import("from gi.repository import Gtk"):
        fix_gtk_import()

    if check_files():
        import main
        main.run()
