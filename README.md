# Lazy Portfolio Allocation Algorithm

The Lazy Portfolio Allocation Algorithm, first described by Albert H. Mao [1],
is a way of keeping your portfolio balanced with regular contributions or
withdraws, without the need for any explicit balancing operations. It takes a
list of assets (which could be funds, accounts, etc), their current values, and
their target or *desired* allocation percentage, as well as an amount to
contribute. The algorithm then calculates the optimal way to split up the
contribution between the assets such as to minimize each asset's deviation from
the desired allocation.

[1] [Optimal lazy portfolio rebalancing calculator (http://optimalrebalancing.tk/index.html)](http://optimalrebalancing.tk/index.html)

This repository holds my writeup and reference implementation for the Lazy
Portfolio Allocation Algorithm. The writeup takes the form of a Jupyter
notebook, and can be viewed in one of these forms:

* [Lazy Portfolio Allocation Algorithm (PDF)](https://github.com/brownan/lazy-allocation/raw/main/Lazy%20Portfolio%20Allocation%20Algorithm.pdf)
* [Lazy Portfolio Allocation Algorithm (HTML)](https://brownan.github.io/lazy-allocation/Lazy%20Portfolio%20Allocation%20Algorithm.html)

Additionally, reference implementations may be found in these files:
* [lazy.py](lazy.py) Python
* [lazy-googlesheets.js](lazy-googlesheets.js) Google Sheets App Script
