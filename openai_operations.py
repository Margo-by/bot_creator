import os
import os.path
from pathlib import Path
from openai import OpenAI
from instructions import *

from config import settings


OPENAI_API_KEY = settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)


def create_assistant(instructions):
    assistant = client.beta.assistants.create(
        name="assistant",
        instructions=instructions,
        model="gpt-4o",
        tools=[{"type": "code_interpreter"}]
    )
    return assistant


def load_assistant(asst_id):
    assistant = client.beta.assistants.retrieve(assistant_id=asst_id)
    return assistant


def create_thread():
    thread = client.beta.threads.create()
    print(thread.id)
    return thread


def load_thread(thread_id):
    thread = client.beta.threads.retrieve(thread_id)
    return thread


def add_message(text, thread):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )
    return message


def create_run(assistant, thread):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    return run


def get_final_result(thread, run):
    if run.status == 'completed':
        answer = get_answer_from_messages(thread, run)
        return answer


def get_answer_from_messages(thread, run):
    messages = client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    try:
        answer = messages.to_dict()['data'][0]['content'][0]['text']['value']
    except:
        answer = messages.to_dict()['data'][0]['content']
    return insert_file_name(messages, answer)


def insert_file_name(messages, answer):
    try:
        messages_list = list(messages)
        content = messages_list[0][1][0].content
        annotations = content[0].text.annotations

        # непосредственно вставка названия файла после цитат
        for index, annotation in enumerate(annotations):
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                answer = answer.replace(annotation.text, f" (Ссылка номер {index} из файла {cited_file.filename}) ")
        return answer
    except:
        return answer


class FileWorker:
    @staticmethod
    def create_vector_store():
        vector_store = client.beta.vector_stores.create(
            name="Documentation"
        )
        print('vs:', vector_store.id)
        return vector_store

    @staticmethod
    def add_file_to_vector_store(vector_store_id, filename):
        path_to_file = os.path.join(Path(__file__).parent, filename)
        with open(path_to_file, 'rb') as file:
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store_id, files=[file]
            )
            print(file_batch.status)
            print(file_batch.file_counts)

    @staticmethod
    def update_assistant(assistant_id, vector_store_id):
        assistant = client.beta.assistants.update(
            assistant_id=assistant_id,
            tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )
        return assistant

    @staticmethod
    def delete_file(vs_id, file_id):
        deleted_vector_store_file = client.beta.vector_stores.files.delete(
            vector_store_id=vs_id,
            file_id=file_id
        )
        print(deleted_vector_store_file)


f = FileWorker()
fb = client.beta.vector_stores.files.list(vector_store_id=settings.VECTOR_STORE_ID)
print(fb)

