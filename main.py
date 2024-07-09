from autogen import UserProxyAgent, ConversableAgent
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.code_utils import create_virtual_env
import autogen

from data import *
from instructions import *
import tempfile

from config import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

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

message = f"""
Напиши телеграм-бота на aiogram, который взаимодействуя с Assistant API,
TTS OpenAI, Whisper принимает голосовые сообщения пользователя, генерирует на них ответ,
а затем отправляет этот ответ в виде голосового сообщения."""


user_proxy = UserProxyAgent(name="user_proxy_and_executor",
                            human_input_mode="NEVER",
                            max_consecutive_auto_reply=10,
                            code_execution_config={"executor": executor},
                            system_message=user_proxy_system_message
                            )

code_writer_agent = ConversableAgent(
    "code_writer",
    system_message=f"""
{code_writer_system_message}

 !!! Вот начальное условие, по которому ты пишешь код:
    {message}.
    При возникновении ошибок ты поправляешь код в соответствии со следующими примерами:
    {aiogram_doc}.
    {audio_api_doc}.
    {assistant_api_doc}
""",
    llm_config={"config_list": config_list},
    code_execution_config=False,
    max_consecutive_auto_reply=10,
    human_input_mode="NEVER",
)

token_inserter_agent = ConversableAgent(
    "token_inserter",
    system_message=token_inserter_system_message,
    llm_config={"config_list": config_list},
    code_execution_config=False,
    max_consecutive_auto_reply=10,
    human_input_mode="NEVER",
)

# developer = GPTAssistantAgent(
#     name="Developer and a code writer. Professional in Python, aiogram, OpenAI API.",
#     description=system_message,
#     llm_config={
#         "config_list": config_list,
#         "assistant_id": settings.ASSISTANT_ID,
#     },
#     instructions=f""" Вот начальное условие, по которому ты пишешь код:
#     {message}.
#     При возникновении ошибок ты поправляешь код в соответствии со следующими примерами на
#     aiogram:
#     {aiogram_doc}.
#
#     """,
#     assistant_config={
#         "tools": [
#             {"type": "file_search"},
#         ],
#         "tool_resources": {
#             "file_search": {
#                 "vector_store_ids": [settings.VECTOR_STORE_ID]
#             }
#         }
#     }
# )


# chat = user_proxy.initiate_chat(code_writer_agent, message=message)
# print(chat)

groupchat = autogen.GroupChat(agents=[user_proxy, code_writer_agent, token_inserter_agent],
                              messages=[],
                              max_round=25,
                              send_introductions=True,
                              speaker_selection_method='round_robin')
group_chat_manager = autogen.GroupChatManager(groupchat=groupchat,
                                              llm_config={"config_list": config_list})

user_proxy.initiate_chat(group_chat_manager, message=message)