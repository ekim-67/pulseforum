document.addEventListener('DOMContentLoaded', () => {
    const clickableDivs = document.querySelectorAll('.media-body[data-url]');

    clickableDivs.forEach(div => {
        div.addEventListener('click', () => {
            const url = div.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
});