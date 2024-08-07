#TODO: add customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from customtkinter import *
import sys
import shutil
import webbrowser as website
#import usb.core 
import zipfile
import json
import os
from datetime import datetime
import serial as list_ports
import socket

global file_name
global file_content
file_name = "N/A"
content_compile = []
file_content = "N/A"
__version__ = "0.0.0.0"
conf_file = "conf.json"
llsp3_file_path = 'Projekt.llsp3'
extracted_folder = llsp3_file_path + 'projectbody.json'

with open(conf_file, "r") as file:
    content = json.load(file)
    calibrate = content["calibrate"]
    __version__ = content["version"]
    module = content["module"]
    motor = content["motor"]
    sensor = content["sensor"]
    variables = content["variables"]

class gui:
    def __init__(self):
        self.font_groesse = 14
        self.font_content = "Arial"
        self.author_name = socket.gethostname()
        self.langs = ["English", "German"]
        self.lang = "N/A"
        self.file = "N/A"
        self.file_content = "N/A"
        self.app = CTk()
        self.app.title("Spike Prime Custom System Programming") # File extension .scsp
        self.app.geometry("800x600")
        self.app.resizable(True, True)
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.bind('<Control-s>', lambda: self.save())
        self.app.iconbitmap("icon.ico")
        self.setup()
        self.main_programm()
        self.app.mainloop()

    def setup(self):
        self.app.withdraw()

        self.setup = CTkToplevel(self.app)
        self.setup.title("Spike Prime Custom System Programming Setup")
        self.setup.geometry("300x400")
        self.setup.resizable(False, False)
        self.setup.iconbitmap("icon.ico")
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.setup_Title1 = CTkLabel(self.setup, text="Setup", font=("Arial", 60))
        self.setup_Title2 = CTkLabel(self.setup, text="Program", font=("Arial", 60))
        self.setup_lang_lable = CTkLabel(self.setup, text="Language:", font=("Arial", 25))
        self.setup_lang = CTkComboBox(self.setup, values=self.langs, font=("Arial", 20), corner_radius=20, border_width=0, dropdown_font=("Arial", 20))
        self.setup_submit = CTkButton(self.setup, text="Submit Settings", command=self.submit, font=("Arial", 30), corner_radius=20, border_width=0)

        self.setup_Title1.place(relx=0.5, rely=0.15, anchor="center")
        self.setup_Title2.place(relx=0.5, rely=0.3, anchor="center")
        self.setup_lang_lable.place(relx=0.5, rely=0.55, anchor="center")
        self.setup_lang.place(relx=0.5, rely=0.65, anchor="center")
        self.setup_submit.place(relx=0.5, rely=0.9, anchor="center")

    def submit(self):
        self.lang = self.setup_lang.get()
        self.setup.destroy()
        self.app.deiconify()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.app.destroy()
            exit(0)
            
    def save(self):
        try:
            if file_name == "N/A":
                Files = [('Ekips Custom System Programming', '*.scsp'), ('Text Document', '*.txt')]
                file = filedialog.asksaveasfile(filetypes = Files, defaultextension = Files)
                file.write(self.file_content.get("1.0", "end-1c"))
                file.close()
                file = file.name
                self.file_label.config(text=f"File: {file}")
            else:
                with open(self.file, "w") as f:
                    f.write(self.file_content.get("1.0", "end-1c"))
        except:
            messagebox.showerror("Error", "Error while saving file")
    
    def update_gui(self):
        # TODO: add the update.py class
        yes = messagebox.askyesno("Update", "Do you want to update the programm?")
        if yes:
            update.update_gui()
            exit(0)
        else:
            messagebox.showinfo("Update", "The programm will not be updated")
        
    def update_spike(self):
        yes = messagebox.askyesno("Update", "Do you want to update the Spike Operating System?")
        if yes:
            update.update_spike()
        else:
            messagebox.showinfo("Update", "The Spike Operating System will not be updated")
    
    def open(self):
        #try:
            if self.file_content.get("1.0", "end-1c") != "": #TODO: add a messagebox to ask if the user want to save the file
                msg = messagebox.askyesno("Save", "Do you want to save the file?")
                if msg:
                    self.save()
                else:
                    pass
            file = filedialog.askopenfilename(filetypes=[('Ekips Custom System Programming', '*.scsp'), ('Text Document', '*.txt')])
            self.file_label.configure(text=f"File: {file}")
            with open(file, "r") as f:
                # TODO:Delete the Author tag from the str and just let the file_content be the content of the str
                file_name = file
                content = f.readlines()
                self.file_content.delete("1.0", "end")
                self.file_content.insert("1.0", f.read())
        #except:
        #    messagebox.showerror("Error", "Error while opening file")
    
    def main_programm(self):
        self.author_name = socket.gethostname()
        self.file_label = CTkLabel(self.app, text="File: N/A")
        self.file_author = CTkLabel(self.app, text=f"Author: {self.author_name}")
        self.file_label.place(x=150, y=0)
        self.file_author.place(x=220, y=0)
        self.file_content = tk.Text(self.app, font=f"{self.font_content} {self.font_groesse} bold")
        self.file_content.place(x=230, y=40, relwidth=1, relheight=1)
        self.menu_top()
        self.toolbar()

    def licence(self):
        messagebox.showinfo("License", f"Ekips System Programming License Agreement\nThis License Agreement (the 'Agreement') is entered into by and between Maximilian Gründinger ('Licensor') and the First Lego League Team known as PaRaMeRoS ('Licensee').\n1. License Grant.\nLicensor hereby grants Licensee a non-exclusive, non-transferable license to use and modify the software program known as Spike Custom System Programming (the 'Program') solely for educational and non-commercial purposes. This license is granted exclusively to the members of the First Lego League Team identified as PaRaMeRoS.\n2. Restrictions.\nLicensee shall not, and shall not permit others to:\na. Use the Program for any purpose other than educational and non-commercial activities within the First Lego League Team.\nb. Allow non-members of the First Lego League Team to use or access the Program.\nc. Commercialize or distribute the Program for financial gain.\nd. Remove or alter any copyright, trademark, or other proprietary notices contained in the Program.\n3. Security.\nLicensor makes no warranties regarding the security of the Program. Licensee acknowledges and agrees that any use of the Program is at their own risk. Licensor shall not be responsible for any security bugs or issues that may arise in connection with the Program.\n4. Term and Termination.\nThis Agreement shall remain in effect until terminated by either party. Licensor reserves the right to terminate this Agreement immediately if Licensee breaches any of its terms. Upon termination, Licensee shall cease all use of the Program and destroy all copies in their possession.\n5. Disclaimer of Warranty.\nTHE PROGRAM IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. LICENSOR DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n6. Limitation of Liability.\nIN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n7. Governing Law.\nThis Agreement shall be governed by and construed in accordance with the laws of Germany, Bavaria, Munic.\n8. Entire Agreement.\nThis Agreement constitutes the entire agreement between the parties and supersedes all prior agreements, whether oral or written, with respect to the Program.\nIN WITNESS WHEREOF, the parties hereto have executed this License Agreement as of the effective date.\nLicensor:\nMaximilian Gründinger\nLicensee:\nPaRaMeRoS\nDate: 1.1.2024")
    
    def toolbar(self, mode=None):
        self.left_frame = CTkFrame(self.app)
        self.left_frame.pack(side="left", fill="y")
        CTkButton(self.left_frame, text="Push", command=tools.push, height=100, width=150, border_width=1).pack()
        CTkButton(self.left_frame, text="Update", command=update.update_spike, height=100, width=150, border_width=1).pack()
        CTkButton(self.left_frame, text="help", command=self.help_web, height=100, width=150, border_width=1).pack()
        CTkButton(self.left_frame, text="Exit", command=self.on_closing, height=100, width=150, border_width=1).pack()
        
    def select_port(self):
        port = list(list_ports.comports())
        port_names = [p.device for p in port]
        for p in port:
            print(p.device)
        self.app1 = CTk()
        self.app1.title("Ekips System Programming") # File extension .scsp
        self.app1.geometry("300x200")
        self.app1.resizable(True, True)
        self.app1.iconbitmap("icon.ico")
        self.port = tk.StringVar()
        CTkLabel(self.app1, text="Select the port of the Spike Prime", font=("Arial", 20)).pack()
        CTkComboBox(self.app1, values=port_names, variable=self.port, font=("Arial", 20)).pack()  # Use port_names
        CTkButton(self.app1, text="Submit", command=self.submit_port, font=("Arial", 20)).pack()
        self.app1.mainloop()
    
    def submit_port(self):
        self.port = self.port.get()
        self.app1.destroy()

    #TODO: Make Custom Menu
    def menu_top(self):
        self.menu = tk.Menu(self.app)
        self.app.config(menu=self.menu)
        self.file = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Open", command=self.open)
        self.file.add_command(label="Save", command=lambda: self.save())
        self.file.add_command(label="Save as", command=self.save)
        self.file.add_command(label="Rename Author", command=self.name_author)
        
        self.tools = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Tools", menu=self.tools)
        self.tools.add_command(label="Debug", command=lambda: self.select_file_deb())
        self.tools.add_command(label="Compile", command=lambda: self.select_file())
        self.tools.add_command(label="Pull", command=tools.pull)
        
        self.spike = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Spike", menu=self.spike)
        self.spike.add_command(label="Run", command=self.open)
        self.spike.add_command(label="Push", command=tools.push)
        self.spike.add_command(label="Pull", command=tools.pull)
        self.spike.add_command(label="Update", command=update.update_spike)
        
        self.usb = tk.Menu(self.menu, tearoff=0)
        self.wireless = tk.Menu
        self.menu.add_cascade(label="Connect", menu=self.usb)
        self.usb.add_command(label="USB", command=connect.usb_connection)
        self.usb.add_command(label="Wireless", command=connect.wireless_connection)
        self.usb.add_command(label="Select Port", command=self.select_port)
        
        self.help = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help)
        self.help.add_command(label="Credit", command=self.credit)
        self.help.add_command(label="License", command=self.licence)
        self.help.add_command(label="About", command=self.about)
        self.help.add_command(label="GitHub", command=self.github)
        self.help.add_command(label="Help/Dokumentation", command=self.help_web)
        self.help.add_command(label="Update", command=update.update_gui)
        
        self.gui_mode = tk.Menu(self.menu, tearoff=0) #TODO:  add the difrent modes and settings
        self.menu.add_cascade(label="Mode", menu=self.gui_mode)
        self.gui_mode.add_command(label="Set font", command=self.font)
        self.gui_mode.add_separator()
        self.gui_mode.add_command(label="Light Mode")
        self.gui_mode.add_command(label="Dark Mode")
        self.gui_mode.add_separator()
        self.gui_mode.add_checkbutton(label="custom python llsp3 compiler")
        
    def name_author(self):
        self.author = tk.Tk()
        self.author.title("Rename Author")
        self.author.geometry("300x100")
        self.author.resizable(False, False)
        self.label = CTkLabel(self.author, text="Enter your name:")
        self.label.pack()
        self.entry = CTkEntry(self.author)
        self.entry.pack()
        self.button = CTkButton(self.author, text="Rename", command=self.rename)
        self.button.pack()
        
    def font(self):
        self.combobox1_get = tk.StringVar()
        self.combobox2_get = tk.StringVar()
        self.font_app = tk.Tk()
        self.font_app.title("Font")
        self.font_app.geometry("300x200")
        self.font_app.resizable(False, False)
        self.combobox1 = CTkComboBox(self.font_app, values=["Arial", "Helvetica", "Times", "Courier", "Verdana", "Impact", "Comic Sans MS", "Fixedsys", "MS Sans Serif", "MS Serif"])
        self.combobox1.pack()
        self.combobox2 = CTkComboBox(self.font_app, values=["9", "10", "12", "14", "16", "18", "20", "22"])
        self.combobox2.pack()
        self.button = CTkButton(self.font_app, text="set font", command=self.set_font)
        self.button.pack()
    
    def set_font(self):
        self.font_groesse = self.combobox2_get.get()
        self.font_content = self.combobox1_get.get()
        self.file_content.config(font=f"{self.font_content} {self.font_groesse} bold")
        self.font_app.destroy()
    
    def rename(self):
        self.author_name = self.entry.get()
        self.file_author.config(text=f"Author: {self.author_name}")
        self.author.destroy()
    
    def credit(self):
        messagebox.showinfo("Credit", "Maximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
        
    def about(self):
        messagebox.showinfo("About", f"Spike Custom System Programming\nVersion {__version__}\nMaximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
    
    def github(self):
        website.open("https://github.com/Ekips-Prime-Pro/Ekips-Prime-Pro-Editor")
        
    def help_web(self):
        messagebox.showinfo("Help", "For help and documentation please visit the GitHub page of the project")
        website.open("https://github.com/Ekips-Prime-Pro/Ekips-Prime-Pro-Editor")
        
    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("Ekips System Programming", "*.scsp")])
        if file:
            self.file = file
            compiler.compile(file)
            compiler.main(file)
    
    def select_file_deb(self):
        file = filedialog.askopenfilename(filetypes=[("Ekips System Programming", "*.scsp")])
        if file:
            self.file = file
            debugger.main_debug(file)


