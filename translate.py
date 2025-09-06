import os
from googletrans import Translator
import json
import argparse
import markdown
from nltk.tokenize import sent_tokenize
import nltk

async def translate_text(sections, dest_language='te'):
    """Translates the text in each section of the dictionary."""
    translated_sections = {}
    translator = Translator()
    for key, text in sections.items():
        print(f"Translating section: {key}...")
        try:
            if not text or text.startswith("Error"):
                translated_sections[key] = f"Cannot translate {key}."
                continue

            if key == 'core_topics':
                sentences = sent_tokenize(text)
                translated_sentences = []
                for sentence in sentences:
                    try:
                        translated_sentence = translator.translate(sentence, dest=dest_language)
                        translated_sentences.append(translated_sentence.text)
                    except Exception as e:
                        print(f"Error translating sentence: {sentence}")
                        print(f"Error: {e}")
                        translated_sentences.append(sentence) # Append the original sentence if translation fails
                translated_sections[key] = " ".join(translated_sentences)
            else:
                translated_text = translator.translate(text, dest=dest_language)
                translated_sections[key] = translated_text.text
        except Exception as e:
            print(f"Error translating section: {key}")
            print(f"Error: {e}")
            print(f"Problematic text: {text}")
            translated_sections[key] = f"Error translating this section."
    return translated_sections

def generate_html_output(summary_sections, translated_sections, video_title):
    """Generates an HTML string from the summary and translated sections."""
    # Convert Markdown to HTML for each section
    english_html = ""
    for title, content in summary_sections.items():
        english_html += f"<h3>{title.replace('_', ' ').title()}</h3>"
        english_html += markdown.markdown(content)

    telugu_html = ""
    for title, content in translated_sections.items():
        telugu_html += f"<h3>{title.replace('_', ' ').title()}</h3>"
        telugu_html += markdown.markdown(content)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{video_title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: #f9f9f9; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1, h2, h3 {{ color: #333; }}
            .section {{ margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background: #fff; }}
            .telugu {{ font-family: 'Noto Sans Telugu', sans-serif; font-size: 1.1em; color: #0056b3; }}
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <h1>{video_title}</h1>

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

async def main():
    """Main function to run the translator."""
    parser = argparse.ArgumentParser(description='YouTube Video Translator')
    parser.add_argument('json_file', help='The path to the JSON summary file.')
    args = parser.parse_args()
    json_file = args.json_file

    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        summary_sections = json.load(f)

    video_title = os.path.basename(json_file).replace(".json", "").replace("_", " ")

    print("\n--- Translating to Telugu ---")
    translated_sections = await translate_text(summary_sections)
    
    if "error" in translated_sections:
        print(translated_sections["error"])
        return
        
    for section, content in translated_sections.items():
        print(f"\n**{section.replace('_', ' ').title()} (Telugu)**")
        print(content)

    # Generate and save HTML output
    output_filename = os.path.join("summaries", f"{os.path.basename(json_file).replace('.json', '.html')}")
    html_output = generate_html_output(summary_sections, translated_sections, video_title)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"\nHTML article saved to {output_filename}")

if __name__ == "__main__":
    # Download necessary NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        
    import asyncio
    asyncio.run(main())
