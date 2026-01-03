# ChromaDB PDF Chat

A Retrieval-Augmented Generation (RAG) chatbot that allows users to query a PDF document interactively. This project uses Google Gemini for embeddings, ChromaDB for vector storage, and OpenAI GPT for generating responses, with built-in conversation memory.

## Features

- **PDF Loading and Processing**: Load and split PDF documents into manageable chunks.
- **Vector Embeddings**: Generate embeddings using Google Gemini API in batches to handle rate limits.
- **Vector Database**: Store and retrieve document embeddings using ChromaDB.
- **Interactive Q&A**: Ask questions about the PDF content with an interactive command-line interface.
- **Conversation Memory**: Maintain context from previous interactions (up to configurable history length).
- **Logging**: Automatically log all Q&A interactions to a file.
- **Configurable**: Easily adjust parameters like chunk size, embedding model, LLM model, etc., via JSON config.

## Prerequisites

Before running this project, ensure you have:

- Python 3.8 or higher
- API keys for Google Gemini and OpenAI
- A PDF file to query (e.g., `attention.pdf`)

## Installation

1. **Clone the repository** (assuming this is on GitHub):
   ```
   git clone https://github.com/shikhar321/Context-Aware-Document-Chatbot-using-RAG.git
   cd chromadb-pdf-chat
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Configure the project**:
   - Place your PDF file in the project directory (default: `attention.pdf`).
   - Adjust settings in `config.json` as needed (e.g., PDF path, chunk size, models).

## Usage

1. **Run the application**:
   ```
   python main.py
   ```

2. **Interact with the chatbot**:
   - Enter your questions about the PDF content at the prompt.
   - Type 'exit' to quit the application.
   - The system will retrieve relevant document sections, generate answers using OpenAI GPT, and maintain conversation history.

3. **View logs**:
   - Check `qa_log.txt` for a record of all Q&A interactions.

## Configuration

Modify `config.json` to customize:

- **PDF Settings**: Path to the PDF file.
- **Text Splitting**: Chunk size and overlap for document splitting.
- **Embedding**: Model, batch size, and sleep interval to handle API rate limits.
- **Vector DB**: Persistence directory, collection name, and number of results to retrieve (top_k).
- **LLM**: Model and temperature for response generation.
- **Conversation**: Maximum history length for memory.
- **Logging**: Path to the Q&A log file.
```

## Project Structure

- `main.py`: Main application script.
- `config.json`: Configuration file.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables (API keys) - not committed to Git.
- `chroma_db/`: Directory where ChromaDB stores vector data.
- `qa_log.txt`: Log file for Q&A interactions.
- `documentation.md`: Additional setup and usage notes.

## How It Works

1. **Initialization**: Load config, API keys, and PDF document.
2. **Text Processing**: Split the PDF into chunks using LangChain's text splitter.
3. **Embedding Generation**: Create embeddings for each chunk using Gemini API (batched to avoid rate limits).
4. **Database Setup**: Store embeddings and text in ChromaDB.
5. **Query Processing**:
   - Embed the user's query.
   - Retrieve similar document chunks.
   - Build a prompt with conversation history and retrieved context.
   - Generate a response using OpenAI GPT.
6. **Memory and Logging**: Update conversation history and log the interaction.

## Dependencies

See `requirements.txt` for the full list. Key libraries include:

- `langchain` and `langchain-community`: For document loading and text splitting.
- `chromadb`: Vector database.
- `google-genai`: For Gemini embeddings.
- `openai`: For GPT-based response generation.
- `python-dotenv`: For loading environment variables.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test thoroughly.
5. Submit a pull request.
