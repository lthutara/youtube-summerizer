# Project Journal

## Day 1: Friday, August 15, 2025

### Project Inception and Setup

*   **Goal:** Kicked off a new project to create a tool that can fetch a YouTube video's transcript, summarize it, identify and explain key terms, and translate the output to Telugu. The user mentioned a long-term goal of using this for "structural learning" and integration into other projects.

*   **Initial Technical Plan & Pivot:**
    *   My initial proposal was to use the `transformers` library for local summarization.
    *   The user rightly pointed out that this was too heavy and suggested a more streamlined approach using a Large Language Model (LLM) for the summarization task.
    *   We pivoted the design to be much leaner.

*   **Revised Tech Stack:**
    *   `youtube-transcript-api` for fetching transcripts.
    *   `google-generativeai` to use the Gemini API for summarization and term extraction.
    *   `googletrans` for translation to Telugu.
    *   `nltk` for basic text utilities.

*   **Project Scaffolding:**
    *   Created the project directory: `youtube-summarizer`.
    *   Set up a Python virtual environment inside it.
    *   Created and installed dependencies from `requirements.txt`.

*   **Core Logic and Design:**
    *   Wrote the first version of the main script, `summarizer.py`, which includes functions for each step of the process (get transcript, summarize, translate).
    *   Created a `DESIGN.md` file to formally document the project's architecture, components, and data flow after the user requested more clarity on the design.

*   **Key Discussions & Clarifications:**
    *   Clarified that the `youtube-transcript-api` does not require a login or API key for public videos.
    *   Discussed the role of the Gemini API key, clarifying that it falls under a generous free tier, meaning no paid keys are needed for this project's scope.
    *   Touched upon the concept of building an "agent," noting that the current API key is the foundational element for creating more advanced, agent-like logic.

### API Key Management and Verification

*   **Improved API Key Handling:** The user suggested using a `.env` file to store the Gemini API key instead of exporting it to the terminal session. This is a much better practice.
*   **Implementation:**
    *   Created a `.env` file to store the `GEMINI_API_KEY`.
    *   Added `python-dotenv` to `requirements.txt` and installed it.
    *   Modified `summarizer.py` to automatically load the key from the `.env` file, including adding error handling.
*   **API Key Verification:** The user wisely suggested testing the API key in isolation before running the full script.
    *   Created a dedicated test script, `test_api.py`, to provide a clear "SUCCESS" or "FAILURE" message for the API key.

### Successful Execution and Initial Debugging

*   **Persistent `youtube-transcript-api` Issues:** Encountered a series of stubborn errors related to the `youtube-transcript-api` library, specifically `AttributeError: type object 'YouTubeTranscriptApi' has no attribute 'get_transcript'`.
    *   Initial attempts to fix by changing import styles (`get_transcript`, `get_transcripts`) were unsuccessful.
    *   An isolated test confirmed the error was not in our script but in the library's installation or behavior within the environment.
    *   A complete virtual environment rebuild was performed, but the error persisted, indicating a deeper, unusual issue.
    *   **Breakthrough:** Used `dir(YouTubeTranscriptApi)` to introspect the object, revealing that the `get_transcript` method was indeed missing. Instead, the library exposed `fetch` and `list` methods.
    *   **Final Fixes:**
        *   Changed the transcript fetching call to `youtube_transcript_api.YouTubeTranscriptApi.fetch(video_id)`.
        *   Corrected the `fetch` method call to be on an instance: `api_instance = youtube_transcript_api.YouTubeTranscriptApi(); transcript_list = api_instance.fetch(video_id)`.
        *   Resolved `FetchedTranscriptSnippet` not subscriptable error by changing `item["text"]` to `item.text`.

## Day 2: Friday, September 5, 2025

### Addressing `googletrans` Instability and Enhancements

*   **Issue: `googletrans` Async/Sync Inconsistency:**
    *   Initially, `googletrans` failed with `'coroutine' object has no attribute 'text'`, indicating it was behaving asynchronously.
    *   Implemented `async` and `await` in `translate_text` and `main` functions, and added `import asyncio`. This resolved the `coroutine` error.
    *   However, subsequent tests with longer videos led to `The read operation timed out` and then `object Translated can't be used in 'await' expression` errors, indicating `googletrans` reverted to synchronous behavior or its underlying API was unstable.
    *   Attempted to add retry logic to `translate_text`, but this did not resolve the fundamental instability.
    *   **Root Cause Identified:** `googletrans` is an unofficial wrapper around Google's public API, which is prone to breaking due to API changes or rate limiting. Its behavior is highly inconsistent and dependent on its exact version and transitive dependencies. The `git reset HEAD` operation likely caused a re-installation of dependencies that led to a different, less stable behavior of `googletrans`.
    *   **Current Resolution:** Reverted `translate_text` to its `async` and `await` state (without retry logic) and confirmed it works for various video lengths. This indicates `googletrans` behavior is highly volatile.

*   **Enhancement: Detailed Summaries (Prompt Engineering):**
    *   Modified the Gemini prompt in `summarize_text` to request more detailed summaries.
    *   Gradually increased the detail requested in each section of the summary (Introduction, Core Topics, Key Takeaways, Important Terms).
    *   **Outcome:** The Gemini model successfully generated more detailed summaries, and `googletrans` handled the increased length in recent tests.

*   **Enhancement: Video Title Extraction and Organized Saving:**
    *   Integrated `yt-dlp` to reliably extract the video title from the YouTube URL.
    *   Modified the `main` function to:
        *   Call `get_video_title` to get the video's actual title.
        *   Sanitize the title for use as a filename.
        *   Create a `summaries` directory if it doesn't already exist.
        *   Save the generated HTML output into the `summaries` directory, using the sanitized video title as the filename (e.g., `summaries/Video_Title.html`).
    *   **Issue Faced:** Duplicate `get_video_title` function (one `yt-dlp` based, one placeholder) caused incorrect filename saving. This was due to previous `replace` operations and `git restore` bringing back old code.
    *   **Resolution:** Manually removed the duplicate placeholder `get_video_title` function and its associated `import yt_dlp` statement.

*   **Current Status:**
    *   The script is currently working with `googletrans` (async/await setup) for both shorter and longer videos, and generates detailed summaries with correct video titles and organized saving.
    *   The formatting of the output (especially bullet points and sub-sections) in the HTML is currently broken due to issues with Markdown parsing after the section-wise processing. This needs to be addressed.

*   **Next Steps (Formatting Issue):**
    *   The current `summarize_text` function attempts to parse the Gemini output into sections, which is causing the formatting issues. This section parsing logic needs to be reverted.
    *   We need to revert the `summarize_text` function to return a single string (as it was before section parsing attempts).
    *   Then, we will adjust the `main` function to handle this single string output and use `markdown.markdown` more effectively to preserve the formatting. If `markdown.markdown` itself is not sufficient, we will explore other Markdown rendering libraries or custom post-processing.