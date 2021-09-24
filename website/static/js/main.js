function deleteNote(NoteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteid: NoteId })
    }).then((_res) => {
        window.location.href = '/'
    })
}