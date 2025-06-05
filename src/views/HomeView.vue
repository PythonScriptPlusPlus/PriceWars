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
        class="leftbar__button"
        @click="endPeriod"
      >
        завершить период
      </button>
      <div class="leftbar__textbox">
        <p class="leftbar__text">
          {{ longText }}
        </p>
      </div>
    </div>
    <div class="rightbar">
      <div class="rightbar__tab-wrapper">
        <p
          class="rightbar__tab"
          :class="tab.pressed ? 'rightbar__tab--chosen' : ''"
          v-for="tab in tabs"
          :key="tab.name"
          @click="changeTab(tab)"
          role="button"
          tabindex="0"
          @keyup.enter="changeTab(tab)"
        >
          {{ tab.name }}
        </p>
      </div>
      <div class="rightbar__options">
        <p
          class="rightbar__data"
          v-for="tab in tabs.filter(t => t.pressed)"
          :key="tab.name"
        >
          {{ tab.description }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
// import { ref } from 'vue';

export default {
  name: 'HomeView',
  data() {
    return {
      longText: `Minim excepteur id enim ut cupidatat est. Ut adipisicing non cupidatat quis velit amet velit cupidatat exercitation.
Qui ad consequat nisi dolore enim. Sint anim voluptate labore incididunt sit do ex pariatur.
Sunt elit labore et irure veniam magna minim eiusmod non. Consequat officia cupidatat sunt irure dolore ipsum fugiat aliqua anim cupidatat tempor ea incididunt mollit.
Magna nisi esse deserunt anim esse duis sunt cupidatat mollit veniam velit irure. In anim pariatur dolor ipsum labore ut eiusmod adipisicing.
Commodo ad id mollit irure nisi fugiat.

Amet aliqua consectetur fugiat anim ad dolore labore esse aliqua qui mollit dolore. Esse velit duis laborum consequat in non dolore elit nostrud ipsum irure cupidatat ipsum. Minim Lorem quis ullamco incididunt anim do elit nostrud.

Sint nisi id voluptate irure nisi enim exercitation labore nostrud enim cillum. Nostrud commodo eiusmod esse adipisicing do dolor Lorem id mollit commodo excepteur amet duis. Cillum non magna quis reprehenderit sit id fugiat adipisicing labore laborum voluptate. Est aliqua pariatur incididunt esse mollit esse ipsum minim dolore nostrud sint laboris elit ea. Fugiat ipsum ex officia fugiat Lorem nulla laboris duis minim culpa.

Tempor voluptate qui voluptate ipsum do commodo fugiat fugiat sint elit ad excepteur in. Aliquip labore ut eu ea non sit ut est. Eiusmod pariatur reprehenderit minim eu occaecat anim elit minim exercitation aliqua Lorem sit. Voluptate cupidatat laboris ea labore culpa nisi amet sit. Magna proident mollit veniam et nisi officia laborum. Magna aliqua nostrud eu sit id irure. Fugiat tempor veniam Lorem sit ipsum in.

Nim sunt duis aute magna voluptate. Amet cupidatat mollit minim eu labore ut est adipisicing in et tempor dolore. Ea ut nostrud incididunt sint consequat id proident ex anim et occaecat.`,
      healthSpent: 0,
      period: 1,
      money: 1000000,
      demand: '100 - Q',
      costs: 50,
      tabs: [
        {
          name: 'Производство',
          description: 'Ea est esse non mollit culpa adipisicing do.',
          pressed: 1,
        },
        {
          name: 'Лобирование',
          description: 'Minim anim culpa anim esse qui reprehenderit consequat excepteur est duis ex aliquip eu veniam.',
          pressed: 0,
        },
        {
          name: 'Lorem Ipsum',
          description: 'Lorem culpa commodo sit tempor officia eu eu ex.',
          pressed: 0,
        },
        {
          name: 'Настройки',
          description: 'Incididunt deserunt pariatur consequat culpa veniam amet anim veniam minim mollit tempor sit.',
          pressed: 0,
        },
      ],
    };
  },
  methods: {
    endPeriod() {
      this.healthSpent += 10;
      this.period += 1;
    },
    changeTab(selectedTab) {
      this.tabs = this.tabs.map((tab) => ({
        ...tab,
        pressed: tab.name === selectedTab.name ? 1 : 0,
      }));
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
  grid-gap: 10px;
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
    z-index: 11;
    position: absolute;
    width: 100%;
    margin: 0;
    top: 50%;
    left: 15px;
    transform: translate(0, -50%);
  }
}

.info {
  height: 50px;
  background-color: #ccc;
  z-index: 10;
  grid-row: 1;
  grid-column: 2;
  padding: 5px;
  display: flex;
  overflow-x: auto;
  white-space: nowrap;

  &::-webkit-scrollbar {
    height: 5px;
  }

  &::-webkit-scrollbar-track {
    background: #ccc;
  }

  &::-webkit-scrollbar-thumb {
    background-color: #888;
    border-radius: 10px;
    border: 3px solid #f0f0f0; /* adds space around thumb */
}

  &__item {
    height: fit-content;
    margin: 0;
    margin-top: 18.125px;
    transform: translate(0,-50%);
    margin-right: 10px;
    border-right: 2px solid #aaa;
    padding-right: 10px;

    &:last-child {
      margin-right: 0;
      border-right: none;
    }
  }
}

.leftbar {
  padding: 5px;
  grid-row: 2;
  grid-column: 1;
  // border: 3px solid #0000ff;
  background-color: white;

  &__button {
    font-size: 2em;
    margin-left: 50%;
    transform: translate(-50%,0);
    width: 70%;
    height: 3em;
  }

  &__textbox {
    background-color: #999;
    margin: 0 25px;
  }
}

.rightbar {
  padding: 5px;
  grid-row: 2;
  grid-column: 2;
  background-color: white;
  // border: 3px solid #ffff00;

  &__tab-wrapper {
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
    background-color: #999;
    width: fit-content;
    // padding: 0 10px;
  }

  &__tab {
    padding: 0 10px;
    margin: 0;
    // margin-right: 10px;

    &--chosen {
      background-color: gold;
    }

    &:last-child {
      margin-right: 0;
    }
  }
}
</style>
