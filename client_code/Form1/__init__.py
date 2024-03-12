from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Create a sidebar container if it doesn't exist in your Anvil designer
        self.left_nav = ColumnPanel()
        self.add_component(self.left_nav, slot="before")  # Adjust 'slot' as needed based on your layout
        
        # Create a TextBox for IP input
        self.ip_address_box = TextBox(text="Enter IP Address", placeholder="e.g., 192.168.1.1")
        self.left_nav.add_component(self.ip_address_box)  # Add the TextBox to the sidebar
        
        # Create a Button to initiate the connection
        self.connect_button = Button(text="Connect")
        self.left_nav.add_component(self.connect_button)  # Add the Button to the sidebar
        self.connect_button.set_event_handler('click', self.connect_button_click)
        
        # Initialize a label for connection status messages
        self.warning_label = Label(text="")
        self.left_nav.add_component(self.warning_label)  # Add the Label to the sidebar

    def connect_button_click(self, **event_args):
        ip_address = self.ip_address_box.text
        
        success, message = anvil.server.call('connect_to_mongodb', ip_address)
        if success:
            self.warning_label.text = message
            self.warning_label.foreground = "green"
        else:
            self.warning_label.text = message
            self.warning_label.foreground = "red"
    
        self.warning_label.visible = True
