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

def adjust_color(color, factor):
    r, g, b = color
    return (
        max(0, min(255, int(r * factor))),
        max(0, min(255, int(g * factor))),
        max(0, min(255, int(b * factor)))
    )

def make_gradient(width, height, start_color, end_color):
    pixels = []
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    for y in range(height):
        for x in range(width):
            t = (x + y) / (width + height - 2) if (width + height - 2) > 0 else 0
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            pixels.append((r, g, b))
    return pixels

# Define the 15 Doctors
doctors = {
    1: {
        "name": "First Doctor",
        "bg_start": (13, 27, 42),
        "bg_end": (59, 76, 106),
        "colors": {
            "h": (224, 224, 224), # White hair
            "s": (252, 208, 180), # Skin
            "e": (40, 40, 40),     # Eyes
            "c": (33, 33, 33),     # Black coat
            "u": (255, 255, 255), # White shirt
            "t": (10, 10, 10),     # Black cravat
            "a": (141, 110, 99),  # Brown cane
            "d": (255, 215, 0),   # Gold handle
        },
        "grid": [
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hHssssssHh....",
            "..hHssssssHh....",
            "..hHsesessHh....",
            "...hssssssh.....",
            "....hssssh......",
            ".....uuuu.......",
            "....ccCccc......",
            "...ccCccCcc.....",
            "..ccCccCcCcc....",
            "..ccCccCcCccd...",
            ".ccCccCcCccca...",
            ".ccCccCcCccca...",
            "ccCccCcCcccaa...",
            "ccCccCcCcccaa..."
        ]
    },
    2: {
        "name": "Second Doctor",
        "bg_start": (49, 27, 146),
        "bg_end": (103, 58, 183),
        "colors": {
            "h": (28, 28, 28),     # Shaggy black hair
            "s": (253, 217, 181), # Skin
            "e": (21, 101, 192),  # Blue eyes
            "c": (62, 39, 35),     # Dark coat
            "u": (227, 242, 253), # Light blue shirt
            "a": (205, 133, 63),  # Tan recorder
        },
        "grid": [
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hHssssssHh....",
            "..hHssssssHh....",
            "..hHsesessHh....",
            "...hssssssh.....",
            "....hsssah......",
            ".....uuua.......",
            "....ccCcac......",
            "...ccCccCac.....",
            "..ccCccCcCcc....",
            "..ccCccCcCcc....",
            ".ccCccCcCccc....",
            ".ccCccCcCccc....",
            "ccCccCcCcccc....",
            "ccCccCcCcccc...."
        ]
    },
    3: {
        "name": "Third Doctor",
        "bg_start": (74, 20, 140),
        "bg_end": (156, 39, 176),
        "colors": {
            "h": (236, 239, 241), # White curly hair
            "s": (252, 208, 180), # Skin
            "e": (46, 125, 50),   # Green eyes
            "c": (136, 14, 79),   # Velvet purple cape
            "d": (21, 21, 21),     # Black suit
            "u": (255, 255, 255), # White ruffled shirt
        },
        "grid": [
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hHssssssHh....",
            "..hHssssssHh....",
            "..hHsesessHh....",
            "...hssssssh.....",
            "....hssssh......",
            ".....uuuu.......",
            "....cdddddc.....",
            "...ccdddddcc....",
            "..cccdddddccc...",
            "..cccdddddccc...",
            ".ccccdddddcccc..",
            ".ccccdddddcccc..",
            "cccccdddddccccc.",
            "cccccdddddccccc."
        ]
    },
    4: {
        "name": "Fourth Doctor",
        "bg_start": (230, 81, 0),
        "bg_end": (255, 152, 0),
        "colors": {
            "h": (78, 52, 46),     # Brown curly hair
            "s": (253, 217, 181), # Skin
            "e": (21, 101, 192),  # Blue eyes
            "c": (93, 64, 55),     # Brown coat
            "a": (253, 216, 53),  # Yellow scarf stripe
            "d": (211, 47, 47),   # Red scarf stripe
            "t": (46, 125, 50),   # Green scarf stripe
        },
        "grid": [
            "...hhhhhhhh.....",
            "..hhhhhhhhhh....",
            ".hhHssssssHhh...",
            ".hhHssssssHhh...",
            ".hhHsesessHhh...",
            "..hhsssssshh....",
            "...hssssssh.....",
            "....adtadt......",
            "....ccCccc......",
            "...accCccc......",
            "..dccCccCcc.....",
            "..tccCccCcc.....",
            ".adccCccCccc....",
            ".taccCccCccc....",
            "dttccCccCcccc...",
            "addccCccCcccc..."
        ]
    },
    5: {
        "name": "Fifth Doctor",
        "bg_start": (27, 94, 32),
        "bg_end": (76, 175, 80),
        "colors": {
            "h": (255, 249, 196), # Blonde hair
            "s": (252, 208, 180), # Skin
            "e": (21, 101, 192),  # Blue eyes
            "c": (245, 245, 220), # Beige/cream coat
            "u": (255, 255, 255), # White shirt
            "a": (129, 199, 132), # Green celery
        },
        "grid": [
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hHssssssHh....",
            "..hHssssssHh....",
            "..hHsesessHh....",
            "...hssssssh.....",
            "....hssssh......",
            ".....uuuu.......",
            "....ccCccc......",
            "...cacCccc......",
            "..ccacCccCcc....",
            "..ccCcCccCcc....",
            ".ccCcCcCccCc....",
            ".ccCcCcCccCc....",
            "ccCcCcCccCccc...",
            "ccCcCcCccCccc..."
        ]
    },
    6: {
        "name": "Sixth Doctor",
        "bg_start": (0, 96, 100),
        "bg_end": (0, 151, 167),
        "colors": {
            "h": (255, 224, 130), # Yellow hair
            "s": (252, 208, 180), # Skin
            "e": (21, 101, 192),  # Blue eyes
            "u": (255, 255, 255), # White shirt
            "c": (229, 57, 53),   # Red patch
            "d": (255, 235, 59),  # Yellow patch
            "t": (0, 230, 118),   # Green patch
            "a": (216, 27, 96),   # Pink patch
        },
        "grid": [
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hHssssssHh....",
            "..hHssssssHh....",
            "..hHsesessHh....",
            "...hssssssh.....",
            "....hssssh......",
            ".....uuuu.......",
            "....cdaatc......",
            "...ccddttaa.....",
            "..ccddttaacc....",
            "..cddttaaccd....",
            ".ccddttaaccd....",
            ".cddttaacccd....",
            "ccddttaacccc....",
            "cddttaaccccc...."
        ]
    },
    7: {
        "name": "Seventh Doctor",
        "bg_start": (38, 50, 56),
        "bg_end": (69, 90, 100),
        "colors": {
            "h": (62, 39, 35),     # Brown hair
            "s": (253, 217, 181), # Skin
            "e": (62, 39, 35),     # Brown eyes
            "c": (78, 52, 46),     # Brown coat
            "d": (255, 224, 130), # Panama hat straw
            "t": (198, 40, 40),   # Hat band red
            "a": (183, 28, 28),   # Red umbrella handle
        },
        "grid": [
            ".....dddd.......",
            "....dddddd......",
            "...tttttttt.....",
            "..dddddddddd....",
            "...hsesessh.....",
            "...hssssssh.....",
            "....hssssh......",
            ".....uuuu.......",
            "....ccCccc......",
            "...ccCccCccaa...",
            "..ccCccCcCcc.a..",
            "..ccCccCcCccha..",
            ".ccCccCcCccaa...",
            ".ccCccCcCcc.a...",
            "ccCccCcCccc.a...",
            "ccCccCcCccc.a..."
        ]
    },
    8: {
        "name": "Eighth Doctor",
        "bg_start": (0, 77, 64),
        "bg_end": (0, 137, 123),
        "colors": {
            "h": (93, 64, 55),     # Long brown hair
            "s": (252, 208, 180), # Skin
            "e": (46, 125, 50),   # Green eyes
            "c": (0, 77, 64),      # Dark green coat
            "u": (255, 255, 255), # White shirt
            "t": (255, 213, 79),  # Gold cravat
        },
        "grid": [
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hhsssssshh....",
            "..hhsssssshh....",
            "..hhsesesshh....",
            "..hhsssssshh....",
            "...hssssssh.....",
            "....hssssh......",
            ".....utuu.......",
            "....ccCccc......",
            "...ccCccCcc.....",
            "..ccCccCcCcc....",
            "..ccCccCcCcc....",
            ".ccCccCcCccc....",
            ".ccCccCcCccc....",
            "ccCccCcCcccc...."
        ]
    },
    9: {
        "name": "Ninth Doctor",
        "bg_start": (33, 33, 33),
        "bg_end": (66, 66, 66),
        "colors": {
            "h": (28, 28, 28),     # Short black hair
            "s": (253, 217, 181), # Skin
            "e": (21, 101, 192),  # Blue eyes
            "c": (33, 33, 33),     # Black leather jacket
            "u": (74, 20, 140),    # V-neck purple sweater
        },
        "grid": [
            "................",
            "....hhhhhh......",
            "...hssssssh.....",
            "...hssssssh.....",
            "...hsesessh.....",
            "...hssssssh.....",
            "....hssssh......",
            ".....uuuu.......",
            "....cCuCcc......",
            "...ccCuCccc.....",
            "..ccCCuCCccc....",
            "..ccCcCcCccc....",
            ".ccCcCcCcccc....",
            ".ccCcCcCcccc....",
            "ccCcCcCccccc....",
            "ccCcCcCccccc...."
        ]
    },
    10: {
        "name": "Tenth Doctor",
        "bg_start": (13, 71, 161),
        "bg_end": (25, 118, 210),
        "colors": {
            "h": (93, 64, 55),     # Spiky brown hair
            "s": (252, 208, 180), # Skin
            "e": (62, 39, 35),     # Brown eyes
            "g": (10, 10, 10),     # Glasses
            "c": (121, 85, 72),    # Brown suit
            "u": (255, 255, 255), # White shirt
            "t": (2, 136, 209),   # Blue tie
        },
        "grid": [
            "...h..h..h......",
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hhsssssshh....",
            "..hhsgeseghh....",
            "...hssssssh.....",
            "....hssssh......",
            ".....utuu.......",
            "....cctccc......",
            "...ccCccCcc.....",
            "..ccCccCcCcc....",
            "..ccCccCcCcc....",
            ".ccCccCcCccc....",
            ".ccCccCcCccc....",
            "ccCccCcCcccc....",
            "ccCccCcCcccc...."
        ]
    },
    11: {
        "name": "Eleventh Doctor",
        "bg_start": (62, 39, 35),
        "bg_end": (93, 64, 55),
        "colors": {
            "h": (109, 76, 65),    # Floppy brown hair
            "s": (252, 208, 180), # Skin
            "e": (46, 125, 50),   # Green eyes
            "c": (141, 110, 99),  # Tweed brown jacket
            "u": (255, 255, 255), # White shirt
            "t": (198, 40, 40),   # Red bowtie
        },
        "grid": [
            "....hhhhhhh.....",
            "...hhhhhhhhh....",
            "..hhhhhhhhhh....",
            "..hhsssssshh....",
            "..hhsesesshh....",
            "..hHsssssshh....",
            "...Hssssssh.....",
            "....Hssssh......",
            ".....tut........",
            "....cccCcc......",
            "...ccCccCcc.....",
            "..ccCccCcCcc....",
            "..ccCccCcCcc....",
            ".ccCccCcCccc....",
            ".ccCccCcCccc....",
            "ccCccCcCcccc...."
        ]
    },
    12: {
        "name": "Twelfth Doctor",
        "bg_start": (26, 6, 6),
        "bg_end": (61, 12, 12),
        "colors": {
            "h": (236, 239, 241), # Grey hair
            "s": (253, 217, 181), # Skin
            "e": (21, 101, 192),  # Blue eyes
            "c": (26, 35, 126),    # Dark blue coat
            "d": (198, 40, 40),   # Red lining
            "u": (255, 255, 255), # White shirt
        },
        "grid": [
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hHssssssHh....",
            "..hHssssssHh....",
            "..hHsesessHh....",
            "...hssssssh.....",
            "....hssssh......",
            ".....uduu.......",
            "....cdcCcc......",
            "...cCdCcCcc.....",
            "..ccdduddcc.....",
            "..ccdduddcc.....",
            ".cccdduddccc....",
            ".cccdduddccc....",
            "ccccdduddcccc...",
            "ccccdduddcccc..."
        ]
    },
    13: {
        "name": "Thirteenth Doctor",
        "bg_start": (1, 87, 155),
        "bg_end": (2, 136, 209),
        "colors": {
            "h": (255, 241, 118), # Blonde bob hair
            "s": (252, 208, 180), # Skin
            "e": (46, 125, 50),   # Green eyes
            "c": (236, 239, 241), # Light grey coat
            "u": (26, 35, 126),    # Dark blue shirt
            "t": (255, 179, 0),   # Yellow suspenders
            "d": (229, 57, 53),   # Rainbow shirt stripe (red)
        },
        "grid": [
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hhhhhhhhhh....",
            "..hhsesesshh....",
            "..hhsssssshh....",
            "..hhsssssshh....",
            "..hhsssssshh....",
            ".....uuuu.......",
            "....cctutcc.....",
            "...cctutccc.....",
            "..ccctutcccc....",
            "..ccctutcccc....",
            ".cccctutccccc...",
            ".cccctutccccc...",
            "ccccctutcccccc..",
            "ccccctutcccccc.."
        ]
    },
    14: {
        "name": "Fourteenth Doctor",
        "bg_start": (21, 101, 192),
        "bg_end": (30, 136, 229),
        "colors": {
            "h": (93, 64, 55),     # Spiky brown hair
            "s": (252, 208, 180), # Skin
            "e": (62, 39, 35),     # Brown eyes
            "c": (21, 101, 192),  # Blue suit
            "u": (255, 255, 255), # White shirt
            "t": (211, 47, 47),   # Red tie
        },
        "grid": [
            "...h..h..h......",
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hhsssssshh....",
            "..hhsesesshh....",
            "...hssssssh.....",
            "....hssssh......",
            ".....utuu.......",
            "....cctccc......",
            "...ccCccCcc.....",
            "..ccCccCcCcc....",
            "..ccCccCcCcc....",
            ".ccCccCcCccc....",
            ".ccCccCcCccc....",
            "ccCccCcCcccc....",
            "ccCccCcCcccc...."
        ]
    },
    15: {
        "name": "Fifteenth Doctor",
        "bg_start": (12, 18, 38),     # Dark navy background start
        "bg_end": (24, 36, 70),       # Dark navy background end
        "colors": {
            "h": (15, 15, 15),        # Black natural hair
            "s": (115, 75, 45),       # Warm dark skin tone
            "e": (25, 20, 15),        # Brown eyes
            "c": (0, 150, 190),       # Bright teal/blue jacket
            "u": (255, 215, 0),       # Patterned shirt color 1 (yellow)
            "p": (235, 30, 110),      # Patterned shirt color 2 (pink)
            "o": (255, 100, 0),       # Patterned shirt color 3 (orange)
            "w": (255, 255, 255),     # White teeth for smile
        },
        "grid": [
            "....hhhhhh......",
            "...hhhhhhhh.....",
            "..hHssssssHh....",
            "..hHssssssHh....",
            "..hHsesessHh....",
            "...hssssssh.....",
            "....hswwsh......",
            ".....sSss.......",
            "....ccupcc......",
            "...ccCpoCcc.....",
            "..ccCcoucCcc....",
            "..ccCcupcCcc....",
            ".ccCccpoCccc....",
            ".ccCccouCccc....",
            "ccCcccupCccc....",
            "ccCcccpoCccc...."
        ]
    }
}

