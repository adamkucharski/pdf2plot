# PDFy

A web app to extract data from PDF figures. All processing happens in your browser - no data is uploaded to any server.

## How It Works

1. **Upload**: Drop a PDF containing a figure with vector graphics
2. **Calibrate**: Select two X-axis tick marks and two Y-axis tick marks, entering their actual values
3. **Select Data**: Click on the lines/paths you want to extract
4. **Export**: Download the rescaled coordinates as CSV

The app uses PDF.js to parse PDF files directly in the browser and extract vector path coordinates. It then applies linear (or logarithmic) interpolation based on your calibration points to convert the raw PDF coordinates to the actual data values.

This new app was inspired by my previous discontinued package [scrapR](https://github.com/adamkucharski/scrapR/).

## Technical Details

- Built with vanilla JavaScript (no frameworks)
- Uses [PDF.js](https://mozilla.github.io/pdf.js/) for PDF parsing
- All computation happens client-side
- Works with modern browsers (Chrome, Firefox, Safari, Edge)

## Limitations

- Only works with vector-based PDFs (not scanned/rasterized images)
- Complex PDFs with many elements may require pre-processing
- First page only is processed

## Citation

If you use PDFy in your work, please cite:

```
Kucharski, A. (2026). PDFy: A web tool for extracting data from PDF figures.
https://github.com/adamkucharski/pdfy
```
