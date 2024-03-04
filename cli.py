# This file provides a simple CLI to allow fine-tuning with Open AI's API. Features include:
# generating training file, uploading training file, fine tuning a model, interacting with the model

import os
import datetime
from openai import OpenAI
import json
from dotenv import load_dotenv


class FineTuningCLI:

    # Set up vars
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")  # INSERT API KEY IN THE .env
        print(self.api_key)
        self.client = OpenAI(api_key=self.api_key)
        self.finetuning_data_dir = "./data"

        # text decoration
        self.BOLD = "\033[1m"
        self.UNDERLINE = "\033[4m"
        self.RESET = "\033[0m"

    # Upload an existing file in data directory
    def upload_file(self):
        print("\nAvailable files for uploading:")
        files = os.listdir(self.finetuning_data_dir)
        for idx, file in enumerate(files):
            print(f"{idx+1}: {file}")
        file_index = int(input("\nSelect a file to upload (number): ")) - 1
        if 0 <= file_index < len(files):
            selected_file = files[file_index]
            full_path = os.path.join(self.finetuning_data_dir, selected_file)
            confirm = input(
                f"Are you sure you want to upload {selected_file}? (yes/no): "
            )
            if confirm.lower() == "yes":
                file = self.client.files.create(
                    file=open(full_path, "rb"),
                    purpose="fine-tune",
                )
                print(f"\nFile uploaded successfully! File ID: {file.id}")
            else:
                print("Upload cancelled.")
        else:
            print("Invalid selection.")

    # Lists existing jobs in easy to read format
    def view_jobs(self):
        jobs = self.client.fine_tuning.jobs.list(limit=10)
        for job in jobs.data:
            print("-" * 50)
            print(f"Job ID: {job.id}")
            print(f"Status: {job.status}")
            print(f"Model: {job.fine_tuned_model}")
            print(
                f"Created at: {datetime.datetime.fromtimestamp(job.created_at).strftime('%Y-%m-%d %H:%M:%S')}"
            )
            if job.finished_at:
                print(
                    f"Finished at: {datetime.datetime.fromtimestamp(job.finished_at).strftime('%Y-%m-%d %H:%M:%S')}"
                )
            print(
                f"Trained Tokens: {job.trained_tokens if job.trained_tokens else 'N/A'}"
            )

    # Fine tune model by choosing from uploaded files and existing models
    def fine_tune_model(self):
        print("\nFiles available to fine-tune from:")
        files = self.client.files.list()
        if not files.data:
            print("No files available for fine-tuning.")
            return

        for idx, file in enumerate(files.data):
            print(f"{idx+1}: {file.filename} (ID: {file.id})")

        file_index = int(input("\nSelect a file to fine-tune (number): ")) - 1
        if 0 <= file_index < len(files.data):
            selected_file = files.data[file_index]
            custom = input(
                f"\nType '1' to fine-tune an existing model of yours or '2' to fine-tune the base model gpt-3.5-turbo: "
            )

            model = "not selected"

            if custom == "2":
                model = "gpt-3.5-turbo"
            elif custom == "1":
                print("\nModels available for fine-tuning:")
                jobs = self.client.fine_tuning.jobs.list()
                completed_jobs = [job for job in jobs.data if job.status == "succeeded"]
                if not completed_jobs:
                    print("No completed fine-tuning jobs available.")
                    return

                for idx, job in enumerate(completed_jobs):
                    completion_date = datetime.datetime.fromtimestamp(
                        job.created_at
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    tokens_trained = job.trained_tokens if job.trained_tokens else "N/A"
                    print("-" * 50)
                    print(
                        f"{idx+1}: Model: {job.fine_tuned_model}\n   Completion Date: {completion_date}\n   Tokens Trained: {tokens_trained}"
                    )

                job_index = int(input("\nSelect a model to chat with (number): ")) - 1
                if 0 <= job_index < len(completed_jobs):
                    selected_job = completed_jobs[job_index]
                    model = selected_job.fine_tuned_model

            if model == "not selected":
                print("\nInvalid input.")
                return

            confirm = input(
                f"\nAre you sure you want to fine-tune the model {model} using {selected_file.filename}? (yes/no): "
            )

            if confirm.lower() == "yes":
                base_model = model
                response = self.client.fine_tuning.jobs.create(
                    training_file=selected_file.id,
                    model=base_model,
                )
                print(f"\nFine-tuning job started. Job ID: {response.id}")
            else:
                print("Fine-tuning cancelled.")
        else:
            print("Invalid selection.")

    # Have a chat with a model that has been fine tuned
    def converse_with_model(self):
        print("\nModels available:")
        jobs = self.client.fine_tuning.jobs.list()
        completed_jobs = [job for job in jobs.data if job.status == "succeeded"]
        if not completed_jobs:
            print("No completed fine-tuning jobs available.")
            return

        for idx, job in enumerate(completed_jobs):
            completion_date = datetime.datetime.fromtimestamp(job.created_at).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            tokens_trained = job.trained_tokens if job.trained_tokens else "N/A"
            print("-" * 50)
            print(
                f"{idx+1}: Model: {job.fine_tuned_model}\n   Completion Date: {completion_date}\n   Tokens Trained: {tokens_trained}"
            )

        job_index = int(input("\nSelect a model to chat with (number): ")) - 1
        if 0 <= job_index < len(completed_jobs):
            selected_job = completed_jobs[job_index]
            fine_tuned_model = selected_job.fine_tuned_model

            convo = [
                {
                    "role": "system",
                    "content": "I am here to help you work with your EMC models through robust physics software!",
                }
            ]

            while True:
                print("\n" + "-" * 70)
                print(
                    f"{self.UNDERLINE}User prompt{self.RESET} (type 'exit' and press Enter to exit): ",
                    end="",
                )

                prompt = input()

                if prompt.lower() == "exit":
                    break

                convo.append({"role": "user", "content": prompt})
                response = self.client.chat.completions.create(
                    model=fine_tuned_model,
                    messages=convo,
                    n=1,
                )

                print("")
                for choice in response.choices:
                    print(f"{self.UNDERLINE}Model response:{self.RESET} ", end="")
                    print(choice.message.content)
                    convo.append(
                        {
                            "role": "assistant",
                            "content": choice.message.content,
                        }
                    )

            print("Exiting conversation.")
        else:
            print("Invalid selection.")

    # CLI to add a sample conversation to the training data
    def add_training_data(self):
        filename = input(
            "\nEnter the name of the training file (without the .jsonl extension): "
        ).strip()
        full_path = os.path.join(self.finetuning_data_dir, f"{filename}.jsonl")

        if os.path.exists(full_path):
            print(f"Adding to existing file: {filename}.jsonl")
        else:
            print(f"Creating new file: {filename}.jsonl")

        print(
            "\nType 'exit' at any prompt to stop adding examples and return to the main menu."
        )

        while True:
            user_prompt = input("\nEnter the sample user prompt: ").strip()
            if user_prompt.lower() == "exit":
                break

            assistant_response = input(
                "\nEnter the corresponding assistant response: "
            ).strip()
            if assistant_response.lower() == "exit":
                break

            training_data_entry = {
                "messages": [
                    {
                        "role": "system",
                        "content": "This assistant will help you with your modeling software.",
                    },
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": assistant_response},
                ]
            }

            with open(full_path, "a") as file:
                file.write(f"{json.dumps(training_data_entry)}\n")

            print("\nTraining data added successfully.")
            print("\nAdded JSON object:")
            print(json.dumps(training_data_entry, indent=4))

        print("Returning to the main menu.")

    # Allows user to choose action
    def run(self):
        while True:
            print("\nActions: ")
            print("1. Upload a file for fine-tuning (has to be in the data directory)")
            print("2. View your existing fine-tuning jobs on OpenAI")
            print("3. Start a fine-tuning job on OpenAI")
            print("4. Chat with one of your fine-tuned models")
            print("5. Add sample conversation to training data")
            print("6. Exit program")
            choice = input("\nSelect an option by entering the number: ")

            if choice == "1":
                self.upload_file()
            elif choice == "2":
                self.view_jobs()
            elif choice == "3":
                self.fine_tune_model()
            elif choice == "4":
                self.converse_with_model()
            elif choice == "5":
                self.add_training_data()
            elif choice == "6":
                print("Exiting the Fine Tuning CLI.")
                break
            else:
                print("Invalid option. Please try again.")


# Main
if __name__ == "__main__":
    cli = FineTuningCLI()
    cli.run()
