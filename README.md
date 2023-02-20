# makeNotes
A python script that combines OpenAI's Whisper and Chat-GPT to summarize audio from a class/lecture (or a custom task)
- Custom prompt (task)
- Custom chunk size (how many words you feed GPT-3 at once)
- Generate or load transcription (for reuse with the same audio)

# Install dependencies:
Use the instructions from these two github repos to install Whisper and Chat-GPT Wrapper in one or two commands:

https://github.com/mmabrouk/chatgpt-wrapper

https://github.com/openai/whisper

# How to:
1. Open up notes.py to customize your settings (change loadTranscription to True if you want to run it using previously generated transcription)
2. Place your audio in the makeNotes folder name it "samp.mp3" (or wav, flac, aiff, whatever's in your settings)
3. Run the script and enjoy
![example](https://github.com/d3n7/makeNotes/blob/main/exampleOutput.png?raw=True)


# Troubleshooting:
In most cases where there's issue with the Chat-GPT Wrapper, you can do the following to fix it:
1. Run 'pkill firefox' in your command line
2. Run 'chatgpt install' in your command line, log out and back into your OpenAI account
3. Quit the browser and rerun the script
