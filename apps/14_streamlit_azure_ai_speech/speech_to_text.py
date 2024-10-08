import argparse
import logging
import os
import time

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


outfilename = "output.txt"


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="speech_to_text",
        description="Azure AI Speech API Speech-to-Text",
    )
    parser.add_argument(
        "-t",
        "--type",
        default="azure",
        help="Inference type, either 'local' or 'azure'",
    )
    parser.add_argument(
        "-e",
        "--endpoint",
        default="ws://localhost:5000",
        help="Host address for local inference",
    )
    parser.add_argument(
        "-s",
        "--subscription",
        default=os.getenv("AZURE_AI_SPEECH_API_SUBSCRIPTION_KEY"),
        help="Azure AI Speech API subscription key",
    )
    parser.add_argument(
        "-r",
        "--region",
        default=os.getenv("AZURE_AI_SPEECH_API_REGION"),
        help="Azure AI Speech API region",
    )
    parser.add_argument(
        "-l",
        "--language",
        default="en-US",
        help="Language code for speech recognition",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.txt",
        help="Output file path",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Set verbose mode",
    )
    return parser.parse_args()


def conversation_transcriber_recognition_canceled_cb(evt: speechsdk.SessionEventArgs):
    logger.info("Canceled event")


def conversation_transcriber_session_stopped_cb(evt: speechsdk.SessionEventArgs):
    logger.info("SessionStopped event")


def conversation_transcriber_transcribed_cb(evt: speechsdk.SpeechRecognitionEventArgs):
    logger.info("TRANSCRIBED:")
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        logger.info(f"\tText={evt.result.text}")
        logger.info(f"\tSpeaker ID={evt.result.speaker_id}")
        if evt.result.text != "":
            with open(outfilename, "a") as f:
                f.write(f"{evt.result.text}\n")
    elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        logger.info(f"\tNOMATCH: Speech could not be TRANSCRIBED: {evt.result.no_match_details}")


def conversation_transcriber_session_started_cb(evt: speechsdk.SessionEventArgs):
    logger.info("SessionStarted event")


def start_transcription(args: argparse.Namespace):
    # FIXME: This is a workaround for setting the output file path
    global outfilename
    outfilename = args.output

    speech_config = None
    if args.type == "local":
        speech_config = speechsdk.SpeechConfig(
            host=args.endpoint,
            speech_recognition_language=args.language,
        )
    if args.type == "azure":
        speech_config = speechsdk.SpeechConfig(
            subscription=args.subscription,
            region=args.region,
            speech_recognition_language=args.language,
        )
    if not speech_config:
        raise ValueError(f"Invalid inference type: {args.type}")

    conversation_transcriber = speechsdk.transcription.ConversationTranscriber(
        speech_config=speech_config,
    )

    transcribing_stop = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        # """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        logger.info(f"CLOSING on {evt}")
        nonlocal transcribing_stop
        transcribing_stop = True

    # Connect callbacks to the events fired by the conversation transcriber
    conversation_transcriber.transcribed.connect(conversation_transcriber_transcribed_cb)
    conversation_transcriber.session_started.connect(conversation_transcriber_session_started_cb)
    conversation_transcriber.session_stopped.connect(conversation_transcriber_session_stopped_cb)
    conversation_transcriber.canceled.connect(conversation_transcriber_recognition_canceled_cb)
    # stop transcribing on either session stopped or canceled events
    conversation_transcriber.session_stopped.connect(stop_cb)
    conversation_transcriber.canceled.connect(stop_cb)

    conversation_transcriber.start_transcribing_async()

    # Waits for completion.
    while not transcribing_stop:
        if os.path.exists(".stop"):
            logger.info("Stopping transcription...")
            conversation_transcriber.stop_transcribing_async()
            os.remove(".stop")
            break
        time.sleep(0.5)

    conversation_transcriber.stop_transcribing_async()


if __name__ == "__main__":
    args = init_args()

    # Set verbose mode
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Parse .env file and set environment variables
    load_dotenv()

    try:
        start_transcription(args=args)
    except Exception as err:
        logger.info(f"Encountered exception. {err}")
