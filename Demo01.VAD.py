import webrtcvad

vad = webrtcvad.Vad()
vad.set_mode(1)

sample_rate = 16000
frame = b"\x00\x00" * 160  # 2 Bit x 1 Frame
print(vad.is_speech(frame, sample_rate))
