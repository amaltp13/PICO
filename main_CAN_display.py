# main.py
# Example usage of MCP2515 + OLED_1inch3 libraries

from mcp2515 import MCP2515
from oled_1inch3 import OLED_1inch3
import time

def main():
    # Initialize CAN
    can = MCP2515(baud="500KBPS")  # adjust if using 8 MHz crystal
    print("CAN initialized at 500 kbps")

    # Initialize OLED
    oled = OLED_1inch3()
    oled.fill(oled.black)
    oled.text("CAN Demo", 20, 0, oled.white)
    oled.show()

    msg_id = 0x123
    i = 1

    while True:
        # Prepare CAN data
        data = [i, 2, 3, 4, 5, 6, 7, 8]

        # Send CAN frame
        print(f"Sending frame ID={hex(msg_id)} Data={data}")
        can.send(msg_id, data)

        # Update OLED display
        oled.fill(oled.black)
        oled.text("CAN TX", 0, 0, oled.white)
        oled.text(f"ID: {hex(msg_id)}", 0, 20, oled.white)
        oled.text("Data:", 0, 40, oled.white)
        oled.text(" ".join(str(x) for x in data), 0, 55, oled.white)
        oled.show()

        time.sleep(0.5)  # avoid flooding
        i += 1

if __name__ == "__main__":
    main()
