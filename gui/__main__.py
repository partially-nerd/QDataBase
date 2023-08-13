from window import Application, Gtk, Window
from widgets import Button, LabeledEntry, Label, GLib
from commons import verify_password
from os import system


class AppWindow(Window):
    def __init__(self, application, geometry: str = "350x1", **kwargs) -> None:
        super().__init__(application, geometry, **kwargs)

        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Select a File")

        self.root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.titlebar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.title_label = Label(self.title, "title-label")
        self.close_btn = Button("×", "close-button")
        self.submit_button = Button("Login", "submit-button")
        self.username_entry = LabeledEntry("Username: ", "Pablo")
        self.password_entry = LabeledEntry("Password: ", "*******")

        self.titlebar.set_css_classes(["titlebar"])
        self.close_btn.connect("clicked", self.close)
        self.submit_button.connect("clicked", self.submit)
        self.pack()

    def close(self, widget):
        exit()

    def submit(self, widget):
        if verify_password(
            self.username_entry.entry.get_text(), self.password_entry.entry.get_text()
        ):
            self.open_dialog.select_folder(self, None, self.dialog_open_callback)

    def dialog_open_callback(self, dialog, result):
        try:
            dir = dialog.select_folder_finish(result).get_path()
            if dir is not None:
                system(f"echo {dir}")
                system(f"python3 gui/workspace.py {dir}")
        except GLib.Error as error:
            print(f"Error opening folder: {error.message}")

    def pack(self):
        self.set_child(self.root)
        self.set_titlebar(self.titlebar)
        self.titlebar.append(self.close_btn)
        self.titlebar.append(self.title_label)
        self.root.append(self.username_entry)
        self.root.append(self.password_entry)
        self.root.append(self.submit_button)


window = Application(AppWindow, title="QDataBase Login", stylesheet="gui/style.css")
window.run()
