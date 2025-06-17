<template>
  <div>
    <label for="learningMode">
      <input
        type="checkbox"
        name="learningMode"
        id="learningMode"
        :checked="learningMode"
        @change="updateLearningMode($event.target.checked)"
      >
      Режим обучения
    </label>
    <br>
    <button @click="resetGame">
      начать игру сначала
    </button>
  </div>
</template>

<script>
export default {
  name: 'SettingsTab',
  props: {
    learningMode: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    async resetGame() {
      try {
        const response = await fetch('/reset', {
          method: 'POST',
        });
        const data = await response.json();
        this.$emit('game-reset', data); // emit event with new values
        console.log('Игра сброшена', data);
      } catch (error) {
        console.error('Ошибка при сбросе игры:', error);
      }
    },
    updateLearningMode(val) {
      this.$emit('update:learning-mode', val);
    },
  },
};
</script>

<style>
</style>
