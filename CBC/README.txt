>> cd ["path to script"]

//Encrypt and Embbed
>> python EncryptWithStegnography.py -t "in.txt" -a "song.wav"

//Extract and Decrypt
>> python DecryptWithStegnography.py -t "out.txt" -a "song_embedded.wav" -k "key.bin"

//Modify Ciphertext embbedded in Audio
>> python Attack.py -a "song_embedded.wav"

//Extract and Decrypt (Attacked Audio)
>> python DecryptWithStegnography.py -t "out.txt" -a "song_embedded_attacked.wav" -k "key.bin"

