import sys
import platform
import importlib

def check_system():
    print("="*50)
    print(f"OpenF.R.I.D.A.Y. Diagnostic Report")
    print("="*50)
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Virtual Env: {sys.prefix != sys.base_prefix}")
    print("-"*50)
    
    modules = [
        ('yaml', 'PyYAML', 'Configuration'),
        ('psutil', 'psutil', 'System Monitor'),
        ('numpy', 'NumPy', 'Calculations'),
        ('cv2', 'OpenCV', 'Vision'),
        ('pygame', 'Pygame', 'HUD Display'),
        ('speech_recognition', 'SpeechRecognition', 'Voice Input'),
        ('pyaudio', 'PyAudio', 'Audio I/O'),
        ('pyttsx3', 'pyttsx3', 'Voice Output'),
        ('keyboard', 'Keyboard', 'Hotkeys'),
        ('threading', 'Threading', 'Concurrency'),
        ('time', 'Time', 'Timing'),
        ('logging', 'Logging', 'Debug')
    ]
    
    all_good = True
    
    for module_name, display_name, purpose in modules:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {display_name:20} {version:12} - {purpose}")
        except ImportError as e:
            print(f"❌ {display_name:20} FAILED - {purpose}")
            print(f"   Error: {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️ {display_name:20} ISSUE - {purpose}")
            print(f"   Error: {e}")
    
    print("-"*50)
    
    # Test audio hardware
    print("\nTesting Audio Hardware:")
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        print(f"✅ PyAudio initialized - Found {device_count} audio devices")
        
        # Check for input devices
        has_input = False
        for i in range(device_count):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                has_input = True
                print(f"   - Input device found: {device_info['name']}")
        if not has_input:
            print("⚠️ No input devices found - microphone won't work")
        
        p.terminate()
    except Exception as e:
        print(f"❌ PyAudio hardware test failed: {e}")
    
    # Test text-to-speech
    print("\nTesting Text-to-Speech:")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"✅ pyttsx3 initialized - {len(voices)} voices available")
        engine.stop()
    except Exception as e:
        print(f"❌ pyttsx3 test failed: {e}")
    
    # Test pygame display (non-blocking)
    print("\nTesting Pygame Display:")
    try:
        import pygame
        pygame.display.init()
        print(f"✅ Pygame display initialized - SDL version: {pygame.get_sdl_version()}")
        pygame.display.quit()
    except Exception as e:
        print(f"❌ Pygame display test failed: {e}")
    
    print("="*50)
    
    if all_good:
        print("\n🎉 All modules loaded successfully! You're ready to run F.R.I.D.A.Y.")
    else:
        print("\n⚠️ Some modules failed. Let's fix them!")
    
    return all_good

if __name__ == "__main__":
    check_system()
