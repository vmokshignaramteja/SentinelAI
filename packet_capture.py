from scapy.all import sniff
from datetime import datetime
from database import insert_packet

def process_packet(packet):
    if packet.haslayer("IP"):

        data = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "src": packet["IP"].src,
            "dst": packet["IP"].dst,
            "protocol": packet.lastlayer().name,
            "size": len(packet)
        }

        insert_packet(
            data["time"],
            data["src"],
            data["dst"],
            data["protocol"],
            data["size"]
        )

        print(data)


print("SentinelAI Packet Capture Started...")
print("Listening...")

sniff(prn=process_packet, store=False, count=100)