<template>
  <div>
    <svg
      :id="id"
      baseProfile="full"
      height="75px"
      version="1.1"
      width="200px"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:ev="http://www.w3.org/2001/xml-events"
      xmlns:xlink="http://www.w3.org/1999/xlink"
    >
      <defs />
      <text x="10" y="50" class="custom-text" font-family="serif">あああ</text>
    </svg>
  </div>
</template>

<script>
export default {
  props: ['id']
}
</script>