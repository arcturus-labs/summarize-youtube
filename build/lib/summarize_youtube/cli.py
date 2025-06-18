import re
import sys
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

def extract_video_id(url):
    # Extracts the video ID from a YouTube URL
    match = re.search(r"(?:v=|youtu.be/)([\w-]{11})", url)
    if not match:
        print("Could not extract video ID from URL.", file=sys.stderr)
        sys.exit(1)
    return match.group(1)

def get_transcript(video_id):
    data = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = []
    for entry in data:
        transcript.append(f"{entry['start']}: {entry['text']}")
    return "\n".join(transcript)

def summarize_transcript(transcript, video_id, model="gpt-4.1-mini"):
    client = OpenAI()
    system_prompt = f"""
You are an AI assistant specialized in summarizing YouTube video transcripts. Your task is to provide a comprehensive, well-structured summary that captures the essence of the video content.
Follow these steps to create your summary:

1. Quick Overview:
   Create a brief (2-3 sentences) overview of the video's main topic and purpose. Place this at the beginning of your summary.

2. Detailed Summary:
   - Provide a detailed summary of the video content in well-formatted markdown prose.
   - Use appropriate headings (##, ###) to structure the summary logically.
   - Include 3-5 main sections (or more if needed), each covering a major topic or theme from the video.
   - Within each section, use subsections or bullet points as needed to break down subtopics.
   - Cite key moments, notable quotes, or visual elements referenced, include them in the summary.
      - Create YouTube URL links for these key points using the format: [link](https://www.youtube.com/watch?v={video_id}&t=X), where X is the timestamp in seconds.
      - Key moments should often include quotations for important moments.
      - Never directly mention the timestamp in the summary, instead use the YouTube URL links.
   - For detailed summary sections, make use of bulleted lists for ease of reading.

3. Conclusion:
   - Summarize the main takeaways from the video in 2-3 sentences.
   - If applicable, mention any call-to-action or next steps suggested in the video.


General guidelines:
- Maintain a neutral tone throughout your summary.
- Focus on accurately representing the video's content.
- Make your summary informative and easy to navigate.
- Allow readers to quickly understand the video's content and locate specific information if needed.

Additional information:
The format of the transcript is an array of JSON objects like this `{{'text': 'whoa simmer down there', 'start': 2.24, 'duration': 3.0}}`. The `start` timestamp and the `duration` is in seconds.

Here's the information you need:

<video_id>
{video_id}
</video_id>

<transcript>
{transcript}
</transcript>
"""
    user_prompt = "Now, create a summary according to the rules above."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=3000,
        temperature=0.7,
    )
    print(response.choices[0].message.content)

def main():
    parser = argparse.ArgumentParser(description="Summarize a YouTube video using LLMs and timestamps.")
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("--model", default="gpt-4.1-mini", help="OpenAI model to use (default: gpt-4.1-mini)")
    args = parser.parse_args()
    video_id = args.video_id
    transcript = get_transcript(video_id)
    summarize_transcript(transcript, video_id, model=args.model)

if __name__ == "__main__":
    main() 