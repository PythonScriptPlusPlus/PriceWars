<template>
  <div class="app">
    <div
      class="health"
      @mouseenter="showHealthPoints = true"
      @mouseleave="showHealthPoints = false"
      @focusin="showHealthPoints = true"
      @focusout="showHealthPoints = false"
      tabindex="0"
    >
      <div class="health__bar">
        <div
          class="health__bar--red"
          :style="{ width: `calc(${health}% )`,
            '--before-width': `${(100-health)/health*100}%` }"
        >
        </div>
        <p class="health__text">терпение инвесторов</p>
        <p
          class="health__points"
          v-show="showHealthPoints"
        >{{ health }}/100</p>
      </div>
    </div>
    <div class="info">
      <p class="info__item">Период: {{ period }}</p>
      <p class="info__item">Деньги: {{ money }}</p>
      <p class="info__item">Функция спроса: p = {{ demand }} - Q</p>
      <p class="info__item">Затраты на производство: {{ costs }}</p>
    </div>
    <div class="leftbar">
      <button
        class="leftbar__button"
        @click="endPeriod"
        @keyup.enter="endPeriod"
        :disabled="health <= 0"
      >
        завершить период
      </button>
      <div class="leftbar__textbox">
        <p
          class="leftbar__text"
          v-if="health > 0"
          v-html="longText.replace(/\n/g, '<br>')"
        ></p>
        <p
          class="leftbar__text--defeat"
          v-if="health <= 0"
        >
          Вы проиграли. Инвесторы потеряли терпение.
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
      <div class="rightbar__component">
        <component
          v-for="tab in tabs.filter(t => t.pressed)"
          :is="tab.component"
          :key="tab.name"
          @update-production="productionAmount = $event"
          @price-increase="handlePriceIncrease"
          @game-reset="handleGameReset"
          @update:money="money = $event"
          @update:property-price="propertyPrice = $event"
          @update:costs="costs = $event"
          :PropertyPrice="propertyPrice"
          :learningMode="learningMode"
          @update:learning-mode="learningMode = $event"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ProductionTab from '@/components/ProductionTab.vue';
import LobbyingTab from '@/components/LobbyingTab.vue';
import PropertyTab from '@/components/PropertyTab.vue';
import SettingsTab from '@/components/SettingsTab.vue';
import { showWelcomeAlert } from '@/utils/alerts';

