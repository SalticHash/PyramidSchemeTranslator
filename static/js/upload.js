async function put_blob(file) {
    const formData = new FormData();
    formData.append('files', file);
    formData.append('expiryHours', '1');

    try {
        const response = await fetch('https://tempfile.org/api/upload/local', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.success) {
            return result
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        if (!error.message) {
            alert("Upload failed")
        } else {
            alert('Upload failed:', error.message);
        }
    }
    return {"success": false}
}

async function handleUpload() {
    const button = document.getElementById("translate_posters")
    if (button.disabled) return

    button.innerText = "Wait for Upload...";
    button.disabled = true;
    const generatedPosters = document.getElementById("generated_posters").files[0]
    const translatedPoster = document.getElementById("translated_poster").files[0]
    if (!generatedPosters || !translatedPoster) {
        alert("Missing file!")
        button.disabled = false;
        button.innerText = "Translate!";
        return
    }

    const generatedPostersURL = await put_blob(generatedPosters)
    const translatedPosterURL = await put_blob(translatedPoster)
    if (!generatedPostersURL.success || !translatedPosterURL.success) {
        button.disabled = false;
        button.innerText = "Translate!";
        return
    }

    const formData = new FormData();
    formData.append('generated_posters_url', `https://tempfile.org/api/file/${generatedPostersURL.files[0].id}`);
    formData.append('translated_poster_url', `https://tempfile.org/api/file/${translatedPosterURL.files[0].id}`);
    console.log(translatedPosterURL.files[0].url)
    const response = await fetch('/api/translate', {
        method: 'POST',
        body: formData
    });
    const url = await response.text()
    window.location = url + "/download";
    button.disabled = false;
    button.innerText = "Translate!";
}