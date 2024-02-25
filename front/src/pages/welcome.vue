<script setup lang="ts">
type ImageType = {
    sign_url: string;
    comment: string;
};
type ImagesType = ImageType[];

const { $anime } = useNuxtApp()

const setImage = async (): Promise<string> => {
  const images: ImagesType = await fetchImages('welcome')
  if (images.length > 0) {
    const randomIndex: number = Math.floor(Math.random() * images.length)
    const signUrl: string = images[randomIndex].sign_url
    return signUrl
  }
  return ''
}

const backgroundImage: any = ref(await setImage())

useHead({
  bodyAttrs: {
    style: computed(() => {
      if (backgroundImage.value) {
        return "background-image: url('" + backgroundImage.value + "')" 
      }
    }),
    class: computed(() => {
      return 'h-screen items-center bg-cover'
    }),
  }
})

onMounted(() => {
  const basicTimeline = $anime.timeline({
    easing: 'easeOutExpo',
    duration: 7000,
    loop: false, // ループしない
  })

  basicTimeline
    .add({
      targets: '#basicTimeline #mysvg1',
      translateY: -50,
      duration: 1000,
      easing: 'easeOutExpo',
    })
    .add({
      targets: '#basicTimeline #mysvg2',
      translateY: -50,
      duration: 500,
      easing: 'easeOutExpo',
    })
    .add({
      targets: '#basicTimeline #mysvg3',
      translateY: 75,
      duration: 500,
      easing: 'easeOutExpo',
    })
    .add({
      targets: '#basicTimeline #mysvg3',
      translateY: -50,
      duration: 750,
      easing: 'easeOutExpo',
    })
    .add({
      targets: '#basicTimeline #next',
      opacity: [0, 1],
      duration: 2000,
      easing: 'easeInOutQuad',
    })
})
</script>

<template>
  <div>
    <div class="h-screen flex justify-center items-center">
      <div id="basicTimeline" class="text-center">
        <my-svg :id="`mysvg1`"></my-svg>
        <my-svg :id="`mysvg2`"></my-svg>
        <my-svg :id="`mysvg3`"></my-svg>
        <next-page
          :buttonColor="`bg-gradient-to-r from-cyan-500 to-blue-500 hover:bg-gradient-to-l`"
          :path="`/sample/1`"
          :text="`こんにちは`"
          :scrollEnd="true"
        ></next-page>
      </div>
    </div>
  </div>
</template>
