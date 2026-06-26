/**
 * Grocery Store Frontend Application
 * Fetches products from the API and displays them in a table.
 * Shows a random "Joke of the Day" banner on each page load.
 */

// ---------------------------------------------------------------------------
// Family-friendly jokes (Option B: static array, no external dependency)
// ---------------------------------------------------------------------------
const JOKES = [
  { setup: "Why did the banana go to the doctor?", punchline: "Because it wasn't peeling well!" },
  { setup: "What do you call a fake noodle?", punchline: "An impasta!" },
  { setup: "Why don't eggs tell jokes?", punchline: "They'd crack each other up!" },
  { setup: "What did the carrot say to the wheat?", punchline: "Lettuce rest, I'm feeling beet!" },
  { setup: "Why did the tomato turn red?", punchline: "Because it saw the salad dressing!" },
  { setup: "What do you call cheese that isn't yours?", punchline: "Nacho cheese!" },
  { setup: "Why did the cookie go to the hospital?", punchline: "Because it felt crummy!" },
  { setup: "What did the grape do when it got stepped on?", punchline: "Nothing but let out a little wine!" },
  { setup: "Why don't melons get married?", punchline: "Because they cantaloupe!" },
  { setup: "What's a skeleton's favorite snack?", punchline: "Spare ribs!" },
  { setup: "Why did the orange stop running?", punchline: "It ran out of juice!" },
  { setup: "How do you make an apple turnover?", punchline: "Push it down a hill!" },
  { setup: "What did the baby corn say to the mama corn?", punchline: "Where's pop corn?" },
  { setup: "Why did the mushroom go to the party alone?", punchline: "Because he's a fungi!" },
  { setup: "What do you get when you cross a dog and a calculator?", punchline: "A friend you can count on!" },
];

// ---------------------------------------------------------------------------
// Joke banner
// ---------------------------------------------------------------------------

/**
 * Pick a random joke from the static array and display it in the banner.
 */
function showRandomJoke() {
  const idx = Math.floor(Math.random() * JOKES.length);
  const joke = JOKES[idx];
  const jokeTextEl = document.getElementById("joke-text");
  if (jokeTextEl) {
    jokeTextEl.textContent = "😂 " + joke.setup + " — " + joke.punchline;
  }
}

// ---------------------------------------------------------------------------
// Product table
// ---------------------------------------------------------------------------

/**
 * Fetch products from the API and render them in the table.
 */
async function loadProducts() {
  const tbody = document.getElementById("product-tbody");
  if (!tbody) return;

  try {
    const response = await fetch("/products/");
    if (!response.ok) {
      throw new Error("Failed to fetch products (status " + response.status + ")");
    }
    const products = await response.json();

    if (products.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="empty-msg">No products found. Add some groceries!</td></tr>';
      return;
    }

    tbody.innerHTML = "";
    products.forEach(function (product) {
      const tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" + escapeHtml(product.name) + "</td>" +
        "<td>" + escapeHtml(product.description || "") + "</td>" +
        "<td>" + escapeHtml(product.category || "Other") + "</td>" +
        "<td>$" + Number(product.price).toFixed(2) + "</td>" +
        "<td>" + escapeHtml(product.unit || "piece") + "</td>" +
        "<td>" + Number(product.stock_quantity || 0) + "</td>" +
        "<td>" + (product.is_available ? "✅ Yes" : "❌ No") + "</td>";
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error(err);
    tbody.innerHTML = '<tr><td colspan="7" class="error-msg">⚠️ Could not load products. Please try again later.</td></tr>';
  }
}

/**
 * Escape HTML special characters to prevent XSS.
 */
function escapeHtml(str) {
  var div = document.createElement("div");
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

// ---------------------------------------------------------------------------
// Initialisation
// ---------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {
  showRandomJoke();
  loadProducts();
});
