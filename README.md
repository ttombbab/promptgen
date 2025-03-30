# promptgen: Staged Prompt Generation with Ollama

This repository contains a Python script (`prompt_genirator.py`) that utilizes the [Ollama](https://ollama.ai/) Python interface to generate prompts for image generation language models. The core idea is to employ a staged approach, leveraging the LLM's capabilities in a structured manner to achieve more nuanced and context-aware prompts.

## Concept: Meta Lookup for Automated Tasks

Instead of directly prompting an LLM to perform a complex task (like generating a Python class), this script uses a meta approach. Think of it as a lookup table, but driven by the LLM. The process involves breaking down the task into smaller, sequential steps, allowing the LLM to build upon previous outputs.

For example, instead of a single prompt like:
