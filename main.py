from sys import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.core.window import Window
Window.size = (480, 320)

import subprocess
import threading
import platform

class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="horizontal")
        side_bar = BoxLayout(orientation="vertical")
        side_bar.size_hint = (0.2, 1.0)
        screen = BoxLayout(orientation="vertical")
        self.result_screen=  BoxLayout(orientation="vertical")
        self.main_layout=main_layout
        self.screen=screen
        self.side_bar=side_bar
        self.choise=2
        self.last_was_operator = None
        self.last_button = None
        self.process=None
        
        self.target = TextInput(
            multiline=False, readonly=False, halign="right", hint_text="192.168.1.1"
        )
        

        self.result = TextInput(
            multiline=True, readonly=True, halign="left", 
        )
        
        self.result_screen.add_widget(self.result)
        button = Button(
                    text="STOP",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    size_hint = (1, 0.2)
                )

        button.bind(on_press=self.on_button_press)
        self.result_screen.add_widget(button)
        
        buttons = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            [".", "0", "C"],
        ]
        
        button = Button(
                    text="INFO",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    
                )

        button.bind(on_press=self.on_button_press)
        side_bar.add_widget(button)
        button = Button(
                    text="PING",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                ) 
        
        button.bind(on_press=self.on_button_press)
        side_bar.add_widget(button)
        button = Button(
                    text="TRACERT",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                ) 
        button.bind(on_press=self.on_button_press)
        side_bar.add_widget(button)
        button = Button(
                    text="IPERF3",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                ) 
        button.bind(on_press=self.on_button_press)
        side_bar.add_widget(button)
        
        button = Button(
                    text="QUIT",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                ) 
        button.bind(on_press=quit)
        side_bar.add_widget(button)
        self.reset_color()
        side_bar.children[3].background_color =[1, 0, 0, 1] 
        
        
        main_layout.add_widget(side_bar)
        main_layout.add_widget(screen)
        screen.add_widget(self.target)
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            screen.add_widget(h_layout)
        
        equals_button = Button(
            text="Run!", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_target)
        
        screen.add_widget(equals_button)
        
        return main_layout
    def reset_color(self):
        for child in  self.side_bar.children:
            child.background_color =[0, 0, 1, 1] 
    def select_button(self,id,instance):
        self.reset_color()
        self.choise=id
        instance.background_color =[1, 0, 0, 1] 
        self.main_layout.remove_widget(self.result_screen)
        self.main_layout.remove_widget(self.screen)
        self.main_layout.add_widget(self.screen)
    
    def on_button_press(self, instance):
        current = self.target.text
        button_text = instance.text
        if button_text == "INFO" :
            self.select_button(1,instance)
        elif button_text == "PING" :
            self.select_button(2,instance)
        elif button_text == "TRACERT" :
            self.select_button(3,instance)
        elif button_text == "IPERF3" :
            self.select_button(4,instance)
        elif button_text == "C":
            self.target.text = ""
        elif button_text == "STOP":
            self.main_layout.add_widget(self.screen)
            self.main_layout.remove_widget(self.result_screen)
            self.process.terminate()
        else:
            new_text = current + button_text
            self.target.text = new_text
    def query(self,command):
        self.process = subprocess.Popen(command,stdout=subprocess.PIPE)
        for line in self.process.stdout:
            self.result.text+=line.decode()
    def on_target(self, instance):
        text = self.target.text
        if text:
            self.main_layout.remove_widget(self.screen)
            self.main_layout.add_widget(self.result_screen)
            if self.choise ==2:
                if platform.system() == "Windows":
                    x = threading.Thread(target=self.query, args=('ping '+self.target.text+" -t",))
                else:
                    x = threading.Thread(target=self.query, args=('ping '+self.target.text,))
                x.start()
            if self.choise ==3:
                if platform.system() == "Windows":
                    x = threading.Thread(target=self.query, args=('tracert '+self.target.text,))
                else:
                    x = threading.Thread(target=self.query, args=('traceroute '+self.target.text,))
                x.start()
            if self.choise ==4:
                x = threading.Thread(target=self.query, args=('iperf3 -c '+self.target.text,))
                x.start()
            
if __name__ == '__main__':
    app = MainApp()
    app.run()