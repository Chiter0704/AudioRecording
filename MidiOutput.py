import mido
from magenta.music import midi_io, note_sequence_io
from magenta.music.protobuf import music_pb2
from magenta.music import midi_synth
import soundfile as sf

# Set paths
soundfont_path = "FluidR3_GM.sf2"  # Path to your SoundFont file
output_wav = "output.wav"  # Path to save the WAV file
output_midi = "output.mid"  # Path to save the MIDI file

# Initialize MIDI Synthesizer
synth = midi_synth.fluidsynth.FluidSynth(soundfont_path)

# List available MIDI input devices
print("Available MIDI Input Ports:")
available_ports = mido.get_input_names()
if not available_ports:
    print("No MIDI input ports found. Ensure your device is connected.")
    exit()

print(available_ports)
input_port_name = available_ports[0]  # Replace with your desired MIDI port name

# Open MIDI input port
with mido.open_input(input_port_name) as inport:
    print(f"Listening to MIDI input on: {input_port_name}. Press Ctrl+C to stop.")

    # Create a Magenta NoteSequence
    sequence = music_pb2.NoteSequence()

    try:
        for msg in inport:
            print(f"Received MIDI message: {msg}")

            # Parse MIDI message
            if msg.type == 'note_on':
                sequence.notes.add(
                    pitch=msg.note,
                    velocity=msg.velocity,
                    start_time=msg.time,
                    end_time=msg.time + 0.5  # Add duration for note_on
                )
            elif msg.type == 'note_off':
                for note in sequence.notes:
                    if note.pitch == msg.note and note.end_time == 0:
                        note.end_time = msg.time
                        break
    except KeyboardInterrupt:
        print("Stopping MIDI input. Saving MIDI file...")

    # Save the NoteSequence as a MIDI file
    midi_io.sequence_proto_to_midi_file(sequence, output_midi)
    print(f"MIDI saved to {output_midi}")

    # Convert MIDI to WAV using Magenta's FluidSynth
    print("Converting MIDI to WAV...")
    audio_data = synth.synthesize(sequence)
    sf.write(output_wav, audio_data, 44100)
    print(f"Audio saved to {output_wav}")
