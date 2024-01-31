import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav


def compare(registered_audio_data: str, captured_audio_data: list, threshold=0.8):
    return resemblyrize(registered_audio_data) > threshold


def resemblyrize(path_a: str):
    encoder = VoiceEncoder()

    wavs = [preprocess_wav(wav) for wav in [path_a, "last.wav"]]

    embed = np.array([encoder.embed_utterance(wav) for wav in wavs])

    similarity = np.inner(embed[0], embed[1])
    print(similarity)
    return similarity
