import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import re
import google.generativeai as genai
from newsapi import NewsApiClient
from googleapiclient.discovery import build

# Initialize the recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init() 

# Set speech rate and volume
engine.setProperty('rate', 160)  # Natural speaking rate
engine.setProperty('volume', 1.0)  # Adjust volume

# set voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

# API keys for external services
newsapi = 'f9a7475633c34449a8e7c7175d948240'  
yt_api_key = "AIzaSyD0Bjt_91xVRb5xOnKmo9Fo0NXqDACsGbs"
gen_api_key = "AIzaSyAj03jUfom70WjMt_waxBXiGAXKjBqhQzQ"

def clean_text(text):
    # Removes special characters that sounds unnatural in speech output
    return re.sub(r'[*_/\\-]', ' ', text)  # Remove * _ / \ - with spaces

def speak(text):
    # Converts text to speech and speaks it out loud.
    text = clean_text(text) # Clean text before speaking
    engine.say(text)
    engine.runAndWait()
     
def aiProcess(command): 
    # Generates AI-based responses using Google-Gemini AI
    genai.configure(api_key=gen_api_key)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config={
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
    )
    response = model.generate_content(contents=[command]) 
    return response.text

def search_youtube(query, search_type="video", max_results=1):
    # Search YouTube for video or channel based on query
    try:
        youtube = build('youtube', 'v3', developerKey=yt_api_key, cache_discovery=False)
        # Make a search request to the YouTube API.
        response = youtube.search().list(q=query, part="snippet", type=search_type, maxResults=max_results).execute() 
        # Check if any results were returned.
        if not response.get('items'):
            return None, None  # No results found
        item = response['items'][0]
        title = item['snippet']['title']
         # Construct the appropriate YouTube URL based on search type.
        url = f"https://www.youtube.com/{
        'watch?v=' + item['id']['videoId'] if search_type == 'video' 
        else 'channel/' + item['id']['channelId']
        }"
        return title, url
    except Exception as e:
        print("Error:", e)
        return None, None

def fetch_news(api_key,source):
    newsapi = NewsApiClient(api_key=api_key) # Initialize the NewsApiClient with API key
    top_headlines = newsapi.get_top_headlines(sources=source) # Fetch the top headlines 
    articles = top_headlines.get('articles', []) # Extract the articles from the response
    titles = [article['title'] for article in articles]
    return titles 

def process_command(command):
    # Processes voice commands and performs correspondings actions.
    command = command.lower()
    if 'who are you' in command:
        speak("Hi, my name is Nova your virtual voice-assistant. I am skilled in performing task like playing songs, telling the current time, and help you go with different sources.")
    elif 'current date and time' in command:
        now = datetime.datetime.now()
        date = now.strftime("%B %d, %Y")  # Format: Month Day, Year
        time = now.strftime("%I:%M %p") # Format: HH:MM AM/PM
        speak(f"The current date is {date}")
        speak(f"The current time is {time}")

    elif "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        
    elif command.startswith("play"):
        # Extract the song name or video name after 'play'
        query = command.replace("play", "").strip()
        speak(f"Searching YouTube for {query}...")
        video_title, video_url = search_youtube(query, search_type="video")
        if video_url: 
            speak(f"Playing {video_title} on YouTube.")
            webbrowser.open(video_url)
        else:
            speak("Sorry, I couldn't find the video on YouTube.")

    elif command.startswith("open") and "youtube channel" in command:
        # Extract the person's name
        name = command.replace("open", " ").replace("youtube channel", "").strip()
        if name:
            speak(f"Searching YouTube for {name}'s channel...")
            channel_title, channel_url = search_youtube(name, search_type="channel", max_results=1)
            if channel_url:
                speak(f"Opening {channel_title}'s YouTube channel.")
                webbrowser.open(channel_url)
            else:
                speak("Sorry, I couldn't find the channel on YouTube.")
        else:
            speak("Please specify the name of the person's YouTube channel you want to open.")

    elif "news" in command:
        speak("Fetching the latest news.")
        headlines = fetch_news(api_key=newsapi, source='bbc-news') # Get BBC news
        for headline in headlines:
            speak(headline) # Read out each headline
    else:
        output = aiProcess(command) # Generate AI response for unkown comamnds
        speak(output) 
        
if __name__ == "__main__":
    speak("Initializing Nova ...")
    while True:
        # Listen for the wake word "Nova"
        # obtain audio from the microphone
        recognizer = sr.Recognizer()
        while True:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2) # Adjust for background noise
                    print("Listening...")
                    audio = recognizer.listen(source,timeout=5) #  Listens for up to 5 seconds for any audio input.
                word = recognizer.recognize_google(audio).lower()
                if(word == "nova"):
                    speak("Yes?") # Prompts the user for command
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.2)
                        print("Nova active....Listening for command....")
                        audio = recognizer.listen(source,timeout=5) # Listens for the comamnd
                        command = recognizer.recognize_google(audio) # Converts the spoken command to text
                    print(f"Command: {command}") # Displays the recognized command
                    process_command(command) # Process the vocie command
            
            except sr.UnknownValueError: # Catches cases where the audio is not understood and prints an appropriate message.
                print("Could not understand the audio.")
            except sr.RequestError as e: # Handles errors related to the speech recognition service and prints the error.
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e: # A general exception block that catches any other unexpected errors and prints the error details.
                print("Error; {0}".format(e))
                