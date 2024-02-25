<template>
  <div>
    <div v-for="(image, index) in images" :key="index">
      <bg-image
        :image="image"
        :textColor="`bg-gradient-to-r from-purple-500 to-pink-500`"
      ></bg-image>

      <template v-if="index === images.length - 1">
        <next-page
          :buttonColor="`bg-gradient-to-r from-pink-500 to-orange-400`"
          :path="`/sample/4`"
          :text="`次へ`"
          :scrollEnd="scrollEnd"
        ></next-page>
      </template>
    </div>

    <div v-if="images !== null" id="end-pos" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: null,
      scrollEnd: false
    }
  },
  mounted() {
    this.getImage()
    this.handleScroll()
  },
  methods: {
    async getImage() {
      const images=await fetchImages('sample3')
      this.images=images
    },

    handleScroll() {
      window.addEventListener('scroll',this.handleScroll)
      const endElem=document.getElementById('end-pos') // 要素のIDを指定

      if(isElementAtBottom(endElem)) {
        this.scrollEnd=true
      }
    }
  },
}
</script>
