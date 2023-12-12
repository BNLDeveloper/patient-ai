from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import time
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

print('>> Loading Hosted Files...')                                        

file_names = ["data/Symptom1.pdf","data/Symptom2.pdf","data/Symtomp4.pdf"]  # Add your file paths here
file_ids = []

for file_name in file_names:
    file = client.files.create(
        file=open(file_name, "rb"),
        purpose='assistants'
    )
    file_ids.append(file.id)
    # Print all file IDs
    print('Uploaded file IDs: ' + ', '.join(file_ids))

print('>> Loading AI Assistants...')

tools = [
    {
        "type": "retrieval"  # Use the 'retrieval' tool
    }
]
assistant = client.beta.assistants.create(
    name="test",
    instructions="You are a helpful assistant. Given a set of files, you extract the most interesting information.",
    model="gpt-4-1106-preview",
    tools= tools,
    file_ids=file_ids  # Using the list of file IDs
)
assistant_id = assistant.id
print('assistant_id: ' + assistant_id)

while True:
    text = input("Enter comand: ")
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": text,  # Your query in Thai
                "file_ids": file_ids  # Using the list of file IDs
            }
        ]
    )
    thread_id = thread.id
    print('thread_id:' + thread_id)


    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_id = run.id
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

        print('run.status: ' + run.status)

        if run.status == 'completed':
            thread_messages = client.beta.threads.messages.list(thread_id)
            print(thread_messages)
            break
        else:
            time.sleep(5)


# # Create Thread
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Symptomp4 เกี่ยวกับอะไร",
#         }
#     ]
# )

# print('thread.id: ' + thread.id)

# # Create Run
# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant_id
# )

# print('run.id: ' + run.id)

# # Check Run Status Every 5 Seconds
# while True:

#     print('>> Checking run status...')
#     # Retrieve Run
#     run = client.beta.threads.runs.retrieve(
#         thread_id=thread.id,
#         run_id=run.id
#     )

#     print('run.status: ' + run.status)

#     # Check if the run status is 'completed'
#     if run.status == 'completed':
#         thread_messages = client.beta.threads.messages.list(thread.id)
#         if thread_messages:
#             print(thread_messages.data)
#         break

#     # Wait for 5 seconds before the next check
#     print('>> Waiting 5 seconds before checking again...')
#     time.sleep(5)