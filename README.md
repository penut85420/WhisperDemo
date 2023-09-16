# VAD & ASR Demo Using Faster Whisper

使用 VAD 加 Whisper 做連續辨識的 Demo 專案。

## 環境

- Ubuntu 22.04
  - `sudo apt install portaudio19-dev python3-pyaudio`
- Python 3.10
  - `pip install pyaudio webrtcvad faster-whisper`

## 說明

- `Demo00.Record.py`
  - 示範如何透過麥克風錄音。
- `Demo01.VAD.py`
  - 示範如何使用 VAD 套件。
- `Demo02.EPD.py`
  - 示範基本的 EPD 判斷邏輯。
- `Demo03.Whisper.py`
  - 示範如何使用 Faster Whisper 做語音辨識。
- `Demo04.FullRecog.py`
  - 完整的連續辨識範例。
