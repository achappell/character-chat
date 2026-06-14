import os
import zlib
import struct

def write_png(filename, width, height, pixels):
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0) # Filter type 0
        for x in range(width):
            r, g, b = pixels[y * width + x]
            raw_data.append(r)
            raw_data.append(g)
            raw_data.append(b)
    
    compressed = zlib.compress(raw_data, level=9)
    
    def chunk(tag, data):
        return struct.pack("!I", len(data)) + tag + data + struct.pack("!I", zlib.crc32(tag + data))
        
    png = (
        b'\x89PNG\r\n\x1a\n' +
        chunk(b'IHDR', struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)) +
        chunk(b'IDAT', compressed) +
        chunk(b'IEND', b'')
    )
    with open(filename, 'wb') as f:
        f.write(png)

# 32x32 Grid Design
# . = Background Navy
# h = Hair Brown
# H = Hair Highlight (light brown)
# d = Hair Shadow (dark brown)
# s = Skin
# S = Skin Shadow
# b = Skin Blush/Warmth
# w = Eye White
# e = Eye Iris (warm brown)
# E = Eye Lash/Brow (dark brown/black)
# c = Coat Burgundy Main
# C = Coat Burgundy Highlight
# k = Coat Burgundy Shadow
# u = Shirt White
# U = Shirt Shadow

grid = [
    "................................", # 0
    "................................", # 1
    "............H...H...............", # 2  (Hair spikes top)
    "...........HHH.HHH..............", # 3
    "..........HHHHHHHHH.............", # 4
    ".........HHHHhhhhhhhhH..........", # 5
    "........HHHHhhhhhhhhhhH.........", # 6
    ".......HHHHhhhhhhhhhhhhH........", # 7
    "......HHHHhhhhhhhhhhhhhh........", # 8
    "......HHhhhhhhhhhhhhhhhhd.......", # 9
    ".....HHhhhhhhhhhhhhhhhhhdd......", # 10
    ".....Hhhhhsssssssssshhhhdd......", # 11
    ".....hhhhsssssssssssshhhdd......", # 12
    "....hhhhsssssssssssssshhdd......", # 13
    "....hhhssSssEssssEssSsshhdd.....", # 14  (Inner brows concerned/sad slant up at x=12 and x=17)
    "....hhhssSEEssssssEEssshhdd.....", # 15  (Outer/mid brows at x=10,11 and x=18,19)
    "....hhhssEwwEssssEwwEssshhdd....", # 16  (Top eyelash at x=9,12 and x=17,20; whites at x=10,11 and x=18,19)
    "....hhssSweewssssweewSsshhdd....", # 17  (Sad eyes: whites at x=9,12 and x=17,20; irises at x=10,11 and x=18,19)
    "....hhssSSeeSssssSSeeSsshhdd....", # 18  (Bottom iris at x=10,11 and x=18,19; eye shadow/border under eye)
    ".....hhssbssssssssssbssshd......", # 19  (Warm cheeks blush)
    ".....hhsssssssSSsssssssshd......", # 20  (Nose area)
    "......hssssssSSSSsssssshd.......", # 21  (Mouth/chin)
    "......hsssssssssssssssshd.......", # 22
    ".......hsssssSSSSssssshd........", # 23
    "............ssssSSSS............", # 24  (Slimmer Neck, 8 pixels wide)
    ".......kkkkUUuuuuUUkkkk.........", # 25  (Collar/Coat start)
    "......kkkkkuuuuuuuukkkkk........", # 26  (Shirt opening / Burgundy coat)
    ".....kkkkkCCuuuuuuckkkkkk.......", # 27  (Coat with top-left highlight 'C')
    "....kkkkkCCCuuuuucccckkkkkk.....", # 28
    "...kkkkkCCCCuuuuccccccckkkkk....", # 29
    "..kkkkkCCCCCuuuuccccccckkkkkk...", # 30
    "..kkkkkCCCCCUuUuccccccckkkkkk..."  # 31
]

# Ensure every line in grid is exactly 32 chars
for i, line in enumerate(grid):
    if len(line) != 32:
        print(f"Warning: Line {i} has length {len(line)}: {line}")

colors = {
    '.': (15, 23, 42),       # Dark Navy background
    'h': (101, 67, 33),      # Hair main brown
    'H': (138, 97, 58),      # Hair highlight
    'd': (65, 42, 20),       # Hair shadow
    's': (252, 215, 190),    # Skin main
    'S': (222, 172, 142),    # Skin shadow
    'b': (242, 180, 160),    # Skin warm / blush
    'w': (245, 245, 245),    # Eye white
    'e': (110, 65, 45),      # Eye iris (warm brown)
    'E': (45, 25, 10),       # Eye lash/brow (dark brown/black)
    'c': (100, 15, 35),      # Coat burgundy main
    'C': (135, 25, 50),      # Coat burgundy highlight
    'k': (65, 8, 22),        # Coat burgundy shadow
    'u': (255, 255, 255),    # Shirt white
    'U': (200, 200, 205),    # Shirt shadow
}

pixels = []
for y in range(32):
    row_chars = grid[y]
    for x in range(32):
        char = row_chars[x]
        color = colors.get(char, (15, 23, 42))
        pixels.append(color)

os.makedirs('/Users/amandachappell/Development/character-chat/scratch', exist_ok=True)
write_png('/Users/amandachappell/Development/character-chat/scratch/doctor_temp.png', 32, 32, pixels)
print("Wrote corrected doctor_temp.png (32x32)")
