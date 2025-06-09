<template>
  <div>
    <label for="learningMode">
      <input type="checkbox" name="learningMode" id="learningMode" v-model="learningMode">
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
  methods: {
    async resetGame() {
      try {
        const response = await fetch('http://127.0.0.1:5000/reset', {
          method: 'POST',
        });
        const data = await response.json();
        this.$emit('game-reset', data); // emit event with new values
        console.log('Игра сброшена', data);
      } catch (error) {
        console.error('Ошибка при сбросе игры:', error);
      }
    },
  },
};
</script>

<style>
</style>
