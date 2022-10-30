import os
import argparse
import os
import os.path
import wave

def modifyLSB(audio_path = 'song_embedded.wav'):
    # read wave audio file
    song = wave.open(audio_path,'rb')

    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    
    
    # Extract the LSB of each byte
    cipher_list = [i & 1 for i in frame_bytes]

    #Convert each byte to char
    cipher_text = b''.join([bytes.fromhex(hex(int(''.join(map(str,cipher_list[i:i+8])),2))[2:].rjust(2,'0')) for i in range(0,len(frame_bytes),8)])
    cipher_len = len(cipher_text.split(b'#'*10)[0])
   
    for i in range(int(cipher_len/2)*8): 
        frame_bytes[i] = ((frame_bytes[i] ^ 0)) if i%2==0 else ((frame_bytes[i] ^ 1))

    # Get the modified bytes
    frame_modified = bytes(frame_bytes)
    
    # Write bytes to a new wave audio file
    with wave.open(audio_path.replace('.wav', '_attacked.wav') , 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_bytes) 
    song.close()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-a',
        '--audio',
        type=str,
        help='Path to the wav audio that ciphertext will be hidden in',
        required=True
    )
    args = parser.parse_args()

    modifyLSB(args.audio)


if __name__ == '__main__':
    main()
