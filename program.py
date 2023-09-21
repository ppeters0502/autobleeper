import requests
import sys
import json
import math
import os
import re
from os.path import exists


def main():
    try:
        audioFile = sys.argv[1]
        transcriptFile = sys.argv[2]
        print(f'Audio File: {audioFile}')
        print(f'Transcript File: {transcriptFile}')
        dictionary = swear_dictionary()
        commandList:list = []
        try:
            with open(transcriptFile, 'r') as file:
                data = json.load(file)
                for line in data['monologues']:
                    for element in line['elements']:
                        if ('value' in element and element['value']):
                            word = element['value'].lower()
                            if word in dictionary:
                                start = math.floor(element['ts'])
                                end = math.ceil(element['end_ts'])
                                if (len(commandList)==0):
                                    command = f"volume=enable='between(t,{start},{end})':volume=0[main];sine=d={(end-start)}:f=800,adelay={start}s,pan=stereo|FL=c0|FR=c0[beep];[main][beep]amix=inputs=2"
                                else:
                                    command = f",volume=enable='between(t,{start},{end})':volume=0[main];sine=d={(end-start)}:f=800,adelay={start}s,pan=stereo|FL=c0|FR=c0[beep];[main][beep]amix=inputs=2"
                                commandList.append(command)
                                print(f'NAUGHTY WORD: {word} from {start} to {end}')
        except FileNotFoundError:
            print(f'[!] Error - File path {transcriptFile} does not exist.')
        except BaseException:
            print(f'[!] Error - Unexpected Error.')

        finalCommand = f'ffmpeg -i {audioFile} -af "'  
        for command in commandList:
            finalCommand += command
        
        finalCommand += f'" outputFile.mp3'

        print(finalCommand)
    except IndexError:
        print('[!] Error - Invalid Arguments')
        print_help()
        exit(1)

def swear_dictionary() -> list:
    dictionary = [
        'arse',
        'arsehead',
        'arsehole',
        'ass',
        'asshat',
        'asshole',
        'bastard',
        'bitch',
        'bitchy',
        'bitching',
        'bloody',
        'bollocks',
        'bugger',
        'bullshit',
        'child-fucker',
        'christ',
        'cock',
        'crap',
        'cunt',
        'damn',
        'dammnit',
        'dick',
        'dickhead',
        'dildo',
        'dyke',
        'fag',
        'faggot',
        'fuck',
        'fucker',
        'fucking',
        'fuckin',
        'fucky',
        'god',
        'goddamn',
        'hell',
        'horseshit',
        'jesus',
        'kike',
        'motherfucker',
        'nigger',
        'nigga',
        'nigra',
        'piss',
        'pissed',
        'pissy',
        'prick',
        'pussy',
        'shit',
        'shitty',
        'shitter',
        'shitting',
        'shite',
        'shat',
        'slut',
        'twat'
    ]
    return dictionary

def print_help():
    """
    Print help and usage message.
    """

    print('\nprogram.py')
    print('=================================================================')
    print('USAGE: python program.py AUDIOFILEPATH TRANSCRIPTFILEPATH')

if __name__ == "__main__":
    main()