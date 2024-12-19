import tkinter as tk
from tkinter import filedialog

def on_ctrl_u(event):
    print("Ctrl+u pressed: upe function triggered!")

def on_ctrl_i(event):
    print("Ctrl+i pressed: ipe function triggered!")
    root.destroy()

class NavigationPane(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgray")
        self.controller = controller

        self.title_label = tk.Label(self, text="", bg="lightgray", font=("Arial", 14))
        self.title_label.pack(side="right", padx=10)

        back_button = tk.Button(self, text="Back", command=self.controller.go_back)
        back_button.pack(side="left", padx=10)

    def update_title(self, title):
        self.title_label.config(text=title)

class View(tk.Frame):
    def __init__(self, parent, controller, bg_color):
        super().__init__(parent, bg=bg_color)
        self.controller = controller
        
# AlertView for handling errors
class AlertView(tk.Toplevel):
    def __init__(self, message):
        super().__init__()
        self.title("Alert")
        label = tk.Label(self, text=message, foreground="red")
        label.pack(padx=20, pady=20)
        close_button = tk.Button(self, text="Close", command=self.destroy)
        close_button.pack(pady=10)

class Modal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.parent = parent
        self.title("Modal")

class WelcomeView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, bg_color="lightblue")
        label = tk.Label(self, text="Welcome to the App!", bg="lightblue")
        label.pack(pady=20)
        btn_menu = tk.Button(self, text="Go to Menu", command=lambda: controller.show_view("MenuView"))
        btn_menu.pack()

class MenuView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, bg_color="lightgreen")
        label = tk.Label(self, text="Menu", bg="lightgreen")
        label.pack(pady=20)
        btn_file_input = tk.Button(self, text="File Input", command=lambda: controller.show_view("FileInputView"))
        btn_file_input.pack()
        btn_data_output = tk.Button(self, text="Data Output", command=lambda: controller.show_view("DataOutputView"))
        btn_data_output.pack()

class FileInputView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, bg_color="lightyellow")
        label = tk.Label(self, text="File Input", bg="lightyellow")
        label.pack(pady=20)
        btn_browse = tk.Button(self, text="Browse File", command=self.open_file_browser)
        btn_browse.pack()
        btn_data_output = tk.Button(self, text="Data Output", command=lambda: controller.show_view("DataOutputView"))
        btn_data_output.pack()

    def open_file_browser(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            tk.Label(self, text=f"Selected File: {file_path}", bg="lightyellow").pack(pady=10)
        else:
            tk.Label(self, text="No file selected.", bg="lightyellow").pack(pady=10)

class DataOutputView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, bg_color="lightblue")
        label = tk.Label(self, text="Data Output", bg="grey")
        label.pack(pady=20)
        btn_data_output = tk.Button(self, text="Edit/Update", command=self.open_edit_update_modal)
        btn_data_output.pack()
        btn_data_output = tk.Button(self, text="Data Acrobatics", command=lambda: controller.show_view("StatVisView"))
        btn_data_output.pack()

    def open_edit_update_modal(self):
        EditUpdateView(self)


class EditUpdateView(Modal):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Edit/Update")
        label.pack(pady=20)
        btn_save = tk.Button(self, text="Save", command=self.destroy)
        btn_save.pack()
        btn_close = tk.Button(self, text="Close", command=self.destroy)
        btn_close.pack()

"""     def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            tk.Label(self, text=f"Selected: {file_path}").pack(pady=10) """



        

class StatVisView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, bg_color="orange")
        label = tk.Label(self, text="Statistics/Visualisations", bg="pink")
        label.pack(pady=20)
        btn_data_output = tk.Button(self, text="See Acrobatics", command=self.open_display_Output_modal)
        btn_data_output.pack()

    def open_display_Output_modal(self):
        DisplayDataOutputsView(self)

class DisplayDataOutputsView(Modal):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Display Data Outputs")
        label.pack(pady=20)
        btn_save = tk.Button(self, text="Save", command=self.destroy)
        btn_save.pack()
        btn_close = tk.Button(self, text="Close", command=self.destroy)
        btn_close.pack()




# Shapes superclass and subclasses
class Shape:
    def draw(self, canvas):
        raise NotImplementedError("Subclasses must implement draw method")

class Circle(Shape):
    def draw(self, canvas):
        canvas.create_oval(50, 50, 150, 150, fill="blue", outline="black")

class Rectangle(Shape):
    def draw(self, canvas):
        canvas.create_rectangle(50, 50, 150, 100, fill="green", outline="black")

class BaseView:
    def __init__(self, root):
        self.root = root
        self.view_stack = []  # Stack to maintain navigation history as view names
        self.current_view = None

        self.navigation_pane = NavigationPane(root, self)
        self.navigation_pane.pack(side="top", fill="x")

        self.container = tk.Frame(root, bg="white")
        self.container.pack(expand=True, fill="both")

        self.views = {
            "WelcomeView": WelcomeView,
            "MenuView": MenuView,
            "FileInputView": FileInputView,
            "DataOutputView": DataOutputView,
            "StatVisView": StatVisView
        }
        print(" triggered!")
        self.show_view("WelcomeView")


    def add_view(self, view_name):
        if view_name in self.views:
            print()
        else:
            self.views.update({
                "{view_name}": view_name
            })


    def show_view(self, view_name, push_to_stack=True):
        if self.current_view:
            if push_to_stack:
                # Push the name of the current view onto the stack
                self.view_stack.append(type(self.current_view).__name__)
            self.current_view.destroy()
        view_class = self.views.get(view_name)
        if view_class:
            self.current_view = view_class(self.container, self)
            self.current_view.pack(expand=True, fill="both")
            self.navigation_pane.update_title(view_name)

    def go_back(self):
        if self.view_stack:
            # Pop the name of the last view from the stack and show it
            last_view_name = self.view_stack.pop()
            self.show_view(last_view_name, push_to_stack=False)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("App Structure Example with Navigation Pane")
    root.geometry("600x400")
    root.bind("<Control-u>", on_ctrl_u)  # Triggered by Ctrl+S
    root.bind("<Control-i>", on_ctrl_i)  # Triggered by Ctrl+Q
    app = BaseView(root)
    root.mainloop()
