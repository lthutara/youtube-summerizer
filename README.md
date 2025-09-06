# YouTube Summarizer

This project is a command-line tool designed to summarize YouTube videos and translate the summaries into Telugu. It has been refactored into a modular structure for better maintainability and efficiency.

## Features

*   **Transcript Fetching:** Extracts full text transcripts from YouTube video URLs.
*   **AI-Powered Summarization:** Uses Google's Gemini AI to generate concise and detailed summaries, broken down into sections (Introduction, Core Topics, Key Takeaways, Important Terms).
*   **Key Term Identification:** Identifies and explains important concepts from the video.
*   **Translation:** Translates the summaries and key terms into Telugu.
*   **Caching:** Caches generated summaries to avoid re-summarizing the same video, improving efficiency.
*   **Modular Design:** Separates summarization and translation logic into distinct Python scripts for improved maintainability.

## Project Structure

*   `summarizer.py`: The main entry point for the application. Orchestrates the summarization and translation processes.
*   `summarize.py`: Handles fetching the transcript and generating the summary using the Gemini API. Saves the summary to a JSON file for caching.
*   `translate.py`: Handles translating the summarized content and generating the final HTML output.
*   `requirements.txt`: Lists all necessary Python dependencies.
*   `summaries_json/`: Directory where generated JSON summaries are cached.
*   `summaries/`: Directory where the final HTML summary articles are saved.

## How to Use

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd youtube-summarizer
    ```

2.  **Set up your Python environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Configure your Gemini API Key:**
    *   Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/fundamentals/api_key).
    *   Create a `.env` file in the root directory of the project and add your API key:
        ```
        GEMINI_API_KEY="YOUR_API_KEY"
        ```

4.  **Run the summarizer:**
    Provide the YouTube video URL as a command-line argument.
    ```bash
    python3 summarizer.py <youtube_video_url>
    ```
    Example:
    ```bash
    python3 summarizer.py https://www.youtube.com/watch?v=KZeIEiBrT_w
    ```

    The script will:
    *   Fetch the video transcript.
    *   Summarize the content using the Gemini API (and cache it).
    *   Translate the summary into Telugu.
    *   Generate an HTML file with both English and Telugu summaries in the `summaries/` directory.
