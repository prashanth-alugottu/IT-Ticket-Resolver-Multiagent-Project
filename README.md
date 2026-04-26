# 🎯 Intelligent IT Ticket Resolver

An AI-powered IT support system that classifies tickets, searches solutions, and escalates unresolved issues using **AutoGen Multi-Agent Framework**, **Azure OpenAI**, and **Azure AI Search**.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Create Azure Resources](#1-create-azure-resources)
  - [2. Clone & Install](#2-clone--install)
  - [3. Configure Environment Variables](#3-configure-environment-variables)
  - [4. Create & Upload Knowledge Base Index](#4-create--upload-knowledge-base-index)
  - [5. Run the Application](#5-run-the-application)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

---

## 📌 Project Overview

This project demonstrates an intelligent IT support chatbot that:
- **Classifies** incoming IT support tickets into categories (Network, Hardware, Software, Password Reset, etc.)
- **Searches** a knowledge base using vector embeddings to find similar solutions
- **Escalates** unresolved tickets to the IT support team via email
- Uses **multi-agent communication** where agents collaborate to resolve issues

The system uses a **group chat** model where multiple specialized agents work together:
- **User Agent**: Accepts user input
- **Classifier Agent**: Categorizes the IT issue
- **Knowledge Base Agent**: Searches for solutions
- **Notification Agent**: Escalates unresolved issues
- **Group Chat Manager**: Orchestrates agent interactions

---

## ✨ Features

✅ **Ticket Classification**: Automatically classifies IT issues into predefined categories
✅ **Vector-Based Search**: Uses embeddings for semantic similarity search in knowledge base
✅ **Multi-Agent Collaboration**: AutoGen agents work together to resolve tickets
✅ **Email Escalation**: Automatically sends escalation emails for unsolved issues
✅ **Azure Integration**: Uses Azure OpenAI and Azure AI Search for enterprise-scale deployment
✅ **Knowledge Base**: Maintains a database of IT problems and their solutions

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **AutoGen** | Multi-agent orchestration and communication |
| **Azure OpenAI** | LLM (GPT-4/3.5) for text generation and embeddings |
| **Azure AI Search** | Vector search and document retrieval with HNSW algorithm |
| **Python 3.11+** | Core programming language |
| **SMTP (Gmail)** | Email escalation notifications |
| **dotenv** | Environment configuration management |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│           USER INPUT (IT Support Ticket)            │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   Classifier Agent         │
        │  (Categorize Issue)        │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────────────────┐
        │   Knowledge Base Agent                │
        │  (Search Solutions via Azure Search)  │
        │  - Embed query using Azure OpenAI    │
        │  - Search similar solutions           │
        │  - Return matching results            │
        └────────────┬───────────────────────────┘
                     │
       ┌─────────────┴──────────────┐
       │                            │
   RESOLVED?                    NOT RESOLVED?
       │                            │
       ▼                            ▼
    RESPOND              ┌────────────────────────────┐
  WITH SOLUTION         │  Notification Agent        │
                        │  (Escalate via Email)      │
                        │  - Send email to IT team   │
                        │  - Mark for manual review  │
                        └────────────────────────────┘
```

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Azure Subscription** with access to create resources
- **Python 3.11 or higher** installed
- **Azure CLI** (optional, for command-line setup)
- **Git** for cloning the repository
- **Gmail Account** (for email escalation feature)

---

## 🚀 Setup Instructions

### 1. Create Azure Resources

#### Step 1.1: Create Azure OpenAI Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **+ Create a resource**
3. Search for **"Azure OpenAI"** and click **Create**
4. Fill in the details:
   - **Resource Group**: Create new (e.g., `it-support-rg`)
   - **Name**: `it-support-openai` (or your preferred name)
   - **Region**: Choose a region that supports GPT-4 (e.g., East US, West Europe)
   - **Pricing Tier**: Standard S0
5. Click **Review + create** → **Create**
6. Wait for deployment to complete

#### Step 1.2: Deploy a Model in Azure OpenAI

1. Once deployed, go to **Azure OpenAI Studio** (link in resource overview)
2. Go to **Deployments**
3. Click **Create new deployment**
4. Select model: **gpt-35-turbo** (or **gpt-4** if available)
5. **Deployment name**: `gpt-35-turbo-deployment` (important: note this name)
6. Click **Create**

#### Step 1.3: Deploy an Embedding Model in Azure OpenAI

1. Go back to **Deployments** in Azure OpenAI Studio
2. Create another deployment
3. Select model: **text-embedding-3-small**
4. **Deployment name**: `text-embedding-3-small` (for embeddings)
5. Click **Create**

#### Step 1.4: Get Azure OpenAI Credentials

1. Go to **Keys and Endpoint** in your Azure OpenAI resource
2. Copy:
   - **API Key**: (Key 1 or Key 2)
   - **Endpoint**: (e.g., `https://your-resource.openai.azure.com/`)
   - **API Version**: Use `2024-02-15-preview`

---

### 2. Create Azure AI Search Resource

#### Step 2.1: Create Search Service

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **+ Create a resource**
3. Search for **"Azure AI Search"** and click **Create**
4. Fill in details:
   - **Resource Group**: Same as OpenAI (e.g., `it-support-rg`)
   - **Service Name**: `it-support-search` (or your preferred name)
   - **Region**: Same as Azure OpenAI for better latency
   - **Pricing tier**: Standard (S1 or higher)
5. Click **Review + create** → **Create**

#### Step 2.2: Get Search Credentials

1. Go to **Keys** in your Azure AI Search resource
2. Copy:
   - **Primary admin key**: (for indexing/management)
   - **Endpoint**: (e.g., `https://your-search-resource.search.windows.net/`)

---

### 3. Clone & Install

```bash
# Clone the repository
git clone <your-repo-url>
cd INTELLIGENT-IT-TICKET-RESOLVER

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

1. Copy the `.env.example` file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your credentials:
   ```bash
   # Azure OpenAI Configuration
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-azure-openai-api-key
   AZURE_DEPLOYMENT_NAME=gpt-35-turbo-deployment        # Model deployment name
   AZURE_OPENAI_DEPLOYMENT=text-embedding-3-small       # Embedding model deployment
   AZURE_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_API_VERSION=2024-02-15-preview

   # Azure AI Search Configuration
   AZURE_SEARCH_ENDPOINT=https://your-search-resource.search.windows.net/
   AZURE_SEARCH_KEY=your-search-admin-key
   ```

3. **⚠️ IMPORTANT**: Add `.env` to `.gitignore` to prevent committing secrets:
   ```bash
   echo ".env" >> .gitignore
   ```

---

### 5. Create & Upload Knowledge Base Index

#### Step 5.1: Prepare Knowledge Base Data

Your knowledge base should be in `data/knowledge_base.json`:

```json
[
  {
    "id": "pr-001",
    "category": "Password Reset",
    "problem": "I forgot my email password.",
    "solution": "Please go to the company login page, click on 'Forgot Password', and follow the steps to reset your email password."
  },
  {
    "id": "net-001",
    "category": "Network Issue",
    "problem": "I can't connect to the VPN.",
    "solution": "Try these steps: 1. Restart your VPN client 2. Clear cache 3. Contact IT if issue persists."
  }
]
```

#### Step 5.2: Create Index and Upload Documents

Run the index creation script:

```bash
python3 create_and_upload_index.py
```

This script will:
1. **Create the AI Search Index** with the schema (if it doesn't exist)
2. **Generate embeddings** for each problem using Azure OpenAI
3. **Upload documents** to Azure AI Search (batch size: 10)

Output:
```
📦 Creating index...
ℹ️ Index 'it-ticket-solutions-index' already exists. Skipping creation.
🔍 Generating embeddings...
100%|████████| 17/17 [00:05<00:00,  3.25it/s]
📤 Uploading 17 documents...
100%|████████| 2/2 [00:01<00:00,  1.50it/s]
✅ Upload completed.
```

---

### 6. Run the Application

#### Option A: Simple Group Chat Demo

Run a basic conversation between agents:

```bash
python3 group_chat.py
```

Example interaction:
```
User: Please resolve this issue: Outlook crashes every time I open it.

ClassifierAgent: {"ticket": "Outlook crashes every time I open it.",
                  "category": "Software Bug"}

KnowledgeBaseAgent: [Searching for solutions...]
Result 1:
Category: Software Bug
Problem: The Outlook application crashes on launch.
Solution: Try uninstalling and reinstalling Outlook...

TERMINATE
```

#### Option B: Interactive Testing

Run the test script:

```bash
python3 agent_test.py
```

#### Option C: Run with Your App

If you have a web interface (`app.py`), run:

```bash
python3 app.py
```

---

## 📁 Project Structure

```
INTELLIGENT-IT-TICKET-RESOLVER/
├── agents/
│   ├── __init__.py
│   ├── classifier_agent.py      # Classifies IT tickets into categories
│   ├── knowledge_base_agent.py  # Searches knowledge base for solutions
│   └── notification_agent.py    # Handles email escalation
│
├── tools/
│   ├── __init__.py
│   ├── knowledge_base_tool.py   # Vector search tool using Azure AI Search
│   └── send_email.py            # Email escalation tool
│
├── utils/
│   ├── __init__.py
│   ├── llm_config.py            # Azure OpenAI configuration
│   └── prompt.py                # System prompts for agents
│
├── data/
│   └── knowledge_base.json      # IT support solutions database
│
├── group_chat.py                # Multi-agent orchestration demo
├── agent_test.py                # Testing script
├── create_and_upload_index.py   # Index creation and upload script
├── app.py                        # Web interface (if available)
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore configuration
└── README.md                     # This file
```

---

## 🔄 How It Works

### Step 1: User Submits a Ticket
```
User: "Outlook crashes every time I open it."
```

### Step 2: Classifier Agent
- Receives the ticket
- Classifies it into one of the categories using LLM
- Output: `{"category": "Software Bug"}`

### Step 3: Knowledge Base Agent
- Takes the ticket and category
- **Generates embedding** for the problem using Azure OpenAI
- **Searches Azure AI Search** for similar problems (vector search)
- **Returns top 3 matching solutions**

### Step 4: Response
- If a good match is found → Return solution
- If no match → Notification Agent escalates via email

### Step 5: Email Escalation (if needed)
- Sends escalation email to IT support team
- Includes original ticket details
- Marks for manual review

---

## 💡 Usage Examples

### Example 1: Common Password Reset Issue
```
Input: "I forgot my password"
Classification: Password Reset
Search Result: Found matching solution
Output: "Go to login page → Click 'Forgot Password' → Follow steps"
Result: ✅ RESOLVED
```

### Example 2: Network Issue
```
Input: "Can't connect to VPN"
Classification: Network Issue
Search Result: Found solution
Output: "Restart VPN client → Clear cache → Contact IT if persists"
Result: ✅ RESOLVED
```

### Example 3: Unknown Issue
```
Input: "Something weird is happening with my monitor"
Classification: Other
Search Result: No matching solution found
Result: 📧 EMAIL ESCALATION - IT support team notified
```

---

## 🔧 Advanced Configuration

### Azure AI Search Vector Settings

The index uses **HNSW (Hierarchical Navigable Small World)** algorithm:
- **Vector dimensions**: 1536 (for text-embedding-3-small)
- **Similarity metric**: Cosine
- **Top-k results**: 3 (in `knowledge_base_tool.py`)

To modify search results:
```python
# In tools/knowledge_base_tool.py, line 48
"k": 3  # Change this to return more/fewer results
```

### Customize Categories

Edit `utils/prompt.py` to change ticket categories:
```python
classifier_prompt = """
Your task is to classify into these categories:
- Category1
- Category2
- Your Custom Category
"""
```

### Add More Knowledge Base Entries

Edit `data/knowledge_base.json`:
```json
{
  "id": "unique-id",
  "category": "Your Category",
  "problem": "User's problem",
  "solution": "Step-by-step solution"
}
```

Then re-run:
```bash
python3 create_and_upload_index.py
```

---

## 🐛 Troubleshooting

### Issue: "Authentication failed for Azure OpenAI"
**Solution**:
- Verify `.env` has correct `AZURE_OPENAI_API_KEY`
- Check API key is not expired
- Verify the endpoint URL includes trailing slash: `https://your-resource.openai.azure.com/`

### Issue: "Index not found in Azure AI Search"
**Solution**:
- Run `python3 create_and_upload_index.py` first
- Check `AZURE_SEARCH_ENDPOINT` is correct
- Verify SearchIndexClient can access the resource

### Issue: "No matching solutions found"
**Solution**:
- Ensure knowledge base has relevant data in `data/knowledge_base.json`
- Re-run index upload script to refresh embeddings
- Check if the problem description is too different from knowledge base

### Issue: "Email not sending"
**Solution**:
- Update SMTP credentials in `tools/send_email.py`
- For Gmail: Use [App Password](https://support.google.com/accounts/answer/185833) instead of regular password
- Enable "Less secure app access" in Gmail settings

### Issue: "Azure OpenAI API call timeout"
**Solution**:
- Add retry logic in `tools/knowledge_base_tool.py`
- Check network connection
- Verify region supports deployment

---

## 📊 Performance Notes

- **Vector embedding**: ~200-300ms per ticket (Azure OpenAI)
- **Search**: ~50-100ms (Azure AI Search)
- **Classification**: ~300-500ms (LLM inference)
- **Total end-to-end**: ~1-2 seconds per ticket

---

## 🚀 Deployment Options

### Local Deployment
```bash
python3 group_chat.py
```

### Azure Container Instances
```bash
az container create --resource-group it-support-rg \
  --name ticket-resolver --image python:3.11 \
  --environment-variables-from-file .env.list
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "group_chat.py"]
```

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Your Name / Team**

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📞 Support

For questions or issues:
- Check the [Troubleshooting](#troubleshooting) section
- Review Azure documentation
- Check AutoGen docs at [microsoft.github.io/autogen](https://microsoft.github.io/autogen)

---

## 🎓 Learning Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure AI Search Vector Search](https://learn.microsoft.com/en-us/azure/search/vector-search-overview)
- [AutoGen Framework](https://microsoft.github.io/autogen/)
- [Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Vector Database Concepts](https://www.pinecone.io/learn/vector-database/)

---

**⭐ If this project helps you, please star the repository!**
