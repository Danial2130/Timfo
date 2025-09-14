from PIL import Image, ImageDraw, ImageFont
import datetime
import os

# --- 1. Buka template ---
template_path = "templates/1.png"
template = Image.open(template_path).convert("RGBA")

# --- 2. Tentukan slot (x, y, width, height) ---
slots = [
    (127, 551, 406, 571),   # Slot 1
    (599, 1012, 406, 571),  # Slot 2
]

# --- 3. Ambil foto dari folder input ---
input_dir = "input"
foto_files = sorted(os.listdir(input_dir))[:len(slots)]  # ambil sesuai jumlah slot

for i, foto_file in enumerate(foto_files):
    foto_path = os.path.join(input_dir, foto_file)
    foto = Image.open(foto_path).convert("RGBA")

    # Resize foto sesuai slot
    x, y, w, h = slots[i]
    foto_resized = foto.resize((w, h))

    # Tambah border putih
    border_size = 8
    bordered = Image.new("RGBA", (w + 2*border_size, h + 2*border_size), "white")
    bordered.paste(foto_resized, (border_size, border_size))

    # Tempel ke template
    template.paste(bordered, (x - border_size, y - border_size), bordered)

# --- 4. Tambahkan tanggal otomatis ---
draw = ImageDraw.Draw(template)
today = datetime.datetime.now().strftime("%d %B %Y").upper()  # kapital semua

# Font Childos Arabic (atau fallback kalau font tidak support angka)
try:
    font = ImageFont.truetype("fonts/WinkyRough-VariableFont_wght.ttf", 50)
except:
    font = ImageFont.load_default()
    print("⚠️ Font tidak ditemukan, pakai font default.")

# Hitung lebar teks biar center di X=540
bbox = draw.textbbox((0, 0), today, font=font)
text_width = bbox[2] - bbox[0]
center_x = 540
y = 400 - 6 - 10  # naik 6 + 10 = 16px lebih atas
x = center_x - (text_width // 2)

# Tulis teks dengan warna coklat + stroke putih lebih tebal
draw.text(
    (x, y),
    today,
    fill="#7b4000",
    font=font,
    stroke_width=3,   # tebal stroke
    stroke_fill="white"
)

# --- 5. Simpan hasil dengan nama unik ---
os.makedirs("output", exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"output/hasil_{timestamp}.png"
template.save(output_path)

print(f"Hasil disimpan di {output_path}")
