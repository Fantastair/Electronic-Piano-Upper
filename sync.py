import fantas
import my_serial

class SyncTrigger(fantas.CircleTrigger):
    order_map = {
        'volume': ([0x01], 20),
        'keyboard': ([0x02], 12),
    }
    
    def __init__(self, state, recv_func):
        state = SyncTrigger.order_map[state]
        super().__init__(my_serial.send_read_order, state[0], recv_func)
        self.set_circle_time(-1)
        self.launch(state[1])
