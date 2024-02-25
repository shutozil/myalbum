// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  devtools: { enabled: true },
  srcDir: 'src',
  // target: 'static',
  ssr: false,
  app: {
    head: {
      title: 'ハローワールド',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'robots', content: 'noindex,nofollow' },
      ],
    },
  },
  components: [
    {
      path: "@/components",
      pathPrefix: false,
    },
  ],
  spaLoadingTemplate: 'spa-loading-template.html',
  modules: [
    '@nuxtjs/tailwindcss',
    '@hypernym/nuxt-anime'
  ],
  tailwindcss: {
    cssPath: '~/assets/css/tailwind.css',
  }
})
