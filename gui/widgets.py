from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, GLib


class Button(Gtk.Button):
    def __init__(self, label: str = "", class_: str = "button"):
        super().__init__()
        self.set_label(label)
        self.set_css_classes([class_])


class Label(Gtk.Label):
    def __init__(self, label: str = "", class_: str = "label"):
        super().__init__(label=label)
        self.set_css_classes([class_])

class Entry(Gtk.Entry):
    def __init__(self, placeholder: str = "", class_: str = "entry"):
        super().__init__()
        self.set_placeholder_text(placeholder)
        self.set_css_classes([class_])


class LabeledEntry(Gtk.Box):
    def __init__(self, label: str = "", placeholder: str = "", class_: str = "entry"):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_css_classes(["labeled-"+class_])
        self.label = Label(label=label, class_=class_+"-label")
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text(placeholder)
        self.entry.set_css_classes([class_])
        self.append(self.label)
        self.append(self.entry)
