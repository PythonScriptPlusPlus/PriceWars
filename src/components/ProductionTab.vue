<template>
  <div>
    <div class="amount">
      <label class="amount__label" for="productionAmount">
        <input
          type="text"
          id="productionAmount"
          class="amount__input"
          v-model="productionAmount"
          @input="emitProductionAmount"
        />
        Сколько произвести в этот период
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductionTab',
  data() {
    return {
      productionAmount: '',
    };
  },
  methods: {
    emitProductionAmount() {
      this.$emit('update-production', this.productionAmount);
    },
  },
};
</script>

<style lang="scss" scoped>
.amount {
  display: flex;
  margin-left: 50%;
  margin-top: 25%;
  transform: translate(-50%,-50%);
}
</style>
