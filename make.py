from gi.repository import Gtk, Gdk
import themer


class SaveDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Gnome Themed", parent, 0,
                            (Gtk.STOCK_YES, Gtk.ResponseType.YES,
                             Gtk.STOCK_NO, Gtk.ResponseType.NO))

        box = self.get_content_area()
        self.text = Gtk.Label("  Save changes to config file?  ")

        box.add(self.text)
        self.show_all()


class SettingError(Gtk.Dialog):
    def __init__(self, parent, setting, method):
        Gtk.Dialog.__init__(self, "Error", parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_border_width(10)
        box = self.get_content_area()
        self.error = Gtk.Label()
        self.error.set_markup("\n\tSorry, <i>{}</i>  \n"
                              "Does not exist for <i>{}</i>\n".format(setting, method))
        box.add(self.error)
        self.show_all()


class GenericError(Gtk.Dialog):
    def __init__(self, parent, error_text):
        Gtk.Dialog.__init__(self, "Error", parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        box = self.get_content_area()
        self.error = Gtk.Label("\n{}\n".format(error_text))
        self.set_border_width(10)
        box.add(self.error)
        self.show_all()


class CustomButton(Gtk.Button):
    def __init__(self, parent, name, icon_image=None):
        super(CustomButton, self).__init__("  {} Settings".format(name))  # Set base class

        # checking for icon if one is set
        if icon_image is not None:
            self.set_image(icon_image)
            self.set_image_position(Gtk.PositionType.LEFT)

        # self.set_relief(Gtk.ReliefStyle.NONE)
        self.connect("clicked", self.on_button_clicked, parent, name)

    def on_button_clicked(self, widget, parent, settings_name):
        """
        creates setting dialog to present settings to user
        :param widget: widget connection
        :param parent: program parent
        :param settings_name: str # string identifying the settings for the dialog
        :return: None
        """
        if parent.config is None:
            parent.get_file()
            self.on_button_clicked(widget, parent, settings_name)

        elif parent.config == "":
            parent.config = None  # set back to None so that user can be prompted for file again
        else:
            settings_dialog = SettingsDialog(parent, settings_name)
            response = settings_dialog.run()

            if response == Gtk.ResponseType.OK:
                settings_dialog.destroy()
            settings_dialog.destroy()


class Image(Gtk.Image):
    def __init__(self, path):
        super(Image, self).__init__()
        self.set_from_file(path)


class Menu(Gtk.MenuItem):
    def __init__(self, label, menu_bar):
        self.menu_item = Gtk.MenuItem(label=label)
        menu_bar.append(self.menu_item)
        self.menu = Gtk.Menu()

    def add_item(self, label, connection):
        """
        adds item to menu and set label and connection
        :param label: str # name of the item
        :param connection: def # function to connect item to
        :return: None
        """
        self.menu_item.set_submenu(self.menu)
        menu_item = Gtk.MenuItem(label=label)
        menu_item.connect("activate", connection)
        self.menu.append(menu_item)


class FileDialog(Gtk.FileChooserDialog):
    def __init__(self, parent):
        super(FileDialog, self).__init__("Please choose a file", parent, Gtk.FileChooserAction.OPEN,
                                         (Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
                                          Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        if not themer.DEBUG:  # if not in debug mode
                self.set_current_folder("/usr/share/themes/")


class AboutDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "About", parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        box = self.get_content_area()
        scroll_box = TextBox("README.md")
        scroll_box.set_min_content_height(500)  # setting custom height
        box.add(scroll_box)
        self.show_all()


class BackupDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Restore Backup", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        box = self.get_content_area()
        self.label = Gtk.Label("\nA '.DEFAULT' file was created before your first edit.\n"
                               "You can use it to restore to default settings.\n")
        self.backup_btn = Gtk.Button("Select Backup")
        self.backup_btn.connect("clicked", self.on_button_clicked)
        self.set_border_width(10)
        self.backup_path = None

        box.add(self.label)
        box.add(self.backup_btn)
        self.show_all()

    def on_button_clicked(self, widget):
        """
        prompts user with file chooser dialog when select
        backup button is selected.
        :param widget: function to connect to
        :return: None
        """
        choose_file = FileDialog(self)
        file_response = choose_file.run()
        if file_response == Gtk.ResponseType.OK:
            self.backup_path = choose_file.get_filename()
            self.destroy()
        choose_file.destroy()

    def get_path(self):
        """
        returns path of backup file
        :return: str # backup file path
        """
        return self.backup_path


class EntryDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Custom Settings", parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                             Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        box = self.get_content_area()
        self.set_border_width(10)
        self.table = Gtk.Table(4, 4)
        self.methods_entry = Gtk.Entry()
        self.settings_entry = Gtk.Entry()
        self.label = Gtk.Label("NOTE: Seperate each entry with ';' "
                               "For methods do not include '{' "
                               "And for settings do not include ':'\n")
        self.method_text = Gtk.Label('Methods')
        self.method_text.set_justify(Gtk.Justification.LEFT)
        self.setting_text = Gtk.Label('Settings')
        self.setting_text.set_justify(Gtk.Justification.LEFT)
        self.table.attach(self.label, 1, 4, 1, 2)
        self.table.attach(self.method_text, 0, 1, 2, 3, xpadding=5)
        self.table.attach(self.methods_entry, 1, 4, 2, 3)
        self.table.attach(self.setting_text, 0, 1, 3, 4, xpadding=5)
        self.table.attach(self.settings_entry, 1, 4, 3, 4)
        box.add(self.table)
        self.show_all()


class SettingsDialog(Gtk.Dialog):
    def __init__(self, parent, settings_name):
        Gtk.Dialog.__init__(self, "{} Settings".format(settings_name), parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        box = self.get_content_area()
        self.table = Gtk.Table(8, 5)

        # setting up scroll window
        scroll_box = Gtk.ScrolledWindow()
        scroll_box.set_min_content_height(600)
        scroll_box.set_min_content_width(700)

        self.set_border_width(5)
        self.panel = themer.get(settings_name)  # getting settings

        # for every method a settings table is made
        for i, method in enumerate(sorted(self.panel)):
            self.table.attach(SettingsTable(method, self.panel[method], parent), 0, 5, i, i+1)

        scroll_box.add(self.table)
        box.add(scroll_box)
        self.show_all()


class SettingsTable(Gtk.Table):
    def __init__(self, method, settings, main_parent):
        super(SettingsTable, self).__init__(4, 3, True)

        self._method = method
        self.main_parent = main_parent
        self.setting_lst = []
        self.settings_dict = {}
        self.color_btn_dict = {}
        self._hex_color = None

        # Method label set in bold text
        self.method_name = Gtk.Label()
        self.method_name.set_markup("<b>{}</b>".format(method))
        self.attach(self.method_name, 0, 1, 1, 2)

        # Setts up color button for the method
        self.color_btn = Gtk.ColorButton()
        self.color_btn.connect("color-set", self.commit_setting, main_parent)

        # makes check boxes for each setting
        if isinstance(settings, str):  # if setting is just one string it is just added
            setting = settings
            self.settings_dict[setting] = Gtk.CheckButton(setting)
            self.settings_dict[setting].connect("clicked", self.on_setting_clicked, setting)
            self.attach(self.settings_dict[setting], 0, 1, 2, 3)
            self.attach(self.color_btn, 0, 1, 3, 4)
        else:
            for i, setting in enumerate(settings):
                self.settings_dict[setting] = Gtk.CheckButton(setting)
                self.settings_dict[setting].connect("clicked", self.on_setting_clicked, setting)
                if i <= 2:  # prevents more than 3 settings per line
                    self.attach(self.settings_dict[setting], i, i+1, 2, 3)
                    # attaches color button to line below last setting
                    self.attach(self.color_btn, 0, 1, 3, 4) if i+1 == len(settings) else None
                else:
                    self.attach(self.settings_dict[setting], i-3, i-2, 3, 4)
                    self.attach(self.color_btn, 0, 1, 4, 5) if i+1 == len(settings) else None

    def on_setting_clicked(self, widget, setting):
        """
        adds setting to the list of settings to be changed,
        if the setting is already in the list it is removed
        :param widget: widget connection
        :param setting: setting to add or remove
        :return: None
        """
        no_color = Gdk.RGBA(red=0.000000, green=0.000000, blue=0.000000, alpha=1.000000)

        if setting in self.setting_lst:
            self.setting_lst.remove(setting)
            if self.color_btn.get_rgba() == no_color:
                pass
            else:
                self.main_parent.config.undo_setting(self._method, setting)
        else:
            self.setting_lst.append(setting)
            if self.color_btn.get_rgba() == no_color:
                pass
            else:
                self.commit_setting(None, self.main_parent)

        print("Selected: {}".format(self.setting_lst)) if themer.DEBUG else None

    def commit_setting(self, widget, parent):
        """
        color button connection that sets gets the selected value
        and calls the change setting method to commit changes.
        :param widget: widget connection
        :param parent: parent of dialog, needed to call config.change_setting
        :return: None
        """
        color = themer.HexColor(self.color_btn.get_rgba())
        hex_color = color.convert()  # converts color to hex format
        for setting in self.setting_lst:
            if parent.config.test_method(self._method, setting):  # testing if method exists
                parent.config.change_setting(self._method, setting, hex_color)
            else:
                error = SettingError(self, setting, self._method)
                error.run()
                error.destroy()


class TextBox(Gtk.ScrolledWindow):
    def __init__(self, text_file):
        super(TextBox, self).__init__()
        self.text = themer.OpenText(text_file)
        self.text_label = Gtk.Label(self.text.get_text())
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add(self.text_label)


class HelpWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Help")
        self.connect("destroy", lambda x: self.hide)
        self.set_default_size(600, 600)  # set custom window size
        self.set_border_width(20)
        self.add(TextBox("help"))
        self.show_all()

if __name__ == '__main__':
    pass

