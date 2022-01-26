from selenium import webdriver

browser = webdriver.Firefox()

# open the app
browser.get('http://localhost:5000')

# check if this is a news app
assert "AptNoise" in browser.title

# click a button to download articles

# The most interesting articles (those containing higher scores) are closer to the top

# The least interesting articles are at the bottom

# Click at the first article title to read it on its original page

# assign a score to the article by typing it into a box near the link

# assign scores to half of the articles

# Save all scores

# Retrain the model

# Reload the app

# Previously rated articles disappeared

# Not sure -> The order of remaining articles changed (as there is some randomness involved)
