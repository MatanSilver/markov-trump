/**
 * Returns a promise of a new donald trump tweet
 */
async function fetchNewTweet() {
  let tweet_resp = await fetch('/generate')
  return tweet_resp.json()
}

/**
 * Fade in and fade out implementations taken and adapted from
 * https://stackoverflow.com/questions/6121203/how-to-do-fade-in-and-fade-out-with-javascript-and-css
 */


/**
 * Fades out the given element. Returns a promise that resolves when the element
 * is fully faded
 */
function fade(element) {
  return new Promise((res, rej) => {
    var op = 1; // initial opacity
    var timer = setInterval(function() {
      if (op <= 0.1) {
        clearInterval(timer);
        element.style.display = 'none';
        res()
      }
      element.style.opacity = op;
      element.style.filter = 'alpha(opacity=' + op * 100 + ")";
      op -= op * 0.1;
    }, 50);
  })
}


/**
 * Fades in the given element. Returns a promise that resolves when the element
 * is fully visible
 */
function unfade(element) {
  return new Promise((res, rej) => {
    var op = 0.1; // initial opacity
    element.style.display = 'block';
    var timer = setInterval(function() {
      if (op >= 1) {
        clearInterval(timer);
        res()
      }
      element.style.opacity = op;
      element.style.filter = 'alpha(opacity=' + op * 100 + ")";
      op += op * 0.1;
    }, 10);
  })
}

/**
 * Replaces the tweet on the page with a new one
 */
async function replaceCurrentTweet() {
  let current_tweet_elem = document.getElementById('current_tweet')
  let new_tweet = await fetchNewTweet()
  await fade(current_tweet_elem)
  current_tweet_elem.innerHTML = new_tweet
  await unfade(current_tweet_elem)
}

setInterval(replaceCurrentTweet, 5 * 1000)
