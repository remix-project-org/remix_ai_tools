# API Documentation

This document outlines the API endpoints for the Flask server that handles various code-related operations using language models.

## Table of Contents

1. [State](#state)
2. [System Information](#system-information)
3. [Server Management](#server-management)
4. [Model Initialization](#model-initialization)
5. [Code Operations](#code-operations)
   - [Code Completion](#code-completion)
   - [Code Insertion](#code-insertion)
   - [Code Generation](#code-generation)
   - [Code Explaining](#code-explaining)
   - [Error Explaining](#error-explaining)
   - [Solidity Answer](#solidity-answer)

## State

### GET /state

Returns the current state of the server.

**Response:**
```json
{
  "status": "running",
  "completion": true,
  "general": true
}
```


## System Information
### GET /sys

Returns system information.
**Response**: JSON object containing system information.

## Server Management
### POST /kill
Terminates the server.

## Model Initialization

### POST /init_completion
Initializes the completion model.
### Request Body:
```json
{
  "model_path": "path/to/model"
}
```

**Response**:
```json
{
  "status": "success"
}
```

### POST /init
Initializes the general model.
### Request Body:

```json
{
  "model_path": "path/to/model"
}
```
**Response**:

```json
{
  "status": "success"
}
```
## Code Operations

## POST /code_completion
Performs code completion.
Request Body:

```json
{
  "context_code": "string",
  "stream_result": false,
  "max_new_tokens": 20,
  "temperature": 0.8,
  "top_p": 0.9,
  "top_k": 50,
  "repeat_penalty": 1.2,
  "frequency_penalty": 0.2,
  "presence_penalty": 0.2
}
```
**Response**:

```json
{
  "generatedText": "string"
}
```

### POST /code_insertion
Performs code insertion.
###Request Body:

```json
{
  "code_pfx": "string",
  "code_sfx": "string",
  "max_new_tokens": 100,
  "temperature": 0.4,
  "top_p": 0.9,
  "top_k": 50,
  "repeat_penalty": 1.2,
  "frequency_penalty": 0.2,
  "presence_penalty": 0.2
}
```
**Response**:

```json
{
  "generatedText": "string"
}
```

### POST /code_generation
Generates code based on a comment.
### Request Body:

```json
{
  "gen_comment": "string",
  "stream_result": true,
  "max_new_tokens": 1024,
  "temperature": 0.1,
  "top_p": 0.9,
  "top_k": 50
}
```
**Response**: Server-Sent Events stream with JSON objects containing `generatedText` and `isGenerating` fields when `stream_result` is true. 
```json
{
  "generatedText": "string",
  "isGenerating" : "boolean"
}
```

Otherwhise,
```json
{
  "generatedText": "string"
}
```

### POST /code_explaining
Explains the provided code.
### Request Body:

```json
{
  "code": "string",
  "context": "string",
  "stream_result": false,
  "max_new_tokens": 20,
  "temperature": 0.8,
  "top_p": 0.9,
  "top_k": 50,
  "repeat_penalty": 1.2,
  "frequency_penalty": 0.2,
  "presence_penalty": 0.2
}
```
**Response**: Server-Sent Events stream with JSON objects containing `generatedText` and `isGenerating` fields when `stream_result` is true. 
```json
{
  "generatedText": "string",
  "isGenerating" : "boolean"
}
```

Otherwhise,
```json
{
  "generatedText": "string"
}
```
### POST /error_explaining
Explains errors in the provided code.
### Request Body:

```json
{
  "prompt": "string",
  "stream_result": false,
  "max_new_tokens": 2000,
  "temperature": 0.8,
  "top_p": 0.9,
  "top_k": 50
}
```
**Response**: Server-Sent Events stream with JSON objects containing `generatedText` and `isGenerating` fields when `stream_result` is true. 
```json
{
  "generatedText": "string",
  "isGenerating" : "boolean"
}
```

Otherwhise,
```json
{
  "generatedText": "string"
}
```
### POST /solidity_answer
Provides answers to Solidity-related questions.
### Request Body:

```json
{
  "prompt": "string",
  "stream_result": false,
  "max_new_tokens": 2000,
  "temperature": 0.8,
  "top_p": 0.9,
  "top_k": 50,
  "repeat_penalty": 1.2,
  "frequency_penalty": 0.2,
  "presence_penalty": 0.2
}
```
**Response**: Server-Sent Events stream with JSON objects containing `generatedText` and `isGenerating` fields when `stream_result` is true. 
```json
{
  "generatedText": "string",
  "isGenerating" : "boolean"
}
```

Otherwhise,
```json
{
  "generatedText": "string"
}
```