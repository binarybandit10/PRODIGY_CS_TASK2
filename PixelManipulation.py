import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

def encrypt_image(image_path, key):
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()

    permutation = generate_permutation(width * height, key)

    encrypted_img = Image.new("RGB", (width, height))
    encrypted_pixels = encrypted_img.load()

    for i, pos in enumerate(permutation):
        x1, y1 = i % width, i // width
        x2, y2 = pos % width, pos // width
        encrypted_pixels[x2, y2] = pixels[x1, y1]

    encrypted_image_path = "encrypted_image.png"
    encrypted_img.save(encrypted_image_path)
    return encrypted_image_path

def decrypt_image(encrypted_image_path, key):
    img = Image.open(encrypted_image_path)
    width, height = img.size
    pixels = img.load()

    permutation = generate_permutation(width * height, key)
    inverse_permutation = [0] * (width * height)
    for i, pos in enumerate(permutation):
        inverse_permutation[pos] = i

    decrypted_img = Image.new("RGB", (width, height))
    decrypted_pixels = decrypted_img.load()

    for i, pos in enumerate(inverse_permutation):
        x1, y1 = i % width, i // width
        x2, y2 = pos % width, pos // width
        decrypted_pixels[x2, y2] = pixels[x1, y1]

    decrypted_image_path = "decrypted_image.png"
    decrypted_img.save(decrypted_image_path)
    return decrypted_image_path

def generate_permutation(size, key):
    permutation = list(range(size))
    random.seed(key)
    random.shuffle(permutation)
    return permutation

def browse_image():
    filename = filedialog.askopenfilename()
    if filename:
        original_image_path.set(filename)
        load_original_image(filename)

def load_original_image(image_path):
    img = Image.open(image_path)
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    original_label.config(image=img)
    original_label.image = img

def encrypt():
    image_path = original_image_path.get()
    key = int(key_entry.get())
    encrypted_image_path = encrypt_image(image_path, key)
    load_encrypted_image(encrypted_image_path)

def load_encrypted_image(image_path):
    img = Image.open(image_path)
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    encrypted_label.config(image=img)
    encrypted_label.image = img

def decrypt():
    encrypted_image_path = "encrypted_image.png"
    key = int(key_entry.get())
    decrypted_image_path = decrypt_image(encrypted_image_path, key)
    load_decrypted_image(decrypted_image_path)

def load_decrypted_image(image_path):
    img = Image.open(image_path)
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    decrypted_label.config(image=img)
    decrypted_label.image = img

root = tk.Tk()
root.title("Image Encryption")

original_image_path = tk.StringVar()

original_label = tk.Label(root, text="Original Image")
original_label.grid(row=0, column=0, padx=10, pady=10)

encrypted_label = tk.Label(root, text="Encrypted Image")
encrypted_label.grid(row=0, column=1, padx=10, pady=10)

decrypted_label = tk.Label(root, text="Decrypted Image")
decrypted_label.grid(row=0, column=2, padx=10, pady=10)

browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

key_label = tk.Label(root, text="Encryption/Decryption Key:")
key_label.grid(row=2, column=0, padx=10, pady=5)

key_entry = tk.Entry(root)
key_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.grid(row=3, column=0, padx=10, pady=5)

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
decrypt_button.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

root.mainloop()
