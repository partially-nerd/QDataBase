from window import Application, Gtk, Window, Gdk
from widgets import Button, LabeledEntry, Label, GLib, Entry
from glob import glob
from re import sub, MULTILINE
from sys import path
from os import unlink, system

path.append("./")
from handler import db
from sys import argv


class AppWindow(Window):
    def __init__(self, application, geometry: str = "800x600", **kwargs) -> None:
        super().__init__(application, geometry, **kwargs)
        self.parser = db.Parser()
        self.paused = False
        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Select a File")
        self.evk = Gtk.EventControllerKey.new()
        self.dir = argv[1]

        self.root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.row_1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.status_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.left_bar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.explorer_wrapper = Gtk.ScrolledWindow()
        self.workspace_buffer = Gtk.TextBuffer()
        self.workspace_wrapper = Gtk.ScrolledWindow()
        self.workspace = Gtk.TextView(buffer=self.workspace_buffer)
        self.parsed_wrapper = Gtk.ScrolledWindow()
        self.parsed_buffer = Gtk.TextBuffer()
        self.parsed = Gtk.TextView(buffer=self.parsed_buffer)

        self.close_btn = Button("×", "close-button")
        self.add_file_btn = Button("+", "left-bar-btn")
        self.backup_btn = Button("📋", "left-bar-btn")
        self.finalize_btn = Button("💾", "left-bar-btn")
        self.delete_btn = Button("⌫", "left-bar-btn")

        self.status_bar_file_label = Label(class_="status-bar-item")
        self.search_entry = LabeledEntry("Locate: ", "eg: sections.rose.classTeacher", "status-bar-entries")
        self.key_entry = LabeledEntry("Key:", "eg: sections.rose.classTeacher", "status-bar-entries")
        self.value_entry = LabeledEntry("Value:", "eg: Deepak Khanal", "status-bar-entries")

        self.status_bar.set_size_request(-1, 40)
        self.left_bar.set_size_request(40, -1)

        self.row_1.set_vexpand(True)
        self.workspace.set_hexpand(True)
        self.parsed.set_hexpand(True)
        self.explorer_wrapper.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.row_1.set_css_classes(["first-row"])
        self.left_bar.set_css_classes(["left-bar"])
        self.workspace.set_css_classes(["workspace"])
        self.parsed.set_css_classes(["parsed"])
        self.status_bar.set_css_classes(["status-bar"])

        self.parsed.set_editable(False)
        self.search_entry.entry.connect("activate", self.search_fn)
        self.key_entry.entry.connect("activate", self.get_value)
        self.value_entry.entry.connect("activate", self.set_value)
        self.add_file_btn.connect("clicked", self.add_file)
        self.backup_btn.connect("clicked", self.backup)
        self.finalize_btn.connect("clicked", self.finalize)
        self.delete_btn.connect("clicked", self.delete)
        self.close_btn.connect("clicked", self.close)

        self.fill_explorer()
        self.pack()

    def search_fn(self, entry):
        self.paused = True
        try:
            value = eval(f"self.evaluated.{entry.get_text()}")
            parsed = self.parsed_buffer.get_text(
                        self.parsed_buffer.get_start_iter(),
                        self.parsed_buffer.get_end_iter(),
                        True,
                    )
            parsed = sub('(.*\"'+entry.get_text().split(".")[-1]+'\"\: "'+value+'".*)', r'<span color="red">\1</span>', parsed, MULTILINE)
            self.parsed_buffer.set_text("")
            self.parsed_buffer.insert_markup(self.parsed_buffer.get_end_iter(), parsed, -1)
        except: pass

    def get_value(self, entry):
        key = entry.get_text()
        try:
            value = eval(f"self.evaluated.{key}")
            self.value_entry.entry.set_text(value)
        except: pass

    def set_value(self, entry):
        key = self.key_entry.entry.get_text()
        value = entry.get_text()
        try: exec(f'self.evaluated.{key} = "{value}"')
        except: pass
        self.workspace_buffer.set_text(self.parser.reConvert(self.evaluated))

    def close(self, widget):
        exit()

    def delete(self, widget):
        unlink(self.active_file)
        self.parsed_buffer.set_text("")
        self.fill_explorer()

    def backup(self, widget):
        path = self.active_file.replace(" ", r"\ ")
        system(f"cp {path} {path}.copy")
        self.fill_explorer()

    def add_file(self, widget):
        self.open_dialog.save(self, None, self.dialog_open_callback)

    def finalize(self, widget):
        self.parser.finalize(self.active_file, self.evaluated)

    def dialog_open_callback(self, dialog, result):
        try:
            path = dialog.save_finish(result).get_path().replace(" ", r"\ ")
            if path is not None:
                system(f"touch {path}")
                self.fill_explorer()
        except GLib.Error as error:
            print(f"Error opening folder: {error.message}")

    def on_key_pressed(self, event, keyval, keycode, state):
        if self.paused:
            self.paused = False
            return
        try:
            parsed = self.parser.parse(
                self.workspace_buffer.get_text(
                    self.workspace_buffer.get_start_iter(),
                    self.workspace_buffer.get_end_iter(),
                    True,
                )
            )
            self.evaluated = self.parser.evaluate(parsed)
            parsed = self.highlight(parsed)
            self.parsed_buffer.set_text("")
            self.parsed_buffer.insert_markup(self.parsed_buffer.get_end_iter(), parsed, -1)
        except Exception as E:
            pass

    def highlight(self, parsed: str):
        parsed = sub(
            r'"([a-zA-Z\s0-9]+)":', r'<span color="green">"\1"</span>:', parsed
        )
        parsed = sub(r':\s"([0-9]+)"', r': <span color="blue">\1</span>', parsed)
        parsed = sub(
            r':\s"([a-zA-Z\d\s]+)"', r': <span color="orange">"\1"</span>', parsed
        )
        return parsed

    def on_file_opened(self, widget):
        self.status_bar_file_label.set_label(f"Active File: {widget.path}")
        read = self.parser.read(widget.path)
        self.workspace_buffer.set_text(read)
        self.active_file = widget.path
        parsed = self.parser.parse(read)
        self.evaluated = self.parser.evaluate(parsed)
        parsed = self.highlight(parsed)
        self.parsed_buffer.set_text("")
        self.parsed_buffer.insert_markup(self.parsed_buffer.get_end_iter(), parsed, -1)

    def fill_explorer(self):
        self.explorer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.explorer.set_size_request(250, -1)
        self.explorer.set_css_classes(["explorer"])
        self.explorer_wrapper.set_child(self.explorer)
        self.dir_label = Label(self.dir[:15] + "...", "explorer-heading")
        for file in glob(self.dir + "/*", recursive=True):
            item = Button(file.removeprefix(self.dir + "/"), "explorer-item")
            item.path = file
            item.connect("clicked", self.on_file_opened)
            self.explorer.append(item)
        self.explorer.prepend(self.dir_label)

    def pack(self):
        self.set_child(self.root)
        self.root.append(self.row_1)
        self.root.append(self.status_bar)
        self.row_1.append(self.left_bar)
        self.row_1.append(self.explorer_wrapper)
        self.row_1.append(self.workspace_wrapper)
        self.row_1.append(self.parsed_wrapper)
        self.explorer_wrapper.set_child(self.explorer)
        self.workspace_wrapper.set_child(self.workspace)
        self.parsed_wrapper.set_child(self.parsed)

        self.left_bar.append(self.close_btn)
        self.left_bar.append(self.add_file_btn)
        self.left_bar.append(self.finalize_btn)
        self.left_bar.append(self.delete_btn)
        self.left_bar.append(self.backup_btn)

        self.status_bar.append(self.status_bar_file_label)
        self.status_bar.append(self.search_entry)
        self.status_bar.append(self.key_entry)
        self.status_bar.append(self.value_entry)

        self.evk.connect("key-released", self.on_key_pressed)
        self.add_controller(self.evk)
        self.maximize()
        self.set_decorated(False)


window = Application(AppWindow, title="Workspace", stylesheet="gui/workspace.css")
window.run()
