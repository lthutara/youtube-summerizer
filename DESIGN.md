# Design Document: YouTube Summarizer

## 1. Project Goal

The primary goal of this project is to provide a user with a concise summary, a list of key terms, and a Telugu translation of a YouTube video's content, using its transcript. This enables users to quickly understand the core concepts of a video without watching it in its entirety.

## 2. Architecture Overview

The application follows a simple, linear pipeline architecture. A user's input (a YouTube URL) triggers a sequence of processing steps, with the output of one step feeding into the next.

```
+-----------------+      +----------------------+      +-----------------------+      +--------------------+      +----------------------+
|   User Input    |----->|  Transcript Fetcher  |----->|  Summarizer &        |----->|     Translator     |----->|   Display to User    |
| (YouTube URL)   |      | (youtube-transcript-api) |      |  Term Extractor (LLM) |      |   (googletrans)    |      |      (CLI Output)      |
+-----------------+      +----------------------+      +-----------------------+      +--------------------+      +----------------------+
```

## 3. Components

### 3.1. Transcript Fetcher (`get_transcript`)

*   **Purpose:** To extract the full text transcript from a given YouTube video URL.
*   **Library:** `youtube-transcript-api`
*   **Input:** A string containing a valid YouTube video URL (e.g., `"https://www.youtube.com/watch?v=dQw4w9WgXcQ"`).
*   **Processing:**
    1.  Extracts the unique `video_id` from the URL.
    2.  Uses the library to request the transcript for that `video_id`.
    3.  Concatenates the individual transcript segments into a single block of text.
*   **Output:** A string containing the entire video transcript.

### 3.2. Summarizer & Term Extractor (`summarize_text`)

*   **Purpose:** To generate a concise summary and identify key terminology from the transcript.
*   **Service:** Google Gemini API (via the `google-generativeai` library).
*   **Input:** A string containing the video transcript.
*   **Processing:**
    1.  Constructs a detailed prompt for the Gemini LLM.
    2.  The prompt instructs the model to perform two tasks:
        *   Summarize the text.
        *   Identify important or lesser-known terms and provide a brief explanation for each.
    3.  Sends the transcript and the prompt to the Gemini API.
*   **Output:** A single string containing both the summary and the list of key terms, as formatted by the LLM.

### 3.3. Translator (`translate_text`)

*   **Purpose:** To translate the generated summary and key terms into Telugu.
*   **Library:** `googletrans`
*   **Input:** The string output from the Summarizer component.
*   **Processing:**
    1.  Initializes the `Translator` object.
    2.  Calls the `translate` method, passing the text and specifying 'te' (Telugu) as the destination language.
*   **Output:** A string containing the translated text.

### 3.4. Main Application (`main`)

*   **Purpose:** To serve as the main entry point and orchestrate the overall workflow.
*   **Processing:**
    1.  Prompts the user to enter a YouTube URL.
    2.  Calls the `get_transcript` function.
    3.  Calls the `summarize_text` function with the transcript.
    4.  Calls the `translate_text` function with the summary.
    5.  Prints the results of each step to the command-line interface (CLI).
    6.  Includes basic error handling to manage issues at each step (e.g., transcript not found, API errors).

## 4. Data Flow

1.  The user runs the script and provides a YouTube URL at the prompt.
2.  The URL is passed to `get_transcript`, which returns the full text of the video's transcript.
3.  This transcript text is passed to `summarize_text`.
4.  `summarize_text` sends the text to the Gemini API and receives a summary and list of key terms.
5.  This combined text is passed to `translate_text`.
6.  `translate_text` returns the Telugu version of the text.
7.  The `main` function prints the summary/key terms and the final Telugu translation to the console.

## 5. Dependencies

The project relies on the following external Python libraries, as listed in `requirements.txt`:

*   `youtube-transcript-api`
*   `google-generativeai`
*   `googletrans==4.0.0-rc1`
*   `nltk`
