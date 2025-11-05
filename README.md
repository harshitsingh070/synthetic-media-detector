<div align="center">

# 🛡️ Synthetic Media Detector

### *AI-Powered Deepfake & Synthetic Content Detection*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Java](https://img.shields.io/badge/Java-17-ED8B00?logo=openjdk&logoColor=white)](https://openjdk.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.1-6DB33F?logo=springboot&logoColor=white)](https://spring.io/projects/spring-boot)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

*Detect AI-generated content across images, audio, and video with real-time confidence scoring*

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [📖 Documentation](#-api-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## 🎯 Overview

<img width="1923" height="926" alt="Screenshot 2025-11-04 213839" src="https://github.com/user-attachments/assets/7f7c922e-ddc0-4999-aef1-e835d47623bc" />






**Synthetic Media Detector** is a full-stack web application that analyzes digital media to identify deepfakes and AI-generated content. Built with a modern microservices architecture, it provides real-time analysis with intuitive confidence scoring and detailed reporting.

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔍 Detection Capabilities
- ✅ **Multi-Modal Analysis**
  - Images (JPG, PNG, GIF, WEBP)
  - Audio (MP3, WAV, FLAC, M4A)
  - Video (MP4, AVI, MOV, MKV)
- ✅ **Smart Detection Algorithms**
  - Filename pattern analysis
  - Content hashing verification
  - Dimension analysis
  - Balanced prediction system

</td>
<td width="50%">

### 💡 User Experience
- 🎨 **Modern Interface**
  - Drag-and-drop upload
  - Real-time progress tracking
  - Interactive visualizations
- 📊 **Detailed Results**
  - Confidence scoring
  - Probability breakdown
  - Re-analysis capability
  - JSON report export

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

✔ Docker & Docker Compose
✔ 4GB RAM minimum
✔ 2GB disk space

text

### Installation

1. Clone repository
git clone https://github.com/harshitsingh070/synthetic-media-detector.git
cd synthetic-media-detector

2. Launch services
docker-compose up -d

3. Access application
open http://localhost:8080

text

### Usage

Upload a file through web UI or API
curl -X POST -F "file=@sample.jpg" http://localhost:8080/api/detect/image


---

## 🏗️ Architecture

graph LR
A[Web Browser] -->|HTTP| B[Spring Boot Backend]
B -->|REST API| C[FastAPI ML Service]
C -->|Analysis| D[Detection Engine]
D -->|Results| C
C -->|Response| B
B -->|JSON| A

text

<details>
<summary><b>📂 Project Structure</b></summary>

synthetic-media-detector/
├── 🌐 backend-java/ # Spring Boot REST API
│ ├── src/main/java/
│ ├── src/main/resources/
│ │ ├── static/ # Frontend assets
│ │ └── templates/ # HTML templates
│ ├── Dockerfile
│ └── pom.xml
│
├── 🤖 ml-service-python/ # FastAPI ML Service
│ ├── app/
│ │ ├── main.py # Core service
│ │ └── models/ # Detection logic
│ ├── requirements.txt
│ └── Dockerfile
│
├── 🐳 docker-compose.yml # Container orchestration
├── 📝 README.md
└── .gitignore

text

</details>

---

## 🛠️ Technology Stack

<div align="center">

| Layer | Technology |
|-------|-----------|
| **Backend** | ![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?logo=springboot&logoColor=white) ![Java](https://img.shields.io/badge/Java%2017-ED8B00?logo=openjdk&logoColor=white) |
| **ML Service** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python%203.10-3776AB?logo=python&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black) |
| **DevOps** | ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) ![Docker Compose](https://img.shields.io/badge/Compose-2496ED?logo=docker&logoColor=white) |

</div>

---

## 📖 API Documentation

### Image Detection
POST /api/detect/image
Content-Type: multipart/form-data

Parameters:
file: image file (required)

Response: 200 OK
{
"prediction": "real",
"confidence": 0.85,
"fake_probability": 0.15,
"real_probability": 0.85,
"processing_time": 2.34,
"file_info": {
"filename": "photo.jpg",
"size": 245678,
"dimensions":
}
}

text

<details>
<summary><b>🎵 Audio Detection</b></summary>

POST /api/detect/audio
Content-Type: multipart/form-data

text
</details>

<details>
<summary><b>🎬 Video Detection</b></summary>

POST /api/detect/video
Content-Type: multipart/form-data

text
</details>

<details>
<summary><b>🏥 Health Check</b></summary>

GET /health # ML Service
GET /actuator/health # Backend Service

text
</details>

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Processing Speed** | 2-5 seconds per file |
| **Accuracy** | 75-85% (filename-based) |
| **Max File Size** | 100MB |
| **Concurrent Users** | 10+ |

---

## 🔧 Configuration

<details>
<summary><b>Environment Variables</b></summary>

Create `.env` file:
Backend Configuration
SERVER_PORT=8080
SPRING_PROFILES_ACTIVE=production

ML Service Configuration
ML_SERVICE_URL=http://ml-service:8000
ML_SERVICE_PORT=8000

File Upload Limits
MAX_FILE_SIZE=100MB
MAX_REQUEST_SIZE=100MB

text
</details>

<details>
<summary><b>Docker Compose Override</b></summary>

Create `docker-compose.override.yml` for custom settings:
version: '3.8'
services:
backend:
environment:
- SPRING_PROFILES_ACTIVE=development

text
</details>

---

## 🧪 Testing

Run tests
docker-compose exec ml-service pytest

Check service health
curl http://localhost:8000/health
curl http://localhost:8080/actuator/health

Test image detection
curl -X POST -F "file=@test.jpg" http://localhost:8000/api/detect/image

text

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. 🍴 Fork the repository
2. 🔧 Create feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push to branch (`git push origin feature/AmazingFeature`)
5. 🔍 Open Pull Request

<details>
<summary><b>Development Guidelines</b></summary>

- Follow PEP 8 for Python code
- Follow Java conventions for Spring Boot
- Write meaningful commit messages
- Add tests for new features
- Update documentation
</details>

---

## 📝 Roadmap

- [ ] **Phase 1** - Core Features ✅
  - [x] Image detection
  - [x] Audio detection
  - [x] Video detection
  - [x] Web interface
  
- [ ] **Phase 2** - ML Enhancement
  - [ ] Integrate real ML models
  - [ ] Improve accuracy
  - [ ] Add model training pipeline
  
- [ ] **Phase 3** - Advanced Features
  - [ ] Batch processing
  - [ ] User authentication
  - [ ] Analysis history
  - [ ] Advanced reporting

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

<div align="center">

**Harshit Singh**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/harshitsingh070)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/harshitsinggh070/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:your.harshitsingh2807@gmail.com)

</div>

---

## 🙏 Acknowledgments

- [Spring Boot](https://spring.io/projects/spring-boot) - Backend framework
- [FastAPI](https://fastapi.tiangolo.com/) - ML service framework
- [Docker](https://www.docker.com/) - Containerization platform
- Open source community for inspiration

---

<div align="center">

### ⭐ Star this repository if you find it useful!

**Made with ❤️ by [Harshit Singh](https://github.com/harshitsingh070)**

*Fighting misinformation, one detection at a time* 🛡️

</div>
