<script lang="ts">
import type { Member } from './Member'

const shuffleMembers = (
  members: Member[],
  pinTheFirstMember = false
): void => {
  let offset = pinTheFirstMember ? 1 : 0
  // `i` is between `1` and `length - offset`
  // `j` is between `0` and `length - offset - 1`
  // `offset + i - 1` is between `offset` and `length - 1`
  // `offset + j` is between `offset` and `length - 1`
  let i = members.length - offset
  while (i > 0) {
    const j = Math.floor(Math.random() * i)
    ;[members[offset + i - 1], members[offset + j]] = [
      members[offset + j],
      members[offset + i - 1]
    ]
    i--
  }
}
</script>

<script setup lang="ts">
// @ts-ignore
import { VTLink } from '@vue/theme'
// @ts-ignore
import membersCoreData from './members-core.json'
// @ts-ignore
import membersPartnerData from './members-partner.json'
import TeamHero from './TeamHero.vue'
// @ts-ignore
import TeamList from './TeamList.vue'

shuffleMembers(membersCoreData, true)
shuffleMembers(membersPartnerData)
</script>

<template>
  <div class="TeamPage">
    <TeamHero>
      <template #title>Team Members</template>
      <template #lead>
        The development and maintenance of the py-xiaozhi project is handled by community members.
        Below is some information about core team members and community contributors.
      </template>
    </TeamHero>

    <TeamList :members="membersCoreData">
      <template #title>Core Team Members</template>
      <template #lead>
        Core team members actively participate in project development and maintenance,
        making significant contributions to the py-xiaozhi project.
      </template>
    </TeamList>

    <TeamList :members="membersPartnerData">
      <template #title>Community Contributors</template>
      <template #lead>
        Thank you to the following community members for their help and support during the early stages of the project.
      </template>
    </TeamList>
  </div>
</template>

<style scoped>
.TeamPage {
  padding-bottom: 16px;
}

@media (min-width: 768px) {
  .TeamPage {
    padding-bottom: 96px;
  }
}

.TeamList + .TeamList {
  padding-top: 64px;
}

* {
  list-style: none;
}
</style>
