import openai
import pyttsx3
import speech_recognition as sr
import time 

# Set your openAi Key
openai.api_key = "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"

# coisa tts
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # Esperar o user dizer "Gepeto"
        print("Diga 'Gepeto' para começar a gravar a pergunta...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "Gepeto":
                    # gravar
                    filename = "input.wav"
                    print("Faça a pergunta")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1 
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    # transcrever
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print("Você disse {text}")
                        
                        # gerar resposta
                        response = generate_response(text)
                        print("ChatGPT disse {response}")

                        # ler a resposta com tts
                        speak_text(response)
            except Exception as e:
                print("Ocorreu um erro: {}".format(e))
if __name__ == "__main__":
    main()