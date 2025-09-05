import os
import google.generativeai as genai
import youtube_transcript_api
from googletrans import Translator
import nltk
from dotenv import load_dotenv
import markdown
import asyncio
import yt_dlp


def get_video_title(youtube_url):
    """Fetches the video title for a given YouTube URL."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'force_generic_extractor': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=False)
            return info.get('title', 'Untitled Video')
        except Exception as e:
            print(f"Error fetching video title: {e}")
            return "Untitled Video"

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
    Your task is to provide a structured, comprehensive summary of the following YouTube transcript. Please format your output in Markdown with the following sections:

    **1. Brief Introduction**
    Provide a short, one-paragraph introduction that sets the stage and describes the video's main purpose.

    **2. Core Topics**
    Create a bulleted list of the main topics or arguments discussed in the video. Each bullet point should be a clear and concise statement.

    **3. Key Takeaways**
    List the most important, actionable, or insightful key takeaways from the video.

    **4. Important Terms**
    Identify and explain any important or less-known terms and concepts mentioned.

    ---

    **Transcript:**
    {transcript}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during summarization: {e}"

async def translate_text(text, dest_language='te'):
    """Translates the text to the specified language."""
    if not text or text.startswith("Error"):
        return "Cannot translate text."
    try:
        translator = Translator()
        translated_text = translator.translate(text, dest=dest_language)
        return translated_text.text
    except Exception as e:
        return f"Error during translation: {e}"

async def main():
    """Main function to run the summarizer."""
    youtube_url = input("Enter the YouTube video URL: ")
    
    print("\nFetching transcript...")
    transcript = get_transcript(youtube_url)

    print("\nFetching video title...")
    video_title = get_video_title(youtube_url)
    # Sanitize title for filename
    sanitized_title = "".join([c for c in video_title if c.isalnum() or c.isspace()]).rstrip()
    sanitized_title = sanitized_title.replace(" ", "_")

    # Create summaries directory if it doesn't exist
    summaries_dir = "summaries"
    os.makedirs(summaries_dir, exist_ok=True)

    output_filename = os.path.join(summaries_dir, f"{sanitized_title}.html")

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
    translated_summary = await translate_text(summary_and_terms)
    
    if translated_summary.startswith("Error"):
        print(translated_summary)
        return
        
    print(translated_summary)

    # Generate and save HTML output
    html_output = generate_html_output(summary_and_terms, translated_summary)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"\nHTML article saved to {output_filename}")


def generate_html_output(summary_and_terms, translated_summary):
    """Generates an HTML string from the summary and translated text."""
    # Convert Markdown to HTML
    english_html = markdown.markdown(summary_and_terms)
    telugu_html = markdown.markdown(translated_summary) # Assuming translated_summary might also contain Markdown

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube Video Summary</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: #f9f9f9; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1, h2 {{ color: #333; }}
            .section {{ margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background: #fff; }}
            .telugu {{ font-family: 'Noto Sans Telugu', sans-serif; font-size: 1.1em; color: #0056b3; }}
            /* Removed pre styling as we are converting to HTML */
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <h1>YouTube Video Summary</h1>

            <div class="section">
                <h2>English Summary & Key Terms</h2>
                {english_html}
            </div>

            <div class="section telugu">
                <h2>తెలుగు సారాంశం & ముఖ్య పదాలు (Telugu Summary & Key Terms)</h2>
                {telugu_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


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
        
    asyncio.run(main())
