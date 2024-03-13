# Form1.py

from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.initialize_sidebar()
        self.initialize_feedback_label()

    def initialize_sidebar(self):
        self.sidebar_setup = ColumnPanel(background="#2E2E2E")  # Darker background for sidebar
        self.add_component(self.sidebar_setup, slot="sidebar")
        
        self.configure_connection_controls()
        self.configure_action_controls()
        self.configure_file_controls()

    def configure_connection_controls(self):
        self.ip_address_box = TextBox(placeholder='Enter MongoDB connection string here', tooltip="Your MongoDB connection string", foreground="#FFFFFF", background="#424242")
        self.sidebar_setup.add_component(self.ip_address_box)

        self.connect_button = Button(text="Connect", role="primary-color", background="#4CAF50")  # Use a green color for the connect button
        self.sidebar_setup.add_component(self.connect_button)
        self.connect_button.set_event_handler('click', self.on_connect_clicked)

        self.sidebar_setup.add_component(Spacer(height=10))

    def configure_action_controls(self):
        self.menu_dropdown = DropDown(items=[("Select Action", None)] + [(item, item) for item in ["Analyze Data", "Find Anomalies", "Embedded Database", "Multi Sense"]], enabled=False, placeholder="Select Action", foreground="#FFFFFF", background="#424242")
        self.sidebar_setup.add_component(self.menu_dropdown)
        self.menu_dropdown.set_event_handler('change', self.on_menu_item_selected)

        self.sidebar_setup.add_component(Spacer(height=10))

    def configure_file_controls(self):
        self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], enabled=False, tooltip="Upload data file", foreground="#FFFFFF", background="#424242")
        self.sidebar_setup.add_component(self.file_loader)

        self.process_file_button = Button(text="Process File", enabled=False, role="secondary-color", background="#2196F3")  # Use a blue color for the process file button
        self.sidebar_setup.add_component(self.process_file_button)
        self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
        
        self.file_loader.set_event_handler('change', self.on_file_loader_changed)

    def initialize_feedback_label(self):
        self.warning_label = Label(text="", foreground="#F44336")  # Initially set to red for errors, will be green for success messages
        self.sidebar_setup.add_component(self.warning_label)

    def on_connect_clicked(self, **event_args):
        connString = self.ip_address_box.text
        success, message, _ = anvil.server.call('connect_to_mongodb', connString)
        self.display_feedback(success, message)
        if success:
            self.menu_dropdown.enabled = True
            self.file_loader.enabled = True

    def on_file_loader_changed(self, **event_args):
        self.process_file_button.enabled = bool(self.file_loader.file)

    def on_process_file_clicked(self, **event_args):
        if self.file_loader.file:
            success, message = anvil.server.call('process_and_load_file', self.file_loader.file, self.ip_address_box.text)
            self.display_feedback(success, message)

    def display_feedback(self, success, message):
        self.warning_label.text = message
        self.warning_label.foreground = "#4CAF50" if success else "#F44336"
        self.warning_label.visible = True

    def on_menu_item_selected(self, sender, **event_args):
        selected_item = sender.selected_value
        if selected_item:
            # Implement actions based on the selected menu item
            pass
