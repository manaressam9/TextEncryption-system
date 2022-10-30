import os
import argparse
from Crypto.Cipher import AES
from base64 import b64encode
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
    
#     return nonce first 11bit, tag next 16 bit, ciphertext
    return cipher_text[:11], cipher_text[11:27], cipher_text[27:].split(b'#'*10)[0]


def decrypt(nonce, tag, ciphertext, key_file_path):
    
    key_handler = open(key_file_path, "rb")
    key = key_handler.read()
    key_handler.close()
    
    cipher = AES.new(key, AES.MODE_CCM, nonce)
    
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    
    return plaintext

def DecWithSteg(audio_embedded_path, key_file_path, out_text_path):
    try:
        nonce, tag, ciphertext = destegno(audio_embedded_path)
        plaintext = decrypt(nonce, tag, ciphertext, key_file_path)    
        file_out = open(out_text_path, "wb") 
        file_out.write(plaintext)
        file_out.close()
        
        p = str(plaintext, 'utf-8')
        print('\n')
        print('#'*len(p))
        print(f"\n[PLAIN TEXT]>> {p}\n")
        print('#'*len(p))
    except Exception as e:
        print('\n')
        print('#'*20)
        print(f'\n{e}\n')
        print('#'*20)


     

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
