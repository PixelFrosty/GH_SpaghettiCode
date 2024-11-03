console.log("script is running");
window.addEventListener('scroll', (event) => {
    const text = document.querySelector('.uppertext');
    const members = document.querySelectorAll('.mem');
    console.log("scrolling");

    const scrollY = window.scrollY;
    console.log(scrollY);

    const newSizeText = Math.max(3, 5 - scrollY / 200);
    const newPosText = Math.max(0, (scrollY / 2) - 50);


    text.style.fontSize = `${newSizeText}rem`;
    text.style.transform = `translateY(-${newPosText}px)`;
    members.forEach((member, index) => {
        const delay = index * 100;

        setTimeout(() => {

            const newPosMem = (182 - scrollY) - 150;
            const newOpMem = Math.min((scrollY / 183) * 1.5 - 0.5, 1);

            member.style.transform = `translateY(${newPosMem}px)`; // Bring it into view
            member.style.opacity = `${newOpMem}`;

        }, delay);
    });

});
