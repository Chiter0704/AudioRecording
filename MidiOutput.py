import mido
import fluidsynth

# Initialize FluidSynth with a soundfont
soundfont_path = "FluidR3_GM.sf2"  # Path to your soundfont file
fs = fluidsynth.Synth()
fs.start(driver="alsa")  # Use "dsound" on Windows, "alsa" on Linux
sfid = fs.sfload(soundfont_path)
fs.program_select(0, sfid, 0, 0)  # Bank 0, Preset 0 (default piano)

# Open MIDI input port
input_port_name = mido.get_input_names()[0]  # Replace with your MIDI device name if necessary
with mido.open_input(input_port_name) as inport:
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
#hello