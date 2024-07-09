aiogram_doc = '''
Пример правильного кода:

import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
    
пример 2
import asyncio
from argparse import ArgumentParser

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("--token", help="Telegram Bot API Token")
    parser.add_argument("--chat-id", type=int, help="Target chat id")
    parser.add_argument("--message", "-m", help="Message text to sent", default="Hello, World!")

    return parser


async def main():
    parser = create_parser()
    ns = parser.parse_args()

    token = ns.token
    chat_id = ns.chat_id
    message = ns.message

    async with Bot(
        token=token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    ) as bot:
        await bot.send_message(chat_id=chat_id, text=message)


if __name__ == "__main__":
    asyncio.run(main())
    
!!!Работа сголосовыми сообщениями:

sendVoice
Returns: Message

class aiogram.methods.send_voice.SendVoice(*, chat_id: int | str, voice: ~aiogram.types.input_file.InputFile | str, business_connection_id: str | None = None, message_thread_id: int | None = None, caption: str | None = None, parse_mode: str | ~aiogram.client.default.Default | None = <Default('parse_mode')>, caption_entities: ~typing.List[~aiogram.types.message_entity.MessageEntity] | None = None, duration: int | None = None, disable_notification: bool | None = None, protect_content: bool | ~aiogram.client.default.Default | None = <Default('protect_content')>, message_effect_id: str | None = None, reply_parameters: ~aiogram.types.reply_parameters.ReplyParameters | None = None, reply_markup: ~aiogram.types.inline_keyboard_markup.InlineKeyboardMarkup | ~aiogram.types.reply_keyboard_markup.ReplyKeyboardMarkup | ~aiogram.types.reply_keyboard_remove.ReplyKeyboardRemove | ~aiogram.types.force_reply.ForceReply | None = None, allow_sending_without_reply: bool | None = None, reply_to_message_id: int | None = None, **extra_data: ~typing.Any)[source]
Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as aiogram.types.audio.Audio or aiogram.types.document.Document). On success, the sent aiogram.types.message.Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.


chat_id: int | str
Unique identifier for the target chat or username of the target channel (in the format @channelusername)

voice: InputFile | str
Audio file to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files »

business_connection_id: str | None
Unique identifier of the business connection on behalf of which the message will be sent

message_thread_id: int | None
Unique identifier for the target message thread (topic) of the forum; for forum supergroups only

caption: str | None
Voice message caption, 0-1024 characters after entities parsing

parse_mode: str | Default | None
Mode for parsing entities in the voice message caption. See formatting options for more details.

caption_entities: List[MessageEntity] | None
A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode

duration: int | None
Duration of the voice message in seconds

model_computed_fields: ClassVar[dict[str, ComputedFieldInfo]] = {}
A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

model_post_init(_ModelMetaclass__context: Any) → None
We need to both initialize private attributes and call the user-defined model_post_init method.

disable_notification: bool | None
Sends the message silently. Users will receive a notification with no sound.

protect_content: bool | Default | None
Protects the contents of the sent message from forwarding and saving

message_effect_id: str | None
Unique identifier of the message effect to be added to the message; for private chats only

reply_parameters: ReplyParameters | None
Description of the message to reply to

reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None
Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user

allow_sending_without_reply: bool | None
Pass True if the message should be sent even if the specified replied-to message is not found


reply_to_message_id: int | None
If the message is a reply, ID of the original message


Usage
As bot method
result: Message = await bot.send_voice(...)
Method as object
Imports:

from aiogram.methods.send_voice import SendVoice

alias: from aiogram.methods import SendVoice

With specific bot
result: Message = await bot(SendVoice(...))
As reply into Webhook in handler
return SendVoice(...)

!!! Работа с голосом:

Voice
class aiogram.types.voice.Voice(*, file_id: str, file_unique_id: str, duration: int, mime_type: str | None = None, file_size: int | None = None, **extra_data: Any)[source]
This object represents a voice note.


file_id: str
Identifier for this file, which can be used to download or reuse the file

file_unique_id: str
Unique identifier for this file, which is supposed to be the same over time and for different bots. Can’t be used to download or reuse the file.

duration: int
Duration of the audio in seconds as defined by sender

model_computed_fields: ClassVar[dict[str, ComputedFieldInfo]] = {}
A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

model_post_init(_ModelMetaclass__context: Any) → None
We need to both initialize private attributes and call the user-defined model_post_init method.

mime_type: str | None
Optional. MIME type of the file as defined by sender

file_size: int | None
Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may 
have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 
64-bit integer or double-precision float type are safe for storing this value.

    '''

