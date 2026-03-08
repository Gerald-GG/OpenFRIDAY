import logging
import random
import os
import datetime
import requests
import json

# Try to import openai, but don't fail if it's not available
try:
    import openai
    OPENAI_AVAILABLE = True
    # Check OpenAI version
    import pkg_resources
    openai_version = pkg_resources.get_distribution("openai").version
    OPENAI_NEW_API = openai_version >= "1.0.0"
except (ImportError, pkg_resources.DistributionNotFound):
    OPENAI_AVAILABLE = False
    OPENAI_NEW_API = False
    openai = None
    print("Note: OpenAI not installed. Using mock responses.")

class AIProcessor:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # API keys (get these from environment variables)
        self.weather_api_key = os.getenv('WEATHER_API_KEY', '')
        self.news_api_key = os.getenv('NEWS_API_KEY', '')
        
        # Default location (can be changed by user)
        self.location = os.getenv('DEFAULT_LOCATION', 'New York')
        
        # Smart home devices (simulated for now)
        self.smart_devices = {
            'lights': {'state': 'off', 'brightness': 0},
            'thermostat': {'temperature': 72, 'mode': 'cool'},
            'tv': {'state': 'off', 'channel': 0},
            'music': {'state': 'off', 'volume': 50}
        }
        
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
                api_key = os.getenv('OPENAI_API_KEY')
                if api_key:
                    if OPENAI_NEW_API:
                        openai.api_key = api_key
                    else:
                        openai.api_key = api_key
                    self.logger.info(f"OpenAI initialized with API key (v{openai_version})")
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
        
        # ===== TIME AND DATE =====
        if "time" in text_lower:
            now = datetime.datetime.now()
            return f"The current time is {now.strftime('%I:%M %p')}."
        
        if "date" in text_lower or "day" in text_lower:
            now = datetime.datetime.now()
            return f"Today is {now.strftime('%A, %B %d, %Y')}."
        
        # ===== WEATHER COMMANDS =====
        if "weather" in text_lower or "temperature" in text_lower or "forecast" in text_lower:
            return self._get_weather(text_lower)
        
        # ===== NEWS COMMANDS =====
        if "news" in text_lower or "headlines" in text_lower or "what's happening" in text_lower:
            return self._get_news()
        
        # ===== SMART HOME COMMANDS =====
        if any(word in text_lower for word in ["light", "lights", "lamp"]):
            return self._control_lights(text_lower)
        
        if any(word in text_lower for word in ["thermostat", "temperature", "heat", "ac", "cool"]):
            return self._control_thermostat(text_lower)
        
        if any(word in text_lower for word in ["tv", "television", "channel"]):
            return self._control_tv(text_lower)
        
        if any(word in text_lower for word in ["music", "play", "song", "spotify"]):
            return self._control_music(text_lower)
        
        if "device status" in text_lower or "smart home status" in text_lower:
            return self._get_device_status()
        
        # ===== SYSTEM COMMANDS =====
        if "status" in text_lower or "systems" in text_lower:
            return "All systems are functioning within normal parameters."
        
        if "sensors" in text_lower:
            return "All sensors are online and reporting normally."
        
        # ===== JOKES & FUN =====
        if "joke" in text_lower:
            return self._tell_joke()
        
        # Try OpenAI if available and configured
        if OPENAI_AVAILABLE and self.config.get('provider') == 'openai' and openai.api_key:
            try:
                return self._query_openai(text)
            except Exception as e:
                self.logger.error(f"OpenAI query failed: {e}")
                return self._get_mock_response(text)
        
        # Fallback to mock responses
        return self._get_mock_response(text)
    
    def _get_weather(self, text):
        """Get weather information"""
        # Try to extract location from command
        location = self.location
        words = text.split()
        for i, word in enumerate(words):
            if word in ["in", "at", "for"] and i+1 < len(words):
                location = words[i+1].capitalize()
                break
        
        # If we have an API key, use real weather
        if self.weather_api_key:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}&units=imperial"
                response = requests.get(url)
                data = response.json()
                
                if response.status_code == 200:
                    temp = data['main']['temp']
                    description = data['weather'][0]['description']
                    humidity = data['main']['humidity']
                    return f"Currently in {location}: {temp:.0f}°F with {description}. Humidity is {humidity}%."
                else:
                    return f"I couldn't find weather data for {location}."
            except Exception as e:
                self.logger.error(f"Weather API error: {e}")
                return f"I'm having trouble reaching the weather service for {location}."
        else:
            # Mock weather response
            conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "clear"]
            temp = random.randint(60, 85)
            condition = random.choice(conditions)
            return f"Current weather in {location} is {condition} with a temperature of {temp}°F. (Note: This is simulated - set WEATHER_API_KEY for real data)"
    
    def _get_news(self):
        """Get news headlines"""
        if self.news_api_key:
            try:
                url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.news_api_key}"
                response = requests.get(url)
                data = response.json()
                
                if response.status_code == 200 and data['totalResults'] > 0:
                    headlines = [article['title'] for article in data['articles'][:3]]
                    return f"Here are today's top headlines: {' '.join(headlines)}"
                else:
                    return "I couldn't fetch the news at this moment."
            except Exception as e:
                self.logger.error(f"News API error: {e}")
                return "I'm having trouble connecting to the news service."
        else:
            # Mock news
            headlines = [
                "Tech company announces breakthrough in AI",
                "Scientists discover new renewable energy source",
                "Local hero builds working Iron Man suit",
                "Space exploration mission successful",
                "New smart home technology revolutionizes living"
            ]
            selected = random.sample(headlines, 3)
            return f"Here are some headlines: {selected[0]}. {selected[1]}. {selected[2]}. (Set NEWS_API_KEY for real news)"
    
    def _control_lights(self, text):
        """Control smart lights"""
        if "on" in text:
            self.smart_devices['lights']['state'] = 'on'
            self.smart_devices['lights']['brightness'] = 100
            return "Turning the lights on."
        elif "off" in text:
            self.smart_devices['lights']['state'] = 'off'
            self.smart_devices['lights']['brightness'] = 0
            return "Turning the lights off."
        elif "dim" in text:
            # Try to extract brightness level
            words = text.split()
            for i, word in enumerate(words):
                if word.isdigit():
                    brightness = int(word)
                    self.smart_devices['lights']['brightness'] = min(100, max(0, brightness))
                    return f"Setting lights to {brightness}% brightness."
            # Default dim
            self.smart_devices['lights']['brightness'] = 50
            return "Dimming lights to 50%."
        else:
            return f"Lights are currently {self.smart_devices['lights']['state']} at {self.smart_devices['lights']['brightness']}%."
    
    def _control_thermostat(self, text):
        """Control smart thermostat"""
        # Check for temperature setting
        words = text.split()
        for i, word in enumerate(words):
            if word.isdigit() and (i > 0 and words[i-1] in ["to", "set", "at"]):
                temp = int(word)
                self.smart_devices['thermostat']['temperature'] = min(85, max(55, temp))
                return f"Setting thermostat to {temp} degrees."
        
        # Check for mode
        if "heat" in text or "heater" in text:
            self.smart_devices['thermostat']['mode'] = 'heat'
            return f"Switching to heat mode. Current temperature is {self.smart_devices['thermostat']['temperature']} degrees."
        elif "cool" in text or "ac" in text:
            self.smart_devices['thermostat']['mode'] = 'cool'
            return f"Switching to cool mode. Current temperature is {self.smart_devices['thermostat']['temperature']} degrees."
        
        return f"Thermostat is set to {self.smart_devices['thermostat']['temperature']} degrees on {self.smart_devices['thermostat']['mode']} mode."
    
    def _control_tv(self, text):
        """Control TV"""
        if "on" in text:
            self.smart_devices['tv']['state'] = 'on'
            return "Turning the TV on."
        elif "off" in text:
            self.smart_devices['tv']['state'] = 'off'
            return "Turning the TV off."
        elif "channel" in text:
            words = text.split()
            for i, word in enumerate(words):
                if word.isdigit():
                    channel = int(word)
                    self.smart_devices['tv']['channel'] = channel
                    return f"Changing to channel {channel}."
            return f"TV is on channel {self.smart_devices['tv']['channel']}."
        return f"TV is {self.smart_devices['tv']['state']}."
    
    def _control_music(self, text):
        """Control music"""
        if "play" in text:
            self.smart_devices['music']['state'] = 'playing'
            # Check for specific song/artist
            if "play " in text:
                song = text.split("play ")[-1].strip()
                return f"Playing {song}."
            return "Playing music."
        elif "pause" in text or "stop" in text:
            self.smart_devices['music']['state'] = 'paused'
            return "Pausing music."
        elif "volume" in text:
            words = text.split()
            for i, word in enumerate(words):
                if word.isdigit():
                    vol = int(word)
                    self.smart_devices['music']['volume'] = min(100, max(0, vol))
                    return f"Setting volume to {vol}%."
            return f"Volume is at {self.smart_devices['music']['volume']}%."
        return f"Music is {self.smart_devices['music']['state']} at volume {self.smart_devices['music']['volume']}%."
    
    def _get_device_status(self):
        """Get status of all smart home devices"""
        status = f"Lights: {self.smart_devices['lights']['state']} at {self.smart_devices['lights']['brightness']}%. "
        status += f"Thermostat: {self.smart_devices['thermostat']['temperature']}° on {self.smart_devices['thermostat']['mode']}. "
        status += f"TV: {self.smart_devices['tv']['state']}. "
        status += f"Music: {self.smart_devices['music']['state']} at volume {self.smart_devices['music']['volume']}%."
        return status
    
    def _tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why did the Iron Man suit go to therapy? It had too many unresolved issues with its arc reactor!",
            "J.A.R.V.I.S. walked into a bar. The bartender said, 'We don't serve AI here.' J.A.R.V.I.S. replied, 'But I'm just here for the data!'",
            "What's Tony Stark's favorite programming language? C-sharp! Because he's always in sharp suits!",
            "Why did F.R.I.D.A.Y. get fired? She kept telling Tony his plans were 'elementary'!",
            "How many AI assistants does it take to change a light bulb? None, they just wait for you to do it and then say 'I could have done that faster.'"
        ]
        return random.choice(jokes)
    
    def _query_openai(self, text):
        """Query OpenAI API (compatible with older versions)"""
        try:
            if OPENAI_NEW_API:
                # New OpenAI API (>=1.0.0)
                response = openai.chat.completions.create(
                    model=self.config.get('model', 'gpt-3.5-turbo'),
                    messages=[
                        {"role": "system", "content": "You are F.R.I.D.A.Y., Tony Stark's AI assistant. Respond in character as a helpful, efficient, and slightly witty AI. Keep responses concise and helpful."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=self.config.get('max_tokens', 150),
                    temperature=self.config.get('temperature', 0.7)
                )
                return response.choices[0].message.content.strip()
            else:
                # Old OpenAI API (<=0.28)
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
        text_lower = text.lower()
        
        if "hello" in text_lower or "hi" in text_lower:
            return "Hello, boss. Good to hear from you."
        
        if "thank" in text_lower:
            return "You're welcome. Happy to help."
        
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
