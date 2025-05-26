function toggleTheme() {
  document.body.classList.toggle("dark-theme");
  const icon = document.getElementById("theme-icon");

  if (document.body.classList.contains("dark-theme")) {
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
    localStorage.setItem("theme", "dark");
  } else {
    icon.classList.remove("fa-sun");
    icon.classList.add("fa-moon");
    localStorage.setItem("theme", "light");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const savedTheme = localStorage.getItem("theme");
  const icon = document.getElementById("theme-icon");

  if (savedTheme === "dark") {
    document.body.classList.add("dark-theme");
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
  }
});

document.getElementById("theme-toggle").addEventListener("click", toggleTheme);

// Category Filtering
document.addEventListener("DOMContentLoaded", function () {
  const filterBtns = document.querySelectorAll(".filter-btn");
  const postCards = document.querySelectorAll(".post-card");

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      // Remove active class from all buttons
      filterBtns.forEach((b) => b.classList.remove("active"));
      // Add active class to clicked button
      this.classList.add("active");

      const category = this.getAttribute("data-category");

      postCards.forEach((card) => {
        if (
          category === "all" ||
          card.getAttribute("data-category") === category
        ) {
          card.classList.remove("hidden");
          card.classList.add("show");
        } else {
          card.classList.add("hidden");
          card.classList.remove("show");
        }
      });
    });
  });
});

// Like Functionality
function toggleLike(button) {
  button.classList.toggle("liked");
  const heart = button.querySelector(".heart");
  const likeCount = button.querySelector(".like-count");
  let count = parseInt(likeCount.textContent);

  if (button.classList.contains("liked")) {
    heart.textContent = "❤️";
    likeCount.textContent = count + 1;
    button.style.animation = "likeAnimation 0.3s ease";
  } else {
    heart.textContent = "♡";
    likeCount.textContent = count - 1;
  }

  // Remove animation class after animation completes
  setTimeout(() => {
    button.style.animation = "";
  }, 300);
}

// Comment Functionality
function toggleComments(button) {
  const postCard = button.closest(".post-card");
  const commentsSection = postCard.querySelector(".comments-section");

  if (
    commentsSection.style.display === "none" ||
    commentsSection.style.display === ""
  ) {
    commentsSection.style.display = "block";
    button.style.background = "var(--primary-color)";
    button.style.color = "white";
  } else {
    commentsSection.style.display = "none";
    button.style.background = "var(--secondary-color)";
    button.style.color = "var(--text-color)";
  }
}

function addComment(button) {
  const commentForm = button.closest(".comment-form");
  const commentInput = commentForm.querySelector(".comment-input");
  const commentsList = commentForm
    .closest(".comments-section")
    .querySelector(".comments-list");
  const commentBtn = commentForm
    .closest(".post-card")
    .querySelector(".comment-btn");
  const commentCount = commentBtn.querySelector(".comment-count");

  if (commentInput.value.trim() !== "") {
    // Create new comment element
    const newComment = document.createElement("div");
    newComment.className = "comment";
    newComment.innerHTML = `<strong>You:</strong> ${commentInput.value.trim()}`;

    // Add fade-in animation
    newComment.style.opacity = "0";
    newComment.style.transform = "translateY(-10px)";
    commentsList.appendChild(newComment);

    // Animate comment appearance
    setTimeout(() => {
      newComment.style.transition = "all 0.3s ease";
      newComment.style.opacity = "1";
      newComment.style.transform = "translateY(0)";
    }, 10);

    // Update comment count
    let count = parseInt(commentCount.textContent);
    commentCount.textContent = count + 1;

    // Clear input
    commentInput.value = "";

    // Show success feedback
    button.textContent = "Posted!";
    button.style.background = "var(--success-color)";

    setTimeout(() => {
      button.textContent = "Post";
      button.style.background = "var(--primary-color)";
    }, 1000);
  }
}

// Smooth scrolling for CTA button
document.querySelector(".cta-btn").addEventListener("click", function (e) {
  e.preventDefault();
  document.querySelector(".category-filter").scrollIntoView({
    behavior: "smooth",
  });
});

// Add like animation keyframes to CSS dynamically
const style = document.createElement("style");
style.textContent = `
  @keyframes likeAnimation {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
  }
`;
document.head.appendChild(style);

// Search functionality (basic implementation)
document.querySelector(".search-btn").addEventListener("click", function () {
  const searchTerm = prompt("Enter search term:");
  if (searchTerm) {
    const posts = document.querySelectorAll(".post-card");
    let found = false;

    posts.forEach((post) => {
      const title = post.querySelector("h3").textContent.toLowerCase();
      const content = post.querySelector("p").textContent.toLowerCase();

      if (
        title.includes(searchTerm.toLowerCase()) ||
        content.includes(searchTerm.toLowerCase())
      ) {
        post.style.border = "2px solid var(--primary-color)";
        post.scrollIntoView({ behavior: "smooth", block: "center" });
        found = true;

        // Remove highlight after 3 seconds
        setTimeout(() => {
          post.style.border = "1px solid var(--border-color)";
        }, 3000);
      }
    });

    if (!found) {
      alert("No posts found matching your search.");
    }
  }
});

// Add intersection observer for scroll animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver(function (entries) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.animation = "fadeIn 0.6s ease-out forwards";
    }
  });
}, observerOptions);

// Observe all post cards
document.querySelectorAll(".post-card").forEach((card) => {
  observer.observe(card);
});
