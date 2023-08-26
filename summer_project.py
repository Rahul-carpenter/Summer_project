import tkinter as tk
import os
import boto3
import uuid
import pywhatkit
from tkinter import simpledialog
import speech_recognition as sr
import datetime as dt
import cv2
import time
from instabot import Bot

# Initialize AWS clients
myec2 = boto3.client("ec2")
s3_client = boto3.client('s3')

# Initialize Instagram bot (you need to provide your credentials)
#bot = Bot()
#bot.login(username="your_username", password="your_password")

# Global variables
voice_assistance_button = None

def create_basic_window():
    global voice_assistance_button
    root = tk.Tk()
    root.title("Feature-Controlled Assistant")
    root.geometry("400x650")
    
    label = tk.Label(root, text="Feature-Controlled Assistant", font=("Helvetica", 16, "bold"))
    label.pack(pady=10)

    date = dt.datetime.now()
    date_label = tk.Label(root, text="Date: %s" % date.strftime("%Y-%m-%d %H:%M:%S"))
    date_label.pack()

    voice_assistance_button = tk.Button(root, text="Voice Assistance", command=enable_voice_assistance)
    voice_assistance_button.pack(pady=20)

    options = [
        ("Email", on_button_email),
        ("EC2", on_button_ec2),
        ("Add S3 Bucket", s3_bucket_create),
        ("Notepad", on_button_click),
        ("Chrome", on_click),
        ("Paint", on_click_paint),
        ("Word", on_click_word),
        ("Play on YouTube", youtube_music),
        ("Take Photo", take_photo),
    ]

    for option_text, command in options:
        button = tk.Button(root, text=option_text, command=command)
        button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", width=10, fg="#fff", bg="#f00", command=root.destroy)
    exit_button.pack(pady=10)

    root.mainloop()

    # ... (Rest of the GUI setup)

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print(f"User said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError:
        print("There was a problem with the speech recognition service.")
        return None
    # ... (Voice input handling)

def enable_voice_assistance():
    global voice_assistance_button

    voice_assistance_button.config(state=tk.DISABLED)
    user_input = get_voice_input()
    if user_input:
        process_voice_command(user_input)
    voice_assistance_button.config(state=tk.ACTIVE)
    # ... (Enabling voice assistance)

def process_voice_command(command):
    if "email" in command:
        on_button_email()
    elif "EC2" in command:
        on_button_ec2()
    elif "notepad" in command:
        on_button_click()
    elif "chrome" in command:
        on_click()
    elif "paint" in command:
        on_click_paint()
    elif "word" in command:
        on_click_word()
    elif "play on YouTube" in command:
        youtube_music()
        
    else:
        print("Command not recognized.")

    # ... (Processing voice commands)

def on_button_ec2():
    instance_info = create_ec2_instance()
    if instance_info:
        print("EC2 instance created successfully!")
        print(f"Instance ID: {instance_info['InstanceId']}")
    else:
        print("Failed to create EC2 instance.")

def create_ec2_instance():
    try:
        ec2_client = boto3.client('ec2')
        response = ec2_client.run_instances(
            ImageId='ami-0ded8326293d3201b',
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1
        )

        if 'Instances' in response and len(response['Instances']) > 0:
            return response['Instances'][0]
        else:
            return None
    except Exception as e:
        print("An error occurred while creating the EC2 instance:", str(e))
        return None

def on_button_email():
    msg = "Hello from python"
    recipient_email = get_voice_input()
    if not recipient_email:  # If voice input fails, use text-based input dialog
        recipient_email = simpledialog.askstring("Input", "Enter recipient's email address:")
    if recipient_email:
        pywhatkit.send_mail("testprect@gmail.com", "aljeobaueiacqtko", "test code",msg, recipient_email)
    # ... (Sending email)

def on_button_click():
    os.system("notepad")

def on_click():
    os.system("start chrome")

def on_click_paint():
    os.system("start mspaint")

def on_click_word():
    os.system("start winword")

def s3_bucket_create():
    ec2_client = boto3.client('ec2')
    response_ec2 = ec2_client.describe_instances()

    # Create an S3 Instance
    s3_client = boto3.client('s3')
    s3_client = boto3.client('s3')
    
    bucket_name = f"my-bucket-{uuid.uuid4()}"  # Generate a unique bucket name using UUID
    
    response = s3_client.create_bucket(
        ACL='private',  # Use 'private' instead of 'enabled' for private ACL
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'  # Use the region code, not the region name
        }
    )
    print(f"S3 bucket '{bucket_name}' created.")

    

def youtube_music():
    song_name = get_voice_input()
    if song_name:
        print(f"Playing {song_name} on YouTube")
        pywhatkit.playonyt(song_name)
    else:
        print("No song name provided.")
    

def take_photo():
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    ret, frame = cap.read()
    if ret:
        cv2.imshow('photo.jpg', frame)
        cv2.imwrite('photo.jpg', frame)
        cap.release()
        cv2.destroyAllWindows()

def post_to_instagram():
    caption = get_voice_input()
    if caption:
        image_path = "photo.jpg"  # Assuming the photo is captured earlier
        bot.upload_photo(image_path, caption=caption)
        print("Photo uploaded to Instagram!")

# Create the GUI window
create_basic_window()