assistant_api_doc='''
Assistants API Beta
The Assistants API allows you to build AI assistants within your own applications. An Assistant has instructions and can leverage models, tools, and files to respond to user queries. The Assistants API currently supports three types of tools: Code Interpreter, File Search, and Function calling.

You can explore the capabilities of the Assistants API using the Assistants playground or by building a step-by-step integration outlined in this guide.

Overview
A typical integration of the Assistants API has the following flow:

Create an Assistant by defining its custom instructions and picking a model. If helpful, add files and enable tools like Code Interpreter, File Search, and Function calling.
Create a Thread when a user starts a conversation.
Add Messages to the Thread as the user asks questions.
Run the Assistant on the Thread to generate a response by calling the model and the tools.
This starter guide walks through the key steps to create and run an Assistant that uses Code Interpreter. In this example, we're creating an Assistant that is a personal math tutor, with the Code Interpreter tool enabled.

Calls to the Assistants API require that you pass a beta HTTP header. This is handled automatically if you’re using OpenAI’s official Python or Node.js SDKs.
OpenAI-Beta: assistants=v2
Step 1: Create an Assistant
An Assistant represents an entity that can be configured to respond to a user's messages using several parameters like model, instructions, and tools.

Create an Assistant
python

python
from openai import OpenAI
client = OpenAI()
  
assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4o",
)
Step 2: Create a Thread
A Thread represents a conversation between a user and one or many Assistants. You can create a Thread when a user (or your AI application) starts a conversation with your Assistant.

Create a Thread
python

python
thread = client.beta.threads.create()
Step 3: Add a Message to the Thread
The contents of the messages your users or applications create are added as Message objects to the Thread. Messages can contain both text and files. There is no limit to the number of Messages you can add to Threads — we smartly truncate any context that does not fit into the model's context window.

Add a Message to the Thread
python

python
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
Step 4: Create a Run
Once all the user Messages have been added to the Thread, you can Run the Thread with any Assistant. Creating a Run uses the model and tools associated with the Assistant to generate a response. These responses are added to the Thread as assistant Messages.

Runs are asynchronous, which means you'll want to monitor their status by polling the Run object until a terminal status is reached. For convenience, the 'create and poll' SDK helpers assist both in creating the run and then polling for its completion.

Create a Run
python

python
run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)
Once the Run completes, you can list the Messages added to the Thread by the Assistant.

python

python
if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
else:
  print(run.status)
You may also want to list the Run Steps of this Run if you'd like to look at any tool calls made during this Run.
'''

whisper_doc = '''
Speech to text
Learn how to turn audio into text

Introduction
The Audio API provides two speech to text endpoints, transcriptions and translations, based on our state-of-the-art open source large-v2 Whisper model. They can be used to:

Transcribe audio into whatever language the audio is in.
Translate and transcribe the audio into english.
File uploads are currently limited to 25 MB and the following input file types are supported: mp3, mp4, mpeg, mpga, m4a, wav, and webm.

Quickstart
Transcriptions
The transcriptions API takes as input the audio file you want to transcribe and the desired output file format for the transcription of the audio. We currently support multiple input and output file formats.

Transcribe audio
python

python
from openai import OpenAI
client = OpenAI()

audio_file= open("/path/to/file/audio.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)
By default, the response type will be json with the raw text included.

{
  "text": "Imagine the wildest idea that you've ever had, and you're curious about how it might scale to something that's a 100, a 1,000 times bigger.
....
}
The Audio API also allows you to set additional parameters in a request. For example, if you want to set the response_format as text, your request would look like the following:

Additional options
python

python
from openai import OpenAI
client = OpenAI()

audio_file = open("/path/to/file/speech.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file, 
  response_format="text"
)
print(transcription.text)
The API Reference includes the full list of available parameters.

Translations
The translations API takes as input the audio file in any of the supported languages and transcribes, if necessary, the audio into English. This differs from our /Transcriptions endpoint since the output is not in the original input language and is instead translated to English text.

Translate audio
python

python
from openai import OpenAI
client = OpenAI()

audio_file= open("/path/to/file/german.mp3", "rb")
translation = client.audio.translations.create(
  model="whisper-1", 
  file=audio_file
)
print(translation.text)
In this case, the inputted audio was german and the outputted text looks like:

Hello, my name is Wolfgang and I come from Germany. Where are you heading today?
We only support translation into English at this time.

Supported languages
We currently support the following languages through both the transcriptions and translations endpoint:

Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

While the underlying model was trained on 98 languages, we only list the languages that exceeded <50% word error rate (WER) which is an industry standard benchmark for speech to text model accuracy. The model will return results for languages not listed above but the quality will be low.

Timestamps
By default, the Whisper API will output a transcript of the provided audio in text. The timestamp_granularities[] parameter enables a more structured and timestamped json output format, with timestamps at the segment, word level, or both. This enables word-level precision for transcripts and video edits, which allows for the removal of specific frames tied to individual words.

Timestamp options
python

python
from openai import OpenAI
client = OpenAI()

audio_file = open("speech.mp3", "rb")
transcript = client.audio.transcriptions.create(
  file=audio_file,
  model="whisper-1",
  response_format="verbose_json",
  timestamp_granularities=["word"]
)

print(transcript.words)
Longer inputs
By default, the Whisper API only supports files that are less than 25 MB. If you have an audio file that is longer than that, you will need to break it up into chunks of 25 MB's or less or used a compressed audio format. To get the best performance, we suggest that you avoid breaking the audio up mid-sentence as this may cause some context to be lost.

One way to handle this is to use the PyDub open source Python package to split the audio:

from pydub import AudioSegment

song = AudioSegment.from_mp3("good_morning.mp3")

# PyDub handles time in milliseconds
ten_minutes = 10 * 60 * 1000

first_10_minutes = song[:ten_minutes]

first_10_minutes.export("good_morning_10.mp3", format="mp3")
OpenAI makes no guarantees about the usability or security of 3rd party software like PyDub.

Prompting
You can use a prompt to improve the quality of the transcripts generated by the Whisper API. The model will try to match the style of the prompt, so it will be more likely to use capitalization and punctuation if the prompt does too. However, the current prompting system is much more limited than our other language models and only provides limited control over the generated audio. Here are some examples of how prompting can help in different scenarios:

Prompts can be very helpful for correcting specific words or acronyms that the model may misrecognize in the audio. For example, the following prompt improves the transcription of the words DALL·E and GPT-3, which were previously written as "GDP 3" and "DALI": "The transcript is about OpenAI which makes technology like DALL·E, GPT-3, and ChatGPT with the hope of one day building an AGI system that benefits all of humanity"
To preserve the context of a file that was split into segments, you can prompt the model with the transcript of the preceding segment. This will make the transcript more accurate, as the model will use the relevant information from the previous audio. The model will only consider the final 224 tokens of the prompt and ignore anything earlier. For multilingual inputs, Whisper uses a custom tokenizer. For English only inputs, it uses the standard GPT-2 tokenizer which are both accessible through the open source Whisper Python package.
Sometimes the model might skip punctuation in the transcript. You can avoid this by using a simple prompt that includes punctuation: "Hello, welcome to my lecture."
The model may also leave out common filler words in the audio. If you want to keep the filler words in your transcript, you can use a prompt that contains them: "Umm, let me think like, hmm... Okay, here's what I'm, like, thinking."
Some languages can be written in different ways, such as simplified or traditional Chinese. The model might not always use the writing style that you want for your transcript by default. You can improve this by using a prompt in your preferred writing style.

'''

