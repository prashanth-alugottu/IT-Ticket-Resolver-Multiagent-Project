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

### Step 3: Knowledge Base Agen
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

