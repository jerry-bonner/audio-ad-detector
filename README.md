# audio-ad-detector

Quick script that uses the whisper API to send an audio file in for analysis and asks for a VTT format return. VTT is used to provide timestamp data that could later be used for editing purposes.

With the VTT data in hand, we reduce it down into complete sentences and add the associated timestamps. From there we send each sentence in for analysis and provide the before and after sentences for context. JSON is dumped.

Example output :

```
...

 {
    "start": "00:01:17.620",
    "end": "00:01:22.860",
    "is_ad": true,
    "text": "Mention code crooked, and you'll get 10% credit back on your first scope of three months or more."
  },
  {
    "start": "00:01:22.860",
    "end": "00:01:26.620",
    "is_ad": true,
    "text": "Marketing experts with flexible contracts tailored to your specific needs."
  },
  {
    "start": "00:01:26.620",
    "end": "00:01:28.820",
    "is_ad": true,
    "text": "Visit rightsideup.com slash crooked today."
  },
  {
    "start": "00:01:28.820",
    "end": "00:01:31.379",
    "is_ad": true,
    "text": "That's rightsideup.com slash crooked."
  },
  {
    "start": "00:01:31.379",
    "end": "00:01:32.379",
    "is_ad": true,
    "text": "Code crooked."
  },
  {
    "start": "00:01:34.099",
    "end": "00:01:55.220",
    "is_ad": false,
    "text": "\u266a\u266a\u266a Welcome to Pod Save America."
  },
  {
    "start": "00:01:55.220",
    "end": "00:01:56.099",
    "is_ad": false,
    "text": "I'm Jon Favreau."
  },
  {
    "start": "00:01:56.099",
    "end": "00:01:56.940",
    "is_ad": false,
    "text": "I'm Dan Pfeiffer."
  },
  {
    "start": "00:01:56.940",
    "end": "00:02:05.820",
    "is_ad": false,
    "text": "On today's show, we'll talk about Trump ordering investigations into two former Trump officials for the crime of telling the truth about him and the 2020 election."
  },

  ...

  ```