from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
import pandas as pd
from kivy.uix.scrollview import ScrollView

Window.size = (400, 600)  # Set window size

class LoginPage(Screen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)

        # BoxLayout for vertical arrangement
        layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 20, 20, 20), size_hint=(None, None),
                          width=300, height=400, pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Canvas with white background
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        # Label
        label = Label(text="Welcome to Your App", font_size='30sp', color=(0, 0.7, 1, 1))
        layout.add_widget(label)

        # TextInput for username
        self.username_input = TextInput(hint_text="Username", multiline=False, size_hint_y=None, height=40,
                                        background_color=(1, 1, 1, 0.7), font_size='16sp',
                                        on_text_validate=self.shift_focus_to_password)
        layout.add_widget(self.username_input)

        # TextInput for password
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint_y=None, height=40,
                                        background_color=(1, 1, 1, 0.7), font_size='16sp')
        layout.add_widget(self.password_input)

        # Login Button
        self.login_button = Button(text="Login", on_press=self.check_login, size_hint_y=None, height=50,
                                   background_color=(0, 0.7, 1, 1), font_size='20sp')
        layout.add_widget(self.login_button)

        self.add_widget(layout)

    def shift_focus_to_password(self, instance):
        self.password_input.focus = True  # Shift focus to password input

    def check_login(self, instance):
        # Check if the username and password match
        if self.username_input.text == "user" and self.password_input.text == "pass":
            App.get_running_app().root.current = "main"
        else:
            print("Login failed")

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)

        # GridLayout for button arrangement
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None, height=300, pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Canvas with white background
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        # Label
        label = Label(text="Main Menu", font_size='30sp', color=(0, 0.7, 1, 1))
        layout.add_widget(label)

        # Button names
        button_names = ["Scan", "Data", "Logout"]
        for button_name in button_names:
            button = Button(text=button_name, on_press=self.button_pressed, size_hint_y=None, height=50,
                            background_color=(0, 0.7, 1, 1), font_size='20sp')
            layout.add_widget(button)

        self.add_widget(layout)

    def button_pressed(self, instance):
        if instance.text == "Scan":
            self.manager.current = "scan"
        elif instance.text == "Data":
            self.manager.current = "data"
        elif instance.text == "Logout":
            self.manager.current = "logout"

