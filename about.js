console.log("script is running");
window.addEventListener('scroll', (event) => {
    const text = document.querySelector('.uppertext');
    console.log("scrolling");

    const scrollY = window.scrollY;

    const newSize = Math.max(3, 5 - scrollY / 200);
    const newPos = Math.max(0, scrollY / 2);

    text.style.fontSize = `${newSize}rem`;
    text.style.transform = `translateY(-${newPos}px)`;
});
