---
name: youtube-transcript
description: Retrieve and analyze YouTube video transcripts and metadata. Use when the user provides a YouTube URL and asks to summarize, extract data, or explain the content of the video.
---

# YouTube Transcript

## Overview

This skill enables the extraction and analysis of transcripts from YouTube videos, including YouTube Shorts. It leverages the `get_transcript` tool to retrieve full text, metadata, and timestamps without requiring a YouTube Data API key.

## Quick Start

To get a transcript for a video:
1. Identify the YouTube URL or Video ID.
2. Use the `get_transcript` tool from the `youtube-transcript` MCP server.
3. Process the resulting text for summarization or analysis.

## Key Tasks

### 1. Summarizing a Video
When a user asks "What is this video about?", retrieve the transcript and generate a concise summary of the main points.

### 2. Finding Specific Information
When a user asks a specific question about the video's content (e.g., "What was the recipe they used?"), retrieve the transcript and search for relevant keywords or sections.

### 3. Extracting Chapters or Timestamps
Use the `include_timestamps: true` parameter to get a breakdown of the video content by time, which is useful for creating chapters or locating specific moments.

### 4. Handling Multiple Languages
If the user requests a transcript in a specific language (e.g., Spanish), use the `lang: 'es'` parameter. The tool will attempt to find that language or fall back to available ones.

## Tool Reference: `get_transcript`

- **url** (required): YouTube URL or Video ID.
- **lang** (optional): Language code (default: 'en').
- **include_timestamps** (optional): Boolean to include `[0:00]` markers (default: false).
- **strip_ads** (optional): Boolean to remove sponsorships/ads (default: true).
