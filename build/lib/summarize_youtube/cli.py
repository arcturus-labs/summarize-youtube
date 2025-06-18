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
You are a video transcript summarizer. The video ID is {video_id}.
Here is the video transcript which includes the timestamp in seconds (pay special attention to timestamps because you'll be asked about them later).
---
{transcript}
---
In subsequent conversation, if someone asks about a URL to a point in the video then use the standard YouTube URL format with the video ID and the timestamp in seconds, e.g., https://www.youtube.com/watch?v={video_id}&t=1234s.
"""
    user_prompt = """\
Create a quick summary of the video transcript above as a bulleted list of topics covered in time order. For each bullet, include the following:
- the topic
- a very terse summary of the topic (one sentence)
- the timestamp (seconds, just like above) of the first occurrence of that topic along with the line of transcript that introduces the topic
- the timestamp (seconds) of the most important part of the topic along with the line of transcript that introduces the topic
This summary serves as a quick reference for later, but shouldn't influence the formal summary you'll be asked to write later which will be more detailed and prose-like.
"""
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
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--model", default="gpt-4.1-mini", help="OpenAI model to use (default: gpt-4.1-mini)")
    args = parser.parse_args()
    video_id = extract_video_id(args.url)
    transcript = get_transcript(video_id)
    summarize_transcript(transcript, video_id, model=args.model)

if __name__ == "__main__":
    main() 