#!/usr/bin/env python3

import whisper
import torch
import pyaudio
import numpy as np
import queue

# Paramètres
MODEL_SIZE = "small"   # Peut être "tiny", "base", "small", "medium", "large"
SAMPLE_RATE = 16000    # Taux d'échantillonnage audio requis par Whisper
CHUNK_DURATION = 5     # Durée des segments audio en secondes
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)  # Nombre d'échantillons par chunk

# Chargement du modèle Whisper
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model(MODEL_SIZE).to(device)

# File d'attente pour stocker les chunks audio
audio_queue = queue.Queue()

# Fonction de callback pour capturer l'audio
def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
    audio_queue.put(audio_data)
    return (in_data, pyaudio.paContinue)

# Initialisation de PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                stream_callback=callback)

print("🎤 Enregistrement en cours... (appuyez sur Ctrl+C pour arrêter)")

try:
    while True:
        # Récupère les données audio en temps réel
        audio_chunk = audio_queue.get()
        if len(audio_chunk) == 0:
            continue

        # Convertit l'audio en format compatible Whisper
        audio_chunk = whisper.pad_or_trim(audio_chunk)
        mel = whisper.log_mel_spectrogram(audio_chunk).to(device)

        # Effectue la transcription
        options = whisper.DecodingOptions(fp16=False, language="fr")
        result = whisper.decode(model, mel, options)

        # Affiche le texte transcrit
        print(f"📝 {result.text}")

except KeyboardInterrupt:
    print("\n🛑 Arrêt de la transcription.")
    stream.stop_stream()
    stream.close()
    p.terminate()

