"""
================================================================================
        MINI DIGITAL NOTICE BOARD - Main Application
================================================================================
A beginner-friendly GUI application built with Python and Tkinter.
Perfect for school announcements and notices with timestamp tracking.

Author: Created for Computer Systems & Architecture Project
Level: 3 (Beginner)
Date: 2026
================================================================================
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import os
from threading import Thread

# Constants for file management
MESSAGES_FILE = "messages.txt"

# Constants for colors (making the app attractive)
PRIMARY_COLOR = "#2c3e50"      # Dark blue-gray for main window
SECONDARY_COLOR = "#3498db"    # Bright blue for buttons
SUCCESS_COLOR = "#27ae60"       # Green for success button
DANGER_COLOR = "#e74c3c"        # Red for clear/exit buttons
TEXT_COLOR = "#ecf0f1"         # Light color for text
ACCENT_COLOR = "#f39c12"        # Orange for title


# ============================================================================
# FUNCTION 1: Add a new message with timestamp
# ============================================================================
def add_message(message_text):
    """
    Add a new message to the messages file with current date and time.
    
    Parameters:
        message_text (str): The message content from input field
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not message_text.strip():
        messagebox.showwarning("Empty Message", "Please type a message first!")
        return False
    
    try:
        # Get current date and time in format: YYYY-MM-DD HH:MM:SS
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        
        # Create formatted message line
        formatted_message = f"{timestamp} {message_text.strip()}\n"
        
        # Append to messages.txt file (create if doesn't exist)
        with open(MESSAGES_FILE, "a", encoding="utf-8") as file:
            file.write(formatted_message)
        
        return True
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save message: {str(e)}")
        return False


# ============================================================================
# FUNCTION 2: Show all messages from the file
# ============================================================================
def show_messages():
    """
    Read and display all messages from messages.txt file.
    Shows them in the display area in the GUI.
    """
    try:
        # Check if file exists
        if not os.path.exists(MESSAGES_FILE):
            display_area.config(state=tk.NORMAL)
            display_area.delete(1.0, tk.END)
            display_area.insert(tk.END, "📋 No messages yet. Add your first message!")
            display_area.config(state=tk.DISABLED)
            update_message_count()
            return
        
        # Read all messages
        with open(MESSAGES_FILE, "r", encoding="utf-8") as file:
            messages = file.read()
        
        # Display in the text area
        display_area.config(state=tk.NORMAL)
        display_area.delete(1.0, tk.END)
        
        if messages.strip():
            display_area.insert(tk.END, "📌 All Notices (Newest at Bottom):\n")
            display_area.insert(tk.END, "─" * 60 + "\n\n")
            display_area.insert(tk.END, messages)
        else:
            display_area.insert(tk.END, "📋 No messages yet. Add your first message!")
        
        display_area.config(state=tk.DISABLED)
        update_message_count()
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read messages: {str(e)}")


# ============================================================================
# FUNCTION 3: Clear all messages with confirmation
# ============================================================================
def clear_messages():
    """
    Clear all messages from the file after asking for confirmation.
    Prevents accidental deletion of important notices.
    """
    # Ask for confirmation
    response = messagebox.askyesno(
        "Confirm Clear", 
        "⚠️ Are you sure you want to clear ALL messages?\nThis action cannot be undone!"
    )
    
    if response:  # User clicked "Yes"
        try:
            # Check if file exists
            if os.path.exists(MESSAGES_FILE):
                # Delete the file
                os.remove(MESSAGES_FILE)
            
            # Clear the display area
            display_area.config(state=tk.NORMAL)
            display_area.delete(1.0, tk.END)
            display_area.insert(tk.END, "📋 All messages cleared!")
            display_area.config(state=tk.DISABLED)
            
            # Update counter
            update_message_count()
            
            # Show success message
            messagebox.showinfo("Success", "✅ All messages have been cleared!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear messages: {str(e)}")


