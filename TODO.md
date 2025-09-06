# Project TODO List

## Future Enhancements:

- [ ] **Handle non-English videos:** Implement logic to detect the language of the video and provide summaries/translations accordingly. This might involve using language detection libraries or leveraging the Gemini API's language capabilities.
- [ ] **Generate comprehensive article from core topics:** Expand the identified core topics into a more detailed and cohesive article, potentially by extracting more information from the transcript or using the LLM for further elaboration.
- [ ] Improve translation formatting and robustness (especially for Markdown content).
- [ ] Explore handling very long video transcripts (chunking and map-reduce summarization) if `googletrans` proves unreliable with extremely long single strings.
- [ ] Implement fetching latest video links from a YouTube channel (requires YouTube Data API integration).