from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import serial

class SerialMonitorApp(App):
    def build(self):
        self.serial_port = None

        # UI layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Serial port selection
        self.serial_label = Label(text='Serial Port:')
        layout.add_widget(self.serial_label)

        self.serial_input = TextInput(multiline=False, input_type='text')
        layout.add_widget(self.serial_input)

        # Connect and Disconnect buttons
        connect_button = Button(text='Connect', on_press=self.connect_serial)
        disconnect_button = Button(text='Disconnect', on_press=self.disconnect_serial)
        layout.add_widget(connect_button)
        layout.add_widget(disconnect_button)

        # Data input and output
        self.data_input = TextInput(multiline=False, input_type='text', readonly=True)
        layout.add_widget(self.data_input)

        self.send_button = Button(text='Send', on_press=self.send_data)
        layout.add_widget(self.send_button)

        # Clock schedule for periodic updates
        Clock.schedule_interval(self.update, 1.0 / 10)  # Update every 0.1 seconds

        return layout

    def connect_serial(self, instance):
        # Get the selected serial port from the input field
        port_name = self.serial_input.text.strip()

        try:
            # Open the serial port
            self.serial_port = serial.Serial(port_name, 9600, timeout=0.1)
            self.serial_label.text = f'Serial Port: {port_name} (Connected)'
        except Exception as e:
            self.data_input.text += f'Error connecting to {port_name}: {e}\n'

    def disconnect_serial(self, instance):
        # Close the serial port
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.serial_label.text = 'Serial Port: (Disconnected)'

    def send_data(self, instance):
        # Get the data from the input field and send it to the serial port
        if self.serial_port and self.serial_port.is_open:
            data = self.data_input.text
            self.serial_port.write(data.encode())
            self.data_input.text = ''

    def update(self, dt):
        # Check for incoming data from the serial port
        if self.serial_port and self.serial_port.is_open and self.serial_port.in_waiting > 0:
            received_data = self.serial_port.readline().decode().strip()
            self.data_input.text += f'Received: {received_data}\n'

if __name__ == '__main__':
    SerialMonitorApp().run()

