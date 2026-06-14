#!/usr/bin/env python3
"""
pdf2plot helper — extract vector paths from a PDF figure and calibrate to data coordinates.

Usage:
  python pdf2plot_helper.py render <pdf_path> [--dpi 150]

  python pdf2plot_helper.py export <paths_json> \
      --x-left  (ID:VAL | @PX:VAL)  --x-right  (ID:VAL | @PX:VAL) \
      --y-bottom (ID:VAL | @PX:VAL) --y-top    (ID:VAL | @PX:VAL) \
      --data ID [ID ...] [--x-log] [--y-log] [--output out.csv]

Calibration anchors accept either a path ID or a pixel coordinate (@-prefix):
  --x-left 5:0      path ID 5 maps to data value 0
  --x-left @150:0   pixel X=150 in the rendered image maps to data value 0
  --y-bottom @820:0 pixel Y=820 in the rendered image maps to data value 0
"""
import sys, json, math, argparse
from pathlib import Path
from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def canvas_pt(p, scale, page_height):
    # PyMuPDF uses Y=0 at top; invert to standard PDF coords (Y=0 at bottom).
    return {'x': p.x * scale, 'y': (page_height - p.y) * scale}


def sample_bezier(p0, p1, p2, p3, scale, page_height, steps=10):
    pts = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1 - t
        bx = mt**3*p0.x + 3*mt**2*t*p1.x + 3*mt*t**2*p2.x + t**3*p3.x
        by = mt**3*p0.y + 3*mt**2*t*p1.y + 3*mt*t**2*p2.y + t**3*p3.y
        pts.append({'x': bx * scale, 'y': (page_height - by) * scale})
    return pts


def get_bounds(points):
    xs = [p['x'] for p in points]
    ys = [p['y'] for p in points]
    return {
        'minX': min(xs), 'maxX': max(xs),
        'minY': min(ys), 'maxY': max(ys),
        'centerX': (min(xs) + max(xs)) / 2,
        'centerY': (min(ys) + max(ys)) / 2,
        'width':  max(xs) - min(xs),
        'height': max(ys) - min(ys),
    }


def classify(bounds, canvas_w, canvas_h):
    w, h = bounds['width'], bounds['height']
    long_dim = max(w, h)
    short_dim = min(w, h)
    if long_dim < canvas_w * 0.06 and short_dim < 6:
        return 'tick'
    if long_dim > canvas_w * 0.15 and short_dim < 6:
        return 'frame'
    if w > canvas_w * 0.05 and h > canvas_h * 0.05:
        return 'data'
    return 'other'


# ---------------------------------------------------------------------------
# render command
# ---------------------------------------------------------------------------

