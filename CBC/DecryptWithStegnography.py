import os
import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
import os
import os.path
import wave

def destegno(audio_path):
    # read wave audio file
    song = wave.open(audio_path,'rb')
    
    # Read frames and convert to byte array
    # frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    frame_bytes = song.readframes(song.getnframes())
    
    # Extract the LSB of each byte
    cipher_list = [i & 1 for i in frame_bytes]

    #Convert each byte to char
    cipher_text = b''.join([bytes.fromhex(hex(int(''.join(map(str,cipher_list[i:i+8])),2))[2:].rjust(2,'0')) for i in range(0,len(frame_bytes),8)])

#     cipher_text = b''
#     for i in range(0,len(frame_bytes),8):        
#         cipher_text += bytes.fromhex(hex(int(''.join(map(str,cipher_list[i:i+8])),2))[2:].rjust(2,'0'))    
            
    song.close()
    
    return cipher_text[:16], cipher_text[16:].split(b'#'*10)[0]

def decrypt(iv, ciphertext, key_file_path):
    
    key_handler = open(key_file_path, "rb")
    key = key_handler.read()
    key_handler.close()
    
    cipher = AES.new(key, AES.MODE_CBC,iv)
    
    #unpad ciphertext from 16 bit of AES.blocksize
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return plaintext

def DecWithSteg(audio_embedded_path, key_file_path, out_text_path):
    iv, ciphertext = destegno(audio_embedded_path)
    plaintext = decrypt(iv, ciphertext, key_file_path)    
    file_out = open(out_text_path, "wb") 
    file_out.write(plaintext)
    file_out.close()
    
    print('\n')
    print('#'*len(plaintext))
    print(f"\n[PLAIN TEXT]>> {plaintext}\n")
    print('#'*len(plaintext))
    

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
    parser.add_argument(
        '-k',
        '--key',
        type=str,        
        help='Path to the key.bin to decrypt ciphertext',
        required=True
    )
    args = parser.parse_args()

    DecWithSteg(args.audio, args.key, args.path)

if __name__ == '__main__':
    main()