tts_doc = '''
Text to speech
Learn how to turn text into lifelike spoken audio

Introduction
The Audio API provides a speech endpoint based on our TTS (text-to-speech) model. It comes with 6 built-in voices and can be used to:

Narrate a written blog post
Produce spoken audio in multiple languages
Give real time audio output using streaming
Here is an example of the alloy voice:

Please note that our usage policies require you to provide a clear disclosure to end users that the TTS voice they are hearing is AI-generated and not a human voice.
Quick start
The speech endpoint takes in three key inputs: the model, the text that should be turned into audio, and the voice to be used for the audio generation. A simple request would look like the following:

Generate spoken audio from input text
python

python
from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Today is a wonderful day to build something people love!"
)

response.stream_to_file(speech_file_path)
By default, the endpoint will output a MP3 file of the spoken audio but it can also be configured to output any of our supported formats.

Audio quality
For real-time applications, the standard tts-1 model provides the lowest latency but at a lower quality than the tts-1-hd model. Due to the way the audio is generated, tts-1 is likely to generate content that has more static in certain situations than tts-1-hd. In some cases, the audio may not have noticeable differences depending on your listening device and the individual person.

Voice options
Experiment with different voices (alloy, echo, fable, onyx, nova, and shimmer) to find one that matches your desired tone and audience. The current voices are optimized for English.

Alloy
Echo
Fable
Onyx
Nova
Shimmer
Supported output formats
The default response format is "mp3", but other formats like "opus", "aac", "flac", and "pcm" are available.

Opus: For internet streaming and communication, low latency.
AAC: For digital audio compression, preferred by YouTube, Android, iOS.
FLAC: For lossless audio compression, favored by audio enthusiasts for archiving.
WAV: Uncompressed WAV audio, suitable for low-latency applications to avoid decoding overhead.
PCM: Similar to WAV but containing the raw samples in 24kHz (16-bit signed, low-endian), without the header.
Supported languages
The TTS model generally follows the Whisper model in terms of language support. Whisper supports the following languages and performs well despite the current voices being optimized for English:

Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

You can generate spoken audio in these languages by providing the input text in the language of your choice.

Streaming real time audio
The Speech API provides support for real time audio streaming using chunk transfer encoding. This means that the audio is able to be played before the full file has been generated and made accessible.

from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello world! This is a streaming test.",
)

response.stream_to_file("output.mp3")
FAQ
How can I control the emotional range of the generated audio?
There is no direct mechanism to control the emotional output of the audio generated. Certain factors may influence the
 output audio like capitalization or grammar but our internal tests with these have yielded mixed results.

Can I create a custom copy of my own voice?
No, this is not something we support.

Do I own the outputted audio files?
Yes, like with all outputs from our API, the person who created them owns the output. You are still required to inform end users that they are hearing audio generated by AI and not a real person talking to them.
'''