# Updated ScanPage
# Updated ScanPage
class ScanPage(Screen):
    def __init__(self, **kwargs):
        super(ScanPage, self).__init__(**kwargs)

        # BoxLayout for vertical arrangement
        layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 20, 20, 20),
                          size_hint=(None, None), width=400, height=500, pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Canvas with a white background
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        # Label
        label = Label(text="Scan Page", font_size='30sp', color=(0, 0.7, 1, 1))
        layout.add_widget(label)

        # TextInput for small barcode
        self.small_barcode_input = TextInput(hint_text="Scan Small Barcode", multiline=False,
                                             size_hint_y=None, height=80,
                                             background_color=(1, 1, 1, 0.7), font_size='20sp')
        self.small_barcode_input.bind(on_text_validate=self.shift_focus_to_big_barcode)
        layout.add_widget(self.small_barcode_input)

        # TextInput for big barcode
        self.big_barcode_input = TextInput(hint_text="Scan Big Barcode", multiline=False,
                                           size_hint_y=None, height=80,
                                           background_color=(1, 1, 1, 0.7), font_size='20sp')
        self.big_barcode_input.bind(on_text_validate=self.process_barcodes)
        layout.add_widget(self.big_barcode_input)

        # Data Send Button
        self.data_send_button = Button(text="Data Send", on_press=self.process_barcodes,
                                       size_hint_y=None, height=60,
                                       background_color=(0, 0.7, 1, 1), font_size='20sp')
        layout.add_widget(self.data_send_button)

        # Back to Main Page Button
        self.back_button = Button(text="Back to Main Page", on_press=self.go_to_main_page,
                                  size_hint_y=None, height=60,
                                  background_color=(0, 0.7, 1, 1), font_size='20sp')
        layout.add_widget(self.back_button)

        self.add_widget(layout)

    def shift_focus_to_big_barcode(self, instance):
        self.big_barcode_input.focus = True  # Shift focus to big barcode input

    def process_barcodes(self, instance):
        # Extract information from small barcode
        small_barcode_info = self.small_barcode_input.text
        box_number = small_barcode_info.split('-')[0]

        # Check if the box number is repeated
        if self.is_box_number_repeated(box_number):
            # Display error notification if box number is repeated
            self.show_popup("Error", "Box number is repeated. Data not transferred.")
            self.reset_text_inputs()
            return

        # Extract information from big barcode
        big_barcode = self.big_barcode_input.text
        big_barcode_parts = big_barcode.split(',')

        # Define the positions of required information
        order_name_position = 4
        quantity_position = 6
        loc_number_position = 10
        item_name_position = 12

        try:
            # Extract the required information based on positions
            order_name = big_barcode_parts[order_name_position]
            quantity = big_barcode_parts[quantity_position]
            loc_number = big_barcode_parts[loc_number_position]
            item_name = big_barcode_parts[item_name_position]

            # Check if item names are the same
            if small_barcode_info.split('-')[1] != item_name:
                # Display error notification if item names are different
                self.show_popup("Error", "Item names in small and big barcodes are different. Data not transferred.")
                self.reset_text_inputs()
                return

            # Append the extracted data to DataPage's extracted_info list
            App.get_running_app().root.get_screen('data').extracted_info.append([
                small_barcode_info, loc_number, order_name, item_name, quantity
            ])

            # Call display_data to update the table
            App.get_running_app().root.get_screen('data').display_data(
                App.get_running_app().root.get_screen('data').extracted_info
            )

            # Reset text inputs
            self.reset_text_inputs()

            # Display success notification
            self.show_popup("Success", "Data transferred successfully")

        except IndexError:
            # Display error notification for invalid format
            self.show_popup("Error", "Invalid format in big barcode")
            self.reset_text_inputs()

    def reset_text_inputs(self):
        self.small_barcode_input.text = ""
        self.big_barcode_input.text = ""

    def is_box_number_repeated(self, box_number):
        # Check if the box number is already in the extracted data
        for data in App.get_running_app().root.get_screen('data').extracted_info:
            if box_number == data[0].split('-')[0]:
                return True
        return False

    def go_to_main_page(self, instance):
        self.manager.current = "main"

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

