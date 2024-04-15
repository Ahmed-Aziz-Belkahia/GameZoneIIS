const progressCircleMini = document.querySelector(".autoplay-progressMini svg");
const progressContentMini = document.querySelector(".autoplay-progressMini span");
var swiperMini = new Swiper(".mySwiperMini", {
  on: {
      autoplayTimeLeft(s, time, progress) {
        progressCircleMini.style.setProperty("--progress", 1 - progress);
        progressContentMini.textContent = `${Math.ceil(time / 1000)}s`;
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
      el: ".swiper-paginationMini",
      dynamicBullets: true,
      clickable: true,
  },
});
