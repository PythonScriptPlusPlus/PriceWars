<template>
  <div class="lobbying">
    <div
      class="lobbying__item"
      v-for="(policy, index) in policies"
      :key="index"
    >
      <button class="lobbying__button">инвестировать</button>
      <p class="lobbying__text">{{ policy.name }} ({{ policy.price }})</p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'LobbyingTab',
  data() {
    return {
      policies: [
        { name: 'Создать лицензии для деятельности в этой сфере', price: 100, invested: false },
        { name: 'Усложнить порядок регистрации предприятий и фирм', price: 200, invested: false },
        { name: 'Усложнить процедуру отвода земельных участков и предоставление служебных помещений', price: 300, invested: false },
      ],
    };
  },
  methods: {},
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
    display: flex;
    margin-top: 25px;
    border: 2px solid #ccc;
    padding: 5px;
    width: calc(60vw - 50px - 10px);
  }

  &__text {
    margin: 0;
    margin-left: 5px;
  }
}
</style>
