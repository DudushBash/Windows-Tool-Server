# Windows Tool Server

A modular backend service that exposes Windows functionality through a simple HTTP API.

The project indexes installed applications, performs intelligent local search, and executes system actions through reusable tools. It is designed to serve as a bridge between AI assistants, automation systems, and the Windows operating system.

> **Platform:** Windows only

---

## Overview

Windows Tool Server provides a unified interface for interacting with Windows applications.

Instead of allowing an AI model to access the operating system directly, the model communicates with this server, which validates requests and executes the appropriate tool.

Current capabilities include:

* indexing installed applications;
* searching applications using TF-IDF;
* launching applications;
* exposing functionality through FastAPI;
* modular tool architecture for future extensions.

---

## Features

* Windows Start Menu scanner
* Windows Registry scanner
* Object deduplication
* SQLite repository
* TF-IDF search engine
* Semantic search foundation
* Application launcher
* FastAPI REST API
* Extensible Tool system

---

## Architecture

```text
Client / AI Assistant
          │
          ▼
      FastAPI Server
          │
          ▼
     Tool Manager
          │
 ┌────────┴────────┐
 ▼                 ▼
Search Tool    Launch Tool
 │                 │
 ▼                 ▼
 Search Engine   Windows
 │
 ▼
SQLite Repository
 │
 ▼
Windows Scanners
```

---

## Project Structure

```text
api/
database/
models/
scanner/
search/
serializers/
tests/
tools/

main.py
requirements.txt
```

---

## Search Pipeline

```text
Windows
   │
   ▼
Scanners
   │
   ▼
Merge Engine
   │
   ▼
SQLite
   │
   ▼
Search Index
   │
   ▼
TF-IDF / Semantic Search
   │
   ▼
Search Results
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/windows-tool-server.git

cd windows-tool-server
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running

Start the API

```bash
uvicorn api.app:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Supported Platform

This project relies on Windows-specific APIs:

* Windows Registry
* COM (pywin32)
* Windows Shell
* Application Launching

Because of these dependencies, the project is intended to run directly on **Windows 10/11**.

Linux and macOS are currently not supported.

---

## Roadmap

### Completed

* Windows Start Menu Scanner
* Windows Registry Scanner
* Merge Engine
* SQLite Repository
* TF-IDF Search
* Search API
* Tool Manager
* Application Launcher

### In Progress

* Semantic Search
* Better ranking
* Improved indexing

### Planned

* File indexing
* File search
* Browser tools
* Clipboard tools
* Process management
* Plugin system
* LLM Function Calling
* Voice Assistant integration

---

## Example Use Cases

* Find installed applications
* Launch applications by name
* Integrate Windows tools with an AI assistant
* Build local desktop automation
* Create voice-controlled Windows assistants

---

## Design Principles

The project follows several principles:

* modular architecture;
* separation of search and execution;
* reusable tools;
* platform-oriented design;
* simple API surface;
* extensibility.

---

## Future Direction

The long-term goal is to provide a reusable Windows backend for AI assistants capable of interacting with the operating system through structured tools instead of unrestricted shell access.
