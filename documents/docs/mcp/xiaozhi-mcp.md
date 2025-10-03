# Xiaozhi MCP External Integration Guide

This document describes how to integrate external MCP services into the Xiaozhi system to achieve functional extension and third-party tool integration.

## Overview

In addition to built-in MCP tools, the Xiaozhi system also supports integrating external MCP servers to achieve:
- Third-party tool integration
- Remote service invocation
- Distributed tool deployment
- Community tool sharing

## Architecture Description

### External MCP Architecture
```
Xiaozhi AI Platform  xiaozhi-mcphub      External MCP Server  Third-party Tools
┌─────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────┐
│             │   │                 │   │                 │   │             │
│ MCP Client  │◄──┤ MCP Server/Proxy│◄──┤ MCP Server      │◄──┤ Actual Tools│
│             │   │                 │   │                 │   │             │
└─────────────┘   └─────────────────┘   └─────────────────┘   └─────────────┘
```

### Connection Methods
1. **Standard Input Output (stdio)**: Start child processes, communicate through stdin/stdout pipes for inter-process communication, suitable for local CLI tools like Playwright, Amap, etc.
2. **Server-Sent Events (SSE)**: Event stream communication based on HTTP long connections, providing real-time bidirectional communication capabilities similar to WebSocket
3. **Streamable HTTP (streamable-http)**: HTTP protocol encapsulation based on TCP, supporting streaming data transmission, suitable for remote API services and microservices
4. **OpenAPI**: Connection method based on standard REST API specifications, automatically parsing OpenAPI specifications and generating tool interfaces, suitable for standardized third-party API services

## Related Open Source Projects
Community-developed Xiaozhi client projects providing different platform integration methods

### xiaozhi-mcphub (Project Companion)

**Xiaozhi MCP Hub** is an intelligent MCP tool bridging system specifically optimized for the Xiaozhi AI platform, developed based on the excellent MCPHub project, with added Xiaozhi platform integration and intelligent tool synchronization features.

- **Project Address**: [xiaozhi-mcphub](https://huangjunsen0406.github.io/xiaozhi-mcphub/)
- **GitHub**: [xiaozhi-mcphub](https://github.com/huangjunsen0406/xiaozhi-mcphub)
- **Core Functions**: 
  - **Xiaozhi AI Platform Integration**: WebSocket automatic tool synchronization, real-time status updates, protocol bridging
  - **Enhanced MCP Management**: Supports stdio, SSE, HTTP protocols, hot-pluggable configuration, centralized console
  - **Intelligent Tool Routing**: Vector-based intelligent tool search and group management
  - **Security Authentication Mechanism**: JWT+bcrypt user management, role permission control
  - **Built-in MCP Store**: Multiple MCP tools online installation without restart, supports hot updates
  
### xiaozhi-client
- **Project Address**: [xiaozhi-client](https://github.com/shenjingnan/xiaozhi-client)
- **Function**: Xiaozhi AI client, specifically designed for MCP integration and aggregation
- **Core Features**: 
  - **Multiple Access Point Support**: Configurable multiple Xiaozhi access points, enabling multiple devices to share one MCP configuration
  - **MCP Server Aggregation**: Aggregates multiple MCP Servers through standard methods, unified management
  - **Dynamic Tool Control**: Controls MCP Server tool visibility, avoiding exceptions caused by too many tools
  - **Multiple Integration Methods**: Supports integration as a regular MCP Server into clients like Cursor/Cherry Studio
  - **Web Visual Configuration**: Modern Web UI interface, supports remote configuration and management
  - **ModelScope Integration**: Supports remote MCP services hosted by ModelScope

### HyperChat
- **Project Address**: [HyperChat](https://github.com/BigSweetPotatoStudio/HyperChat)
- **Function**: Next-generation AI workspace, pioneering multi-platform intelligent collaboration platform with "AI as Code" concept
- **Core Features**: 
  - **AI as Code**: Configuration-driven AI capability management, supports version control and team collaboration
  - **Workspace-Driven**: Project-centric AI environment isolation and management
  - **Deep MCP Ecosystem Integration**: Complete MCP protocol support, rich built-in tools and dynamic loading
  - **Multi-Platform Unification**: Web applications, Electron desktop, CLI command line, VSCode plugins
- **Technical Highlights**:
  - Configurable AI agent system, supports specialized Agent customization
  - Multi-model parallel comparison testing (Claude, OpenAI, Gemini, etc.)
  - Intelligent content rendering (Artifacts, Mermaid, mathematical formulas)
  - Scheduled tasks and workflow automation
