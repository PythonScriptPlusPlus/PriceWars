<template>
  <div class="lobbying">
    <div
      class="lobbying__item"
      v-for="(policy, index) in policies"
      :key="index"
    >
      <button
        class="lobbying__button"
        @click="invest(index)"
        :disabled="policy.invested"
      >
        инвестировать
      </button>
      <p class="lobbying__text">{{ policy.name }}
        <span class="lobbying__text--price">
          ({{ policy.price }})
        </span>
      </p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'LobbyingTab',
  data() {
    return {
      policies: [
        {
          name: 'Создать лицензии для деятельности в этой сфере',
          price: 1000,
          invested: false,
          one_time_payment: 1000,
        },
        {
          name: 'Усложнить порядок регистрации предприятий и фирм',
          price: 2000,
          invested: false,
          one_time_payment: 2000,
        },
        {
          name: 'Усложнить процедуру отвода земельных участков и предоставление служебных помещений',
          price: 3000,
          invested: false,
          one_time_payment: 3000,
        },
      ],
    };
  },
  methods: {
    async invest(index) {
      this.policies[index].invested = true;
      try {
        const response = await fetch('/invest', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            investedMoney: this.policies[index].price,
            action: this.policies[index].one_time_payment,
            isInvested: this.policies[index].invested,
          }),
        });
        const data = await response.json();
        if (data.isInvested !== undefined) {
          this.policies[index].invested = data.isInvested;
        }
        if (data.newMoney !== undefined) {
          this.$emit('update:money', data.newMoney);
        }
      } catch (error) {
        console.error('Error sending production amount:', error);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.lobbying {
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: space-evenly;
  width: 100%;
  padding: 0 25px;

  &__item {
    background-color: #ddd;
    display: flex;
    align-items: center;
    margin-top: 25px;
    border: 2px solid #ccc;
    padding: 5px;
    width: calc(60vw - 50px - 10px);
  }

  &__button {
    height: fit-content;
    cursor: pointer;
  }

  &__text {
    margin: 0;
    margin-left: 5px;

    &--price {
      color: #008005;
    }
  }
}
</style>
