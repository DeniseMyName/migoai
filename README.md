Here's the updated `README.md` to reflect your latest code changes:

```markdown
# Migo AI

Migo AI is a terminal-based Python application designed to interact with AI models, allowing users to chat with an AI, manage chat histories, and customize AI settings. It supports various features such as saving chat history, using different models and characters, and displaying a spinning loader while the AI is processing.

## Features

- **Interactive AI**: Communicate with the AI through the terminal.
- **History Management**: View, load, and save chat histories.
- **Character & Modal Settings**: Customize the AI's behavior using characters and models.
- **Spinning Loader**: Indicates when the AI is processing a request.
- **Text Wrapping**: Automatically wraps long text to a specified width.

## Installation

To use Migo AI, follow these steps:

1. Clone this repository:
   ```bash
      pip install git+https://github.com/DeniseMyName/migoai.git
   ```

## Usage

To start using Migo AI, open your terminal and simply run:

```bash
migoai
```

### Command Line Arguments

- `--character <character_name>`: Set a specific character for the AI.
- `--defaultcharacter <character_name>`: Set a default character for all interactions.
- `--modal <modal_name>`: Specify the modal for the AI to operate in.
- `--viewmodals`: View all available modals.
- `--defaultmodal <modal_name>`: Set the default modal for all interactions.
- `--chat <chat_name>`: Specify a name for the chat history.
- `--viewchats`: View all available chat histories.
- `--activatevoice`: Activate voice command for migo. You can say "Hey Migo" or "Migo" to start migo.

### Example:

```bash
migoai --viewmodals
migoai --character "Assistant" --modal "helpful"
```

This will start a conversation with the AI using the "Assistant" character and the "helpful" modal.

### Exiting the Chat

To end the conversation, type `migoai-exit`. The chat will be saved automatically.

## Configuration

Migo AI allows you to configure settings like default characters and models. These settings are saved in a configuration file, which can be edited manually or through the application.

## Spinner

While the AI is processing, a spinner will appear in the terminal to indicate that it is "thinking."

## History

Migo AI saves chat history in a JSON file. This file can be loaded to resume previous conversations or for debugging purposes. If you want to view your chat histories, you can use the `--viewchats` argument.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

This version of the `README.md` provides users with a more detailed description of the latest changes, including the ability to specify a chat name, view chat history, and handle configuration settings for characters and models. Let me know if you'd like further adjustments!