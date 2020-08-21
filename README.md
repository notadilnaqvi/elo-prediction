# Elo calculation
* Scraps chess PGNs from a [website](https://www.pgnmentor.com/files.html) using beautifulsoup4 & requests 
* Extracts Black's Elo, White's Elo & Result using regex 
* Calculates Elo change using FIDE's formula 
* Uses this data to train a neural network (made using Tensorflow) to predict the updated Elo when given both players' Elo and result as an input
