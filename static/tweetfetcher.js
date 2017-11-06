/**
 * Returns a promise of a new donald trump tweet
 */
async function fetchNewTweet() {
  let tweet_resp = await fetch('/generate')
  return tweet_resp.json()
}


/**
 * Replaces the tweet on the page with a new one
 */
async function replaceCurrentTweet() {
  let current_tweet_elem = document.getElementById('current_tweet')
  let new_tweet = await fetchNewTweet()
  current_tweet_elem.innerHTML = new_tweet
}

setInterval(replaceCurrentTweet, 5 * 1000)
