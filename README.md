# FineTuningCLI

Authored by Triton Consulting Group for RobustPhysics

This program allows a user to interact with the fine tuning feature from OpenAI's API. 

> Consider reading [OpenAI's documentation](https://platform.openai.com/docs/guides/fine-tuning/common-use-cases) on Fine Tuning before proceeding.
> Fine tuning UI can be found [here](https://platform.openai.com/finetune/).

## Set Up and Run
1. Clone or download repository
2. Open repository folder in Terminal or Command Prompt
3. Ensure that Python3 is installed
4. Run `pip install openai` 
5. Run `pip install python-dotenv` 
6. Create a file called .env, type `API_KEY=` and enter your OpenAI API Key next to `API_KEY=`. do not include quotations. 

Generate an API Key [here](https://platform.openai.com/api-keys). Ensure that you have loaded a balance into your associated account.
What the .env file should look like:
```
API_KEY=sk-aiwufhawiuhfaliuawlifhikhjkawfawefo
```

7. Run `python3 cli.py`

NOTE: Never push any code with the api key in it, as Open AI will immediately disable the api key (due to the repository being public)

## Troubleshooting

If, after following the instructions, you get the following error:
```
 from openai import OpenAI
ModuleNotFoundError: No module named 'openai'
```

Run these commands in the project directory:

1. `pip3 uninstall openai`
2. `python3 --version`
3. `pip{INSERT_YOUR_PYTHON_VERSION_HERE} install openai` for example: `pip3.9.7 install openai`
4. `python3 cli.py`

## Features
The User is prompted with this when the program runs:
```
Actions: 
1. Upload a file for fine-tuning (has to be in the data directory)
2. View your existing fine-tuning jobs on OpenAI
3. Start a fine-tuning job on OpenAI
4. Chat with one of your fine-tuned models
5. Add sample conversation to training data
6. Exit program

Select an option by entering the number:
```

### Upload a file for fine-tuning
This option enables users to upload a file from the data directory to OpenAI for fine-tuning purposes. The program lists all files available in the data directory, allowing the user to select a file for upload by entering the corresponding number. After selection, the program asks for confirmation before proceeding with the upload. Once confirmed and successfully uploaded, it displays the File ID, which is essential for initiating a fine-tuning job with the specific training data.

### View your existing fine-tuning jobs on OpenAI
Selecting this option presents the user with a list of their last 10 fine-tuning jobs submitted to OpenAI. For each job, it displays detailed information including the Job ID, status (e.g., succeeded, failed, running), the fine-tuned model ID, creation time, completion time, and the number of tokens trained. This allows users to track the progress and outcome of their fine-tuning requests.

### Start a fine-tuning job on OpenAI
Through this feature, users can initiate a new fine-tuning job using one of their previously uploaded files. The program lists all files available for fine-tuning, prompting the user to select one. After selection, it requires confirmation to start the fine-tuning process. Upon confirmation, the program initiates the fine-tuning job with OpenAI and provides the user with the Job ID, which can be used to track the job's progress and status through the "View your existing fine-tuning jobs on OpenAI" feature.

### Chat with one of your fine-tuned models
This option allows users to interact with one of their successfully fine-tuned models. The program lists all models that have completed the fine-tuning process, and the user can select a model to start a conversation. The conversation interface prompts the user to enter their messages, and the selected model responds in real-time. This feature is useful for testing and interacting with fine-tuned models to assess their performance and capabilities.

### Add sample conversation to training data
This feature is designed for users who wish to expand their training dataset with additional sample conversations. The user is prompted to specify a filename (without the .jsonl extension). If the file exists in the data directory, it adds to it; otherwise, it creates a new file. Then, it asks the user for a sample user prompt and the corresponding assistant response, which are added to the specified .jsonl file in a predefined format. This helps in continuously improving and customizing the training data based on specific needs or scenarios.

### Exit program
Exits the program.



