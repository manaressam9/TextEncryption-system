import os
import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os
import os.path
import wave

def encrypt(file_path):
    #Random key generator
    key = get_random_bytes(32) # 32 bytes --> 256 bits

    # print(f"\nKEY: {key}") 
    
    #store the key to use it in decryption
    key_location = "key.bin"
    file_in = open(key_location, "wb") 
    file_in.write(key)
    file_in.close()
    
    cipher = AES.new(key, AES.MODE_CBC)
    plaintext = open(file_path, "rb").read()
    
    #pad plain text to block_size = 16 bytes if less than
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    print('\n')
    print('#'*len(ciphertext))
    print(f"\n[CIPHER TEXT]>> {ciphertext}\n")
    print('#'*len(ciphertext))

    
    #store ciphertext and IV  
    file_in = open(file_path.replace('txt','bin'), "wb") 
    file_in.write(cipher.iv)
    file_in.write(ciphertext)
    file_in.close()
    cipher_bits = ''.join(list(map(lambda i : bin(i).lstrip('0b').rjust(8,'0'),ciphertext)))
    iv_bits = ''.join(list(map(lambda i : bin(i).lstrip('0b').rjust(8,'0'),cipher.iv)))
    
    #return cipher.iv + ciphertext as bits to stegnography 16bytes for IV = first 128bits = 16bytes
    return iv_bits + cipher_bits

def stegno(audio_loc, ciphered_data):
    song = wave.open(audio_loc, mode= "r")
    
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    
    # The "secret" text message
#     ciphered_data = open(encrypted_file_loc , "r").read()
#     ciphered_data = encrypt(encrypted_file_loc)
    
    # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
    ciphered_data = ciphered_data + int((len(frame_bytes)-(len(ciphered_data)))/8) * bin(ord('#')).lstrip('0b').rjust(8,'0')
    
    # Convert text to bit array
    bits = list(map(int, ciphered_data))
    # Replace LSB of each byte of the audio data by one bit from the text bit array
    # 1- make AND logic between the audio bytes and 254 (1111 1110) 
    # 2 - make OR logic between the result bytes and secret message
    for i, bit in enumerate(bits): 
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    
    # Get the modified bytes
    frame_modified = bytes(frame_bytes)
    
    # Write bytes to a new wave audio file
    with wave.open(audio_loc.replace('.wav', '_embedded.wav') , 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified) 
    song.close()

def EncWithSteg(audio_path, file_path):
    ciphered_data = encrypt(file_path)
    stegno(audio_path, ciphered_data)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-t',
        '--path',
        type=str,
        help='Path to the text file to be encrypted in audio.',
        required=True
    )
    parser.add_argument(
        '-a',
        '--audio',
        type=str,
        help='Path to the wav audio that ciphertext will be hidden in',
        required=True
    )
    args = parser.parse_args()

    EncWithSteg(args.audio, args.path)


if __name__ == '__main__':
    main()
