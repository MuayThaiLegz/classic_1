from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Stylish and organized sidebar setup
        self.setup_sidebar()

        # Improved error handling and user feedback
        self.warning_label = Label(text="")
        self.left_nav.add_component(self.warning_label)

    def setup_sidebar(self):
        """Setup sidebar elements with enhanced UX design."""
        self.left_nav = ColumnPanel()
        self.add_component(self.left_nav, slot="sidebar")

        self.ip_address_box = TextBox(placeholder='Enter MongoDB connection string here',
                                      tooltip="Your MongoDB connection string")
        self.left_nav.add_component(self.ip_address_box)

        self.connect_button = Button(text="Connect", role="primary-color")
        self.left_nav.add_component(self.connect_button)
        self.connect_button.set_event_handler('click', self.connect_button_click)

        self.left_nav.add_component(Spacer(height=10))  # Adds some space for visual separation
        
        # Dynamic dropdown for menu selection
        self.menu_dropdown = DropDown(items=[(item, item) for item in ["Analyze Data", "Find Anomalies", "Embedded Database", "Multi Sense"]],
                                       enabled=False, placeholder="Select Action")
        self.left_nav.add_component(self.menu_dropdown)
        self.menu_dropdown.set_event_handler('change', self.menu_item_selected)

        self.left_nav.add_component(Spacer(height=10))  # Adds some space before the file loader
        
        self.setup_file_loader()

    def setup_file_loader(self):
        """Setup file loader with conditional activation."""
        self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"],
                                      enabled=False, tooltip="Upload data file")
        self.left_nav.add_component(self.file_loader)

        self.process_file_button = Button(text="Process File", enabled=False, role="secondary-color")
        self.left_nav.add_component(self.process_file_button)
        self.process_file_button.set_event_handler('click', self.process_file_click)
        
        self.file_loader.set_event_handler('change', self.file_loader_change)

    def connect_button_click(self, **event_args):
        """Manage connection logic with enhanced feedback."""
        connString = self.ip_address_box.text
        try:
            success = anvil.server.call('connect_to_mongodb', connString)
            if success:
                self.menu_dropdown.enabled = True
                self.file_loader.enabled = True
                self.show_success("Connected successfully.")
            else:
                self.show_error("Connection failed.")
        except Exception as e:
            self.show_error(f"Error: {e}")

    def show_success(self, message):
        """Utility to display success messages."""
        self.warning_label.text = message
        self.warning_label.foreground = "green"
        self.warning_label.visible = True

    def show_error(self, message):
        """Utility to display error messages."""
        self.warning_label.text = message
        self.warning_label.foreground = "red"
        self.warning_label.visible = True

    def file_loader_change(self, **event_args):
        """Enable the process button when a file is selected."""
        self.process_file_button.enabled = bool(self.file_loader.file)

    def process_file_click(self, **event_args):
        """Handle file processing and load it to the server."""
        if self.file_loader.file:
            try:
                result = anvil.server.call('process_and_load_file', self.file_loader.file)
                if result:
                    alert("File processed successfully.")
                else:
                    alert("Failed to process file.")
            except Exception as e:
                alert(f"Error processing file: {str(e)}")

    def menu_item_selected(self, sender, **event_args):
        """Placeholder for handling menu item selection."""
        selected_item = self.menu_dropdown.selected_value
        print(f"Menu item selected: {selected_item}")
        # Implement actions based on the selected menu item
