import pygame.midi

pygame.midi.init()

# List available MIDI input devices
for i in range(pygame.midi.get_count()):
    print(f"{i}: {pygame.midi.get_device_info(i)}")

# Open the first MIDI input device
input_id = pygame.midi.get_default_input_id()
if input_id != -1:
    print(f"Using MIDI input device {input_id}")
    midi_input = pygame.midi.Input(input_id)

    print("Listening to MIDI input. Press Ctrl+C to stop.")
    try:
        while True:
            if midi_input.poll():
                midi_events = midi_input.read(10)
                print(midi_events)
    except KeyboardInterrupt:
        print("Exiting.")
    finally:
        midi_input.close()
else:
    print("No MIDI input device found.")
