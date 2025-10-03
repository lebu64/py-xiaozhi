# Camera Tools

Camera Tools is an intelligent visual recognition MCP tool that provides image capture, visual analysis, and image understanding functions.

### Common Usage Scenarios

**Image Recognition Analysis:**
- "Help me take a photo to see what this is"
- "Take a photo to identify this object"
- "Use the camera to see what's in front of me"
- "See what this thing is"
- "Identify what this is"
- "Help me look at this"
- "Take a photo to analyze this item"

**Scene Understanding:**
- "Take a photo to describe the current scene"
- "Use the camera to see what's in the room"
- "Take a photo to analyze this environment"
- "See the surrounding situation"
- "Describe this scene"
- "Analyze the environment here"

**Text Recognition:**
- "Take a photo to recognize the text on this document"
- "Use the camera to read the information on this label"
- "Take a photo to translate this English text"
- "Read this text"
- "Recognize text content"
- "Help me read this"
- "Translate this text"
- "Extract text information"

**Problem Solving:**
- "Take a photo to help me see how to solve this problem"
- "Use the camera to analyze this chart"
- "Take a photo to explain what this sign means"
- "How to solve this problem"
- "Analyze this chart"
- "Explain this sign"
- "Help me answer this question"

**Life Assistant:**
- "Take a photo to identify this plant species"
- "Use the camera to look at this recipe"
- "Take a photo to help me identify this product"
- "What plant is this"
- "Identify this flower"
- "Look at this recipe"
- "What product is this"
- "Help me look at this product"

### Usage Tips

1. **Ensure Adequate Lighting**: Good lighting conditions help improve recognition accuracy
2. **Keep Stable**: Try to keep the device stable when taking photos to avoid blur
3. **Be Specific**: Describe in detail what you want to know, such as "identify this plant" instead of "what is this"
4. **Appropriate Distance**: Maintain appropriate shooting distance to ensure the target object is clearly visible

The AI assistant will automatically call the camera tools based on your needs, capture images, and perform intelligent analysis.

## Feature Overview

### Image Capture Function
- **Smart Photography**: Automatically adjusts camera parameters to capture clear images
- **Size Optimization**: Automatically adjusts image size to improve processing efficiency
- **Format Conversion**: Converts images to standard JPEG format

### Visual Analysis Function
- **Object Recognition**: Recognizes objects and scenes in images
- **Text Recognition**: Extracts text content from images
- **Scene Understanding**: Analyzes image content and provides descriptions
- **Problem Solving**: Answers user questions based on image content

### Device Management Function
- **Camera Configuration**: Automatically detects and configures camera devices
- **Parameter Adjustment**: Supports resolution, frame rate, and other parameter settings
- **Error Handling**: Comprehensive error handling and recovery mechanism

## Tool List

### 1. Image Capture and Analysis Tools

#### take_photo - Take Photo and Analyze
Capture images and perform intelligent analysis.

**Parameters:**
- `question` (optional): Specific question or analysis requirement for the image

**Usage Scenarios:**
- Object recognition
- Scene analysis
- Text recognition
- Problem solving
- Life assistant

## Usage Examples

### Basic Photo Analysis Examples

```python
# Simple photo analysis
result = await mcp_server.call_tool("take_photo", {
    "question": "What is this object?"
})

# Scene description
result = await mcp_server.call_tool("take_photo", {
    "question": "Describe this scene"
})

# Text recognition
result = await mcp_server.call_tool("take_photo", {
    "question": "Recognize text content in the image"
})

# Problem solving
result = await mcp_server.call_tool("take_photo", {
    "question": "How to solve this math problem?"
})
```

## Technical Architecture

### Camera Management
- **Singleton Pattern**: Ensures only one camera instance globally
- **Thread Safety**: Supports safe access in multi-threaded environments
- **Resource Management**: Automatically manages camera resource opening and releasing

### Image Processing
- **OpenCV Integration**: Uses OpenCV for image capture and processing
- **Smart Scaling**: Automatically adjusts image size while maintaining optimal effect
- **Format Optimization**: Converts to JPEG format to reduce transmission load

### Visual Service
- **Remote Analysis**: Supports connecting to remote visual analysis services
- **Authentication**: Supports Token and device ID authentication
- **Error Handling**: Comprehensive network error handling mechanism

## Configuration Description

### Camera Configuration
Camera-related configuration is located in the configuration file:

```json
{
  "CAMERA": {
    "camera_index": 0,
    "frame_width": 640,
    "frame_height": 480
  }
}
```

**Configuration Item Description:**
- `camera_index`: Camera device index, default 0
- `frame_width`: Image width, default 640
- `frame_height`: Image height, default 480

### Visual Service Configuration
Visual analysis service requires configuration:
- **Service URL**: Interface address of the visual analysis service
- **Authentication**: Token or API key
- **Device Information**: Device ID and client ID

## Data Structure

### Image Data Format
```python
{
    "buf": bytes,      # JPEG image byte data
    "len": int         # Data length
}
```

### Analysis Result Format
```python
{
    "success": bool,           # Whether successful
    "message": str,            # Result information or error information
    "analysis": {              # Analysis result (when successful)
        "objects": [...],      # Recognized objects
        "text": str,           # Extracted text
        "description": str,    # Scene description
        "answer": str          # Problem answer
    }
}
```

## Image Processing Flow

### 1. Image Capture
1. Initialize camera device
2. Set capture parameters (resolution, frame rate, etc.)
3. Capture single frame image
4. Release camera resources

### 2. Image Preprocessing
1. Get image dimension information
2. Calculate scaling ratio (longest side not exceeding 320 pixels)
3. Scale image proportionally
4. Convert to JPEG format

### 3. Visual Analysis
1. Prepare request header information
2. Build multimedia request
3. Send to visual analysis service
4. Parse analysis results

## Best Practices

### 1. Image Quality Optimization
- Ensure adequate lighting conditions
- Keep camera clean
- Avoid overexposure or darkness
- Keep the subject clear

### 2. Problem Description Techniques
- Use specific and clear questions
- Avoid vague expressions
- Provide context information
- Indicate analysis focus

### 3. Performance Optimization
- Reasonably set image resolution
- Avoid frequent photography
- Release resources promptly
- Handle network timeouts

### 4. Error Handling
- Check camera availability
- Handle network connection errors
- Verify analysis results
- Provide user-friendly error messages

## Supported Analysis Types

### Object Recognition
- Daily item recognition
- Plant and animal recognition
- Food recognition
- Product recognition

### Text Recognition
- Printed text recognition
- Handwritten text recognition
- Multi-language text recognition
- Document content extraction

### Scene Understanding
- Indoor scene analysis
- Outdoor environment description
- Human action recognition
- Activity scene understanding

### Problem Solving
- Math problem solving
- Chart analysis
- Sign explanation
- Technical problems

## Precautions

1. **Privacy Protection**: Photography function involves privacy, please use with caution
2. **Network Dependency**: Visual analysis requires network connection
3. **Device Permissions**: Requires camera access permissions
4. **Processing Time**: Image analysis may take some time

## Troubleshooting

### Common Issues
1. **Camera Cannot Open**: Check device connection and permissions
2. **Image Blurry**: Check lighting conditions and focus
3. **Analysis Failure**: Check network connection and service status
4. **Inaccurate Results**: Optimize image quality and problem description

### Debugging Methods
1. Check camera device status
2. Verify network connection
3. Check log error information
4. Test different shooting conditions

With Camera Tools, you can easily implement intelligent visual recognition and image analysis, providing convenience for daily life and work.
