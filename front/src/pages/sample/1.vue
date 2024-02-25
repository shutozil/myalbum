<template>
  <div>
    <div v-for="(image, index) in images" :key="index">
      <bg-image
        :image="image"
        :textColor="`bg-gradient-to-r from-cyan-500 to-blue-500`"
      ></bg-image>

      <div v-if="index === 0">
        <div class="scroll-hint" :class="{ hide: launchScroll }">
          <p class="bounce text-white text-xl">スクロールしてください</p>
        </div>
      </div>

      <template v-if="index === images.length - 1">
        <next-page
          :buttonColor="`bg-gradient-to-r from-purple-500 to-pink-500`"
          :path="`/sample/2`"
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
      launchScroll: false,
      scrollEnd: false
    }
  },
  mounted() {
    this.getImage()
    this.handleScroll()
  },
  methods: {
    async getImage() {
      const images=await fetchImages('sample1')
      this.images=images
    },

    handleScroll() {

      window.addEventListener('scroll',this.handleScroll)

      // スクロール位置が一定値を超えたかどうかを確認し、フラグを更新する
      const scrollPosition=window.scrollY
      if(scrollPosition>0&&!this.launchScroll) {
        this.launchScroll=true
      } else if(scrollPosition===0&&this.launchScroll) {
        this.launchScroll=false
      }

      const endElem=document.getElementById('end-pos') // 要素のIDを指定
      if(isElementAtBottom(endElem)) {
        this.scrollEnd=true
      }
    },

  },
}
</script>
