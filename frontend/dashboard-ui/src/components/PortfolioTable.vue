<script setup lang="ts">
import type { Portfolio } from '../api/portfolio';
import { ref } from "vue";
defineProps<{
  portfolios: Portfolio[];
}>();

const emit = defineEmits<{
  select: [portfolio: Portfolio];
}>();
const selectedPortfolio = ref<Portfolio|null>(null);
function selectPortfolio(portfolio: Portfolio) {
  emit('select', portfolio);
  selectedPortfolio.value = portfolio
}
</script>

<template>
  <table class="portfolio-table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Description</th>
      </tr>
    </thead>

    <tbody>
      <tr
        v-for="portfolio in portfolios"
        :key="portfolio.id"
        @click="selectPortfolio(portfolio)"
        :class="(selectedPortfolio && portfolio.id == selectedPortfolio.id) ? 'selected' : '' "
      >
        <td>{{ portfolio.name }}</td>
        <td>{{ portfolio.description }}</td>
      </tr>
    </tbody>
  </table>
</template>