class DataPage(Screen):
    def __init__(self, **kwargs):
        self.extracted_info = []

        super(DataPage, self).__init__(**kwargs)

        # BoxLayout for vertical arrangement
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 20, 20, 20),
                                size_hint=(None, None), width=400, height=600,
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Canvas with white background
        with main_layout.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=Window.size, pos=main_layout.pos)

        # Label
        label = Label(text="Data Page", font_size='30sp', color=(0, 0.7, 1, 1))
        main_layout.add_widget(label)

        # Table to display extracted information
        self.table = GridLayout(cols=4, spacing=20, size_hint_y=None)
        self.table.bind(minimum_height=self.table.setter('height'))
        main_layout.add_widget(self.table)

        # Excel Preview Button
        self.excel_preview_button = Button(text="Excel Preview", on_press=self.show_excel_preview,
                                           size_hint_y=None, height=50, background_color=(0, 0.7, 1, 1),
                                           font_size='20sp')
        main_layout.add_widget(self.excel_preview_button)

        # Export to Excel Button
        self.export_button = Button(text="Export to Excel", on_press=self.export_to_excel,
                                    size_hint_y=None, height=50, background_color=(0, 0.7, 1, 1),
                                    font_size='20sp')
        main_layout.add_widget(self.export_button)

        # Delete Data Button
        self.delete_data_button = Button(text="Delete Data", on_press=self.delete_data,
                                         size_hint_y=None, height=50, background_color=(1, 0, 0, 1),
                                         font_size='20sp')
        main_layout.add_widget(self.delete_data_button)

        # Go to Main Page Button
        self.main_page_button = Button(text="Go to Main Page", on_press=self.go_to_main_page,
                                       size_hint_y=None, height=50, background_color=(0.7, 0, 1, 1),
                                       font_size='20sp')
        main_layout.add_widget(self.main_page_button)

        self.add_widget(main_layout)

    def display_data(self, extracted_info):
        # Display the extracted information in a table format
        headers = ["LOC Number", "Order Name", "Item Name", "Quantity"]

        # Clear existing widgets in the table
        self.table.clear_widgets()

        # Create a new GridLayout for the table
        layout = GridLayout(cols=4, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Add headers to the table
        for header in headers:
            label = Label(text=header, font_size='16sp', color=(0, 0, 0, 1), size_hint_x=None, width=100)
            layout.add_widget(label)

        # Add data to the table
        for data in extracted_info:
            for value in data[1:]:
                label = Label(text=value, font_size='16sp', color=(0, 0, 0, 1), size_hint_x=None, width=100)
                layout.add_widget(label)

        # Add the table layout to the main layout
        self.table.add_widget(layout)

    def show_excel_preview(self, instance):
        # Display a preview of the data in a table format using a Popup
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 20, 20, 20))
        scroll_view = ScrollView()

        # Create a new GridLayout for the table in the Popup
        excel_preview_table = GridLayout(cols=4, spacing=10, size_hint_y=None)
        excel_preview_table.bind(minimum_height=excel_preview_table.setter('height'))

        # Add headers to the table
        for header in ["LOC Number", "Order Name", "Item Name", "Quantity"]:
            label = Label(text=header, font_size='16sp', color=(0, 0, 0, 1), size_hint_x=None, width=100)
            excel_preview_table.add_widget(label)

        # Add data to the table
        for data in self.extracted_info:
            for value in data[1:]:
                label = Label(text=value, font_size='16sp', color=(0, 0, 0, 1), size_hint_x=None, width=100)
                excel_preview_table.add_widget(label)

        scroll_view.add_widget(excel_preview_table)
        popup_layout.add_widget(scroll_view)

        # Excel Preview Popup
        popup = Popup(title="Excel Preview", content=popup_layout, size_hint=(None, None), size=(600, 400))
        popup.open()

    def export_to_excel(self, instance):
        # Export the data to Excel
        df = pd.DataFrame(self.extracted_info, columns=["Small Barcode", "LOC Number", "Order Name", "Item Name", "Quantity"])
        df.to_excel("data_export.xlsx", index=False)
        self.show_popup("Export Successful", "Data exported to 'data_export.xlsx'")

    def delete_data(self, instance):
        # Delete the extracted data
        self.extracted_info = []
        self.show_popup("Data Deleted", "All data has been deleted.")

    def go_to_main_page(self, instance):
        self.manager.current = "main"

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(300, 200))
        popup.open()


class LogoutPage(Screen):
    def __init__(self, **kwargs):
        super(LogoutPage, self).__init__(**kwargs)

        # BoxLayout for vertical arrangement
        layout = BoxLayout(orientation='vertical', spacing=10, padding=(20, 20, 20, 20),
                          size_hint=(None, None), width=400, height=500, pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Canvas with a white background
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        # Label
        label = Label(text="Logout Page", font_size='30sp', color=(0, 0.7, 1, 1))
        layout.add_widget(label)

        # Logout Button
        self.logout_button = Button(text="Logout", on_press=self.logout,
                                    size_hint_y=None, height=60,
                                    background_color=(1, 0, 0, 1), font_size='20sp')
        layout.add_widget(self.logout_button)

        self.add_widget(layout)

    def logout(self, instance):
        # Redirect to the Login Page
        self.manager.current = "login"


class TestApp(App):
    def build(self):
        # Create a screen manager
        sm = ScreenManager()
        sm.add_widget(LoginPage(name="login"))
        sm.add_widget(MainPage(name="main"))
        sm.add_widget(ScanPage(name="scan"))
        sm.add_widget(DataPage(name="data"))
        sm.add_widget(LogoutPage(name="logout"))
        return sm

if __name__ == '__main__':
    TestApp().run()
