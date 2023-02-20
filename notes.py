import whisper, os
from chatgpt_wrapper import ChatGPT

#SETTINGS FOR YOU
###############################################################################################
###############################################################################################
#How you want note taker to behave. Gets repeated at the beginning of every chunk.
preprompt = "Here's an excerpt from a lecture that I'm sending you in pieces. Make a summary of this exceprt: "

#how many words of text you want to feed to Chat-GPT at at time
#(there's a limit, I think at 4000 tokens (roughly 3000 words.)
chunkSize = 1000

#false means it will generate a new transcription, true means it will load it from transcription.txt
loadTranscription = False

#file extension of your audio sample named "samp"
audExtension = "mp3"
###############################################################################################
###############################################################################################

#note the audio and transcription path, based on current script path
path = os.path.realpath(os.path.dirname(__file__))
audioPath = "{}/samp.{}".format(path,audExtension)
transcriptionPath = "{}/{}".format(path, "transcription.txt")
gptResponsePath = "{}/{}".format(path, "gptresponses.txt")

#Make or load transcription
if loadTranscription:
    print("[*] Loading transcription...")
    transcription = open(transcriptionPath, 'r').readlines()[0]
else:
    print("[*] Loading OpenAI Whisper model...")
    model = whisper.load_model("base")

    print("[*] Transcribing audio, this could a short while...")
    transcription = model.transcribe(audioPath)["text"]
    temp = open(transcriptionPath, 'w').write(transcription)
    print("[*] Transcription saved as transcription.txt")


#Split transcription into chunks
words = transcription.split(" ")
wordsLen = len(words) #for later calculation of reduction
chunks = []
while (len(words) > 0):
    wordChunk = words[:chunkSize]
    wordString = ""
    for i in wordChunk:
        wordString += i+" "
    chunks.append(wordString)
    del words[:chunkSize]
print("[*] Chunked into {} chunks of {} words".format(len(chunks),chunkSize))

#ChatGPT time
print("[*] Loading ChatGPT Client...")
bot = ChatGPT()
bot.new_conversation()
gptChunks = []
temp = open(gptResponsePath, 'w').write("------------------summarized from {} chunks of {} words------------------\n\nUsing Prompt, \"{}\"\n".format(len(chunks),chunkSize, preprompt)) #erase previous file
#Retrieve chunks, display them, and log them
print("----[-] Using Prompt, \"{}\"\n".format(preprompt))
chunkCount = 1
gptLen = 0 #for later calculation of reduction
for i in chunks:
    print("----[-] Asking for chunk "+str(chunkCount))
    response = bot.ask(preprompt+" \""+i+"\"")
    gptLen += len(response.split(" "))
    print(response+"\n")
    temp = open(gptResponsePath, 'a').write("------------------CHUNK #{}------------------\n\n{}\n\n".format(chunkCount,response))
    chunkCount += 1
#calculate reduction of size and add it to the log
temp = open(gptResponsePath, 'a').write("--------REDUCED BY {}% ({} to {} words)--------".format((wordsLen-gptLen)/float(wordsLen)*100, wordsLen, gptLen))
print("[*] All done and saved to gptresponses.txt...")
print("----[-] If you don't want it overwritten, copy it somewhere else.")
