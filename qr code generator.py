import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk

def generate_qr():
    data = entry.get()
    if data.strip() == "":
        messagebox.showwarning("Input Error", "Please enter some data to generate QR Code.")
        return
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code
    img.save("qr_code.png")

    # Display the QR code
    img_display = Image.open("qr_code.png")
    img_display = img_display.resize((200, 200))
    qr_img = ImageTk.PhotoImage(img_display)
    qr_label.config(image=qr_img)
    qr_label.image = qr_img

# GUI setup
window = tk.Tk()
window.title("QR Code Generator")
window.geometry("500x400")
window.configure(bg="pink")

# Instruction Title
title_label = tk.Label(window, text="Enter Data to Generate QR Code:", font=("Arial", 16, "bold"),
                       fg="white", bg="purple", pady=10, padx=10)
title_label.pack(pady=20)

# Entry field
entry = tk.Entry(window, font=("Arial", 14), width=30)
entry.pack(pady=10)

# Button
generate_button = tk.Button(window, text="Generate QR Code", command=generate_qr, font=("Arial", 12))
generate_button.pack(pady=10)

# Label to show QR Code
qr_label = tk.Label(window, bg="pink")
qr_label.pack(pady=10)

window.mainloop()
