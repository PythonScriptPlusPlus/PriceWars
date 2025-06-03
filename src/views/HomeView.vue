<template>
  <div class="app">
    <div class="healthbar"></div>
    <div class="info"></div>
    <div class="leftbar"></div>
    <div class="rightbar"></div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue';

// export default {
//   name: 'HomeView',
//   components: {
//     HelloWorld,
//   },
// };
</script>

<style scoped lang="scss">
.app {
  height: 100vh;
  width: 100vw;
  display: grid;
  grid-template-columns: 2fr 3fr;
  grid-template-rows: 50px 1fr;
}

.healthbar,
.info,
.leftbar,
.rightbar {
  box-sizing: border-box; // ensures border is inside the element
  height: 100%;
  width: 100%;
}

.healthbar {
  grid-row: 1;
  grid-column: 1;
  border: 3px solid #ff0000;
}

.info {
  grid-row: 1;
  grid-column: 2;
  border: 3px solid #00ff00;
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
