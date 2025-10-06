---
title: XiaoZhiAI_server32_Unity
description: Unity-based Xiaozhi AI visual interaction service, implementing voice and Live2D multimodal human-computer interaction experience
---

# XiaoZhiAI_server32_Unity

<div class="project-header">
  <div class="project-logo">
    <img src="./images/logo.png" alt="Unity Logo">
  </div>
  <div class="project-badges">
    <span class="badge platform">Cross-platform</span>
    <span class="badge language">C#/Unity</span>
    <span class="badge status">Active Development</span>
  </div>
</div>

## Project Introduction

XiaoZhiAI_server32_Unity is an AI application developed based on Unity, focusing on providing high-quality voice interaction and network service functions. This project leverages Unity's cross-platform features to support multiple devices and operating systems, including PC, Android, iOS, WebGL, and WeChat Mini Programs, providing users with a smooth AI voice and Live2D interaction experience.

## Technical Architecture

XiaoZhiAI_server32_Unity is built on the following technology stack:

- **Development Engine**: Unity 2020.3 or higher
- **Target Platforms**: PC, Android, iOS, WebGL, WeChat Mini Programs
- **Core Function Modules**:
  - **Voice Interaction System**: Real-time speech recognition, natural language processing, speech synthesis
  - **Live2D Interaction**: Server returns LLM expression interaction Live2D
  - **Mqtt Hardware Interaction**: Server functioncall handles IoT returns

- **Dependencies**:
  - OPUS decoding SDK
  - WebSocket network communication library
  - YooAsset resource management framework version 2.3.7
  - YuikFrameWork (YOO branch)
  - Hycrl hot update framework


## Core Features

### Voice Interaction Capabilities

<div class="features-grid">
  <div class="feature-card">
    <div class="feature-icon">🎤</div>
    <h3>Real-time Speech Recognition</h3>
    <p>Supports real-time speech-to-text in multiple languages with accuracy over 95%</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🧠</div>
    <h3>Natural Language Understanding</h3>
    <p>Deep learning-based semantic analysis for precise understanding of user intent</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🔊</div>
    <h3>Speech Synthesis</h3>
    <p>Natural and smooth voice output, supports multiple voice tones and speed adjustment</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🤖</div>
    <h3>Live2D Expression Interaction</h3>
    <p>Real-time expression changes and emotional expression based on LLM return results</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">📱</div>
    <h3>IoT and Mqtt Integration</h3>
    <p>Smart home device control and status feedback through functioncall</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🔄</div>
    <h3>Hot Update Support</h3>
    <p>Hot update capability based on Hycrl framework, upgrade without reinstallation</p>
  </div>
</div>

## Environment Requirements

### Development Environment
- Unity Version: 2020.3 or higher
- Operating System: Windows 10/11 (development environment)

### Runtime Environment
- **PC Platform**:
  - Operating System: Windows 10/11, macOS 10.14+
  - Processor: Intel i5 or equivalent performance
  - Memory: 8GB or more
  - Graphics Card: Supports DirectX 11
  
- **Mobile Platform**:
  - Android 6.0+
  - iOS 11.0+
  
- **Web Platform**:
  - Modern browsers supporting WebGL 2.0

- **Hardware Requirements**:
  - Microphone: High-quality microphone supporting 16kHz sampling rate (for voice interaction)
  - Network: Stable network connection, recommended 5Mbps or higher bandwidth

## Project Structure

```
XiaoZhiAI_server32_Unity/
├── Assets/                      # Unity resource files
│   ├── Scenes/                  # Scene files
│   ├── Scripts/                 # Script files
│   │   ├── VoiceInteraction/    # Voice interaction related scripts
│   │   ├── Networking/          # Network communication related scripts
│   │   └── ...
│   ├── Prefabs/                 # Prefabs
│   ├── Plugins/                 # Third-party plugins
│   │   ├── VoiceSDK/            # Speech recognition SDK
│   │   └── NetworkLibs/         # Network libraries
│   └── ...
├── Packages/                    # Project dependencies
├── ProjectSettings/             # Unity project settings
└── README.md                    # Project documentation
```

## Installation Guide

### Developer Installation

1. Clone the repository locally:
   ```bash
   git clone https://gitee.com/vw112266/XiaoZhiAI_server32_Unity.git
   ```

2. Install dependencies:
   - Manually import YooAsset resource management framework (v2.3.7): https://github.com/tuyoogame/YooAsset
   - Manually import YuikFrameWork-YOO branch: https://gitee.com/NikaidoShinku/YukiFrameWork

3. Open the project using Unity Hub and ensure Unity version compatibility

### User Installation

1. Download the installation package for the corresponding platform from the release page
2. Complete installation following the wizard
3. Launch the application and complete initial configuration

## Feature Showcase

### Live2D Interaction

<div class="feature-highlight">
  <div class="highlight-content">
    <h3>Expressive Live2D Models</h3>
    <ul>
      <li>Real-time expression changes based on conversation content</li>
      <li>Supports multiple emotional state expressions</li>
      <li>Accurate lip synchronization</li>
      <li>Natural blinking and head movements</li>
      <li>Customizable character appearances</li>
    </ul>
  </div>
   <div class="highlight-image">
    <img src="./images/界面1.png" alt="Demo Interface" >
  </div>
