from __future__ import annotations

import cv2
import numpy as np
import pywt


FEATURE_NAMES = [
    "laplacian_var",
    "sobel_mean",
    "sobel_std",
    "brightness_mean",
    "brightness_std",
    "dark_ratio",
    "bright_ratio",
    "contrast_rms",
    "noise_est",
    "saturation_mean",
    "entropy",
    "edge_density",
    "blur_fft",
    "block_std",
    "color_hist_skew",
]


def extract_features(image_bgr: np.ndarray) -> dict:
    if image_bgr is None or image_bgr.size == 0:
        raise ValueError("Input image is empty")

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_var = float(laplacian.var())

    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(gx**2 + gy**2)
    sobel_mean = float(mag.mean())
    sobel_std = float(mag.std())

    v_channel = hsv[:, :, 2].astype(np.float32)
    brightness_mean = float(v_channel.mean())
    brightness_std = float(v_channel.std())
    dark_ratio = float((v_channel < 40).mean())
    bright_ratio = float((v_channel > 215).mean())

    contrast_rms = float(gray.std())

    coeffs = pywt.dwt2(gray.astype(np.float32), "db1")
    _, (cH, cV, cD) = coeffs if isinstance(coeffs, tuple) and len(coeffs) == 3 else (None, coeffs[1])
    if cD.size == 0:
        noise_est = 0.0
    else:
        noise_est = float(np.median(np.abs(cD)) / 0.6745)

    saturation_mean = float(hsv[:, :, 1].mean())

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten().astype(np.float64)
    hist = hist / (hist.sum() + 1e-7)
    entropy = float(-(hist * np.log2(hist + 1e-7)).sum())

    edges = cv2.Canny(gray, 100, 200)
    edge_density = float(edges.mean() / 255.0)

    fft = np.fft.fft2(gray)
    fft_shift = np.fft.fftshift(fft)
    magnitude_spectrum = 20 * np.log(np.abs(fft_shift) + 1)
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2
    high_freq_region = magnitude_spectrum[: max(1, crow - 10), : max(1, ccol - 10)]
    blur_fft = float(high_freq_region.mean())

    block_size = 32
    if rows < block_size or cols < block_size:
        block_std = float(gray.std())
    else:
        blocks = []
        for i in range(0, rows, block_size):
            for j in range(0, cols, block_size):
                block = gray[i : i + block_size, j : j + block_size]
                if block.size > 0:
                    blocks.append(float(block.std()))
        block_std = float(np.mean(blocks)) if blocks else 0.0

    hist_b = cv2.calcHist([image_bgr], [0], None, [256], [0, 256]).flatten().astype(np.float64)
    hist_b = hist_b + 1e-7
    hist_mean = hist_b.mean()
    hist_std = hist_b.std() + 1e-7
    color_hist_skew = float(np.mean((hist_b - hist_mean) ** 3) / (hist_std**3))

    return {
        "laplacian_var": laplacian_var,
        "sobel_mean": sobel_mean,
        "sobel_std": sobel_std,
        "brightness_mean": brightness_mean,
        "brightness_std": brightness_std,
        "dark_ratio": dark_ratio,
        "bright_ratio": bright_ratio,
        "contrast_rms": contrast_rms,
        "noise_est": noise_est,
        "saturation_mean": saturation_mean,
        "entropy": entropy,
        "edge_density": edge_density,
        "blur_fft": blur_fft,
        "block_std": block_std,
        "color_hist_skew": color_hist_skew,
    }
