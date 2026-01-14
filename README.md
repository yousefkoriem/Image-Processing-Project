# Image Processing Project

A small Python toolkit demonstrating basic image processing filters and example workflows using both scripts and Jupyter notebooks.

## Overview

This repository contains implementations of common image processing filters grouped by category (smoothing, sharpening, noise) along with example notebooks and simple page scripts to run and preview filters.

## Features

- Collection of spatial filters: mean, median, min, max, Gaussian, and more.
- Edge detection and sharpening: Sobel, Prewitt, Laplace.
- Noise generators and removers: salt, pepper, salt-and-pepper.
- Example notebooks for exploration and interactive experimentation.

## Team (CS351: Image Processing Module)

Team of five students:

- [Yousef Koriem](https://github.com/yousefkoriem) — Team Leader/GUI Developer
- [Ahmed Maher](https://github.com/ahmedmaheroo) — Smoother
- [Hajer Fathi](https://github.com/HJR403) — Sharpner
- [Yousef Rady](https://github.com/) — Noise Remover/ MainUI Developer
- [Farah Ahmed](https://github.com/Speedfarah77) — Documentation/Function Builder

## Requirements

- Python 3.8+
- Install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Quick Usage

- Run the example script:

```bash
python main.py
```

- Open the notebooks to explore filters interactively (e.g., `Noise.ipynb`, `Smoothing.ipynb`, `Sharpening.ipynb`).

## Repository layout

- `filters/`
	- `smooth/` — smoothing filters: `gauss.py`, `mean.py`, `median.py`, `min.py`, `max.py`
	- `sharp/` — sharpening and edge operators: `sobel.py`, `prewitt.py`, `laplace.py`
	- `noise/` — noise generation/removal: `salt.py`, `pepper.py`, `salt_and_pepper.py`
- `pages/` — simple page scripts and a `filter_toolkit.py` helper used by the pages.
- `main.py` — example runner to exercise filters from the command line.
- Notebooks: `Noise.ipynb`, `Smoothing.ipynb`, `Sharpening.ipynb` — interactive demos.

## How to use filters in code

Import filters directly from the package, for example:

```python
from filters.smooth import gauss

# apply functions are defined in each module; see notebooks for exact usage
```

Check the example notebooks for ready-to-run code snippets showing how to load images, apply filters, and visualize results.

## Contributing

Contributions are welcome. Please open issues for bugs or feature requests, and submit pull requests for changes.

## License

Add a license file if you wish to release this project publicly.

## Contact

For questions, reach out to the repository owner.