</div>

### IoT Smart Control

<div class="feature-highlight reverse">
  <div class="highlight-content">
    <h3>Smart Home Device Control</h3>
    <ul>
      <li>Control smart home devices through voice</li>
      <li>Intelligent intent recognition based on functioncall</li>
      <li>Supports multiple MQTT protocol devices</li>
      <li>Real-time device status feedback</li>
      <li>Scene linkage and automation</li>
    </ul>
  </div>
  <div class="highlight-image">
    <img src="./images/界面2.png" alt="Demo Interface">
  </div>
</div>

## Development Plan

<div class="roadmap">
  <div class="roadmap-item done">
    <div class="status-dot"></div>
    <div class="item-content">
      <h4>Completed Features</h4>
      <ul>
        <li>Basic voice interaction system</li>
        <li>Live2D model integration</li>
        <li>WebSocket network communication</li>
        <li>Basic MQTT support</li>
      </ul>
    </div>
  </div>
  
  <div class="roadmap-item progress">
    <div class="status-dot"></div>
    <div class="item-content">
      <h4>Features in Development</h4>
      <ul>
        <li>More Live2D model support</li>
        <li>Expression system optimization</li>
        <li>Mobile platform performance optimization</li>
        <li>More IoT device support</li>
      </ul>
    </div>
  </div>
  
  <div class="roadmap-item planned">
    <div class="status-dot"></div>
    <div class="item-content">
      <h4>Planned Features</h4>
      <ul>
        <li>WeChat Mini Program integration</li>
        <li>AR interactive experience</li>
        <li>Multi-character scene support</li>
        <li>User custom model system</li>
      </ul>
    </div>
  </div>
</div>

## Contribution Guide

We welcome community developers to participate in the development of XiaoZhiAI_server32_Unity project:

- Submit bug reports and feature suggestions
- Contribute code improvements and new features
- Create and share Live2D models
- Optimize performance and user experience
- Improve documentation and tutorials

Please refer to our contribution guide to learn how to participate in project development.

## Related Links

- [Project Repository](https://gitee.com/vw112266/XiaoZhiAI_server32_Unity)

<style>
.project-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.project-logo {
  width: 100px;
  height: 100px;
  margin-right: 1.5rem;
}

.project-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.project-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge.platform {
  background-color: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-dark);
}

.badge.language {
  background-color: rgba(59, 130, 246, 0.2);
  color: rgb(59, 130, 246);
}

.badge.status {
  background-color: rgba(16, 185, 129, 0.2);
  color: rgb(16, 185, 129);
}

.project-images {
  display: flex;
  gap: 1rem;
  margin: 2rem 0;
  overflow-x: auto;
}

.image-container {
  flex: 1;
  min-width: 300px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
}

.image-container img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.architecture-diagram {
  margin: 2rem 0;
  text-align: center;
}

.diagram-container {
  max-width: 100%;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
}

.diagram-container img {
  max-width: 100%;
  height: auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.feature-card {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid var(--vp-c-divider);
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: var(--vp-c-brand);
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.feature-highlight {
  display: flex;
  margin: 3rem 0;
  background-color: var(--vp-c-bg-soft);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
}

.feature-highlight.reverse {
  flex-direction: row-reverse;
}

.highlight-image {
  flex: 1;
  min-width: 40%;
}

.highlight-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.highlight-content {
  flex: 1;
  padding: 2rem;
}

.highlight-content h3 {
  color: var(--vp-c-brand);
  margin-top: 0;
  margin-bottom: 1rem;
}

.highlight-content ul {
  padding-left: 1.5rem;
}

.highlight-content li {
  margin-bottom: 0.5rem;
}

.roadmap {
  position: relative;
  margin: 3rem 0;
  padding-left: 2rem;
}

.roadmap:before {
  content: "";
  position: absolute;
  left: 7px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: var(--vp-c-divider);
}

.roadmap-item {
  position: relative;
  margin-bottom: 2rem;
}

.status-dot {
  position: absolute;
  left: -2rem;
  top: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  z-index: 1;
}

.roadmap-item.done .status-dot {
  background-color: rgb(16, 185, 129);
}

.roadmap-item.progress .status-dot {
  background-color: rgb(245, 158, 11);
}

.roadmap-item.planned .status-dot {
  background-color: rgb(99, 102, 241);
}

.item-content {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid var(--vp-c-divider);
}

.item-content h4 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.roadmap-item.done h4 {
  color: rgb(16, 185, 129);
}

.roadmap-item.progress h4 {
  color: rgb(245, 158, 11);
}

.roadmap-item.planned h4 {
  color: rgb(99, 102, 241);
}

pre {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 1.5rem;
  overflow-x: auto;
}

@media (max-width: 768px) {
  .feature-highlight, 
  .feature-highlight.reverse {
    flex-direction: column;
  }
  
  .highlight-image {
    height: 200px;
  }
  
  .project-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .project-logo {
    margin-bottom: 1rem;
  }
  
  .project-images {
    flex-direction: column;
  }
}
</style>
