from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
    def __init__(self, **properties):
        # Initialize form and components from the designer file.
        self.init_components(**properties)
        
        # Dynamically create a sidebar container.
        self.left_nav = ColumnPanel()
        self.add_component(self.left_nav, slot="sidebar")
        
        # Define menu items and initially disabled menu buttons list
        self.menu = ["Analyze Data", "Find Anomalies", "Embedded Database", "Multi Sense"]
        self.menu_buttons = []
        
        # Dynamically create and add a disabled button for each menu item to the sidebar.
        for item in self.menu:
            button = Button(text=item, icon="view-list", role="secondary-menu", enabled=False)
            button.set_event_handler('click', self.menu_item_clicked)
            self.left_nav.add_component(button)
            self.menu_buttons.append(button)
        
        # Add a separator for visual distinction
        self.left_nav.add_component(Label(text="--------------", bold=True))
        
        # Create a TextBox for IP input and add it to the sidebar.
        self.ip_address_box = TextBox(placeholder="e.g., 192.168.1.1")
        self.left_nav.add_component(self.ip_address_box)
        
        # Create a Button to initiate the connection and add it to the sidebar.
        self.connect_button = Button(text="Connect")
        self.left_nav.add_component(self.connect_button)
        self.connect_button.set_event_handler('click', self.connect_button_click)
        
        # Initialize a label for connection status messages and add it to the sidebar.
        self.warning_label = Label(text="")
        self.left_nav.add_component(self.warning_label)

    def menu_item_clicked(self, sender, **event_args):
        # Placeholder for handling menu item click events
        print(f"Menu item clicked: {sender.text}")

    def connect_button_click(self, **event_args):
        # Retrieve the IP address from the input box.
        ip_address = self.ip_address_box.text
        
        # Call the server function to attempt MongoDB connection.
        success, message = anvil.server.call('connect_to_mongodb', ip_address)
        
        # Update the warning label based on the connection attempt's outcome.
        self.warning_label.text = message
        self.warning_label.foreground = "green" if success else "red"
        self.warning_label.visible = True
        
        # If the connection is successful, enable the menu buttons.
        if success:
            for button in self.menu_buttons:
                button.enabled = True
        else:
            # Optionally, disable the menu buttons again if the connection fails.
            # Remove or comment out this block if you want the buttons to remain enabled once they've been enabled.
            for button in self.menu_buttons:
                button.enabled = False
