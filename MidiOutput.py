import pygame.midi
import fluidsynth
import soundfile as sf

# Set paths
soundfont_path = "FluidR3_GM.sf2"  # Replace with your SoundFont file path
output_wav = "output.wav"  # Path to save the WAV file

# Initialize FluidSynth
fs = fluidsynth.Synth()

# Configure audio output to a WAV file
fs.start(driver="dsound")  # Use "dsound" for real-time playback
sfid = fs.sfload(soundfont_path)
fs.program_select(0, sfid, 0, 0)  # Bank 0, Preset 0 (default piano)

# Initialize Pygame MIDI
pygame.midi.init()

# List available MIDI input devices
print("Available MIDI Input Devices:")
for i in range(pygame.midi.get_count()):
    print(f"{i}: {pygame.midi.get_device_info(i)}")

# Open the first available MIDI input device
input_id = pygame.midi.get_default_input_id()
if input_id == -1:
    print("No MIDI input device found.")
    pygame.midi.quit()
    exit()

input_id = 1  # Use the input port for AKM320
midi_input = pygame.midi.Input(input_id)

# Start listening to MIDI input
print(f"Listening to MIDI input on device {input_id}. Press Ctrl+C to stop.")

try:
    while True:
        if midi_input.poll():
            midi_events = midi_input.read(10)  # Read up to 10 MIDI events at a time
            for event in midi_events:
                data = event[0]
                status, note, velocity, _ = data
                print(f"Received MIDI event: status={status}, note={note}, velocity={velocity}")

                # Handle note on/off events
                if status == 144 and velocity > 0:  # Note on
                    fs.noteon(0, note, velocity)
                elif status == 128 or (status == 144 and velocity == 0):  # Note off
                    fs.noteoff(0, note)
except KeyboardInterrupt:
    print("Stopping MIDI input and saving audio output...")
finally:
    # Record audio output to a file
    print("Recording audio...")
    audio_data = fs.get_audio()
    sf.write(output_wav, audio_data, 44100)  # Write audio data to WAV
    print(f"Audio saved to {output_wav}")

    # Cleanup
    midi_input.close()
    pygame.midi.quit()
    fs.delete()