<template>
  <div>
    <div v-for="(image, index) in images" :key="index">
      <bg-image
        :image="image"
        :textColor="`bg-gradient-to-r from-cyan-500 to-blue-500`"
      ></bg-image>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: null,
    }
  },
  mounted() {
    this.getImage()
  },
  methods: {
    async getImage() {
      const images=await fetchImages('sample5')
      this.images=images
    },
  },
}
</script>
