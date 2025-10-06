---
title: open-xiaoai
description: Let XiaoAI speakers "hear your voice", an open-source project that unlocks infinite possibilities
---

# open-xiaoai

<div class="project-header">
  <div class="project-logo">
    <img src="https://avatars.githubusercontent.com/u/35302658?s=48&v=4" alt="open-xiaoai Logo">
  </div>
  <div class="project-badges">
    <span class="badge platform">Cross-platform</span>
    <span class="badge language">Rust/Python/Node.js</span>
    <span class="badge status">Experimental</span>
  </div>
</div>

<div class="project-banner">
  <img src="./images/logo.png" alt="Open-XiaoAI Project Cover">
</div>

## Project Introduction

Open-XiaoAI is an open-source project that lets XiaoAI speakers "hear your voice", seamlessly integrating XiaoAI speakers with the Xiaozhi AI ecosystem. This project directly takes over the "ears" and "mouth" of XiaoAI speakers, fully unleashing their potential through multimodal large models and AI Agent technology, unlocking infinite possibilities.

In 2017, when the world's first smart speaker with tens of millions of sales was born, we thought we had touched the future. But we soon discovered that these devices were trapped in the cage of "command-response":

- It can hear decibels, but cannot understand emotions
- It can execute commands, but cannot think proactively
- It has tens of millions of users, but only one set of thinking

The "Jarvis"-level artificial intelligence we once imagined has been reduced to "alarm clock + music player" in real-world scenarios.

**True intelligence should not be bound by preset code logic, but should evolve like a living organism through interaction.**