# ============================================================================
# FUNCTION 4: Update live clock
# ============================================================================
def update_clock():
    """
    Update the clock display every second.
    Runs in a separate thread to not freeze the GUI.
    """
    def clock_thread():
        while True:
            try:
                # Get current time
                current_time = datetime.now().strftime("%H:%M:%S")
                current_date = datetime.now().strftime("%A, %d %B %Y")
                
                # Update label (thread-safe)
                clock_label.config(text=f"🕐 {current_time} | {current_date}")
                
                # Wait 1 second before next update
                root.after(1000, lambda: None)
                
            except:
                break
    
    # Start clock update in background thread
    thread = Thread(target=clock_thread, daemon=True)
    thread.start()


# ============================================================================
# FUNCTION 5: Count and update total messages
# ============================================================================
def update_message_count():
    """
    Count the total number of messages and update the counter label.
    """
    try:
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, "r", encoding="utf-8") as file:
                count = len(file.readlines())
        else:
            count = 0
        
        # Update the counter label
        counter_label.config(text=f"📊 Total Messages: {count}")
    
    except:
        counter_label.config(text="📊 Total Messages: 0")


# ============================================================================
# FUNCTION 6: Handle Add Message button click
# ============================================================================
def on_add_message():
    """
    Handler for the Add Message button.
    Gets text from input field, saves it, and shows confirmation.
    """
    message = message_input.get()
    
    if add_message(message):
        # Success! Clear input field
        message_input.delete(0, tk.END)
        messagebox.showinfo("Success", "✅ Message added successfully!")
        
        # Automatically show the updated messages
        show_messages()
    
    # Focus back to input field for quick typing
    message_input.focus()


# ============================================================================
# FUNCTION 7: Exit application
# ============================================================================
def exit_app():
    """
    Close the application safely.
    Shows confirmation dialog.
    """
    response = messagebox.askyesno("Exit", "Exit the Mini Digital Notice Board?")
    if response:
        root.destroy()


# ============================================================================
# MAIN GUI SETUP
# ============================================================================

# Create main window
root = tk.Tk()
root.title("Mini Digital Notice Board - School Announcement System")
root.geometry("800x650")
root.configure(bg=PRIMARY_COLOR)

# Make window non-resizable for consistent layout (optional)
root.resizable(False, False)

# ============================================================================
# TOP SECTION: Title and Clock
# ============================================================================

# Title frame
title_frame = tk.Frame(root, bg=ACCENT_COLOR, height=100)
title_frame.pack(fill=tk.X, pady=0)
title_frame.pack_propagate(False)

# Main title
title_label = tk.Label(
    title_frame,
    text="📢 MINI DIGITAL NOTICE BOARD",
    font=("Arial", 24, "bold"),
    bg=ACCENT_COLOR,
    fg="white"
)
title_label.pack(pady=(15, 5))

# Subtitle (School name)
subtitle_label = tk.Label(
    title_frame,
    text="🏫 Central High School - Announcement System",
    font=("Arial", 12, "italic"),
    bg=ACCENT_COLOR,
    fg="white"
)
subtitle_label.pack(pady=(0, 10))

# Clock display
clock_label = tk.Label(
    title_frame,
    text="🕐 Loading...",
    font=("Arial", 10),
    bg=ACCENT_COLOR,
    fg="white"
)
clock_label.pack(pady=(0, 10))

# Start the clock update
root.after(500, update_clock)

# ============================================================================
# MIDDLE SECTION: Input Area
# ============================================================================

# Input frame
input_frame = tk.Frame(root, bg=PRIMARY_COLOR)
input_frame.pack(fill=tk.X, padx=15, pady=15)

# Input label
input_label = tk.Label(
    input_frame,
    text="📝 Type Your Message:",
    font=("Arial", 12, "bold"),
    bg=PRIMARY_COLOR,
    fg=TEXT_COLOR
)
input_label.pack(anchor=tk.W, pady=(0, 5))

