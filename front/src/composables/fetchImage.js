export const fetchImages = async (keyName) => {
  try {
    const response = await fetch('/images.json')
    const data = await response.json()
    return data[keyName]
  } catch(error) {
    console.error('Error fetching images:', error)
    return []
  }
}