Building on the previous [MiGPT](https://github.com/idootop/mi-gpt) project, Open-XiaoAI evolves again, providing new ways for the Xiaozhi ecosystem to interact with XiaoAI speakers.

## Core Features

<div class="features-grid">
  <div class="feature-card">
    <div class="feature-icon">🎤</div>
    <h3>Voice Input Takeover</h3>
    <p>Directly capture XiaoAI speaker's microphone input, bypassing original speech recognition limitations</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🔊</div>
    <h3>Audio Output Control</h3>
    <p>Completely take over XiaoAI speaker's speakers, can play custom audio and TTS content</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🧠</div>
    <h3>AI Model Integration</h3>
    <p>Supports integration with Xiaozhi AI, ChatGPT and other large models for natural conversation experience</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🌐</div>
    <h3>Cross-platform Support</h3>
    <p>Client developed in Rust, Server supports Python and Node.js implementations</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🛠️</div>
    <h3>Extensible Architecture</h3>
    <p>Modular design, convenient for developers to add custom functions and integrate other services</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🎮</div>
    <h3>Developer Friendly</h3>
    <p>Detailed documentation and tutorials to help developers get started quickly and customize their own functions</p>
  </div>
</div>

## Demo Videos

<div class="demo-videos">
  <div class="video-item">
    <a href="https://www.bilibili.com/video/BV1NBXWYSEvX" target="_blank" class="video-link">
      <div class="video-thumbnail">
        <img src="https://raw.githubusercontent.com/idootop/open-xiaoai/main/docs/images/xiaozhi.jpg" alt="XiaoAI Speaker Connected to Xiaozhi AI">
      </div>
      <div class="video-title">
        <span class="video-icon">▶️</span>
        <span>XiaoAI Speaker Connected to Xiaozhi AI Demo</span>
      </div>
    </a>
  </div>
  
  <div class="video-item">
    <a href="https://www.bilibili.com/video/BV1N1421y7qn" target="_blank" class="video-link">
      <div class="video-thumbnail">
        <img src="https://github.com/idootop/open-xiaoai/raw/main/docs/images/migpt.jpg" alt="XiaoAI Speaker Connected to MiGPT">
      </div>
      <div class="video-title">
        <span class="video-icon">▶️</span>
        <span>XiaoAI Speaker Connected to MiGPT Demo</span>
      </div>
    </a>
  </div>
</div>

## Quick Start

<div class="important-notice">
  <div class="notice-icon">⚠️</div>
  <div class="notice-content">
    <strong>Important Notice</strong>
    <p>This tutorial only applies to <strong>XiaoAI Speaker Pro (LX06)</strong> and <strong>Xiaomi Smart Speaker Pro (OH2P)</strong> models. <strong>Do not use directly</strong> with other models of XiaoAI speakers!</p>
  </div>
</div>

The Open-XiaoAI project consists of Client and Server components. You can get started quickly by following these steps:

### Installation Steps

<div class="steps">
  <div class="step">
    <div class="step-number">1</div>
    <div class="step-content">
      <h4>XiaoAI Speaker Firmware Update</h4>
      <p>Flash and update XiaoAI speaker patch firmware, enable and SSH connect to XiaoAI speaker</p>
      <a href="https://github.com/idootop/open-xiaoai/blob/main/docs/flash.md" target="_blank" class="step-link">View Detailed Tutorial</a>
    </div>
  </div>
  
  <div class="step">
    <div class="step-number">2</div>
    <div class="step-content">
      <h4>Client Deployment</h4>
      <p>Compile Client patch program on computer, then copy and run on XiaoAI speaker</p>
      <a href="https://github.com/idootop/open-xiaoai/blob/main/packages/client-rust/README.md" target="_blank" class="step-link">View Detailed Tutorial</a>
    </div>
  </div>
  
  <div class="step">
    <div class="step-number">3</div>
    <div class="step-content">
      <h4>Server Deployment</h4>
      <p>Run Server demo program on computer to experience XiaoAI speaker's new capabilities</p>
      <ul class="step-options">
        <li><a href="https://github.com/idootop/open-xiaoai/blob/main/packages/server-python/README.md" target="_blank">Python Server - XiaoAI Speaker Connected to Xiaozhi AI</a></li>
        <li><a href="https://github.com/idootop/open-xiaoai/blob/main/packages/server-node/README.md" target="_blank">Node.js Server - XiaoAI Speaker Connected to MiGPT-Next</a></li>
      </ul>
    </div>
  </div>
</div>

## How It Works

Open-XiaoAI works in the following way:

1. **Firmware Patch**: Modify XiaoAI speaker's firmware to allow SSH access and low-level system control
2. **Audio Stream Hijacking**: Client program directly captures microphone input and controls speaker output
3. **Network Communication**: Establish WebSocket connection between client and server for real-time communication
4. **AI Processing**: Server receives voice input, processes it through AI models and returns responses
5. **Custom Functions**: Developers can implement various custom functions and integrations on the server

## Related Projects

If you don't want to flash firmware, or don't have a XiaoAI Speaker Pro, the following projects might be useful:

- [MiGPT](https://github.com/idootop/mi-gpt) - Original project for connecting ChatGPT to XiaoAI speakers
- [MiGPT-Next](https://github.com/idootop/migpt-next) - Next generation version of MiGPT
- [XiaoGPT](https://github.com/yihong0618/xiaogpt) - Another XiaoAI speaker ChatGPT integration solution
- [XiaoMusic](https://github.com/hanxi/xiaomusic) - XiaoAI speaker music playback enhancement

## Technical References

If you want to learn more technical details, the following links might be helpful:

- [xiaoai-patch](https://github.com/duhow/xiaoai-patch) - XiaoAI speaker firmware patch

## Disclaimer

<div class="disclaimer">
  <h4>Scope of Application</h4>
  <p>This project is a non-profit open-source project, limited to technical principle research, security vulnerability verification, and non-profit personal use. Strictly prohibited for commercial services, network attacks, data theft, system destruction, and other scenarios that violate the "Cybersecurity Law" and the legal regulations of the user's jurisdiction.</p>
  
  <h4>Unofficial Statement</h4>
  <p>This project is independently developed by third-party developers and has no affiliation/cooperative relationship with Xiaomi Group and its affiliates (hereinafter referred to as "rights holders"), nor has it received official authorization/recognition or technical support. All rights to trademarks, firmware, and cloud services involved in the project belong to Xiaomi Group. If rights holders claim rights, users should immediately and proactively stop using and delete this project.</p>
  
  <p>Continued use of this project indicates that you have fully read and agreed to the <a href="https://github.com/idootop/open-xiaoai/blob/main/agreement.md" target="_blank">User Agreement</a>, otherwise please immediately terminate use and completely delete this project.</p>
</div>

## License

This project uses the [MIT](https://github.com/idootop/open-xiaoai/blob/main/LICENSE) License © 2024-PRESENT Del Wang

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
  background-color: rgba(139, 92, 246, 0.2);
  color: rgb(139, 92, 246);
}

.project-banner {
  width: 100%;
  margin: 2rem 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
}

.project-banner img {
  width: 100%;
  height: auto;
  display: block;
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

.demo-videos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.video-item {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.video-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.video-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.video-thumbnail {
  width: 100%;
  height: 180px;
  overflow: hidden;
}

.video-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.video-item:hover .video-thumbnail img {
  transform: scale(1.05);
}

.video-title {
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.video-icon {
  color: var(--vp-c-brand);
}

.important-notice {
  background-color: rgba(234, 179, 8, 0.1);
  border-left: 4px solid rgba(234, 179, 8, 0.8);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.5rem;
  margin: 2rem 0;
  display: flex;
  gap: 1rem;
}

.notice-icon {
  font-size: 1.5rem;
}

.notice-content strong {
  display: block;
  margin-bottom: 0.5rem;
}

.steps {
  margin: 2rem 0;
}

.step {
  display: flex;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background-color: var(--vp-c-brand);
  color: white;
  border-radius: 50%;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: var(--vp-c-brand);
}

.step-link {
  display: inline-block;
  margin-top: 0.5rem;
  color: var(--vp-c-brand);
  text-decoration: none;
  font-weight: 500;
}

.step-link:hover {
  text-decoration: underline;
}

.step-options {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin-top: 0.5rem;
}

.architecture-diagram {
  text-align: center;
  margin: 2rem 0;
}

.architecture-diagram img {
  max-width: 100%;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
}

.disclaimer {
  background-color: rgba(239, 68, 68, 0.1);
  border-left: 4px solid rgba(239, 68, 68, 0.8);
  border-radius: 0 8px 8px 0;
  padding: 1.5rem;
  margin: 2rem 0;
}

.disclaimer h4 {
  margin-top: 0;
  color: rgba(239, 68, 68, 0.8);
  margin-bottom: 0.5rem;
}

.disclaimer p {
  margin: 0.5rem 0;
}

@media (max-width: 768px) {
  .project-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .project-logo {
    margin-bottom: 1rem;
  }
  
  .demo-videos {
    grid-template-columns: 1fr;
  }
}
</style>
