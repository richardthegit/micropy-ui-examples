from rb.ui.menu import Menu, MenuItem


class WifiMenu(Menu):
    def __init__(self, display, btns, wifi, back):
        super().__init__(display, btns, title = 'Wifi Networks', back = back)
        self.wifi = wifi

    def enter(self):
        self.set_items([MenuItem('Scanning for networks...')])
        super().enter()

        items = []
        for ssid, mac, channel, db, sec in self.wifi.scan():
            print(ssid, mac, channel, db, sec)
            items.append(MenuItem(ssid, None))

        self.set_items(items)
