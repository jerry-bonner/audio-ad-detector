#!/usr/bin/env python3
from openai import OpenAI
from dotenv import load_dotenv
import re
from typing import List, Dict
import os
import json

def parse_vtt_to_sentences(vtt_text: str) -> List[Dict[str, str]]:
    lines = vtt_text.strip().splitlines()
    entries = []

    timestamp = None
    buffer = []

    def is_end_of_sentence(text: str) -> bool:
        return text.strip().endswith(('.', '!', '?'))

    def flush_entry(start, end, sentence):
        return {"start": start, "end": end, "is_ad": False,"text": sentence.strip()}

    for line in lines:
        time_match = re.match(r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})", line)
        if time_match:
            timestamp = time_match.groups()
        elif line.strip() == "":
            continue
        else:
            if timestamp:
                buffer.append((timestamp, line.strip()))
                timestamp = None

    # Merge sentence fragments
    results = []
    current_text = ""
    current_start = None
    current_end = None

    for (start, end), fragment in buffer:
        if current_text == "":
            current_start = start
        current_text += (" " if current_text else "") + fragment
        current_end = end

        if is_end_of_sentence(fragment):
            results.append(flush_entry(current_start, current_end, current_text))
            current_text = ""
            current_start = None
            current_end = None

    # Handle trailing fragments
    if current_text:
        results.append(flush_entry(current_start, current_end, current_text))

    return results

if __name__ == "__main__":

  load_dotenv('secret.env')

  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

  with open("audio.mp3", "rb") as audio_file:
      transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="vtt")
      
      if transcript:
          sentences = parse_vtt_to_sentences(transcript)
          for sentence in sentences:
              response = client.responses.create(
                model="o3-mini",
                input=[
                  {
                      "role": "system",
                      "content": "You are an assistant that determines if a sentence from a podcast is an advertistement or not. You will be given the timestamp of the sentence and the sentence itself. Your output must be a boolean value. 'True' if it is an advertistement, 'False' if it is not. No other output is allowed."},
                  {
                      "role": "user",
                      "content": f"start:{sentence['start']} stop:{sentence['end']} sentence:{sentence['text']}"
                  }
                ]
              
              )

              if response.output_text == "True":
                  sentence["is_ad"] = True

          with open("sentences.json", "w") as f:
              json.dump(sentences, f)