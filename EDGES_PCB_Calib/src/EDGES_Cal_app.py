from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
import serial

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)

    def on_size(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)  # Adjust color as needed
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

class SerialPortApp(App):
    def build(self):
        # Create a BoxLayout as the root widget
        #layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Create a TextInput for entering the serial port number
        self.port_input = TextInput(
            multiline=False,
            font_size=20,
            halign='center',
            hint_text='Enter port number (e.g., COM1 or /dev/ttyUSB0)'
        )

        # Create a TextInput for entering a message to send
        self.message_input = TextInput(
            multiline=False,
            font_size=20,
            halign='center',
            hint_text='Enter message to send'
        )

        # Create a Label for displaying the output
        self.output_label = Label(text='Port message will appear here', font_size=20, halign='center')

        # Create round buttons
        connect_button = Button(text='Connect', on_press=self.connect_to_serial,pos=(800,500),size=(50,50), size_hint=(None, None))
        disconnect_button = Button(text='Disconnect', on_press=self.disconnect_serial, size_hint=(None, None))
        send_button = Button(text='Send Message', on_press=self.send_message, size_hint=(None, None))
        
        # Create a Button to read messages from the serial port
        read_button = RoundedButton(text='Read Message', on_press=self.read_message, size_hint=(None, None))

        # Add widgets to the layout
        layout.add_widget(self.port_input)
        layout.add_widget(connect_button)
        layout.add_widget(disconnect_button)
        layout.add_widget(self.message_input)
        layout.add_widget(send_button)
        layout.add_widget(read_button)
        layout.add_widget(self.output_label)

        return layout

    def connect_to_serial(self, instance):
        # Get the serial port number from the TextInput
        port_number = self.port_input.text

        try:
            # Open the serial port
            self.ser = serial.Serial(port=port_number, baudrate=9600, timeout=1)

            # Read a message from the serial port
            message = self.ser.readline().decode('utf-8')

            # Display the message in the output label
            self.output_label.text = f'Received message: {message}'
        except Exception as e:
            # Display an error message if there is an issue with the serial port
            self.output_label.text = f'Error: {str(e)}'

    def disconnect_serial(self, instance):
        # Check if the serial port is open before attempting to close it
        if hasattr(self, 'ser') and self.ser.is_open:
            # Close the serial port
            self.ser.close()
            self.output_label.text = 'Serial port disconnected'
        else:
            self.output_label.text = 'No active serial connection'

    def send_message(self, instance):
        # Check if the serial port is open before attempting to send a message
        if hasattr(self, 'ser') and self.ser.is_open:
            # Get the message from the TextInput
            message_to_send = self.message_input.text

            # Send the message to the serial port
            self.ser.write(message_to_send.encode('utf-8'))

            # Read the response from the serial port
            response = self.ser.readline().decode('utf-8')

            # Display the received message in the output label
            self.output_label.text = f'Received message: {response}'
        else:
            self.output_label.text = 'No active serial connection'

    def read_message(self, instance):
        # Check if the serial port is open before attempting to read a message
        if hasattr(self, 'ser') and self.ser.is_open:
            # Read a message from the serial port
            message = self.ser.readline().decode('utf-8')

            # Display the received message in the output label
            self.output_label.text = f'Received message: {message}'
        else:
            self.output_label.text = 'No active serial connection'


if __name__ == '__main__':
    SerialPortApp().run()
