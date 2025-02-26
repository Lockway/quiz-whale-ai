from pydub import AudioSegment
import os

def split_audio(file_path, chunk_length_ms=300000):  # 300,000ms = 5 minutes
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    
    output_files = []
    for i, chunk in enumerate(chunks):
        output_file = f"chunk_{i}.mp3"
        chunk.export(output_file, format="mp3")
        output_files.append(output_file)
    
    return output_files

# Example usage
split_files = split_audio("mp3/large_audio.mp3")
print("Chunks created:", split_files)
