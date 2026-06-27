// Hardcoded array of funny dog & cat blog posts — no network requests needed!
const posts = [
  {
    title: "Why My Dog Thinks He's a Cat",
    body: "Every morning, I find my 80-pound Labrador perched on the windowsill, glaring at birds with the intensity of a feline assassin. He's started grooming himself with his paw — poorly, I might add — and has taken a peculiar interest in the laser pointer. Last Tuesday, I caught him attempting to squeeze into a shoebox. The box did not survive. Neither did my sanity."
  },
  {
    title: "Top 10 Ways Cats Plot World Domination",
    body: "Number one: they've already trained us to feed them on demand. Number two: the unblinking stare at 3 AM isn't curiosity — it's surveillance. Number three: knocking things off tables is not clumsiness; it's testing gravity for their doomsday device. Numbers four through ten are classified, and my cat is watching me type this. Send help."
  },
  {
    title: "The Secret Life of Socks (According to My Cat)",
    body: "I used to blame the washing machine for eating my socks. Then I found the stash. Behind the couch, under the bed, inside an old shoe — a veritable sock empire. My cat, Sir Whiskers III, had been collecting them for months. He sits on his throne of cotton blends like a tiny, purring dragon guarding his treasure. I've accepted that I now pay rent in argyle."
  },
  {
    title: "My Cat Hired a Dog as Her Bodyguard",
    body: "It started innocently. The dog would bark at the mailman; the cat would watch approvingly from the sofa. Now they've formalized the arrangement. She pays him in kibble she knocks off the counter, and he escorts her to the food bowl like a furry Secret Service agent. I'm not saying they've formed a cross-species mafia, but my slippers have been missing for a week and no one's talking."
  },
  {
    title: "Confessions of a Dog Who Failed Obedience School",
    body: "Look, I tried. I really did. But when the instructor said 'stay,' I heard 'investigate that fascinating smell over there.' When she said 'heel,' I assumed it was a fashion critique. And 'roll over'? Please. I have dignity. Sort of. Okay, fine, I rolled over for the treat, but only because it was bacon-flavored. I regret nothing. — Chewbacca, Professional Good Boy"
  },
  {
    title: "The Great Laser Pointer Conspiracy",
    body: "Scientists claim the red dot is just light. Scientists have clearly never met my dog. He spent four hours yesterday trying to dig through the hardwood floor to catch it. Meanwhile, the cat sat on the couch, watching with an expression that can only be described as 'exactly according to plan.' I'm fairly certain the cat invented the laser pointer. Probably in her secret underground lair."
  },
  {
    title: "Why Cats Always Sit on Your Keyboard",
    body: "You think it's about warmth. It's not. Your cat has read everything you've typed and is deeply unimpressed. That passive-aggressive paw on the delete key? Editorial feedback. The sudden sprint across the keyboard that opens seventeen terminal windows? A performance review. According to my cat, my typing speed is 'adequate' but my choice of emojis is 'pedestrian at best.'"
  },
  {
    title: "A Dog's Guide to Home Security",
    body: "Rule 1: Bark at everything. Rule 2: If it moves, bark louder. Rule 3: If it doesn't move, investigate, then bark. Rule 4: The vacuum cleaner is an existential threat and must be destroyed — or fled from heroically. Rule 5: The Amazon delivery person is definitely hiding treats, and your failure to retrieve them is a strategic blunder of historic proportions. Woof."
  }
];

/**
 * Renders all hardcoded blog posts into the #blog-posts container.
 * Each post becomes a styled card with title and body.
 */
function renderPosts() {
  const container = document.getElementById('blog-posts');
  if (!container) return;

  posts.forEach(function(post) {
    const card = document.createElement('article');
    card.className = 'blog-card';

    const title = document.createElement('h2');
    title.className = 'blog-title';
    title.textContent = post.title;

    const body = document.createElement('p');
    body.className = 'blog-body';
    body.textContent = post.body;

    card.appendChild(title);
    card.appendChild(body);
    container.appendChild(card);
  });
}

document.addEventListener('DOMContentLoaded', renderPosts);
