export const isElementAtBottom = (element) => {
  if(element===null) {
    return
  }
  const rect=element.getBoundingClientRect()
  // 要素の下端が画面の下端と同じか、それより上にあるかを確認
  return rect.bottom<=window.innerHeight
}