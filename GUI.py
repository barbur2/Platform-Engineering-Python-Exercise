import customtkinter as ctk
import boto3
from tkinter import messagebox
import botocore
ctk.set_default_color_theme("pink.json")


# --- AWS Session (באמצעות פרופיל קיים, בלי סודות בקוד) ---
session = boto3.Session(profile_name="default")
ec2 = session.client("ec2")
s3 = session.client("s3")
route53 = session.client("route53")

# --- הגדרות GUI ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("pink.json")   # 🌸 נושא ורוד מותאם אישית

app = ctk.CTk()
app.title("💖 Platform Princess GUI 🌸")
app.geometry("850x650")

# מכאן ממשיך כל הקוד שלך (טאבים, כפתורים, פונקציות boto3 וכו')
app.mainloop()