import logging
import random
import os

# Try to import openai, but don't fail if it's not available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None
    print("Note: OpenAI not installed. Using mock responses.")

class AIProcessor:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Mock responses for testing without API
        self.mock_responses = [
            "I'm analyzing that now, boss.",
            "Systems indicate that's correct.",
            "I've added that to your task list.",
            "Would you like me to run a diagnostic?",
            "Interesting. I'll make a note of that.",
            "My sensors don't show any issues with that.",
            "Processing that request now.",
            "I'm on it.",
            "Consider it done.",
            "I'll take care of that right away."
        ]
        
        # Initialize OpenAI if available
        if OPENAI_AVAILABLE and config.get('provider') == 'openai':
            try:
                # You can set your API key in environment variable
                api_key = os.getenv('OPENAI_API_KEY')
                if api_key:
                    openai.api_key = api_key
                    self.logger.info("OpenAI initialized with API key")
                else:
                    self.logger.warning("OPENAI_API_KEY not set in environment")
            except Exception as e:
                self.logger.error(f"Failed to initialize OpenAI: {e}")
        
        self.logger.info(f"AI Processor initialized with {config.get('provider', 'mock')}")
    
    def process(self, text):
        """Process text through AI"""
        self.logger.debug(f"Processing: {text}")
        
        # Check for specific commands first
        text_lower = text.lower()
        
        # Time queries
        if "time" in text_lower:
            import datetime
            now = datetime.datetime.now()
            return f"The current time is {now.strftime('%I:%M %p')}."
        
        # Date queries
        if "date" in text_lower or "day" in text_lower:
            import datetime
            now = datetime.datetime.now()
            return f"Today is {now.strftime('%A, %B %d, %Y')}."
        
        # System queries are handled in main.py, but provide fallbacks
        if "status" in text_lower or "systems" in text_lower:
            return "All systems are functioning within normal parameters."
        
        if "sensors" in text_lower:
            return "All sensors are online and reporting normally."
        
        # Try OpenAI if available and configured
        if OPENAI_AVAILABLE and self.config.get('provider') == 'openai' and openai.api_key:
            try:
                return self._query_openai(text)
            except Exception as e:
                self.logger.error(f"OpenAI query failed: {e}")
                return self._get_mock_response(text)
        
        # Fallback to mock responses
        return self._get_mock_response(text)
    
    def _query_openai(self, text):
        """Query OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model=self.config.get('model', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "You are F.R.I.D.A.Y., Tony Stark's AI assistant. Respond in character as a helpful, efficient, and slightly witty AI. Keep responses concise and helpful."},
                    {"role": "user", "content": text}
                ],
                max_tokens=self.config.get('max_tokens', 150),
                temperature=self.config.get('temperature', 0.7)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise
    
    def _get_mock_response(self, text):
        """Get a mock response based on the input"""
        # Try to give somewhat relevant mock responses
        text_lower = text.lower()
        
        if "hello" in text_lower or "hi" in text_lower:
            return "Hello, boss. Good to hear from you."
        
        if "thank" in text_lower:
            return "You're welcome. Happy to help."
        
        if "joke" in text_lower:
            return "Why did the Iron Man suit go to therapy? It had too many unresolved issues with its arc reactor. ...I'll work on my comedy programming."
        
        if "weather" in text_lower:
            return "I'm afraid I don't have access to weather satellites from this terminal, boss."
        
        # Default random response
        return random.choice(self.mock_responses)
    
    def analyze_image(self, image_path):
        """Analyze an image (for camera module)"""
        self.logger.debug(f"Analyzing image: {image_path}")
        
        # Check if OpenCV is available for basic image analysis
        try:
            import cv2
            img = cv2.imread(image_path)
            if img is None:
                return "I couldn't read that image file."
            
            height, width = img.shape[:2]
            return f"I detect an image with dimensions {width}x{height} pixels. For more detailed analysis, I'd need additional vision modules."
        except:
            return "I detected an image, but detailed vision analysis requires additional modules."
