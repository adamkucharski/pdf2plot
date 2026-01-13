# PDFy

A web app to extract data from PDF figures. All processing happens in your browser - no data is uploaded to any server.

## How It Works

1. **Upload**: Drop a PDF containing a figure with vector graphics
2. **Calibrate**: Select two X-axis tick marks and two Y-axis tick marks, entering their actual values
3. **Select Data**: Click on the lines/paths you want to extract
4. **Export**: Download the rescaled coordinates as CSV

The app uses PDF.js to parse PDF files directly in the browser and extract vector path coordinates. It then applies linear (or logarithmic) interpolation based on your calibration points to convert the raw PDF coordinates to the actual data values.

## Open Locally

Simply open `index.html` in a modern web browser. Due to browser security restrictions with local files, you may need to serve it via a local server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve .
```

Then navigate to `http://localhost:8000`

## Usage Guide

### Step 1: Prepare Your PDF

For best results:
- The PDF should contain vector graphics (not a rasterized image)
- Remove unnecessary elements using a vector editor (Illustrator, Inkscape, Affinity Designer) if the figure has too many elements
- Keep at least 2 tick marks on each axis for calibration

### Step 2: Upload and View

- Drag and drop your PDF or click to select
- The app extracts all vector paths and displays them numbered

### Step 3: Calibrate Axes

1. **Select X-Axis Ticks**: Click "Select X-Axis Ticks" button, then click on two tick marks on the X-axis. Enter their actual values in the form fields.

2. **Select Y-Axis Ticks**: Click "Select Y-Axis Ticks" button, then click on two tick marks on the Y-axis. Enter their actual values.

3. **Log Scale**: If either axis uses a logarithmic scale, check the corresponding checkbox.

### Step 4: Select Data

- Click "Select Data Lines" button
- Click on each line/path you want to extract
- Selected paths are highlighted in purple

### Step 5: Extract and Export

- Click "Extract Data" to calculate the rescaled coordinates
- Preview the data in the table
- Download as a single CSV (all lines with a `line` column) or separate files for each line

## Output Format

### Single CSV (Download CSV)
```csv
line,x,y
1,0.5,10.2
1,1.0,15.3
...
2,0.5,8.1
2,1.0,12.4
...
```

### Separate Files (Download All)
Creates `filename_1.csv`, `filename_2.csv`, etc.:
```csv
x,y
0.5,10.2
1.0,15.3
...
```

## Technical Details

- Built with vanilla JavaScript (no frameworks)
- Uses [PDF.js](https://mozilla.github.io/pdf.js/) for PDF parsing
- All computation happens client-side
- Works with modern browsers (Chrome, Firefox, Safari, Edge)

## Limitations

- Only works with vector-based PDFs (not scanned/rasterized images)
- Complex PDFs with many elements may require pre-processing
- First page only is processed

## License

MIT
