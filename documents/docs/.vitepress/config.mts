import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vitepress'
// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "PY-XIAOZHI",
  description: "py-xiaozhi is a Python-implemented Xiaozhi voice client, designed to learn coding and experience AI Xiaozhi's voice features without hardware requirements.",
  base: '/py-xiaozhi/',
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      {
        text: 'Guide',
        items: [
          { text: 'Documentation Directory (Important)', link: '/guide/documentation-directory' },
          { text: 'System Dependencies Installation', link: '/guide/system-dependencies-installation' },
          { text: 'Configuration Guide', link: '/guide/configuration-guide' },
          { text: 'Voice Interaction Mode Guide', link: '/guide/voice-interaction-mode-explanation' },
          { text: 'Shortcuts Guide', link: '/guide/shortcut-explanation.md'},
          { text: 'Echo Cancellation', link: '/guide/echo-cancellation' },
          { text: 'Voice Wake-up', link: '/guide/voice-wake-up' },
          { text: 'Device Activation Process', link: '/guide/device-activation-process' },
          { text: 'Packaging Tutorial', link: '/guide/packaging-tutorial' },
          { text: 'Exception Summary', link: '/guide/error-summary' },
        ]
      },
      { text: 'System Architecture', link: '/architecture/' },
      { text: 'Related Ecosystem', link: '/ecosystem/' },
      {
        text: 'IoT',
        items: [
          { text: 'Development Guide', link: '/iot/' },
        ]
      },
      {
        text: 'MCP',
        items: [
          { text: 'Development Guide', link: '/mcp/' },
          { text: 'Amap (Amap)', link: '/mcp/amap' },
          { text: 'Bazi (Bazi)', link: '/mcp/bazi' },
          { text: 'Calendar (Calendar)', link: '/mcp/calendar' },
          { text: 'Camera (Camera)', link: '/mcp/camera' },
          { text: 'Home Assistant (HA)', link: '/mcp/ha' },
          { text: 'Music (Music)', link: '/mcp/music' },
          { text: 'Railway (Railway)', link: '/mcp/railway' },
          { text: 'Recipe (Recipe)', link: '/mcp/recipe' },
          { text: 'Search (Search)', link: '/mcp/search' },
          { text: 'System (System)', link: '/mcp/system' },
          { text: 'Timer (Timer)', link: '/mcp/timer' }
        ]
      },
      { text: 'Team', link: '/about/team' },
      { text: 'Contribution Guide', link: '/contributing' },
      { text: 'Sponsors', link: '/sponsors/' }
    ],

    sidebar: {
      '/ecosystem/': [
        {
          text: 'Ecosystem Overview',
          link: '/ecosystem/'
        },
        {
          text: 'Related Projects',
          collapsed: false,
          items: [
            { text: 'Xiaozhi Mobile Client', link: '/ecosystem/projects/xiaozhi-android-client/' },
            { text: 'xiaozhi-esp32-server', link: '/ecosystem/projects/xiaozhi-esp32-server/' },
            { text: 'XiaoZhiAI_server32_Unity', link: '/ecosystem/projects/xiaozhi-unity/' },
            { text: 'IntelliConnect', link: '/ecosystem/projects/intelliconnect/' },
            { text: 'open-xiaoai', link: '/ecosystem/projects/open-xiaoai/' }
          ]
        },
      ],
      '/about/': [],
      // MCP pages do not show sidebar
      '/mcp/': [],
      // IoT pages do not show sidebar
      '/iot/': [],
      // Sponsors pages do not show sidebar
      '/sponsors/': [],
      // Contribution guide pages do not show sidebar
      '/contributing': [],
      // System architecture pages do not show sidebar
      '/architecture/': [],
      // Team pages do not show sidebar
      '/about/team': []
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/huangjunsen0406/py-xiaozhi' }
    ]
  },
  vite: {
    plugins: [
        tailwindcss()
    ]
  }
})
