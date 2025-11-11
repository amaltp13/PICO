# main.py
# Example usage of MCP2515 library

from mcp2515 import MCP2515
import time

def main():
    can = MCP2515(baud="500KBPS")  # adjust if using 8 MHz crystal
    print("CAN initialized at 500 kbps")

    msg_id = 0x123
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    i=1
    while True:
        data = [i, 2, 3, 4, 5, 6, 7, 8]
        print(f"Sending frame ID={hex(msg_id)} Data={data}")
        can.send(msg_id, data)
        time.sleep(0.5)  # avoid flooding
        i=i+1

if __name__ == "__main__":
    main()
