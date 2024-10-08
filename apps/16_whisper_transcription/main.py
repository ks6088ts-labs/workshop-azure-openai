import argparse
import logging

import whisper
from dotenv import load_dotenv


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="whisper_transcription",
        description="Transcript with Whisper model",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="turbo",
        help="Model name",
    )
    parser.add_argument(
        "-f",
        "--file",
        default="dist/sample_audio.wav",
        help="Audio file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = init_args()

    # Set verbose mode
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Parse .env file and set environment variables
    load_dotenv()

    model = whisper.load_model(name=args.model)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(
        file=args.file,
    )
    audio = whisper.pad_or_trim(
        array=audio,
        length=30 * 16000,
    )

    # make log-Mel spectrogram and move to the same device as the model
    # https://github.com/openai/whisper/pull/1764
    mel = whisper.log_mel_spectrogram(
        audio=audio,
        n_mels=128,
    ).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)
