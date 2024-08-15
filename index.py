
from pytube import YouTube
import ffmpeg
import openai

# Baixar o áudio com a URL do vídeo
def download_audio(youtube_url, output_path='audio.mp3'):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename=output_path)
    return output_path

def transcribe_audio (audio_path):
    # Converter o áudio para um formato que o modelo da OpenAI possa processar
    output_wav = "audio.wav"
    ffmpeg.input(audio_path).output(output_wav).run()

    # Carregar o áudio convertido
    with open(output_wav, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
    return transcript

# Gerar um resumo do texto transcrito usando a API da OpenAI.
def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Resuma o seguinte texto:\n\n{text}\n\nResumo:",
        max_tokens=150
    )
    return response.choices[0].text.script()
    
def summarize_youtube_video(youtube_url):
    # Baixar o audio
    audio_path = download_audio(youtube_url)

    # Transcrever audio
    transcription = transcribe_audio(audio_path)

    # Gerar resumo
    summary = summarize_text(transcription)

    return summary

youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
summary = summarize_youtube_video(youtube_url)
print(summary)
