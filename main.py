
from autogen import UserProxyAgent
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.code_utils import create_virtual_env

from data import *
from instructions import *
import tempfile

from config import settings

OPENAI_API_KEY=settings.OPENAI_API_KEY
TELEGRAM_BOT_TOKEN=settings.TELEGRAM_BOT_TOKEN

venv_dir = ".rarara"
venv_context = create_virtual_env(venv_dir)

config_list = [
    {
        'model': 'gpt-4o',
        'api_key': OPENAI_API_KEY
    }
]

temp_dir = tempfile.TemporaryDirectory()

executor = LocalCommandLineCodeExecutor(
    timeout=150,
    virtual_env_context=venv_context,
)



user_proxy = UserProxyAgent(name="user_proxy_and_executor",
                            human_input_mode="NEVER",
                            max_consecutive_auto_reply=2,
                            code_execution_config={"executor": executor},
                            system_message=f"""Ты просишь разработчика написать код.
                                           Так же ты требуешь от него, чтобы он использовал 
                                           инструменты file-search.
                                           При получении кода от разработчика, ты его тестируешь.
                                           Если есть ошибки, просишь переписать код.
                                           Требуешь переписывать код столько раз, сколько потребуется!
                                           Используй во время тестирования бота: 
                                           OPENAI_API_KEY={OPENAI_API_KEY},
                                           TELEGRAM_BOT_TOKEN={TELEGRAM_BOT_TOKEN}
                                           """
                            )

developer = GPTAssistantAgent(
    name="Developer and a code writer. Professional in Python, aiogram, OpenAI API.",
    description=code_writer_instructions,
    llm_config={
        "config_list": config_list,
        "assistant_id": settings.ASSISTANT_ID,
    },
    instructions=code_writer_instructions,
    assistant_config={
        "tools": [
            {"type": "file_search"},
        ],
        "tool_resources": {
            "file_search": {
                "vector_store_ids": [settings.VECTOR_STORE_ID]
            }
        }
    }
)

message = f"""
Напиши телеграм-бота на aiogram, который взаимодействуя с Assistant API,
TTS OpenAI, Whisper принимает голосовые сообщения пользователя, генерирует на них ответ,
а затем отправляет этот ответ в виде голосового сообщения.

"""

chat = user_proxy.initiate_chat(developer, message=message)
print(chat)