# Input field
message_input = tk.Entry(
    input_frame,
    font=("Arial", 11),
    bg="#ecf0f1",
    fg=PRIMARY_COLOR,
    relief=tk.FLAT,
    bd=0,
    height=2
)
message_input.pack(fill=tk.X, ipady=10, pady=(0, 10))

# Bind Enter key to add message quickly
message_input.bind("<Return>", lambda event: on_add_message())

# ============================================================================
# BUTTONS SECTION
# ============================================================================

# Button frame
button_frame = tk.Frame(root, bg=PRIMARY_COLOR)
button_frame.pack(fill=tk.X, padx=15, pady=10)

# Add Message button (Green - Success)
add_btn = tk.Button(
    button_frame,
    text="✅ Add Message",
    command=on_add_message,
    font=("Arial", 11, "bold"),
    bg=SUCCESS_COLOR,
    fg="white",
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=10,
    cursor="hand2"
)
add_btn.pack(side=tk.LEFT, padx=5)

# Show Messages button (Blue - Primary)
show_btn = tk.Button(
    button_frame,
    text="👁️ Show Messages",
    command=show_messages,
    font=("Arial", 11, "bold"),
    bg=SECONDARY_COLOR,
    fg="white",
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=10,
    cursor="hand2"
)
show_btn.pack(side=tk.LEFT, padx=5)

# Clear Messages button (Red - Danger)
clear_btn = tk.Button(
    button_frame,
    text="🗑️ Clear All",
    command=clear_messages,
    font=("Arial", 11, "bold"),
    bg=DANGER_COLOR,
    fg="white",
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=10,
    cursor="hand2"
)
clear_btn.pack(side=tk.LEFT, padx=5)

# Exit button
exit_btn = tk.Button(
    button_frame,
    text="❌ Exit",
    command=exit_app,
    font=("Arial", 11, "bold"),
    bg="#95a5a6",
    fg="white",
    relief=tk.FLAT,
    bd=0,
    padx=15,
    pady=10,
    cursor="hand2"
)
exit_btn.pack(side=tk.RIGHT, padx=5)

# ============================================================================
# DISPLAY AREA: Messages Display with Scrollbar
# ============================================================================

# Display frame
display_frame = tk.Frame(root, bg=PRIMARY_COLOR)
display_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# Display label
display_label = tk.Label(
    display_frame,
    text="📋 All Notices:",
    font=("Arial", 12, "bold"),
    bg=PRIMARY_COLOR,
    fg=TEXT_COLOR
)
display_label.pack(anchor=tk.W, pady=(0, 5))

# Display area with scrollbar
display_area = scrolledtext.ScrolledText(
    display_frame,
    font=("Arial", 10),
    bg="#ecf0f1",
    fg=PRIMARY_COLOR,
    relief=tk.FLAT,
    bd=0,
    wrap=tk.WORD,
    height=12
)
display_area.pack(fill=tk.BOTH, expand=True)
display_area.config(state=tk.DISABLED)  # Read-only

# ============================================================================
# FOOTER SECTION: Message Counter
# ============================================================================

# Footer frame
footer_frame = tk.Frame(root, bg=PRIMARY_COLOR)
footer_frame.pack(fill=tk.X, padx=15, pady=10)

# Counter label
counter_label = tk.Label(
    footer_frame,
    text="📊 Total Messages: 0",
    font=("Arial", 10, "bold"),
    bg=PRIMARY_COLOR,
    fg=ACCENT_COLOR
)
counter_label.pack(side=tk.LEFT)

# Info label
info_label = tk.Label(
    footer_frame,
    text="💡 Tip: Press Enter to quickly add a message",
    font=("Arial", 9, "italic"),
    bg=PRIMARY_COLOR,
    fg="#95a5a6"
)
info_label.pack(side=tk.RIGHT)

# ============================================================================
# STARTUP: Load existing messages and set focus
# ============================================================================

# Load and display existing messages on startup
root.after(100, show_messages)

# Set focus to input field
message_input.focus()

# ============================================================================
# START THE APPLICATION
# ============================================================================

if __name__ == "__main__":
    root.mainloop()
