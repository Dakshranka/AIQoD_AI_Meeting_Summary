import sounddevice as sd
import numpy as np
import wave
import os
import psutil
import pygetwindow as gw
import pyautogui
import keyboard  # ✅ Allows manual stopping with a key press

# Audio settings
SAMPLE_RATE = 44100  # CD-quality audio
CHANNELS = 2  # Stereo
CHUNK_DURATION = 10  # Record in 10-second chunks (adjust as needed)
OUTPUT_DIR = "live_recordings"
DEVICE_NAME = "Stereo Mix"  # Change this based on your system (use `sd.query_devices()` to check)

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Paths to Zoom & Google Meet controls screenshots
ZOOM_IMAGE_PATH = os.path.abspath("backend/zoom_controls.png")
MEET_IMAGE_PATH = os.path.abspath("backend/google_meet_controls.png")

def is_meeting_active():
    """Check if a Zoom or Google Meet meeting is happening."""
    meeting_apps = ["zoom.exe", "chrome.exe"]  # Chrome for Google Meet
    running_meeting_apps = [p.info['name'].lower() for p in psutil.process_iter(attrs=['name'])]

    zoom_running = any("zoom.exe" in app for app in running_meeting_apps)
    chrome_running = any("chrome.exe" in app for app in running_meeting_apps)

    if not zoom_running and not chrome_running:
        print("⚠ No Active Meeting Apps Detected.")
        return False

    zoom_windows = [win for win in gw.getWindowsWithTitle("Zoom Meeting")]
    if zoom_running and not zoom_windows:
        print("⚠ Zoom is running, but no active meeting window detected.")
        return False

    meet_tabs = [win for win in gw.getWindowsWithTitle("Meet")]
    if chrome_running and not meet_tabs:
        print("⚠ Google Meet is not active in Chrome.")
        return False

    try:
        if os.path.exists(ZOOM_IMAGE_PATH):
            zoom_controls = pyautogui.locateOnScreen(ZOOM_IMAGE_PATH, confidence=0.4)
            if zoom_controls:
                print("✅ Zoom meeting is active!")
                return True

        if os.path.exists(MEET_IMAGE_PATH):
            meet_controls = pyautogui.locateOnScreen(MEET_IMAGE_PATH, confidence=0.4)
            if meet_controls:
                print("✅ Google Meet meeting is active!")
                return True

    except Exception as e:
        print(f"⚠ Could not check screen controls: {e}")
        return False

    print("⚠ No active meeting detected.")
    return False

def is_audio_active(audio_data, threshold=100):
    """Check if system audio is active (someone is talking)."""
    mean_amplitude = np.abs(audio_data).mean()
    print(f"🔊 Audio Amplitude: {mean_amplitude}")
    return mean_amplitude > threshold

def record_meeting_audio(filename="live_meeting.wav"):
    """Continuously records until the meeting ends or user stops."""
    if not is_meeting_active():
        print("❌ No active meeting detected. Recording cancelled.")
        return None

    print("🎙 Recording Live Meeting Audio... (Press 'q' to stop manually)")

    output_path = os.path.join(OUTPUT_DIR, filename)
    
    try:
        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(SAMPLE_RATE)

            while is_meeting_active():  # ✅ Keeps recording until the meeting ends
                print("⏺ Recording chunk... Press 'q' to stop manually.")
                
                # Record for CHUNK_DURATION seconds
                audio_data = sd.rec(
                    int(CHUNK_DURATION * SAMPLE_RATE),
                    samplerate=SAMPLE_RATE,
                    channels=CHANNELS,
                    dtype=np.int16
                )
                sd.wait()

                # Check if audio is silent
                if not is_audio_active(audio_data):
                    print("⚠ No active audio detected! Waiting for sound...")
                    continue  # Skip writing if no audio is detected

                # Write recorded audio to file
                wf.writeframes(audio_data.tobytes())

                # Allow manual stopping with 'q'
                if keyboard.is_pressed("q"):
                    print("⏹ Manual stop triggered.")
                    break

        print(f"✅ Audio saved: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error capturing system audio: {e}")
        return None

if __name__ == "__main__":
    record_meeting_audio()
