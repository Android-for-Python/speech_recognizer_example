Speech Recognizer Example
=========================

*Transcribe and copy to clipboard.*

Uses Android [SpeechRecognizer](https://developer.android.com/reference/android/speech/SpeechRecognizer) to transcribe.

Key `buildozer.spec` changes:

```
requirements = python3,kivy, gestures4kivy

android.permissions = INTERNET, RECORD_AUDIO

# android.api MUST BE >= 33
android.api = 33

# the java directory tree and files MUST EXIST 
android.add_src = java
```