target_dir = "/Users/amandachappell/Development/character-chat/images/doctors"
os.makedirs(target_dir, exist_ok=True)

for num, data in doctors.items():
    name = data["name"]
    bg_start = data["bg_start"]
    bg_end = data["bg_end"]
    base_colors = data["colors"]
    grid = data["grid"]
    
    # Pre-populate 80x80 with diagonal gradient background
    pixels = make_gradient(80, 80, bg_start, bg_end)
    
    # Compile actual colors mapping (lower/uppercase)
    resolved_colors = {}
    for char, color in base_colors.items():
        if color is None:
            continue
        resolved_colors[char] = color
        # Automatically generate shadows/highlights for uppercase characters
        if char == "h": # hair shadow
            resolved_colors["H"] = adjust_color(color, 0.75)
        elif char == "s": # skin shadow
            resolved_colors["S"] = adjust_color(color, 0.82)
        elif char == "c": # coat highlight
            resolved_colors["C"] = adjust_color(color, 1.25)
        elif char == "u": # shirt shadow
            resolved_colors["U"] = adjust_color(color, 0.85)
        elif char == "t": # tie shadow
            resolved_colors["T"] = adjust_color(color, 0.8)
        elif char == "a": # accessory shadow
            resolved_colors["A"] = adjust_color(color, 0.8)
            
    # Draw drop shadow map at 16x16 grid level
    shadow_map = [[False] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            char = grid[y][x]
            if char == ".":
                # Check if there is a non-empty cell above-left
                if y >= 1 and x >= 1 and grid[y-1][x-1] != ".":
                    shadow_map[y][x] = True
                    
    # Draw shadows to 80x80 pixels list
    for y in range(16):
        for x in range(16):
            if grid[y][x] == "." and shadow_map[y][x]:
                for sub_y in range(5):
                    for sub_x in range(5):
                        px = x * 5 + sub_x
                        py = y * 5 + sub_y
                        idx = py * 80 + px
                        r, g, b = pixels[idx]
                        # Blend 45% black shadow
                        pixels[idx] = (int(r * 0.55), int(g * 0.55), int(b * 0.55))
                        
    # Draw character to 80x80 pixels list
    for y in range(16):
        for x in range(16):
            char = grid[y][x]
            if char != ".":
                color = resolved_colors.get(char, resolved_colors.get(char.lower(), (255, 255, 255)))
                for sub_y in range(5):
                    for sub_x in range(5):
                        px = x * 5 + sub_x
                        py = y * 5 + sub_y
                        idx = py * 80 + px
                        pixels[idx] = color
                        
    filename = os.path.join(target_dir, f"doctor-{num}.png")
    write_png(filename, 80, 80, pixels)
    print(f"Generated {filename} for {name}")