export default {
  components: {
    ProductionTab, LobbyingTab, PropertyTab, SettingsTab,
  },
  name: 'HomeView',
  data() {
    return {
      learningMode: true,
      propertyPrice: 400,
      showHealthPoints: false,
      longText: '',
      health: 100,
      period: 1,
      money: 0,
      demand: '',
      costs: 0,
      tabs: [
        {
          name: 'Производство',
          component: 'production-tab',
          pressed: 1,
          index: 0,
          new: false,
        },
        {
          name: 'Лоббирование',
          component: 'lobbying-tab',
          pressed: 0,
          index: 1,
          new: true,
        },
        {
          name: 'Собственность',
          component: 'property-tab',
          pressed: 0,
          index: 2,
          new: true,
        },
        {
          name: 'Настройки',
          component: 'settings-tab',
          pressed: 0,
          index: 3,
          new: false,
        },
      ],
      test: '',
      productionAmount: '',
    };
  },
  methods: {
    async endPeriod() {
      this.period += 1;
      console.log('health', this.health);
      try {
        const response = await fetch('http://127.0.0.1:5000/production', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            productionAmount: this.productionAmount,
            longText: this.longText,
            health: this.health,
          }),
        });
        const data = await response.json();
        if (data.money !== undefined) {
          this.money = data.money;
        }
        if (data.costs !== undefined) {
          this.costs = data.costs;
        }
        if (data.long_text !== undefined) {
          this.longText = data.long_text;
        }
        if (data.health !== undefined) {
          this.health = data.health;
        }
        if (data.demand !== undefined) {
          this.demand = data.demand;
        }
        if (data.property_price !== undefined) {
          this.propertyPrice = data.property_price;
        }
        console.log('Server response:', data);
      } catch (error) {
        console.error('Error sending production amount:', error);
      }
      if ((this.period === 2 || this.period === 9) && this.learningMode) {
        showWelcomeAlert(this.setLearningMode);
      }
    },
    changeTab(selectedTab) {
      this.tabs = this.tabs.map((tab) => {
        // If tab.new is true and will be set to false, log it
        if (tab.name === selectedTab.name && tab.new === true && this.learningMode) {
          showWelcomeAlert(this.setLearningMode, 6 + selectedTab.index);
        }
        return {
          ...tab,
          pressed: tab.name === selectedTab.name ? 1 : 0,
          new: tab.name === selectedTab.name ? false : tab.new,
        };
      });
    },
    handleGameReset(data) {
      this.propertyPrice = data.property_price;
      this.health = data.health;
      this.period = data.period;
      this.money = data.money;
      this.demand = data.demand;
      this.costs = data.costs;
      this.longText = data.long_text;

      if (this.period === 1 && this.learningMode) {
        console.log(this.learningMode);
        showWelcomeAlert(this.setLearningMode, -1, true);
      }
      this.tabs = [
        {
          name: 'Производство',
          component: 'production-tab',
          pressed: 0,
          index: 0,
          new: false,
        },
        {
          name: 'Лоббирование',
          component: 'lobbying-tab',
          pressed: 0,
          index: 1,
          new: true,
        },
        {
          name: 'Собственность',
          component: 'property-tab',
          pressed: 0,
          index: 2,
          new: true,
        },
        {
          name: 'Настройки',
          component: 'settings-tab',
          pressed: 1,
          index: 3,
          new: false,
        },
      ];
    },
    handleGlobalEnter(e) {
      if (e.key === 'Enter' && this.health > 0) {
        this.endPeriod();
      }
    },
    async handlePriceIncrease(amount) {
      try {
        const response = await fetch('http://127.0.0.1:5000/increase_cost', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ amount }),
        });
        const data = await response.json();
        this.costs = data.costs;
      } catch (e) {
        console.error('Failed to increase cost:', e);
      }
    },
    setLearningMode(val) {
      this.learningMode = val;
    },
  },
  mounted() {
    fetch('http://127.0.0.1:5000/data')
      .then((response) => response.json())
      .then((data) => {
        this.test = data;
        this.costs = data.costs;
        this.money = data.money;
        this.demand = data.demand;
        this.health = data.health;
        this.period = data.period;
        this.propertyPrice = data.property_price;
        this.longText = data.long_text;

        // Now period is updated, so check here:
        if (this.period === 1 && this.learningMode) {
          console.log(this.learningMode);
          showWelcomeAlert(this.setLearningMode);
        }
      })
      .catch((error) => console.error('Error fetching message:', error));
    window.addEventListener('keydown', this.handleGlobalEnter);
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleGlobalEnter);
  },
};
</script>

<style lang="scss">
.alert {
  &__header {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    font-size: 1.5em;
    margin: 0;
    color: #333;
  }

  &__text {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    font-size: 1em;
    margin: 0;
    color: #666;
  }
}

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

  &__points {
    z-index: 11;
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translate(0, -50%);
    margin: 0;
    font-weight: bold;
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
  overflow-y: hidden;
  white-space: nowrap;

  &::-webkit-scrollbar {
    height: 5px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
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
    cursor: pointer;
  }

  &__textbox {
    background-color: #999;
    margin: 25px;
    height: calc(100vh - 70px - 100px - 50px);
    overflow: auto; // Add this line to enable scrolling
    padding: 10px;  // Optional: for better appearance

    &::-webkit-scrollbar {
      width: 5px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }

    &::-webkit-scrollbar-thumb {
      background-color: #f0f0f0;
    }
  }

  &__text {
    // color: white;
    margin: 0;
    word-break: break-word;

    &--defeat {
      color: red;
      font-weight: bold;
      font-size: 3em;
      margin: 0;
    }
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
    width: fit-content;
    padding-bottom: 5px;
    border-bottom: 2px solid #999;
    width: calc(60vw + 10px);
  }

  &__tab {
    background-color: #999;
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

  &__component {
    height: 100%;
    width: 100%;
    // background-color: skyblue;
  }
}
</style>
