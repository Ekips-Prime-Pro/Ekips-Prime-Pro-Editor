#TODO: add customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from customtkinter import *
import os
import sys
import shutil
import webbrowser as website
#import usb.core 
import serial as list_ports
import socket

#TODO: remove global variables
global file_name
global file_content
file_name = "N/A"
file_content = "N/A"

class gui:
    def __init__(self):
        self.font_groesse = 14
        self.font_content = "Arial"
        self.author_name = socket.gethostname()
        self.lang = "N/A"
        self.file = "N/A"
        self.file_content = "N/A"
        self.app = CTk()
        self.app.title("Spike Prime Custom System Programming") # File extension .scsp
        self.app.geometry("800x600")
        self.app.resizable(True, True)
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        # add the background style
        self.app.iconbitmap("icon.ico")
        self.main_programm()
        self.app.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.app.destroy()
            exit(0)
            
    def save(self):
        if self.file == "N/A":
            Files = [('Spike Custom System Programming', '*.scsp'), ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes = Files, defaultextension = Files)
            file.write(self.file_content.get("1.0", "end-1c"))
            file.close()
            file = file.name
            self.file_label.config(text=f"File: {file}")
        else:
            with open(self.file, "w") as f:
                f.write(self.file_content.get("1.0", "end-1c"))
    
    def open(self):
        try:
            if self.file_content.get("1.0", "end-1c") != "": #TODO: add a messagebox to ask if the user want to save the file
                msg = messagebox.askyesno("Save", "Do you want to save the file?")
                if msg:
                    self.save()
                else:
                    pass
            file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Spike Custom System Programming", "*.scsp")])
            self.file_label.config(text=f"File: {file}")
            with open(file, "r") as f:
                # TODO:Delete the Author tag from the str and just let the file_content be the content of the str
                content = f.readlines()
                content = delete_line(content, 0)
                self.file_content.delete("1.0", "end")
                self.file_content.insert("1.0", f.read())
        except:
            messagebox.showerror("Error", "Error while opening file")
    
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
        messagebox.showinfo("License", f"Spike Custom System Programming License Agreement\nThis License Agreement (the 'Agreement') is entered into by and between Maximilian Gründinger ('Licensor') and the First Lego League Team known as PaRaMeRoS ('Licensee').\n1. License Grant.\nLicensor hereby grants Licensee a non-exclusive, non-transferable license to use and modify the software program known as Spike Custom System Programming (the 'Program') solely for educational and non-commercial purposes. This license is granted exclusively to the members of the First Lego League Team identified as PaRaMeRoS.\n2. Restrictions.\nLicensee shall not, and shall not permit others to:\na. Use the Program for any purpose other than educational and non-commercial activities within the First Lego League Team.\nb. Allow non-members of the First Lego League Team to use or access the Program.\nc. Commercialize or distribute the Program for financial gain.\nd. Remove or alter any copyright, trademark, or other proprietary notices contained in the Program.\n3. Security.\nLicensor makes no warranties regarding the security of the Program. Licensee acknowledges and agrees that any use of the Program is at their own risk. Licensor shall not be responsible for any security bugs or issues that may arise in connection with the Program.\n4. Term and Termination.\nThis Agreement shall remain in effect until terminated by either party. Licensor reserves the right to terminate this Agreement immediately if Licensee breaches any of its terms. Upon termination, Licensee shall cease all use of the Program and destroy all copies in their possession.\n5. Disclaimer of Warranty.\nTHE PROGRAM IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. LICENSOR DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n6. Limitation of Liability.\nIN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n7. Governing Law.\nThis Agreement shall be governed by and construed in accordance with the laws of Germany, Bavaria, Munic.\n8. Entire Agreement.\nThis Agreement constitutes the entire agreement between the parties and supersedes all prior agreements, whether oral or written, with respect to the Program.\nIN WITNESS WHEREOF, the parties hereto have executed this License Agreement as of the effective date.\nLicensor:\nMaximilian Gründinger\nLicensee:\nPaRaMeRoS\nDate: 1.1.2024")
    
    def toolbar(self, mode=None):
        self.left_frame = CTkFrame(self.app)
        self.left_frame.pack(side="left", fill="y")
        CTkButton(self.left_frame, text="compile", command=compiler_gui, height=100, width=150, border_width=1).pack()
        CTkButton(self.left_frame, text="save", command=self.save, height=100, width=150, border_width=1).pack()
        CTkButton(self.left_frame, text="help", command=self.help_web, height=100, width=150, border_width=1).pack()
        CTkButton(self.left_frame, text="Exit", command=self.on_closing, height=100, width=150, border_width=1).pack()

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
        self.tools.add_command(label="Debug", command=compiler_gui)
        self.tools.add_command(label="Compile", command=compiler_gui)
        self.tools.add_command(label="compile to llsp3 file", command=compiler_gui)
        
        self.help = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help)
        self.help.add_command(label="Credit", command=self.credit)
        self.help.add_command(label="License", command=self.licence)
        self.help.add_command(label="About", command=self.about)
        self.help.add_command(label="GitHub", command=self.github)
        self.help.add_command(label="Help/Dokumentation", command=self.help_web)
        
        self.gui_mode = tk.Menu(self.menu, tearoff=0) #TODO:  add the difrent modes and settings
        self.menu.add_cascade(label="Mode", menu=self.gui_mode)
        self.gui_mode.add_command(label="Light Mode", command=self.app.config(bg="white"))
        self.gui_mode.add_command(label="Dark Mode", command=self.app.config(bg="black"))
        
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
    
    def rename(self):
        self.author_name = self.entry.get()
        self.file_author.config(text=f"Author: {self.author_name}")
        self.author.destroy()
    
    def credit(self):
        messagebox.showinfo("Credit", "Maximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
        
    def about(self):
        messagebox.showinfo("About", "Spike Custom System Programming\nVersion 0.0.1\nMaximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
    
    def github(self):
        website.open("https://github.com/Iron-witch/Coding_lang_spike_PaRaMeRoS")
        
    def help_web(self):
        messagebox.showinfo("Help", "For help and documentation please visit the GitHub page of the project")
        website.open("https://github.com/Iron-witch/Coding_lang_spike_PaRaMeRoS/wiki")
        
    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()


class compiler_gui:
    def __init__(self):
        self.root1 = CTk()
        self.root1.title("Spike Custom Programming Language Compiler")
        self.root1.geometry("400x450")
        self.root1.iconbitmap("icon.ico")
        self.main_frame()
        self.root1.mainloop()  

    def main_frame(self):
        heief = 40
        wighf = 120
        CTkLabel(self.root1, text="Spike Custom Programming Language Compiler", text_color="Blue").pack(pady=10)
        CTkButton(self.root1, text="select and compile file", command=self.select_file, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        CTkButton(self.root1, text="License", command=self.licence, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        CTkButton(self.root1, text="About", command=self.about, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        CTkButton(self.root1, text="GitHub", command=self.github, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        CTkButton(self.root1, text="Help", command=self.help_web, corner_radius=32, width=wighf, height=heief).pack(pady=10)
        CTkLabel(self.root1, text="Maximilian Gründinger\nFirst Lego League Team PaRaMeRoS", text_color="Blue").pack(pady=10)
        CTkLabel(self.root1, text="Version 0.2", text_color="Blue").pack(pady=10)

    def licence(self):
        messagebox.showinfo("License", f"Spike Custom System Programming License Agreement\nThis License Agreement (the 'Agreement') is entered into by and between Maximilian Gründinger ('Licensor') and the First Lego League Team known as PaRaMeRoS ('Licensee').\n1. License Grant.\nLicensor hereby grants Licensee a non-exclusive, non-transferable license to use and modify the software program known as Spike Custom System Programming (the 'Program') solely for educational and non-commercial purposes. This license is granted exclusively to the members of the First Lego League Team identified as PaRaMeRoS.\n2. Restrictions.\nLicensee shall not, and shall not permit others to:\na. Use the Program for any purpose other than educational and non-commercial activities within the First Lego League Team.\nb. Allow non-members of the First Lego League Team to use or access the Program.\nc. Commercialize or distribute the Program for financial gain.\nd. Remove or alter any copyright, trademark, or other proprietary notices contained in the Program.\n3. Security.\nLicensor makes no warranties regarding the security of the Program. Licensee acknowledges and agrees that any use of the Program is at their own risk. Licensor shall not be responsible for any security bugs or issues that may arise in connection with the Program.\n4. Term and Termination.\nThis Agreement shall remain in effect until terminated by either party. Licensor reserves the right to terminate this Agreement immediately if Licensee breaches any of its terms. Upon termination, Licensee shall cease all use of the Program and destroy all copies in their possession.\n5. Disclaimer of Warranty.\nTHE PROGRAM IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. LICENSOR DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n6. Limitation of Liability.\nIN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM, EVEN IF LICENSOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n7. Governing Law.\nThis Agreement shall be governed by and construed in accordance with the laws of Germany, Bavaria, Munic.\n8. Entire Agreement.\nThis Agreement constitutes the entire agreement between the parties and supersedes all prior agreements, whether oral or written, with respect to the Program.\nIN WITNESS WHEREOF, the parties hereto have executed this License Agreement as of the effective date.\nLicensor:\nMaximilian Gründinger\nLicensee:\nPaRaMeRoS\nDate: 1.1.2024")
            
    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("Spike Custom System Programming", "*.scsp")])
        if file:
            self.file = file
            compiler.compile(file)
            compiler.main(file)
            
    def credit(self):
        messagebox.showinfo("Credit", "Maximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
        
    def about(self):
        messagebox.showinfo("About", "Spike Custom System Programming\nVersion 0.0.1\nMaximilian Gründinger\nFirst Lego League Team PaRaMeRoS")
    
    def github(self):
        website.open("https://github.com/Iron-witch/Coding_lang_spike_PaRaMeRoS")
        
    def help_web(self):
        messagebox.showinfo("Help", "For help and documentation please visit the GitHub page of the project")
        website.open("https://github.com/Iron-witch/Coding_lang_spike_PaRaMeRoS/wiki")
     
        
class compiler:
    # Functions
    def compile(file):
        click.echo(f"Compiling {file}...")
        if file.endswith(".scsp"):
            with open(file, "r") as f:
                content = f.readlines()
                for line in content:
                    content_compile.append(line)
        else:
            click.echo(f"Error: The file {file} is not a valid file type.", err=True)
            sys.exit(1)

    def get_active_function(line):
        content_line = line
        function, variable = content_line.split("(")
        variable = variable.replace("{","")
        variable = variable.replace("}","")
        variable = variable.replace("\n","")
        return function, variable

    def write_function(function,file,value=False):
        click.echo(f"Writing {function} function...")
        file_name = file.split(".")
        file_name = file_name[0]
        with open(f"{file_name}.py", "a") as f:
            match function:
                case "log":
                    print_out = f"print('{str(value)}')\n"
                    f.write(print_out)
                case "sleep":
                    sleep_out = f"time.sleep({str(value)})\n"
                    f.write(sleep_out)
                case "init":
                    init_out = f"import force_sensor, distance_sensor, motor, motor_pair\nfrom hub import port\nimport time\nfrom app import linegraph as ln\nimport runloop\nfrom math import *\nimport random\n"
                    f.write(init_out)
                case "ai.chose":
                    ai_chose_out = f"ai_chose = '{str(value)}'\n"
                    f.write(ai_chose_out)
                case "ai.init":
                    ai_init_out = f"ai = runloop.AI()\n"
                    f.write(ai_init_out)
                    with open("ai.fll", "r") as r:
                        ai_content = r.readlines()
                        for line in ai_content:
                            f.write(line)
                case "module.init":
                    with open("module.fll", "r") as r:
                        ai_content = r.readlines()
                        for line in ai_content:
                            f.write(line)
                case "motor.init":
                    with open("motor.fll", "r") as r:
                        ai_content = r.readlines()
                        for line in ai_content:
                            f.write(line)
                case "sensor.init":
                    with open("sensor.fll", "r") as r:
                        ai_content = r.readlines()
                        for line in ai_content:
                            f.write(line)
                case "calibration.init":
                    with open("calibration.fll", "r") as r:
                        ai_content = r.readlines()
                        for line in ai_content:
                            f.write(line)
                case "variables.init":
                    with open("variables.fll", "r") as r:
                        ai_content = r.readlines()
                        for line in ai_content:
                            f.write(line)
                case "drive":
                    f.write(f"  await drive({value})\n")
                case "tank":
                    f.write(f"  await tank({value})\n")
                case "obstacle":
                    f.write(f"  await obstacle({value})\n")
                case "ai.sensor":
                    # add the sensor to the ai input
                    f.write(f"ai_sensor.append('{value}\n')")
                case "module":
                    f.write(f"  await module({value})\n")
                case "calibrate":
                    f.write("   await calibrate()\n")
                case "ai.data_save":
                    f.write(f"  write_ai_data('{value}')\n")
                case "ai.data_load":
                    for line in value:
                        f.write(f"ai_data.append({line})\n")
                case "main.init":
                    f.write("runloop.run(main())\n")
                    f.write("async def main():\n")

    def main(file):
        file_name = file.split(".")
        file_name = file_name[0]
        with open(f"{file_name}.py", "w") as f:
            f.write("")
        for line in content_compile:
            # Komentare herausfiltern
            function, value = get_active_function(line)
            write_function(function, file, value)

if __name__ == "__main__":
    gui()
