<template>
  <div class="production">
    <div class="production__item">
      <label for="productionAmount">
        <input
          type="text"
          id="productionAmount"
          v-model="productionAmount"
          @input="emitProductionAmount"
        />
        Сколько произвести в этот период?
      </label>
    </div>
    <div class="production__item price">
      <label for="price">
        <input
          type="text"
          id="price"
          v-model="priceIncrease"
        />
          На сколько увеличить цену производства?
      </label>
      <button class="price__button" @click="emitPriceIncrease">увеличить</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductionTab',
  data() {
    return {
      productionAmount: 0,
      priceIncrease: 0,
    };
  },
  methods: {
    emitProductionAmount() {
      this.$emit('update-production', this.productionAmount);
    },
    emitPriceIncrease() {
      this.$emit('price-increase', Number(this.priceIncrease));
    },
  },
};
</script>

<style lang="scss" scoped>
.production {
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: space-evenly;
  width: 100%;
  padding: 0 25px;

  &__item {
    display: flex;
    margin-top: 25px;
    border: 2px solid #ccc;
    padding: 5px;
    width: calc(60vw - 50px - 10px);
  }
}

.price {
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: space-evenly;

  &__button {
    width: 100%;
    height: 25px;
    margin-top: 5px;
    // background-color: #4CAF50; /* Green */
    // color: white;
    // border: none;
    cursor: pointer;
  }
}
</style>
