#Learn how to pronounce words in Japanese
#Needs a gui and maybe ill just use google translate
import whisper
#Kinda dont wanna use os but seems like the only way to force to japanese using this model. Maybe I could add a bunch of japanese phrases in the beggining of mp3s so it learns its japanese?
import os
import pyaudio
import wave

#Creates audio file for the Whisper model to use
def record(file_name):
    # Record in chunks of 1024 samples
    chunk = 1024 
    
    # 16 bits per sample
    sample_format = pyaudio.paInt16 
    chanels = 1
    
    # Record at 44400 samples per second
    smpl_rt = 44400 
    seconds = 4
    filename = file_name + ".wav"
    
    # Create an interface to PortAudio
    pa = pyaudio.PyAudio() 
    
    stream = pa.open(format=sample_format, channels=chanels,
                    rate=smpl_rt, input=True,
                    frames_per_buffer=chunk)
    
    print('Recording...')
    
    # Initialize array that be used for storing frames
    frames = [] 
    
    # Store data in chunks for 8 seconds
    for i in range(0, int(smpl_rt / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    
    # Terminate - PortAudio interface
    pa.terminate()
    
    print('Done !!! ')
    
    # Save the recorded data in a .wav format
    sf = wave.open(filename, 'wb')
    sf.setnchannels(chanels)
    sf.setsampwidth(pa.get_sample_size(sample_format))
    sf.setframerate(smpl_rt)
    sf.writeframes(b''.join(frames))
    sf.close()
    return filename

def main():
    #Initializations
    model_type = "base"
    model = whisper.load_model(model_type)
    language = "Japanese"
    #Record Audio
    file_name = "audio"
    audio = record(file_name)
    #audio = "test.wav"
    #Tell Whisper to translate audio to text from Japanese to English
    command = "whisper " + audio + " --model " + model_type + " --language " + language + " --task translate --output_format txt"
    os.system(command)

    #Now just trancript the speech in Japanese
    command = "whisper " + audio + " --model " + model_type + " --language " + language + " --task transcribe --output_format txt"
    os.system(command)
   
if __name__ == "__main__":
    main()
    
#Forces model to listne in japanese
#whisper Jap3.mp3 --model base --language Japanese --task translate