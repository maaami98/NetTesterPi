from sys import platform
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color
from sys import exit
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown

Window.size = (480, 320)

import subprocess
import threading
import platform
import selectors
import netifaces 
class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="horizontal")
        side_bar = BoxLayout(orientation="vertical")
        side_bar.size_hint = (0.2, 1.0)
        screen = BoxLayout(orientation="vertical")
        self.result_screen=  BoxLayout(orientation="vertical")
        self.info_screen =  BoxLayout(orientation="vertical")
        self.main_layout=main_layout
        self.screen=screen
        self.side_bar=side_bar
        self.choise=2
        self.last_was_operator = None
        self.last_button = None
        self.process=None
        
        """ Info Page """
        netif = DropDown()
        for nic in netifaces.interfaces():
            btn =Button(text=nic,size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: netif.select(btn.text))
            btn.bind(on_press=self.refresh_info)
            netif.add_widget(btn)
        mainbutton = Button(text='Interfaces', halign="left",size_hint=(0.25,None))
        mainbutton.bind(on_release=netif.open)
        netif.bind(on_select=lambda instance, x: setattr(mainbutton,'text',x))
        mainbutton.pos=(0,0)
        self.ip_label=Label(text='IP:',markup=True)
        self.net_label=Label(text='NET:',markup=True)
        self.gw_label=Label(text='GW:',markup=True)
        
        default_if=netifaces.gateways()['default'][netifaces.AF_INET][1]
        
        try:
            self.ip_label.text='[b]IP: '+list(netifaces.ifaddresses(default_if).values())[1][0]['addr']+'[/b]'
            self.net_label.text='[b]NET: ' +list(netifaces.ifaddresses(default_if).values())[1][0]['netmask']+'[/b]'
            self.gw_label.text='[b]GW: '+netifaces.gateways()['default'][netifaces.AF_INET][0]+'[/b]'
        except:
            self.ip_label.text='IP:'
            self.net_label.text='NET:'
            self.gw_label.text='GW:'
        
        
        self.info_screen.add_widget(mainbutton)
        self.info_screen.add_widget(self.ip_label)
        self.info_screen.add_widget(self.net_label)
        self.info_screen.add_widget(self.gw_label)
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
        button.bind(on_press=exit)
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
        self.main_layout.remove_widget(self.info_screen)
        if self.choise == 1:
            self.main_layout.add_widget(self.info_screen)
        else:
            self.main_layout.add_widget(self.screen)
    def refresh_info(self,instance):
        default_if=instance.text
        try:
            self.ip_label.text='[b]IP: '+list(netifaces.ifaddresses(default_if).values())[1][0]['addr']+'[/b]'
            self.net_label.text='[b]NET: ' +list(netifaces.ifaddresses(default_if).values())[1][0]['netmask']+'[/b]'
            self.gw_label.text='[b]GW: '+netifaces.gateways()['default'][netifaces.AF_INET][0]+'[/b]'
        except:
            self.ip_label.text='IP:'
            self.net_label.text='NET:'
            self.gw_label.text='GW:'
        
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
        self.process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        sel = selectors.DefaultSelector()
        sel.register(self.process.stdout,selectors.EVENT_READ)
        sel.register(self.process.stderr,selectors.EVENT_READ)
        while True:
            for key, _ in sel.select():
                data = key.fileobj.read1().decode()
                if not data:
                    break
                self.result.text+=data
                """
        for line in self.process.stdout:
            self.result.text+=line.decode()
        for line in self.process.stderr:
            self.result.text+=line.decode()
            """
    def on_target(self, instance):
        text = self.target.text
        if text:
            self.main_layout.remove_widget(self.screen)
            self.main_layout.add_widget(self.result_screen)
            if self.choise ==2:
                if platform.system() == "Windows":
                    x = threading.Thread(target=self.query, args=('ping '+self.target.text+" -t",))
                else:
                    x = threading.Thread(target=self.query, args=(['ping',self.target.text],))
                x.start()
            if self.choise ==3:
                if platform.system() == "Windows":
                    x = threading.Thread(target=self.query, args=('tracert '+self.target.text,))
                else:
                    x = threading.Thread(target=self.query, args=(['traceroute',self.target.text],))
                x.start()
            if self.choise ==4:
                x = threading.Thread(target=self.query, args=(['iperf3','-c ',self.target.text],))
                x.start()
            
if __name__ == '__main__':
    app = MainApp()
    app.run()