const progressCircle = document.querySelector(".autoplay-progress svg");
const progressContent = document.querySelector(".autoplay-progress span");
var swiper = new Swiper(".mySwiper", {
  on: {
      autoplayTimeLeft(s, time, progress) {
        progressCircle.style.setProperty("--progress", 1 - progress);
        progressContent.textContent = `${Math.ceil(time / 1000)}s`;
      }
  },
  autoplay: {
      delay: 3500,
      disableOnInteraction: false,
  },
  slidesPerView: 1,
  spaceBetween: 0,
  loop: true,
  pagination: {
      el: ".swiper-pagination",
      dynamicBullets: true,
      clickable: true,
  },
  navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
  },
});
