import fantas
import my_serial

class SyncTrigger(fantas.CircleTrigger):
    order_map = {
        'volume': ([0x01], 20),
        'keyboard': ([0x02], 6),
        'play_info': ([0x06], 15),
     }

    def __init__(self, state, recv_func):
        self.state = SyncTrigger.order_map[state]
        super().__init__(my_serial.send_read_order, self.state[0], recv_func)
        self.set_circle_time(-1)
        self.launch()

    def launch(self):
        return super().launch(self.state[1])
