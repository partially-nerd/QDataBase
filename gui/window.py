from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")
from gi.repository import Gtk, Gdk, Adw
from sys import exit as sys_exit


class Window(Gtk.ApplicationWindow):
    def __init__(self, application, geometry: str = "350x500", **kwargs) -> None:
        super().__init__(application=application)

        self.display = Gdk.Display.get_default()
        self.css_provider = Gtk.CssProvider()
        self.set_css_classes(["main-window"])
        self.geometry = geometry.split("x")
        self.set_kwargs(**kwargs)

    def set_kwargs(self, **kwargs):
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

    def setup(self):
        if self.stylesheet is not None:
            self.css_provider.load_from_path(self.stylesheet)
            Gtk.StyleContext.add_provider_for_display(
                self.display, self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        self.set_title(self.title if self.title is not None else "")
        self.connect("destroy", exit)
        self.set_default_size(int(self.geometry[0]), int(self.geometry[1]))


class Application(Adw.Application):
    def __init__(self, window, **kwargs):
        self.kwargs = kwargs
        self.Window = window
        super().__init__()
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.window = self.Window(application=app, **self.kwargs)
        self.window.setup()
        self.window.present()
