from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.left_nav = ColumnPanel()
        self.add_component(self.left_nav, slot="sidebar")

        self.ip_address_box = TextBox(placeholder='Enter MongoDB connection string here')
        self.left_nav.add_component(self.ip_address_box)

        self.connect_button = Button(text="Connect")
        self.left_nav.add_component(self.connect_button)
        self.connect_button.set_event_handler('click', self.connect_button_click)

        self.menu = ["Analyze Data", "Find Anomalies", "Embedded Database", "Multi Sense"]
        self.menu_buttons = []

        for item in self.menu:
            button = Button(text=item, enabled=False)
            button.set_event_handler('click', self.menu_item_clicked)
            self.left_nav.add_component(button)
            self.menu_buttons.append(button)

        self.left_nav.add_component(Label(text="--------------", bold=True))

        self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"])
        self.left_nav.add_component(self.file_loader)

        self.process_file_button = Button(text="Process File", enabled=False)
        self.process_file_button.set_event_handler('click', self.process_file_click)
        self.left_nav.add_component(self.process_file_button)
      
        # self.left_nav.add_component(self.process_file_button)
        # self.file_loader.set_event_handler('change', self.file_loader_change)

        self.warning_label = Label(text="")
        self.left_nav.add_component(self.warning_label)

    def file_loader_change(self, **event_args):
        self.process_file_button.enabled = bool(self.file_loader.file)

    def process_file_click(self, **event_args):
      if self.file_loader.file:
          connString = self.ip_address_box.text  # Assuming this is where you store your MongoDB connection string
          try:
              # Call server to process and load file
              result = anvil.server.call('process_and_load_file', self.file_loader.file, connString)
              if result:
                  alert("File processed successfully.")
              else:
                  alert("Failed to process file.")
          except Exception as e:
              alert(f"Error processing file: {str(e)}")

    # def process_file_click(self, **event_args):
    #     if self.file_loader.file:
    #         db_name = "Specify_DB_name_based_on_user_choice"  # This should be set based on user input.
    #         collection_name = "Specify_collection_name_based_on_user_input"  # Ditto.
    #         success = anvil.server.call('process_and_load_file', self.file_loader.file, self.ip_address_box.text, db_name, collection_name)
    #         if success:
    #             alert("File processed successfully.")
    #         else:
    #             alert("Error processing file.")
    # def process_file_click(self, **event_args):
    #     if self.file_loader.file:
    #         try:
    #             result = anvil.server.call('process_and_load_file', self.file_loader.file)
    #             if result:
    #                 alert("File processed successfully.")
    #         except Exception as e:
    #             alert(f"Error processing file: {str(e)}")

    def menu_item_clicked(self, sender, **event_args):
        print(f"Menu item clicked: {sender.text}")

    def connect_button_click(self, **event_args):
        connString = self.ip_address_box.text
        success = anvil.server.call('connect_to_mongodb', connString)
        if success:
            verticals = anvil.server.call('get_verticals')
            self.warning_label.text = "Connection Successful"
            self.warning_label.foreground = "green"
            for button in self.menu_buttons:
                button.enabled = True
            self.process_file_button.enabled = True
        else:
            self.warning_label.text = "Connection failed"
            self.warning_label.foreground = "red"
            for button in self.menu_buttons:
                button.enabled = False
            self.process_file_button.enabled = False
        self.warning_label.visible = True

    def update_menu(self, verticals):
        pass  # Implement functionality to update menu based on 'verticals'
