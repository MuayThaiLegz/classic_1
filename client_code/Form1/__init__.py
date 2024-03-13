# form1.py

# form1.py

from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.users

class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.setup_sidebar()

    def setup_sidebar(self):
        self.sidebar = ColumnPanel(background="#2E2E2E")
        components = [
            TextBox(placeholder='MongoDB connection string', foreground="#FFFFFF", background="#424242", tag='ip_address_box'),
            Button(text="Connect", role="primary-color", background="#4CAF50", tag='connect_button'),
            DropDown(items=[("Choose where to store the data:", ""), ("New Database", "new"), ("Existing Database", "existing")], placeholder="Select Option", background="#424242", foreground="#FFFFFF", tag='db_option_dropdown'),
            TextBox(placeholder='Enter New Database Name', visible=False, foreground="#FFFFFF", background="#424242", tag='new_db_name_box'),
            DropDown(items=[], placeholder="Select Existing Database", visible=False, background="#424242", foreground="#FFFFFF", tag='existing_db_dropdown'),
            TextBox(placeholder='Confirm Collection Name', visible=False, foreground="#FFFFFF", background="#424242", tag='collection_name_box'),
            FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], enabled=False, background="#424242", foreground="#FFFFFF", tag='file_loader'),
            Button(text="Process File", enabled=False, role="secondary-color", background="#2196F3", visible=False, tag='process_file_button'),
            Label(text="", foreground="#F44336", tag='feedback_label')
        ]
        for component in components:
            self.sidebar.add_component(component)
            if hasattr(component, 'tag'):
                setattr(self, component.name, component)

        self.connect_button.set_event_handler('click', self.on_connect_clicked)
        self.db_option_dropdown.set_event_handler('change', self.on_db_option_changed)
        self.file_loader.set_event_handler('change', self.on_file_loader_changed)
        self.process_file_button.set_event_handler('click', self.on_process_file_clicked)

    def on_connect_clicked(self, **event_args):
        connString = self.ip_address_box.text
        success, message = anvil.server.call('connect_to_mongodb', connString)
        self.display_feedback(success, message)
        if success:
            # If connection successful, enable file loader and potentially update datasets if existing DB is selected
            self.file_loader.enabled = True
            self.db_option_dropdown.enabled = True

    def on_db_option_changed(self, **event_args):
        # Toggle visibility based on selection
        option = self.db_option_dropdown.selected_value
        if option == "new":
            self.new_db_name_box.visible = True
            self.existing_db_dropdown.visible = False
            self.collection_name_box.visible = True
        elif option == "existing":
            self.new_db_name_box.visible = False
            self.existing_db_dropdown.visible = True
            self.collection_name_box.visible = True
            # Assuming 'update_existing_dbs_dropdown' fetches databases and updates the dropdown
            self.update_existing_dbs_dropdown()
        else:
            self.new_db_name_box.visible = False
            self.existing_db_dropdown.visible = False
            self.collection_name_box.visible = False
        self.process_file_button.visible = option in ["new", "existing"]

    def on_file_loader_changed(self, **event_args):
        self.process_file_button.enabled = bool(self.file_loader.file)

    def on_process_file_clicked(self, **event_args):
        connString = self.ip_address_box.text
        if self.file_loader.file:
            db_option = self.db_option_dropdown.selected_value
            db_name = self.new_db_name_box.text if db_option == "new" else self.existing_db_dropdown.selected_value
            collection_name = self.collection_name_box.text
            anvil.server.call('initiate_file_processing', self.file_loader.file, db_name, collection_name, connString)
            
        else:
          self.display_feedback(False, "Please select a file to upload.")

    def display_feedback(self, success, message):
        self.feedback_label.text = message
        self.feedback_label.foreground = "#4CAF50" if success else "#F44336"

    def update_existing_dbs_dropdown(self):
        # This function would call a server function to fetch existing databases and update 'self.existing_db_dropdown'
        # Placeholder for fetching and updating logic
        pass
