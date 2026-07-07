import sqlite3

DB_NAME = "sentinel.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            src TEXT,
            dst TEXT,
            protocol TEXT,
            size INTEGER
        )
    """)

    conn.commit()
    conn.close()


def insert_packet(time, src, dst, protocol, size):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO packets(time, src, dst, protocol, size)
        VALUES (?, ?, ?, ?, ?)
    """, (time, src, dst, protocol, size))

    conn.commit()
    conn.close()


def get_packets(limit=100):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT time, src, dst, protocol, size
        FROM packets
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "time": row[0],
            "src": row[1],
            "dst": row[2],
            "protocol": row[3],
            "size": row[4]
        }
        for row in rows
    ]


init_db()
def get_statistics():

    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM packets")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM packets WHERE protocol='TCP'")
    tcp = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM packets WHERE protocol='UDP'")
    udp = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT src)
        FROM packets
    """)
    unique_ips = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "tcp": tcp,
        "udp": udp,
        "unique_ips": unique_ips
    }
def get_top_ips():
    

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT src, COUNT(*) as total
        FROM packets
        GROUP BY src
        ORDER BY total DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "ip": row[0],
            "count": row[1]
        }
        for row in rows
    ]
def get_protocol_distribution():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT protocol, COUNT(*)
        FROM packets
        GROUP BY protocol
    """)

    rows = cursor.fetchall()

    conn.close()

    return {
        row[0]: row[1]
        for row in rows
    }
def get_protocols():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT protocol, COUNT(*)
        FROM packets
        GROUP BY protocol
    """)

    rows = cursor.fetchall()

    conn.close()

    protocols = {}

    for row in rows:
        protocols[row[0]] = row[1]

    return protocols
def get_alerts(limit=10):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT time, src, protocol, size
        FROM packets
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    alerts = []

    for row in rows:

        level = "Low"
        message = "Normal Traffic"

        if row[3] > 1200:
            level = "High"
            message = "Large Packet Detected"

        elif row[2] == "TCP":
            level = "Medium"
            message = "Heavy TCP Traffic"

        alerts.append({
            "time": row[0],
            "ip": row[1],
            "level": level,
            "message": message
        })

    return alerts
def export_packets():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT time, src, dst, protocol, size
        FROM packets
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows