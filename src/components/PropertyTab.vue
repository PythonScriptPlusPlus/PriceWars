<template>
  <div class="property">
    <div class="property__info">
      <p class="property__item">куплено участков: {{ playersPlots.length }}</p>
      <p class="property__item">стоимость нового участка: {{ PropertyPrice }}</p>
      <p class="property__item">налог при покупке: {{ purchaseTax }}</p>
      <p class="property__item">налоги на имущество в следующем периоде: {{ propertyTax }}</p>
    </div>
    <button
      class="property__button"
      @click="buyProperty"
    >
      Купить землю
    </button>
  </div>
</template>

<script>
export default {
  name: 'PropertyTab',
  props: {
    PropertyPrice: {
      type: [String, Number, Object], // Use the correct type
      required: false,
    },
  },
  data() {
    return {
      playersPlots: [],
    };
  },
  mounted() {
    fetch('http://127.0.0.1:5000/data')
      .then((response) => response.json())
      .then((data) => {
        this.playersPlots = data.playersPlots;
      })
      .catch((error) => console.error('Error fetching message:', error));
  },
  computed: {
    purchaseTax() {
      return (this.PropertyPrice * 0.005).toFixed(2);
    },
    propertyTax() {
      return (
        (this.playersPlots.reduce(
          (accumulator, currentValue) => accumulator + currentValue,
          0,
        ) * 0.005).toFixed(2)
      );
    },
  },
  methods: {
    async buyProperty() {
      try {
        const response = await fetch('http://127.0.0.1:5000/buy_property', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            plots: this.playersPlots,
          }),
        });
        const data = await response.json();
        this.playersPlots = data.playersPlots;
        if (data.money !== undefined) {
          this.$emit('update:money', data.money);
        }
        if (data.property_price !== undefined) {
          this.$emit('update:property-price', data.property_price);
        }
        if (data.costs !== undefined) {
          this.$emit('update:costs', data.costs); // <-- Emit new cost
        }
      } catch (error) {
        console.error('Error buying property:', error);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.property {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  width: calc(60vw - 40px);
  margin: 0 25px;

  &__info {
    margin-top: 25px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: repeat(3, auto);
    grid-gap: 5px;
  }

  &__item {
    background-color: #ddd;
    margin: 0;
    border: 2px solid #ccc;
    padding: 5px;
    height: fit-content;

    &:first-child,
    &:last-child {
      grid-column: 1 / span 2;
    }
  }

  &__button {
    display: flex;
    align-items: center;
    margin-top: 25px;
    border: 2px solid #ccc;
    padding: 5px;
    width: calc(60vw - 50px - 10px);
    height: fit-content;
    cursor: pointer;
  }
}
</style>
