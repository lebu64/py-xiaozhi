<template>
  <div class="module-container">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
      <div v-for="(module, index) in modules" :key="index" class="module-card">
        <div class="flex items-start">
          <div class="w-12 h-12 rounded-lg flex items-center justify-center"
            :class="moduleColors[index % moduleColors.length]">
            <component :is="module.icon" class="w-6 h-6 text-white" />
          </div>
          <div class="ml-4 flex-1">
            <h3 class="module-title">{{ module.name }}</h3>
            <ul class="space-y-2">
              <li v-for="(feature, featureIndex) in module.features" :key="featureIndex" class="flex items-start">
                <CheckCircleIcon class="w-5 h-5 text-green-500 mt-1 mr-2" />
                <span class="feature-text">{{ feature }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  CogIcon, 
  ArrowsRightLeftIcon,
  DocumentIcon,
  SpeakerXMarkIcon,
  ComputerDesktopIcon,
  ServerIcon,
  LightBulbIcon,
  WrenchIcon,
  CheckCircleIcon,
  CpuChipIcon,
  MapIcon
} from '@heroicons/vue/24/solid';
import { useData } from 'vitepress';

const { isDark } = useData();

// Module Details
const modules = [
  {
    name: 'src/application.py',
    icon: CogIcon,
    features: [
      'Application main class, singleton pattern manages global state',
      'Asynchronous task management and state machine control',
      'Device states (IDLE/CONNECTING/LISTENING/SPEAKING)',
      'Thread-safe command queue processing'
    ]
  },
  {
    name: 'src/mcp/',
    icon: WrenchIcon,
    features: [
      'JSON-RPC 2.0 based MCP server',
      'Rich tool ecosystem (system, calendar, maps, etc.)',
      'Extensible plugin architecture',
      'Type-safe parameter validation'
    ]
  },
  {
    name: 'src/protocols/',
    icon: ArrowsRightLeftIcon,
    features: [
      'Abstract protocol interface design',
      'WebSocket and MQTT protocol implementations',
      'TLS encryption and automatic reconnection mechanism',
      'Unified communication abstraction layer'
    ]
  },
  {
    name: 'src/audio_codecs/',
    icon: DocumentIcon,
    features: [
      'Real-time audio codec based on Opus',
      'WebRTC audio echo cancellation (AEC) processor',
      'SoXR high-quality audio resampling',
      'System audio recording and loopback processing',
      'Asynchronous audio stream processing',
      'Low-latency audio buffer management'
    ]
  },
  {
    name: 'src/audio_processing/',
    icon: SpeakerXMarkIcon,
    features: [
      'AEC acoustic echo cancellation processor',
      'Sherpa-ONNX based voice activity detection (VAD)',
      'Multi-language wake word detection',
      'Real-time audio processing and callback mechanism'
    ]
  },
  {
    name: 'src/display/',
    icon: ComputerDesktopIcon,
    features: [
      'Strategy pattern UI system architecture',
      'PyQt5 GUI and CLI interface implementations',
      'Asynchronous interface updates',
      'Status display and user interaction'
    ]
  },
  {
    name: 'src/iot/',
    icon: LightBulbIcon,
    features: [
      'Thing abstraction based IoT device framework',
      'Unified device management and state synchronization',
      'Dynamic device discovery',
      'Smart home device control'
    ]
  },
  {
    name: 'src/utils/',
    icon: MapIcon,
    features: [
      'Configuration management and device fingerprinting',
      'Logging system and resource finding',
      'Volume control and common utilities',
      'Cross-platform compatibility handling'
    ]
  }
];

const moduleColors = [
  'bg-blue-600',
  'bg-indigo-600',
  'bg-purple-600',
  'bg-pink-600',
  'bg-red-600',
  'bg-orange-600',
  'bg-yellow-600',
  'bg-green-600'
];
</script>

<style scoped>
.module-container {
  background-color: var(--vp-c-bg);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 40px;
}

.module-card {
  transition: all 0.3s ease;
  padding: 1.5rem;
}

.module-card:hover {
  background-color: var(--vp-c-bg-soft);
}

.module-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 0.5rem;
}

.feature-text {
  color: var(--vp-c-text-2);
}
</style>