class update:
    def __init__():
        pass
    
    def update_gui():
        pass
    
    def update_spike():
        pass


class connect:
    def __init__():
        pass
     
    def usb_connection():
        pass
     
    def wireless_connection():
        pass
    
    
class tools:
    def __init__():
        pass
    
    def pull():
        pass
    
    def push():
        pass
     
     
class debugger:
    
    def check_for_format(requestet, value):
        """
        Checks if the value matches the requested format.

        Parameters:
            requestet (str): The requested format.
            value (str): The value to check.
        """
        if requestet == "int":
            try:
                int(value)
            except:
                messagebox.askokcancel(f"Error: The value {value} is not a valid integer.")
    
    def get_active_function(line):
        content_line = line
        function, variable = content_line.split("{")
        variable = variable.replace("{","")
        variable = variable.replace("}","")
        variable = variable.replace("\n","")
        return function, variable
    
    def debug_function(function,value=False):
        """
        Debugs the specified function.

        Parameters:
            function (str): The function to debug.
            value (str, optional): The value associated with the function. Defaults to False.
        """
        print(f"Debuging {function} function...")
        match function:
            case "log":
                pass
            case "sleep":
                check_for_format("int", value)
            case "init":
                pass
            case "ai.chose":
                value = f"{value}"
                match value:
                    case "supervised":
                        pass
                    case "unsupervised":
                        pass
                    case "deep_learning":
                        pass
                    case _:
                        messagebox.askokcancel(f"Error: The AI {value} does not exist.")
                        exit(1)
            case "ai.init":
                pass
            case "module.init":
                pass
            case "motor.init":
                pass
            case "sensor.init":
                pass
            case "calibration.init":
                pass
            case "variable.init":
                pass
            case "drive":
                check_for_format("int", value)
            case "tank":
                check_for_format("int", value)
            case "obstacle":
                check_for_format("int", value)
            case "ai.sensor":
                value = f"{value}"
                match value:
                    case "force":
                        pass
                    case "distance":
                        pass
                    case "color":
                        pass
                    case "gyro":
                        pass
                    case _:
                        messagebox.askokcancel(f"Error: The sensor {value} does not exist.")
            case "module":
                check_for_format("int", value)
            case "calibrate":
                pass
            case "ai.data_save":
                pass
            case "ai.data_load":
                pass
            case "main.init":
                pass
            case "main.run":
                pass
            case _:
                if function == "//":
                    pass
                elif function == "#":
                    pass
                else:
                    messagebox.showwarning(f"Error: The function {function} does not exist.")

    def main_debug(file):
        """
        Main function for debugging the compiled file.

        Parameters:
            file (str): The name of the file to debug.
        """
        for line in content_compile:
            # Komentare herausfiltern
            function, value = get_active_function(line)
            debug_function(function, value)
        messagebox.showinfo("Debug", "The file has been successfully debugged.")


