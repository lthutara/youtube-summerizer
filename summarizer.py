import os
import google.generativeai as genai
import youtube_transcript_api
from googletrans import Translator
import nltk
from dotenv import load_dotenv

def get_transcript(youtube_url):
    """Fetches the transcript for a given YouTube video."""
    try:
        video_id = youtube_url.split("v=")[1]
        api_instance = youtube_transcript_api.YouTubeTranscriptApi()
        transcript_list = api_instance.fetch(video_id)
        transcript = " ".join([item.text for item in transcript_list])
        return transcript
    except Exception as e:
        return f"Error fetching transcript: {e}"

def summarize_text(transcript):
    """Summarizes the text using the Gemini API."""
    if not transcript or transcript.startswith("Error"):
        return "Cannot summarize text."
    
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    prompt = f"""
    Summarize the following transcript. Also, identify key terms or less-known concepts mentioned and provide a brief, one-sentence explanation for each.

    Transcript:
    {transcript}

    Provide the output in two parts:
    1. A concise summary.
    2. A list of key terms with their explanations.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during summarization: {e}"

def translate_text(text, dest_language='te'):
    """Translates the text to the specified language."""
    if not text or text.startswith("Error"):
        return "Cannot translate text."
    try:
        translator = Translator()
        translated_text = translator.translate(text, dest=dest_language)
        return translated_text.text
    except Exception as e:
        return f"Error during translation: {e}"

def main():
    """Main function to run the summarizer."""
    youtube_url = input("Enter the YouTube video URL: ")
    
    print("\nFetching transcript...")
    transcript = get_transcript(youtube_url)
    
    if transcript.startswith("Error"):
        print(transcript)
        return
        
    print("\nSummarizing and extracting key terms...")
    summary_and_terms = summarize_text(transcript)
    
    if summary_and_terms.startswith("Error"):
        print(summary_and_terms)
        return
        
    print("\n--- Summary and Key Terms ---")
    print(summary_and_terms)
    
    print("\n--- Translating to Telugu ---")
    translated_summary = translate_text(summary_and_terms)
    
    if translated_summary.startswith("Error"):
        print(translated_summary)
        return
        
    print(translated_summary)


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Configure the Gemini API key
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file or environment variables.")
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error configuring API key: {e}")
        exit()

    # Download necessary NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        
    main()