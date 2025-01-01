import os
import mido
import fluidsynth

# Set the correct path for the SoundFont file
soundfont_path = "C:/tools/soundfonts/FluidR3_GM.sf2"

# Initialize FluidSynth
fs = fluidsynth.Synth()
fs.start(driver="dsound")  # Use "dsound" on Windows
sfid = fs.sfload(soundfont_path)
fs.program_select(0, sfid, 0, 0)  # Bank 0, Preset 0 (default piano)

# List available MIDI input ports
print("Available MIDI Input Ports:")
print(mido.get_input_names())

# Open a specific MIDI input port
input_port_name = mido.get_input_names()[0]  # Replace with the correct port if necessary
with mido.open_input(input_port_name, client_name="MidiOutput.py") as inport:
    print(f"Listening to MIDI inputs on: {input_port_name}")
    try:
        for msg in inport:
            print(msg)  # Print MIDI message for debugging
            if msg.type == "note_on" and msg.velocity > 0:
                fs.noteon(0, msg.note, msg.velocity)
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                fs.noteoff(0, msg.note)
    except KeyboardInterrupt:
        print("Stopping MIDI playback...")
fs.delete()
