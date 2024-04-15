VanillaTilt.init(document.querySelectorAll(".featured__card"), {
    perspective: 1000,
    scale: 1.1,
    speed: 1000,
    transition: true,
    glare: true,
    "max-glare": 0.3,
    max: 2,
});

// featured cards
try {
  const featuredCards = document.querySelectorAll('.featured__card');

  featuredCards.forEach((card, index) => {
    card.onclick = function() {
      // You can perform different actions based on the card's index.
      // For example, navigate to different URLs for different cards.
      if (index === 0) {
          window.location.href = 'shop';
      } else if (index === 1) {
          window.location.href = 'shop';
      } else {
          window.location.href = 'shop';
      }
    };
  });
} catch (error) {
  const featuredcards = document.querySelectorAll('.featured__card');

  featuredcards.forEach((card, index) => {
    card.onclick = function() {
      // You can perform different actions based on the card's index.
      // For example, navigate to different URLs for different cards.
      if (index === 0) {
          window.location.href = 'shop';
      } else if (index === 1) {
          window.location.href = 'shop';
      } else {
          window.location.href = 'shop';
      }
    };
  });
}