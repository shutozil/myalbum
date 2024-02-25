<template>
  <div
    class="h-screen bg-cover flex justify-center items-center"
    :style="{
      backgroundImage: `url(${image.sign_url})`,
    }"
  >
    <div
      v-if="image.comment"
      :class="textColor"
      class="font-bold text-transparent text-4xl bg-clip-text"
    >
      <div v-html="decodeComment(image.comment)" />
    </div>
  </div>
</template>

<script>
export default {
  props: ['image','textColor'],

  methods: {
    decodeComment(comment) {
      const newComment=decodeURIComponent(escape(atob(comment)))

      const commentSplit=newComment.split('・')

      if(commentSplit.length===1) {
        return '<div>'+newComment+'</div>'
      } else {
        let finalComment=''
        commentSplit.forEach(
          (item) => (finalComment+='<div>'+item+'</div>'),
        )
        return finalComment
      }
    },
  },
}
</script>