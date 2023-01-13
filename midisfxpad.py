titlescreen = """

wryhode presents:
  __  __ _____ _____ _____      __                      _ 
 |  \/  |_   _|  __ \_   _|    / _|                    | |
 | \  / | | | | |  | || |  ___| |___  ___ __   __ _  __| |
 | |\/| | | | | |  | || | / __|  _\ \/ / '_ \ / _` |/ _` |
 | |  | |_| |_| |__| || |_\__ \ |  >  <| |_) | (_| | (_| |
 |_|  |_|_____|_____/_____|___/_| /_/\_\ .__/ \__,_|\__,_|  ver.0
                                       | |                
                                       |_|                

"""
print(titlescreen)

import pygame.midi,pygame.mixer,os,json,time
pygame.mixer.init()
pygame.midi.init()


numdevices = pygame.midi.get_count()
for device in range(numdevices):
    print("ID:" + str(device) + " " + str(pygame.midi.get_device_info(device)[1]))

print("Select a MIDI (input) device by typing in it's ID")
deviceid = -1
while deviceid == -1:
    deviceid = int(input(">"))
    try:
        mididevice = pygame.midi.Input(deviceid)
    except pygame.midi.MidiException:
        print("That's not an input port! Please select another one.")
        deviceid = -1


print("Select a MIDI (output) device by typing in it's ID (to not send output, type -1)")
deviceid = -2
while deviceid == -2:
    deviceid = int(input(">"))
    use_output = False
    if deviceid > -1:
        use_output = True
        try:
            midioutputdevice = pygame.midi.Output(14)
            for i in range(127):
                midioutputdevice.write_short(144,i,0)
        except pygame.midi.MidiException:
            print("That's not an output port! Please select another one.")
            deviceid = -2
        

audiopath = "./audio/"

print("Loading keymap")
keymapfile = open("./keymap.json","r")
keymap = json.loads(keymapfile.read())

for i in range(127):
    if use_output:
        if str(i) in keymap.keys():
            midioutputdevice.write_short(144,i,1)

print("Started succesfully!")

while True:
    try:
        if mididevice.poll():
            data = mididevice.read(1)
            if data[0][0][0] == 144: # Key is pulsed
                key = str(data[0][0][1])
                if data[0][0][2] > 0: # Key is pressed down 
                    try:
                        if use_output:
                            midioutputdevice.write_short(144,int(key),3)
                        try:
                            sound = pygame.mixer.Sound(audiopath+keymap[key])
                            sound.play()
                        except FileNotFoundError:
                            print(f"Error! Couldn't locate audio file {keymap[key]}")
                        
                    except KeyError:
                        pass
                else:
                    if use_output:
                        if key in keymap.keys():
                            midioutputdevice.write_short(144,int(key),1)
                        else:
                            midioutputdevice.write_short(144,int(key),0)
            #time.sleep(0.1)
    except KeyboardInterrupt:
        mididevice.close()
        if use_output:
            for i in range(127):
                if use_output:
                    midioutputdevice.write_short(144,i,0)
            midioutputdevice.close()
        print("Exit!")
        exit()