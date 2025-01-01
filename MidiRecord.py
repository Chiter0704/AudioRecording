import mido
from mido import MidiFile, Message, MidiTrack

# Open MIDI input port
input_port_name = mido.get_input_names()[0]  # Replace with your MIDI device name if necessary
midi_file = MidiFile()
track = MidiTrack()
midi_file.tracks.append(track)

try:
    with mido.open_input(input_port_name) as inport:
        print(f"Listening to MIDI inputs on: {input_port_name}")

        for msg in inport:
            print(msg)  # Print received MIDI message
            if not msg.is_meta:
                track.append(msg)  # Append the MIDI message to the track
except KeyboardInterrupt:
    print("Stopping MIDI recording...")
finally:
    midi_file.save('output.mid')  # Save the recorded MIDI data to a file
    print("MIDI saved as output.mid")
