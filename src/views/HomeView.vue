<template>
  <div class="app">
    <div class="health">
      <div class="health__bar">
        <div
          class="health__bar--red"
          :style="{ width: `calc(100% - ${healthSpent}% )`,
            '--before-width': `${healthSpent*100/(100-healthSpent)}%` }"
        >
        </div>
        <p class="health__text">терпение инвесторов</p>
      </div>
    </div>
    <div class="info">
      <p class="info__item">Период: {{ period }}</p>
      <p class="info__item">Деньги: {{ money }}</p>
      <p class="info__item">Функция спроса: p = {{ demand }}</p>
      <p class="info__item">Затраты на производство: {{ costs }}</p>
    </div>
    <div class="leftbar">
      <button
        class="end"
        @click="endPeriod"
      >
        завершить период
      </button>
    </div>
    <div class="rightbar"></div>
  </div>
</template>

<script>
// import { ref } from 'vue';

export default {
  name: 'HomeView',
  data() {
    return {
      healthSpent: 0,
      period: 1,
      money: 1000000,
      demand: '100 - Q',
      costs: 50,
    };
  },
  methods: {
    endPeriod() {
      this.healthSpent += 10;
    },
  },
};
</script>

<style scoped lang="scss">
.app {
  height: 100vh;
  width: 100vw;
  display: grid;
  grid-template-columns: 2fr 3fr;
  grid-template-rows: 50px 1fr;
}

.health,
.info,
.leftbar,
.rightbar {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
}

.health {
  grid-row: 1;
  grid-column: 1;

  &__bar {
    position: relative;
    height: 40px;
    width: calc(100% - 10px);
    background-color: #ccc;
    padding: 5px;

    &--red {
      position: relative;
      transition: width 0.5s;
      height: 40px;
      background-color: red;

      &::before {
        z-index: 9;
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: var(--before-width, 100%);
        height: 100%;
        background-color: #999;
        transform: translate(100%, 0);
        transition: width 0.5s;
      }
    }
  }

  &__text {
    position: absolute;
    width: 100%;
    margin: 0;
    top: 50%;
    left: 15px;
    transform: translate(0, -50%);
  }
}

.info {
  background-color: #ccc;
  z-index: 10;
  grid-row: 1;
  grid-column: 2;
  display: flex;
  overflow-x: auto;
  white-space: nowrap;

  &__item {
    margin: 0;
    margin-right: 10px;

    &:last-child {
      margin-right: 0;
    }
  }
}

.leftbar {
  grid-row: 2;
  grid-column: 1;
  border: 3px solid #0000ff;
}

.rightbar {
  grid-row: 2;
  grid-column: 2;
  border: 3px solid #ffff00;
}
</style>