class compiler:
    # Functions
    def compile(file):
        if file.endswith(".scsp"):
            with open(file, "r") as f:
                content = f.readlines()
                for line in content:
                    content_compile.append(line)
        else:
            messagebox.askokcancel(f"Error: The file {file} is not a valid file type.")
            sys.exit(1)

    def get_active_function(line):
        content_line = line
        function, variable = content_line.split("{")
        variable = variable.replace("{","")
        variable = variable.replace("}","")
        variable = variable.replace("\n","")
        return function, variable

    def write_function(function,file,value=False):
        """
        Writes the specified function and its value to a Python file.

        Parameters:
            function (str): The function to write.
            file (str): The name of the file to write to.
            value (str, optional): The value associated with the function. Defaults to False.
        """
        print(f"Writing {function} function...")
        file_name = file.split(".")
        file_name = file_name[0]
        with open(f"{file_name}.py", "a") as f:
            match function:
                case "log":
                    print_out = f"\nprint('{str(value)}')"
                    f.write(print_out)
                case "sleep":
                    sleep_out = f"\ntime.sleep({str(value)})"
                    f.write(sleep_out)
                case "init":
                    init_out = f"\nimport force_sensor, distance_sensor, motor, motor_pair\nfrom hub import port\nimport time\nfrom app import linegraph as ln\nimport runloop\nfrom math import *\nimport random\n"
                    f.write(init_out)
                case "ai.chose":
                    ai_chose_out = f"ai_chose = '{str(value)}'\n"
                    f.write(ai_chose_out)
                case "ai.init":
                    ai_init_out = f"\nai = runloop.AI()\n"
                    f.write(ai_init_out)
                    with open("ai.fll", "r") as r:
                        ai_content = r.readlines()
                        for line in ai_content:
                            f.write(line)
                case "module.init":
                    ai_content = module
                    for line in ai_content:
                        f.write(line)
                case "motor.init":
                    ai_content = motor
                    for line in ai_content:
                        f.write(line)
                case "sensor.init":
                    ai_content = sensor
                    for line in ai_content:
                        f.write(line)
                case "calibration.init":
                    ai_content = calibrate
                    for line in ai_content:
                       f.write(line)
                case "variable.init":
                    ai_content = variables
                    for line in ai_content:
                        f.write(line)
                case "drive":
                    f.write(f"\n  await drive({value})\n")
                case "tank":
                    f.write(f"\n  await tank({value})\n")
                case "obstacle":
                    f.write(f"\n  await obstacle({value})\n")
                case "ai.sensor":
                    # add the sensor to the ai input
                    f.write(f"\nai_sensor.append('{value}\n')")
                case "module":
                    f.write(f"\nawait module({value})\n")
                case "calibrate":
                    f.write("\n   await calibrate()\n")
                case "ai.data_save":
                    f.write(f"\n  write_ai_data('{value}')\n")
                case "ai.data_load":
                    for line in value:
                        f.write(f"\nai_data.append({line})\n")
                case "main.init":
                    f.write("\nasync def main():")
                case "main.run":
                    f.write("\nrunloop.run(main())")
                case _:
                    if function == "//":
                        f.write(f"# {value}")
                    elif function == "#":
                        f.write(f"# {value}")
                    else:
                        print(f"Error: The function {function} does not exist.")
                        sys.exit(1)

    def compile_llsp3(file, directory, project_name):
        os.makedirs(directory, exist_ok=True)
        projectbody_data = {
            "main": ""
        }
        icon_svg_content = """
        <svg width="60" height="60" xmlns="http://www.w3.org/2000/svg">
            <g fill="none" fill-rule="evenodd">
                <g fill="#D8D8D8" fill-rule="nonzero">
                    <path d="M34.613 7.325H15.79a3.775 3.775 0 00-3.776 3.776v37.575a3.775 3.775 0 003.776 3.776h28.274a3.775 3.775 0 003.776-3.776V20.714a.8.8 0 00-.231-.561L35.183 7.563a.8.8 0 00-.57-.238zm-.334 1.6l11.96 12.118v27.633a2.175 2.175 0 01-2.176 2.176H15.789a2.175 2.175 0 01-2.176-2.176V11.1c0-1.202.973-2.176 2.176-2.176h18.49z"/>
                    <path d="M35.413 8.214v11.7h11.7v1.6h-13.3v-13.3z"/>
                </g>
                <path fill="#0290F5" d="M23.291 27h13.5v2.744h-13.5z"/>
                <path fill="#D8D8D8" d="M38.428 27h4.32v2.744h-4.32zM17 27h2.7v2.7H17zM17 31.86h2.7v2.744H17zM28.151 31.861h11.34v2.7h-11.34zM17 36.72h2.7v2.7H17zM34.665 36.723h8.1v2.7h-8.1z"/>
                <path fill="#0290F5" d="M28.168 36.723h4.86v2.7h-4.86z"/>
            </g>
        </svg>
        """
        projectbody_path = os.path.join(directory, 'projectbody.json')
        with open(file, 'r') as file:
            projectbody_data['main'] = file.read()
        with open(projectbody_path, 'w') as file:
            json.dump(projectbody_data, file)
        icon_svg_path = os.path.join(directory, 'icon.svg')
        with open(icon_svg_path, 'w') as file:
            file.write(icon_svg_content)
        current_datetime = datetime.utcnow().isoformat() + 'Z'
        manifest_data = {
            "type": "python",
            "appType": "llsp3",
            "autoDelete": False,
            "created": current_datetime,
            "id": "wJI4suuRFvcs",
            "lastsaved": current_datetime,
            "size": 1004,
            "name": project_name,
            "slotIndex": 0,
            "workspaceX": 120,
            "workspaceY": 120,
            "zoomLevel": 0.5,
            "hardware": {
                "python": {
                    "type": "flipper"
                }
            },
            "state": {
                "canvasDrawerOpen": True
            },
            "extraFiles": []
        }
        manifest_path = os.path.join(directory, 'manifest.json')
        with open(manifest_path, 'w') as file:
            json.dump(manifest_data, file)
        llsp3_file_path = os.path.join(directory, project_name + '.llsp3')
        with zipfile.ZipFile(llsp3_file_path, 'w') as zip_ref:
            for foldername, subfolders, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, directory)
                    zip_ref.write(file_path, arcname)

    def main(file):
        """
        Main function for compiling the file.

        Parameters:
            file (str): The name of the file to compile.
        """
        file_name = file.split(".")
        file_dir = file_name[1]
        file_name = file_name[0]
        with open(f"{file_name}.py", "w") as f:
            f.write("")
        for line in content_compile:
            # Komentare herausfiltern
            function, value = get_active_function(line)
            write_function(function, file, value)
        compile_llsp3(file_name + ".py", file_dir, file_name)



if __name__ == "__main__":
    gui()
