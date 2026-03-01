async function put_blob(file) {
    const res = await fetch("/api/blob_upload_url")
    const data = await res.json()

    await fetch(data.uploadUrl, {
        method: "PUT",
        body: file
    })
    console.log(data)
    return data.url
}

async function handleUpload() {
    const generatedPosters = document.getElementById("generated_posters").files[0]
    const translatedPoster = document.getElementById("translated_poster").files[0]

    const generatedPostersURL = await put_blob(generatedPosters)
    const translatedPosterURL = await put_blob(translatedPoster)

    const url = await fetch("/api/translate", {
        method: "POST",
        body: JSON.stringify({
            generated_posters_url: generatedPostersURL,
            translated_poster_url: translatedPosterURL,
        })
    })

    console.log(url)
    // window.location.href = url
}