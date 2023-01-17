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


def update_keymap():
    for i in range(16,127):
        if use_output:
            if str(i) in keymap[str(page)].keys():
                midioutputdevice.write_short(144,i,1)
            else:
                midioutputdevice.write_short(144,i,0)

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

for i in range(16,127):
    if use_output:
        if str(i) in keymap["0"].keys():
            midioutputdevice.write_short(144,i,1)
midioutputdevice.write_short(144,0,2)

print("Started succesfully!")

page = 0
pages = 8

while True:
    try:
        if mididevice.poll():
            data = mididevice.read(1)
            if data[0][0][0] == 144: # Key is pulsed
                key = str(data[0][0][1])
                if int(key) > 15:
                    if data[0][0][2] > 0: # Key is pressed down 
                        try:
                            if use_output:
                                midioutputdevice.write_short(144,int(key),3)
                            try:
                                sound = pygame.mixer.Sound(audiopath+keymap[str(page)][key])
                                sound.play()
                            except FileNotFoundError:
                                print(f"Error! Couldn't locate audio file {keymap[str(page)][key]}")
                            
                        except KeyError:
                            pass
                    else:
                        if use_output:
                            if key in keymap[str(page)].keys():
                                midioutputdevice.write_short(144,int(key),1)
                            else:
                                midioutputdevice.write_short(144,int(key),0)
                else:
                    if data[0][0][2] > 0:
                        prevpage = page
                        page = data[0][0][1]
                        try:
                            update_keymap()
                        except KeyError:            
                            page = prevpage
                        midioutputdevice.write_short(144,page,2)
                        if prevpage != page:
                                midioutputdevice.write_short(144,prevpage,0)

            elif data[0][0][0] == 176:
                if data[0][0][1] == 104:
                    if data[0][0][2] > 0:
                        prevpage = page
                        if page > 0:
                            page -= 1
                        try:
                            update_keymap()
                        except KeyError:
                            page -= 1
                        midioutputdevice.write_short(144,page,2)
                        if prevpage != page:
                                midioutputdevice.write_short(144,prevpage,0)
                    
                elif data[0][0][1] == 105:
                    if data[0][0][2] > 0:
                        prevpage = page
                        if page < pages:
                            page += 1
                            try:
                                update_keymap()
                            except KeyError:
                                page -= 1
                            midioutputdevice.write_short(144,page,2)
                            if prevpage != page:
                                midioutputdevice.write_short(144,prevpage,0)

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