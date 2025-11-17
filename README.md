# Nano Banana

An OOMOL workflow package for AI-powered image editing using the Nano Banana model.

## Overview

Nano Banana is a powerful image editing solution that leverages AI to transform images based on natural language instructions. This package provides seamless integration with the Nano Banana AI service through OOMOL workflows, making advanced image editing accessible and easy to use.

## Features

- **Natural Language Image Editing**: Describe your desired changes in plain language, and the AI will apply them to your images
- **Multiple Input Methods**: Support for both URL-based images and local image files
- **Reference Image Support**: Optionally provide reference images for style guidance
- **LLM-Enhanced Prompts**: Automatically refines your editing instructions for optimal results
- **Batch Processing**: Edit multiple images in a single workflow
- **Automatic Result Polling**: Handles asynchronous processing and retrieves results automatically
- **Local File Handling**: Upload local images to the cloud and optionally download edited results

## Functional Modules

### 1. Task Blocks

#### Nano Banana Edit
Submits image editing requests to the Nano Banana AI service.

- **Inputs**:
  - `image_urls`: Array of publicly accessible image URLs to process
  - `prompt`: Natural language instruction describing desired modifications
- **Outputs**:
  - `result`: API response containing request_id and status information

#### Extract Request ID
Extracts the request identifier from the API response for tracking.

- **Inputs**:
  - `response`: API response object from nano-banana-edit
- **Outputs**:
  - `request_id`: Unique request identifier for polling results

#### Nano Banana Get Result
Polls the service and retrieves edited images using the request ID.

- **Inputs**:
  - `request_id`: Request ID from nano-banana-edit
  - `poll_interval` (optional): Seconds between polling attempts
  - `max_attempts` (optional): Maximum polling attempts before timeout
- **Outputs**:
  - `images`: Array of URLs to the successfully edited images

### 2. Subflows

#### URL Images Nano Banana Edit
Complete workflow for editing images from URLs with LLM-enhanced prompts.

- **Inputs**:
  - `main_picture`: URL of primary image to edit
  - `reference_picture` (optional): Reference image URL for style guidance
  - `prompt`: Natural language editing instructions
  - `poll_interval` (optional): Polling interval configuration
  - `max_attempts` (optional): Maximum polling attempts
- **Outputs**:
  - `images`: Array of URLs to edited images

This subflow automatically:
1. Enhances your prompt using an LLM to create precise editing instructions
2. Submits the editing request to Nano Banana
3. Polls for results until completion
4. Returns the edited image URLs

#### Local Image Nano Banana Edit
Complete workflow for editing local image files.

- **Inputs**:
  - `main_picture`: Local path to primary image file
  - `reference_picture` (optional): Local path to reference image file
  - `prompt`: Natural language editing instructions
  - `save_dir` (optional): Directory to save edited images locally
  - `poll_interval` (optional): Polling interval configuration
  - `max_attempts` (optional): Maximum polling attempts
- **Outputs**:
  - `images`: Array of edited image URLs or local paths

This subflow automatically:
1. Uploads local images to the cloud
2. Uses the URL-based editing workflow
3. Optionally downloads edited images to your specified directory
4. Returns either URLs or local file paths

## Getting Started

### Prerequisites

- OOMOL Studio installed
- Python 3.10+ environment
- Internet connection for API access

### Installation

1. Install the package in OOMOL Studio
2. Dependencies will be automatically installed via the bootstrap script

### Basic Usage

#### Example 1: Edit Images from URLs

1. Use the "URL Images Nano Banana Edit" subflow
2. Provide the main image URL
3. Optionally add a reference image URL
4. Enter your editing instruction (e.g., "Change the sky to sunset colors")
5. Run the workflow
6. Receive edited image URLs

#### Example 2: Edit Local Images

1. Use the "Local Image Nano Banana Edit" subflow
2. Select your main image file
3. Optionally select a reference image
4. Enter your editing instruction
5. Optionally specify a save directory
6. Run the workflow
7. Receive edited images (saved locally if directory specified)

## How It Works

The Nano Banana package operates in several stages:

1. **Input Processing**: Accepts images either as URLs or local files. Local files are automatically uploaded to cloud storage.

2. **Prompt Enhancement**: Your natural language instructions are processed by an LLM to create precise, optimized editing prompts that the AI model can better understand.

3. **API Submission**: The images and enhanced prompts are sent to the Nano Banana AI service via the OOMOL Fusion API.

4. **Asynchronous Processing**: The service processes your request asynchronously, returning a request ID for tracking.

5. **Result Polling**: The workflow automatically polls the service at regular intervals to check if processing is complete.

6. **Result Retrieval**: Once processing is complete, edited images are retrieved and returned as URLs or saved locally.

## Technical Details

### Architecture

The package is built using OOMOL's workflow architecture with three core task blocks and two high-level subflows that combine these tasks into complete editing pipelines.

### API Integration

- **Service**: OOMOL Fusion API
- **Endpoint**: `https://fusion-api.oomol.com/v1/fal-nano-banana-edit/submit`
- **Authentication**: Automatic token management via OOMOL context
- **Error Handling**: Automatic retry with exponential backoff for SSL and connection errors

### Dependencies

- `requests`: HTTP client for API communication
- `downloaderx`: File download utilities
- `upload-to-cloud` package: Cloud storage integration
- `array` package: Array processing utilities
- `llm` package: LLM integration for prompt enhancement

## Configuration

### Polling Options

Both subflows support optional polling configuration:

- **poll_interval**: Time in seconds between result checks (default: service-defined)
- **max_attempts**: Maximum number of polling attempts before timeout (default: service-defined)

Adjust these values based on your image complexity and processing time requirements.

## Troubleshooting

### Common Issues

**API Connection Errors**
- The package includes automatic retry logic with exponential backoff
- SSL errors are automatically handled with up to 3 retry attempts

**Timeout During Polling**
- Increase `max_attempts` for complex editing tasks
- Increase `poll_interval` to reduce server load

**File Upload Failures**
- Ensure local files are accessible and not corrupted
- Check that file paths are correct

## License

See project license file for details.

## Support

For issues and questions, please refer to the OOMOL documentation or contact support through the OOMOL platform.
