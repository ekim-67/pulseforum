/*document.addEventListener('DOMContentLoaded', () => {
    const clickableDivs = document.querySelectorAll('.media-body[data-url]');

    clickableDivs.forEach(div => {
        div.addEventListener('click', () => {
            const url = div.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
});*/

document.addEventListener('DOMContentLoaded', () => {
    const container = document.body; // Or use a specific parent container if needed

    container.addEventListener('click', (event) => {
        // Check if the clicked element or one of its parents has the 'media-body' class
        const mediaBody = event.target.closest('.content-section[data-url]');
        if (mediaBody) {
            const url = mediaBody.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        }
    });
});