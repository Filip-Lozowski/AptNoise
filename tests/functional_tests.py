from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert "Flask" in browser.title

# open the app

# download the articles / be able to look at them

# The most interesting articles (those containing higher scores) are closer to the top

# The least interesting articles are at the bottom

# Click at the first article title to read it on its original page

# assign a score to the article

# assign scores to half of the articles

# Save all scores

# Retrain the model

# Reload the app

# Previously rated articles disappeared

# Not sure -> The order of remaining articles changed (as there is some randomness involved)
