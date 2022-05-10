# Amer-v-Brit-Lexicon-Analysis
## William Kariampuzha

### Purpose
Do a divergence (or convergence?) analysis of the American and British lexicon sets.

Requirements:
1. Rewrite and optimize the preprocessing algorithm
2. 

Derivation of Normalized and Sample-Size Adjusted $\chi^2$ Test

<img src="https://render.githubusercontent.com/render/math?math={\chi^2 = \sum \frac{(O_i-E_i)^2}{E_i}}#gh-light-mode-only">
<img src="https://render.githubusercontent.com/render/math?math={\color{white}\chi^2 = \sum \frac{(O_i-E_i)^2}{E_i}}#gh-dark-mode-only">


We will consider consider British English to be the parent language (containing the expected distribution) under the null hypothesis that there has been no divergence. Thus,
A<sub>i</sub> = frequency of the American lexeme
B<sub>i</sub> = frequency of British lexeme.
$$\chi^2 = \sum \frac{(A_i-B_i)^2}{B_i}$$
<img src="https://render.githubusercontent.com/render/math?math={\chi^2 = \sum \frac{(A_i-B_i)^2}{B_i}}#gh-light-mode-only">
<img src="https://render.githubusercontent.com/render/math?math={\color{white}\chi^2 = \sum \frac{(A_i-B_i)^2}{B_i}}#gh-dark-mode-only">

The (sample) sizes of the American and British corpora are not the same. To normalize this, we will multiply A<sub>i</sub> by 
<img src="https://render.githubusercontent.com/render/math?math={\frac{\sum B_i}{\sum A_i}}#gh-light-mode-only">
<img src="https://render.githubusercontent.com/render/math?math={\color{white}\frac{\sum B_i}{\sum A_i}}#gh-dark-mode-only">

<img src="https://render.githubusercontent.com/render/math?math={\chi^2 = \sum \frac{(A_i \cdot \frac{\sum B_i}{\sum A_i} -B_i )^2}{B_i}}#gh-light-mode-only">
<img src="https://render.githubusercontent.com/render/math?math={\color{white}\chi^2 = \sum \frac{(A_i \cdot \frac{\sum B_i}{\sum A_i} -B_i )^2}{B_i}}#gh-dark-mode-only">

As we only calculated normalized data (it would be a hassle to go back and get the raw data), we will multiply the terms by 1/B<sub>i</sub>

<img src="https://render.githubusercontent.com/render/math?math={\chi^2 = \sum \frac{(A_i \cdot \frac{\sum B_i}{\sum A_i} -B_i )^2}{B_i}}#gh-light-mode-only">
<img src="https://render.githubusercontent.com/render/math?math={\color{white}\chi^2 = \sum \frac{(A_i \cdot \frac{\sum B_i}{\sum A_i} -B_i )^2}{B_i}}#gh-dark-mode-only">

$$\chi^2 \cdot \frac{1}{B_i}=  \sum \frac{(\frac{A_i \cdot \frac{\sum B_i}{\sum A_i}}{\sum{A_i}} \cdot \frac{\sum A_i}{\sum B_i} -$$\frac{B_i}{\sum{B_i}})^2}{\frac{B_i}{\sum{B_i}}}$$
from [Stats Exchange](https://stats.stackexchange.com/questions/114859/can-we-run-a-chi-squared-test-on-a-normalized-function)
and the first term by \frac{A_i}{A_i}
This simplifies to:
$$\chi^2 = B_i \cdot \sum \frac{(\frac{A_i}{\sum{A_i}} -\frac{B_i}{\sum{B_i}})^2}{\frac{B_i}{\sum{B_i}}}$$
