---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "PY-XIAOZHI"
  tagline: py-xiaozhi is a Python-implemented Xiaozhi voice client, designed to learn through code and experience AI Xiaozhi's voice features without hardware requirements.
  actions:
    - theme: brand
      text: Get Started
      link: /guide/文档目录
    - theme: alt
      text: View Source Code
      link: https://github.com/huangjunsen0406/py-xiaozhi

features:
  - title: AI Voice Interaction
    details: Supports voice input and recognition, enabling intelligent human-computer interaction with natural and smooth conversation experience. Uses asynchronous architecture design, supporting real-time audio processing and low-latency response.
  - title: Visual Multimodal
    details: Supports image recognition and processing, providing multimodal interaction capabilities to understand image content. Integrates OpenCV camera processing, supporting real-time visual analysis.
  - title: MCP Tool Server
    details: Modular tool system based on JSON-RPC 2.0 protocol, supporting rich features including schedule management, music playback, 12306 query, map services, recipe search, Bazi fortune telling, and more, with dynamic tool plugin extension.
  - title: IoT Device Integration
    details: Uses Thing abstraction pattern design, supporting smart home device control including lights, volume, temperature sensors, etc. Integrates with Home Assistant smart home platform, easily extensible.
  - title: High-Performance Audio Processing
    details: Real-time audio transmission based on Opus codec, supporting intelligent resampling technology, 5ms audio frame interval processing, ensuring low-latency high-quality audio experience.
  - title: Cross-Platform Support
    details: Compatible with Windows 10+, macOS 10.15+, and Linux systems, supports both GUI and CLI dual-mode operation, adapts to different platform audio devices and system interfaces.
---

<style>
.developers-section {
  text-align: center;
  max-width: 960px;
  margin: 4rem auto 0;
  padding: 2rem;
  border-top: 1px solid var(--vp-c-divider);
}

.developers-section h2 {
  margin-bottom: 0.5rem;
  color: var(--vp-c-brand);
}

.contributors-wrapper {
  margin: 2rem auto;
  max-width: 800px;
  position: relative;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.contributors-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.contributors-link {
  display: block;
  text-decoration: none;
  background-color: var(--vp-c-bg-soft);
}

.contributors-image {
  width: 100%;
  height: auto;
  display: block;
  transition: all 0.3s ease;
}

.developers-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.developers-actions a {
  text-decoration: none;
}

.dev-button {
  display: inline-block;
  border-radius: 20px;
  padding: 0.5rem 1.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
}

.dev-button:not(.outline) {
  background-color: var(--vp-c-brand);
  color: white;
}

.dev-button.outline {
  border: 1px solid var(--vp-c-brand);
  color: var(--vp-c-brand);
}

.dev-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 640px) {
  .developers-actions {
    flex-direction: column;
  }
  
  .contributors-wrapper {
    margin: 1.5rem auto;
  }
}

.join-message {
  text-align: center;
  margin-top: 2rem;
  padding: 2rem;
  border-top: 1px solid var(--vp-c-divider);
}

.join-message h3 {
  margin-bottom: 1rem;
}
</style>
