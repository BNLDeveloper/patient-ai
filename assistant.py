from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import time
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

print('>> Loading Hosted Files...')                                        

file = client.files.create(
        file=open("data/CentralWorld.pdf", "rb"),
        purpose='assistants'
    )
file_id = file.id

print('file.id: ' + file_id)

print('>> Loading AI Assistants...')

tools = [
            {"type": "retrieval"},
    ]

# Create the AI Assistant
assistant = client.beta.assistants.create(
        name="test",
        instructions="You are a helpful assistant. Given a set of files, you extract the most interesting information.",
        model="gpt-4-1106-preview",
        tools=tools,
        file_ids=[file_id]
)
assistant_id = assistant.id

print('assistant.id: ' + assistant_id)

while True:
    text = input("Enter comand: ")
    # Create Thread
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ]
    )

    print('thread.id: ' + thread.id)

    # Create Run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    print('run.id: ' + run.id)

    # Check Run Status Every 5 Seconds
    while True:

        print('>> Checking run status...')
        # Retrieve Run
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        print('run.status: ' + run.status)

        # Check if the run status is 'completed'
        if run.status == 'completed':
            thread_messages = client.beta.threads.messages.list(thread.id)
            if thread_messages:
                print(thread_messages.data)
            break

        # Wait for 5 seconds before the next check
        print('>> Waiting 5 seconds before checking again...')
        time.sleep(5)