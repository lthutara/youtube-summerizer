import os
import google.generativeai as genai
import youtube_transcript_api
from dotenv import load_dotenv
import json
import argparse
import re
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
    """Summarizes the text using the Gemini API and returns a dictionary of sections."""
    if not transcript or transcript.startswith("Error"):
        return {"error": "Cannot summarize text."}

    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    prompt = f"""
    Your task is to provide a structured, comprehensive summary of the following YouTube transcript. Please format your output in Markdown with the following sections:

    **1. Brief Introduction**
    Provide a detailed, one-paragraph introduction that sets the stage and describes the video's main purpose and what viewers can expect to learn.

    **2. Core Topics**
    Create a detailed, multi-level bulleted list of the main topics and sub-topics discussed. Go into greater detail for each point, providing specific examples or data points mentioned in the transcript.

    **3. Key Takeaways (In-Depth)**
    Provide an in-depth, bulleted list of the most important, actionable, or insightful key takeaways. Each point should be a full sentence or two, offering more context than a simple phrase.

    **4. Important Terms Explained**
    Identify and explain any important or less-known terms and concepts. Provide a clear definition and explain its relevance in the context of the video.

    ---

    **Transcript:**
    {transcript}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text
        print("\n--- Raw Gemini Output ---")
        print(text)
        print("--- End Raw Gemini Output ---")

        # Use regex to find sections, making it more robust
        sections = {}
        # Find all the bolded titles
        titles = re.findall(r"\*\*(.*?)\*\*", text)
        for i, title in enumerate(titles):
            # The content is between the current title and the next title
            start_index = text.find(f"**{title}**") + len(title) + 4
            end_index = -1
            if i + 1 < len(titles):
                end_index = text.find(f"**{titles[i+1]}**")
            
            content = text[start_index:end_index].strip()
            key = title.lower().replace(" ", "_").replace("_(in-depth)", "").replace("_explained", "")
            sections[key] = content

        # Fallback if regex fails
        if not sections:
            return {"error": "Could not parse summary sections. Please check the model's output format."}
        return sections
    except Exception as e:
        return {"error": f"Error during summarization: {e}"}

def main():
    """Main function to run the summarizer."""
    parser = argparse.ArgumentParser(description='YouTube Video Summarizer')
    parser.add_argument('youtube_url', help='The URL of the YouTube video to summarize.')
    args = parser.parse_args()
    youtube_url = args.youtube_url
    
    print("\nFetching transcript...")
    transcript = get_transcript(youtube_url)

    print("\nFetching video title...")
    video_title = get_video_title(youtube_url)
    # Sanitize title for filename
    sanitized_title = "".join([c for c in video_title if c.isalnum() or c.isspace()]).rstrip()
    sanitized_title = sanitized_title.replace(" ", "_")

    # Create summaries directory if it doesn't exist
    summaries_json_dir = "summaries_json"
    os.makedirs(summaries_json_dir, exist_ok=True)

    summary_json_filename = os.path.join(summaries_json_dir, f"{sanitized_title}.json")

    if os.path.exists(summary_json_filename):
        print("\nSummary already exists. Skipping summarization.")
        return

    print("\nSummarizing and extracting key terms...")
    summary_sections = summarize_text(transcript)
    
    if "error" in summary_sections:
        print(summary_sections["error"])
        return

    # Save the summary to a json file
    with open(summary_json_filename, "w", encoding="utf-8") as f:
        json.dump(summary_sections, f, ensure_ascii=False, indent=4)
    
    print(f"\nSummary saved to {summary_json_filename}")

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

    main()
