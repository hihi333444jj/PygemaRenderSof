import socket
import threading
import time
import random

HOST = "127.0.0.1"
PORT = 65432

# -------- LOAD WORLD AS ARRAY --------
with open("Test/World.txt", "r") as file:
    lines = file.read().splitlines()

world = [line.split("|") for line in lines]

world_lock = threading.RLock()

world_dirty = True 
WorldString = b""


def rebuild_world_string():
    """Convert world array to bytes"""
    global WorldString, world_dirty
    with world_lock:
        WorldString = "~".join(
            "|".join(row) for row in world
        ).encode()
        world_dirty = False
    
rebuild_world_string()

def in_bounds(y, x):
    return 0 <= y < len(world) and 0 <= x < len(world[0])

WIRE_TURNS = {
    "Wire_TB": {"top": "bottom", "bottom": "top"},
    "Wire_LR": {"left": "right", "right": "left"},
    "Wire_TR": {"top": "right", "right": "top"},
    "Wire_TL": {"top": "left", "left": "top"},
    "Wire_BR": {"bottom": "right", "right": "bottom"},
    "Wire_BL": {"bottom": "left", "left": "bottom"},
}

def PowerFrom(y, x, direction,Change,To):
    ArrayToSend = []
    dy = {"top": 1, "bottom": -1, "left": 0, "right": 0} #Lazyness made this... Top is -1 but i needed to flop them same for richg and left and bottom
    dx = {"top": 0, "bottom": 0, "left": 1, "right": -1}
    OPPOSITE = {
        "top": "bottom","bottom": "top",
        "left": "right","right": "left",
    }
    #dy clarifys inverted direcshens for moving/activating on Y
    #dx means invertted X axes for moving/activating
    ny, nx = y + dy[direction], x + dx[direction]
    if not in_bounds(ny, nx):return[]

    block = world[ny][nx]
    if not block.endswith(Change):return[] #dose the block have _Off at the end if not stop the def

    wire = block.replace(Change, "")
    if wire not in WIRE_TURNS:return[] #check if it is a wire if not return

    if direction not in WIRE_TURNS[wire]:return[] #checks if direcshe is valid

    # Next power :D
    
    out_dir = WIRE_TURNS[wire][direction]
    print(out_dir)
    ArrayToSend = [[nx, ny, wire + To]]
    for i in ArrayToSend:
        if (i[0] == ny):
            if (i[1] == nx):
                return []
    ArrayToSend.extend(PowerFrom(ny, nx, OPPOSITE[out_dir],Change,To))
    return ArrayToSend


def StrictAdd(x,y,block):
    global world_dirty,CurrentUpdate

    with world_lock:
        if 0 <= y < len(world) and 0 <= x < len(world[y]):

            world[y][x] = block
            world_dirty = True

def set_block(x, y, block):
    global world_dirty,CurrentUpdate
    #manage wires
    change = []
    if block == "PowerBlock":
        change.extend(PowerFrom(y, x, "top","_Off","_On"))
        change.extend(PowerFrom(y, x, "bottom","_Off","_On"))
        change.extend(PowerFrom(y, x, "left","_Off","_On"))
        change.extend(PowerFrom(y, x, "right","_Off","_On"))
    if world[y][x] == "PowerBlock":
        if block != "PowerBlock":
            change.extend(PowerFrom(y, x, "top","_On","_Off"))
            change.extend(PowerFrom(y, x, "bottom","_On","_Off"))
            change.extend(PowerFrom(y, x, "left","_On","_Off"))
            change.extend(PowerFrom(y, x, "right","_On","_Off"))
    print(change)
    with world_lock:
        for i in change:
            StrictAdd(*i)
        
        if 0 <= y < len(world) and 0 <= x < len(world[y]):
            world[y][x] = block
            world_dirty = True
    CurrentUpdate += 1

ClientUpdateList = [[],[]]
CurrentUpdate = 0
def handle_client(conn, addr):
    global WorldString, world_dirty,ClientUpdateList,CurrentUpdate
    ClientUpdateList[0].append(addr)
    ClientUpdateList[1].append(-1)
    print(f"Connected by {addr}")
    conn.setblocking(False)

    buffer = ""

    with conn:
        conn.sendall(WorldString)
        while True:
            try:
                try:
                    data = conn.recv(4096)
                    if data:
                        buffer += data.decode()

                        while "\n" in buffer:
                            msg, buffer = buffer.split("\n", 1)
                            if msg:
                                print(f"From {addr}: {msg}")

                                # example message: "2,3|dirt"
                                try:
                                    pos, block = msg.split("|")
                                    x, y = map(int, pos.split(","))
                                    set_block(x, y, block)
                                except ValueError:
                                    pass

                except BlockingIOError:
                    pass

                if world_dirty:
                    rebuild_world_string()

                #Value = ClientUpdateList[1][ClientUpdateList[0].index(addr)]
                #if Value != CurrentUpdate:
                    #ClientUpdateList[1][ClientUpdateList[0].index(addr)] = CurrentUpdate
                conn.sendall(WorldString)
                

                time.sleep(.1)

            except (ConnectionResetError, BrokenPipeError):
                print(f"Connection closed: {addr}")
                break


# -------- MAIN SERVER --------
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server listening...")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        thread.start()
