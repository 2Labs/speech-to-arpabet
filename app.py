import streamlit as st
import speech_recognition as sr
import nltk
from nltk.corpus import cmudict

# Download CMUdict if not already
nltk.download('cmudict', quiet=True)
arpabet = cmudict.dict()

def get_arpabet(word):
    word = word.lower()
    if word in arpabet:
        return [' '.join(pron) for pron in arpabet[word]]
    else:
        return [f"[{word} not found]"]

def transcribe_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak clearly into the mic.")
        audio = r.listen(source)
        st.success("✅ Audio captured. Processing...")

        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
            return None

# Streamlit UI
st.title("🎙️ Speech to ARPAbet Converter")

if st.button("Record from Microphone"):
    transcription = transcribe_audio()
    if transcription:
        st.subheader("📝 Transcription:")
        st.write(transcription)

        st.subheader("🔡 ARPAbet Phonemes:")
        for word in transcription.split():
            phonemes = get_arpabet(word)
            for p in phonemes:
                st.text(f"{word} -> {p}")
    else:
        st.warning("Could not understand the audio. Try again.")