def render_cmd(args):
    try:
        import fitz
    except ImportError:
        sys.exit("ERROR: PyMuPDF not installed. Run:  pip install pymupdf")

    pdf_path = Path(args.pdf)
    dpi = args.dpi
    scale = dpi / 72.0

    doc = fitz.open(str(pdf_path))
    page = doc[0]
    page_height = page.rect.height
    canvas_w = page.rect.width * scale
    canvas_h = page_height * scale

    # Extract vector paths
    paths = []
    for drawing in page.get_drawings():
        points = []
        current = None
        for item in drawing['items']:
            kind = item[0]
            if kind == 'm':
                p = item[1]
                current = p
                points.append(canvas_pt(p, scale, page_height))
            elif kind == 'l':
                p = item[1]
                points.append(canvas_pt(p, scale, page_height))
                current = p
            elif kind == 'c':
                p1, p2, p3 = item[1], item[2], item[3]
                if current is not None:
                    points.extend(sample_bezier(current, p1, p2, p3, scale, page_height))
                current = p3
            elif kind == 're':
                r = item[1]
                for px, py in [(r.x0,r.y0),(r.x1,r.y0),(r.x1,r.y1),(r.x0,r.y1),(r.x0,r.y0)]:
                    points.append({'x': px * scale, 'y': (page_height - py) * scale})

        if len(points) < 2:
            continue
        bounds = get_bounds(points)
        if max(bounds['width'], bounds['height']) < 1:
            continue

        color = drawing.get('color') or (0.0, 0.0, 0.0)
        color_hex = '#{:02x}{:02x}{:02x}'.format(
            int(color[0]*255), int(color[1]*255), int(color[2]*255))

        paths.append({
            'id': len(paths),
            'points': points,
            'bounds': bounds,
            'color': color_hex,
            'nPoints': len(points),
            'type': classify(bounds, canvas_w, canvas_h),
        })

    # Extract axis labels from PDF text (same coordinate space as paths)
    frame_paths = [p for p in paths if p['type'] == 'frame']
    y_frame = max(frame_paths, key=lambda p: p['bounds']['height']) if frame_paths else None

    axis_labels = {'y': [], 'x': []}
    for w in page.get_text("words"):
        x0, y0, x1, y1, word = w[0], w[1], w[2], w[3], w[4]
        try:
            val = float(word.replace(',', ''))
        except ValueError:
            continue
        cx = ((x0 + x1) / 2) * scale
        cy = (page_height - (y0 + y1) / 2) * scale  # same Y-flip as canvas_pt
        if y_frame:
            if cy < y_frame['bounds']['minY']:
                # Below the frame bottom: X-axis label (its canvas_x is the calibration coord)
                axis_labels['x'].append({'value': val, 'canvasX': cx, 'canvasY': cy})
            elif cx < y_frame['bounds']['centerX']:
                # Left of the Y-axis and within frame height: Y-axis label (canvas_y is the coord)
                axis_labels['y'].append({'value': val, 'canvasX': cx, 'canvasY': cy})

    output = {
        'canvas': {'width': canvas_w, 'height': canvas_h},
        'paths': paths,
        'labels': axis_labels,
    }
    paths_path = pdf_path.with_name(pdf_path.stem + '_paths.json')
    with open(str(paths_path), 'w') as f:
        json.dump(output, f, indent=2)

    counts = Counter(p['type'] for p in paths)
    print(f"Extracted: {paths_path}  ({len(paths)} paths total)")
    for t in ('tick', 'data', 'frame', 'other'):
        n = counts.get(t, 0)
        if n:
            ids = [p['id'] for p in paths if p['type'] == t][:10]
            suffix = '...' if n > 10 else ''
            print(f"  {t:6s}: {n:3d}  IDs: {ids}{suffix}")

    if not counts.get('tick', 0):
        print()
        yl = axis_labels['y']
        xl = axis_labels['x']
        if yl and xl:
            y_bot = min(yl, key=lambda l: l['canvasY'])
            y_top = max(yl, key=lambda l: l['canvasY'])
            x_lft = min(xl, key=lambda l: l['canvasX'])
            x_rgt = max(xl, key=lambda l: l['canvasX'])
            # Use frame path bounds for Y pixel positions: more precise than text label centers
            # (text centers can be ~1px off the true axis boundary due to font metrics)
            y_bot_px = round(canvas_h - (y_frame['bounds']['minY'] if y_frame else y_bot['canvasY']))
            y_top_px = round(canvas_h - (y_frame['bounds']['maxY'] if y_frame else y_top['canvasY']))
            print("Axis labels extracted from PDF geometry (use these as calibration anchors):")
            print(f"  --y-bottom @{y_bot_px}:{y_bot['value']:g}")
            print(f"  --y-top    @{y_top_px}:{y_top['value']:g}")
            print(f"  --x-left   @{round(x_lft['canvasX'])}:{x_lft['value']:g}")
            print(f"  --x-right  @{round(x_rgt['canvasX'])}:{x_rgt['value']:g}")
            print(f"  --data <id1> [<id2> ...]   (data path IDs: {[p['id'] for p in paths if p['type'] == 'data']})")
        else:
            print("Note: no tick paths found and axis labels could not be parsed from PDF text.")
            print("      Estimate calibration pixel positions from the rendered PNG.")



# ---------------------------------------------------------------------------
# export command
# ---------------------------------------------------------------------------

def resolve_anchor(spec, path_map, canvas_h, axis):
    """
    Resolve a calibration anchor to a canvas coordinate.

    Canvas coordinate system (paths JSON):
      X: 0 at left, increases rightward
      Y: 0 at bottom of page, increases upward

    Image pixel coordinate system (rendered PNG):
      X: same as canvas
      Y: 0 at top, increases downward  →  canvas_y = canvas_h - image_y
    """
    kind, coord, data_val = spec
    if kind == 'id':
        path = path_map[coord]
        canvas_coord = path['bounds']['centerX' if axis == 'x' else 'centerY']
    else:
        if axis == 'x':
            canvas_coord = coord
        else:
            canvas_coord = canvas_h - coord  # flip PNG Y to canvas Y
    return canvas_coord, data_val


