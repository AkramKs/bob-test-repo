/**
 * Paws & Jokes – Dog & Cat Blog
 * Injects dummy blog posts into the #blog-posts container on page load.
 */
(function () {
  "use strict";

  const blogPosts = [
    {
      title: "Breaking News: Local Cat Knocks Over 14th Glass of Water This Week",
      author: "Whiskers McFluff",
      date: "2025-04-01",
      image: "🐱",
      excerpt:
        "In what can only be described as a 'purr-sistent' campaign, Whiskers has once again asserted dominance over gravity. Scientists remain baffled. The water glass industry is in shambles.",
    },
    {
      title: "Dog Discovers Tail, Declares It 'Suspicious'",
      author: "Bark Ruffalo",
      date: "2025-03-28",
      image: "🐶",
      excerpt:
        "After three full spins and a confused head-tilt, local good boy Buddy determined his own tail 'cannot be trusted.' Sources confirm the tail has been placed under 24/7 surveillance.",
    },
    {
      title: "Cat Logic 101: If I Fits, I Sits – Even If I Clearly Don't Fits",
      author: "Professor Meowington",
      date: "2025-03-25",
      image: "📦",
      excerpt:
        "A groundbreaking study confirms that cardboard boxes of any size are legally required to be sat in, regardless of feline dimensions. 'The laws of physics are merely a suggestion,' said one participant.",
    },
    {
      title: "Golden Retriever Greets Mailman Like Long-Lost War Hero For 847th Consecutive Day",
      author: "Buddy Wigglebutt",
      date: "2025-03-20",
      image: "✉️",
      excerpt:
        "Eyewitnesses report tail wagging so vigorous it could power a small turbine. 'Every. Single. Day,' sighed the mailman, secretly loving every second of it.",
    },
  ];

  function createPostCard(post) {
    const article = document.createElement("article");
    article.className = "post-card";

    const iconSpan = document.createElement("span");
    iconSpan.className = "post-icon";
    iconSpan.textContent = post.image;

    const contentDiv = document.createElement("div");
    contentDiv.className = "post-content";

    const title = document.createElement("h2");
    title.className = "post-title";
    title.textContent = post.title;

    const meta = document.createElement("p");
    meta.className = "post-meta";
    meta.textContent = `By ${post.author} on ${post.date}`;

    const excerpt = document.createElement("p");
    excerpt.className = "post-excerpt";
    excerpt.textContent = post.excerpt;

    contentDiv.appendChild(title);
    contentDiv.appendChild(meta);
    contentDiv.appendChild(excerpt);

    article.appendChild(iconSpan);
    article.appendChild(contentDiv);

    return article;
  }

  function renderPosts() {
    const container = document.getElementById("blog-posts");
    if (!container) {
      return;
    }

    blogPosts.forEach(function (post) {
      container.appendChild(createPostCard(post));
    });
  }

  // Run on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderPosts);
  } else {
    renderPosts();
  }
})();
