# pyJianYingDraft API Documentation

## Overview

pyJianYingDraft Web API provides Django REST Framework endpoints for creating JianYing drafts with audio, video, and text components.

## Basic Information

- **Base URL**: `http://localhost:8000`
- **Data Format**: JSON
- **Encoding**: UTF-8
- **Framework**: Django + Django REST Framework

## API Endpoints

### Health Check
- **Path**: `GET /api/health/`
- **Function**: Service health status
- **Parameters**: None

### Basic Project
- **Path**: `POST /api/basic-project/`
- **Function**: Create basic JianYing project
- **Parameters**: None

### Text Segment
- **Path**: `POST /api/text-segment/`
- **Function**: Create text segment
- **Parameters**:
```json
{
    "text": "Sample text",
    "duration": "3s",
    "color": [1.0, 1.0, 0.0],
    "font": "文轩体"
}
```

### Audio Segment
- **Path**: `POST /api/audio-segment/`
- **Function**: Create audio segment
- **Parameters**:
```json
{
    "duration": "5s",
    "volume": 0.6,
    "fade_in": "1s"
}
```

### Video Segment
- **Path**: `POST /api/video-segment/`
- **Function**: Create video segment
- **Parameters**:
```json
{
    "duration": "4.2s"
}
```

### Comprehensive Project
- **Path**: `POST /api/comprehensive/`
- **Function**: Create comprehensive project with all features
- **Parameters**: None

### Project Management
- **Path**: `GET /api/projects/`
- **Function**: Get project list
- **Parameters**: None

- **Path**: `GET /api/dashboard/`
- **Function**: Get dashboard statistics
- **Parameters**: None

## Usage Examples

### Python Example
```python
import requests

# Health check
response = requests.get('http://localhost:8000/api/health/')
print(response.json())

# Create text segment
data = {
    "text": "Hello World",
    "duration": "3s",
    "color": [1.0, 0.0, 0.0]
}
response = requests.post('http://localhost:8000/api/text-segment/', json=data)
print(response.json())
```

### cURL Example
```bash
# Health check
curl -X GET http://localhost:8000/api/health/

# Create basic project
curl -X POST http://localhost:8000/api/basic-project/ \
  -H "Content-Type: application/json"
```

## Notes

1. **Assets**: Ensure asset files exist in the `assets` directory
2. **Output**: Generated files are saved in the `outputs` directory
3. **Django Admin**: Available at `/admin/` for project management
4. **Authentication**: JWT tokens supported for protected endpoints

## Version Information

- **Current Version**: 2.0.0 (Django)
- **Framework**: Django 4.2.7 + DRF 3.14.0
- **Python**: 3.7+