def export_cmd(args):
    with open(args.paths_json) as f:
        data = json.load(f)

    if isinstance(data, list):  # legacy format
        paths = data
        canvas_h = max(p['bounds']['maxY'] for p in paths) if paths else 900.0
    else:
        paths = data['paths']
        canvas_h = data['canvas']['height']

    pm = {p['id']: p for p in paths}

    x_left_loc,   x_left_val   = resolve_anchor(args.x_left,   pm, canvas_h, 'x')
    x_right_loc,  x_right_val  = resolve_anchor(args.x_right,  pm, canvas_h, 'x')
    y_bottom_loc, y_bottom_val = resolve_anchor(args.y_bottom,  pm, canvas_h, 'y')
    y_top_loc,    y_top_val    = resolve_anchor(args.y_top,     pm, canvas_h, 'y')

    # Canvas Y=0 is at the bottom; the bottom tick should have a smaller Y than the top tick.
    # Swap both location and value together if the user supplied them in reverse order.
    if y_bottom_loc > y_top_loc:
        y_bottom_loc, y_top_loc = y_top_loc, y_bottom_loc
        y_bottom_val, y_top_val = y_top_val, y_bottom_val

    rows = []
    for line_num, path_id in enumerate(args.data, 1):
        for pt in pm[path_id]['points']:
            x_t = (pt['x'] - x_left_loc) / (x_right_loc - x_left_loc)
            y_t = (pt['y'] - y_bottom_loc) / (y_top_loc - y_bottom_loc)

            if args.x_log:
                x = 10 ** (math.log10(x_left_val) + x_t * (math.log10(x_right_val) - math.log10(x_left_val)))
            else:
                x = x_left_val + x_t * (x_right_val - x_left_val)

            if args.y_log:
                y = 10 ** (math.log10(y_bottom_val) + y_t * (math.log10(y_top_val) - math.log10(y_bottom_val)))
            else:
                y = y_bottom_val + y_t * (y_top_val - y_bottom_val)

            rows.append((line_num, x, y))

    rows.sort(key=lambda r: (r[0], r[1]))

    out = args.output or str(Path(args.paths_json).with_name(
        Path(args.paths_json).stem.replace('_paths', '') + '.csv'))
    with open(out, 'w') as f:
        f.write('series,x,y\n')
        for line, x, y in rows:
            f.write(f'{line},{x:.6g},{y:.6g}\n')

    print(f"\nExported {len(rows)} points → {out}")
    by_line = defaultdict(list)
    for line, x, y in rows:
        by_line[line].append((x, y))
    for line in sorted(by_line):
        pts = by_line[line]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        print(f"  Line {line}: {len(pts)} pts | x=[{min(xs):.4g}, {max(xs):.4g}] | y=[{min(ys):.4g}, {max(ys):.4g}]")

    _plot_extracted(out)


def _plot_extracted(csv_path):
    """Save a simple matplotlib line plot of the extracted CSV data."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Note: install matplotlib for a plot: pip install matplotlib")
        return

    by_line = defaultdict(lambda: {'x': [], 'y': []})
    with open(csv_path) as f:
        next(f)  # skip header
        for row in f:
            parts = row.strip().split(',')
            ln, x, y = int(parts[0]), float(parts[1]), float(parts[2])
            by_line[ln]['x'].append(x)
            by_line[ln]['y'].append(y)

    colors = ['#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9467bd']
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, ln in enumerate(sorted(by_line)):
        d = by_line[ln]
        ax.plot(d['x'], d['y'], color=colors[i % len(colors)], label=f'Line {ln}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    if len(by_line) > 1:
        ax.legend()
    plt.tight_layout()
    plot_path = Path(csv_path).with_suffix('.png')
    plt.savefig(str(plot_path), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Plot:       {plot_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_anchor(s):
    """Parse ID:VAL or @PIXEL:VAL into (kind, coord, data_val)."""
    if s.startswith('@'):
        parts = s[1:].split(':')
        if len(parts) != 2:
            raise argparse.ArgumentTypeError(f"Expected @PIXEL:VALUE, got '{s}'")
        return ('px', float(parts[0]), float(parts[1]))
    parts = s.split(':')
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"Expected ID:VALUE, got '{s}'")
    return ('id', int(parts[0]), float(parts[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='cmd', required=True)

    r = sub.add_parser('render', help='Render PDF and extract paths')
    r.add_argument('pdf', help='Path to PDF file')
    r.add_argument('--dpi', type=int, default=150, help='Render resolution (default 150)')

    e = sub.add_parser('export', help='Calibrate paths and export CSV')
    e.add_argument('paths_json', help='Path to *_paths.json from render step')
    e.add_argument('--x-left',   type=parse_anchor, required=True, metavar='ID:VAL|@PX:VAL')
    e.add_argument('--x-right',  type=parse_anchor, required=True, metavar='ID:VAL|@PX:VAL')
    e.add_argument('--y-bottom', type=parse_anchor, required=True, metavar='ID:VAL|@PX:VAL')
    e.add_argument('--y-top',    type=parse_anchor, required=True, metavar='ID:VAL|@PX:VAL')
    e.add_argument('--data', type=int, nargs='+', required=True, metavar='ID',
                   help='Path IDs of the data lines to extract')
    e.add_argument('--x-log', action='store_true', help='X-axis is logarithmic')
    e.add_argument('--y-log', action='store_true', help='Y-axis is logarithmic')
    e.add_argument('--output', metavar='CSV', help='Output CSV path (default: <stem>.csv)')

    args = parser.parse_args()
    if args.cmd == 'render':
        render_cmd(args)
    else:
        export_cmd(args)


if __name__ == '__main__':
    main()
