---
title: Py-Xiaozhi Project Architecture
description: Python-implemented Xiaozhi voice client, using modular design, supporting multiple communication protocols and device integration
sidebar: false,
pageClass: architecture-page-class
---
<script setup>
import CoreArchitecture from './components/CoreArchitecture.vue'
import ModuleDetails from './components/ModuleDetails.vue'
import TechnologyStack from './components/TechnologyStack.vue'
import ArchitectureFeatures from './components/ArchitectureFeatures.vue'
</script>

<div class="architecture-page">

# Py-Xiaozhi Project Architecture

<p class="page-description">Python-implemented Xiaozhi voice client, using modular design, supporting multiple communication protocols and device integration</p>

## Core Architecture
<CoreArchitecture/>

## Module Details
<ModuleDetails/>

## Technology Stack
<TechnologyStack/>

## Architecture Features
<ArchitectureFeatures/>
</div>

<style>
.page-description {
  font-size: 1.125rem;
  color: var(--vp-c-text-2);
  margin-bottom: 2rem;
  line-height: 1.6;
}
</style>

<style>
.architecture-page {
  max-width: 100%;
  padding: 0 2rem;
}
</style>
