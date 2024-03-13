from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from anvil.users import login_with_form, logout, get_user


class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Authenticate user at startup
        if get_user() is None:
            login_with_form()
        
        # Initialize UI components after successful login
        self.initialize_ui_components()

    def initialize_ui_components(self):
        """Initialize UI components after user authentication."""
        self.setup_sidebar()
        self.setup_feedback_label()

    def setup_sidebar(self):
        """Set up sidebar components."""
        self.sidebar = ColumnPanel(background="#2E2E2E")
        self.add_component(self.sidebar, slot="sidebar")
        
        # Connection controls
        self.setup_connection_controls()
        
        # Action controls (Dropdown menu for datasets will be enabled after successful connection)
        self.setup_action_controls()
        print('setup_file_controls')
        # File controls
        self.setup_file_controls()

    def setup_connection_controls(self):
        """Setup MongoDB connection controls."""
        self.ip_address_box = TextBox(placeholder='Enter MongoDB connection string here', tooltip="MongoDB connection string", foreground="#FFFFFF", background="#424242")
        self.sidebar.add_component(self.ip_address_box)

        self.connect_button = Button(text="Connect", role="primary-color", background="#4CAF50")
        self.sidebar.add_component(self.connect_button)
        self.connect_button.set_event_handler('click', self.on_connect_clicked)
        self.sidebar.add_component(Spacer(height=10))

    def setup_action_controls(self):
        """Setup action controls."""
        self.dataset_dropdown = DropDown(items=[("Select Dataset", None)], enabled=False, placeholder="Select Dataset", foreground="#FFFFFF", background="#424242")
        self.sidebar.add_component(self.dataset_dropdown)
        self.dataset_dropdown.set_event_handler('change', self.on_dataset_selected)
        self.sidebar.add_component(Spacer(height=10))

    def setup_file_controls(self):
        """Setup file upload and processing controls."""
        print('Cuddy')
        self.file_loader = FileLoader(multiple=False, file_types=[".csv"], enabled=False, tooltip="Upload data file", foreground="#FFFFFF", background="#424242")
        # , ".xlsx", ".json", ".parquet"
        self.sidebar.add_component(self.file_loader)

        self.process_file_button = Button(text="Process File", enabled=False, role="secondary-color", background="#2196F3")
        self.sidebar.add_component(self.process_file_button)
        self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
        self.file_loader.set_event_handler('change', self.on_file_loader_changed)

    def setup_feedback_label(self):
        """Setup feedback label."""
        self.feedback_label = Label(text="", foreground="#F44336")
        self.sidebar.add_component(self.feedback_label)

    def on_connect_clicked(self, **event_args):
        """Handle MongoDB connection."""
        connString = self.ip_address_box.text
        success, message = anvil.server.call('connect_to_mongodb', connString)
        if success:
            self.update_datasets(connString)
        self.display_feedback(success, message)

    def update_datasets(self, connString):
        """Fetch and update dataset dropdown after successful MongoDB connection."""
        success, datasets = anvil.server.call('get_verticals', connString)
        if success:
            self.dataset_dropdown.items = [("Select Dataset", None)] + [(name, name) for name in datasets]
            self.dataset_dropdown.enabled = True
        else:
            self.display_feedback(False, "Failed to fetch datasets.")

    def on_file_loader_changed(self, **event_args):
        """Enable process button when a file is loaded."""
        self.process_file_button.enabled = bool(self.file_loader.file)

    def on_process_file_clicked(self, **event_args):
        """Process uploaded file."""
        if self.file_loader.file:
            success, message = anvil.server.call('initiate_file_processing', self.file_loader.file, self.ip_address_box.text)
            self.display_feedback(success, message)

    def display_feedback(self, success, message):
        """Display feedback to the user."""
        self.feedback_label.text = message
        self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
        self.feedback_label.visible = True

    def on_dataset_selected(self, sender, **event_args):
        """Handle actions based on the selected dataset."""
        selected_dataset = sender.selected_value
        if selected_dataset:
            print(f"Dataset selected: {selected_dataset}")
            # Placeholder for dataset selection actions
            
