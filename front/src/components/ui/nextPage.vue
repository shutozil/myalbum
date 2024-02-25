<template>
  <div class="next-page" :class="{ hide: !scrollEnd }">
    <nuxt-link
      id="next"
      :to="path"
      :class="buttonColor"
      class="text-white font-bold text-base py-5 px-5 rounded-full shadow-md hover:shadow-lg"
    >
      {{ text }}
    </nuxt-link>
  </div>
</template>
<script>
export default {
  props: ['text','path','buttonColor','scrollEnd']
}
</script>