# Project TODO List

## Next Steps:

- [ ] Fix formatting of generated HTML output (especially bullet points and sub-sections). This involves reverting `summarize_text` to return a single string and adjusting `main` to handle it, ensuring `markdown.markdown` correctly renders the output.
- [ ] Implement caching for already summarized links (using a JSON file or similar).

## Future Enhancements:

- [ ] Explore handling very long video transcripts (chunking and map-reduce summarization) if `googletrans` proves unreliable with extremely long single strings.
- [ ] Integrate HTML output into the existing Flask web interface.
- [ ] Implement fetching latest video links from a YouTube channel (requires YouTube Data API integration).
- [ ] Consider migrating to `google-cloud-translate` for more robust and reliable translation if `googletrans` continues to be unstable in the future.