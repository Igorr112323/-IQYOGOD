#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рендер схем в PNG без внешних сервисов:
 1) мини-рендерер рукописных SVG (rect/text/line/path/circle/ellipse/polyline/polygon);
 2) рендер Mermaid flowchart TB (узлы []/{}, подграфы, метки рёбер).
"""
import math, re, sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, int(size))

NAMED = {"white": "#ffffff", "black": "#000000", "red": "#ff0000",
         "green": "#008000", "blue": "#0000ff", "none": None}

def color(v, default=None):
    if v is None:
        return default
    v = v.strip()
    if v in NAMED:
        return NAMED[v]
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return "#" + h[:6]
    return default

def with_alpha(hexc, opacity):
    if hexc is None or opacity >= 1.0:
        return hexc
    r = int(hexc[1:3], 16); g = int(hexc[3:5], 16); b = int(hexc[5:7], 16)
    return (r, g, b, int(opacity * 255))

# ---------------------------------------------------------------- SVG render

def _f(v, d=0.0):
    try:
        return float(v)
    except Exception:
        return d

def parse_path(d):
    """Возвращает список полилиний (списки точек); замыкание помечается флагом."""
    subs = []
    cur = []
    closed = []
    toks = re.findall(r"[a-zA-Z]|-?\d*\.?\d+(?:[eE][-+]?\d+)?", d)
    i = 0
    cmd = None
    start = (0, 0)
    pos = (0, 0)

    def nums(n):
        nonlocal i
        out = []
        for _ in range(n):
            out.append(float(toks[i])); i += 1
        return out

    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]; i += 1
            if cmd in "Mm":
                x, y = nums(2)
                if cmd == "m" and cur:
                    x += pos[0]; y += pos[1]
                elif cmd == "m":
                    pass
                pos = (x, y); start = (x, y)
                if cur:
                    subs.append(cur); closed.append(False)
                cur = [(x, y)]
                cmd = "L" if cmd == "M" else "l"
                continue
        if cmd is None:
            i += 1
            continue
        c = cmd
        if c in "Ll":
            x, y = nums(2)
            if c == "l":
                x += pos[0]; y += pos[1]
            pos = (x, y); cur.append(pos)
        elif c in "Hh":
            (x,) = nums(1)
            if c == "h":
                x += pos[0]
            pos = (x, pos[1]); cur.append(pos)
        elif c in "Vv":
            (y,) = nums(1)
            if c == "v":
                y += pos[1]
            pos = (pos[0], y); cur.append(pos)
        elif c in "Qq":
            x1, y1, x, y = nums(4)
            if c == "q":
                x1 += pos[0]; y1 += pos[1]; x += pos[0]; y += pos[1]
            for t in [k / 16 for k in range(1, 17)]:
                bx = (1 - t) ** 2 * pos[0] + 2 * (1 - t) * t * x1 + t * t * x
                by = (1 - t) ** 2 * pos[1] + 2 * (1 - t) * t * y1 + t * t * y
                cur.append((bx, by))
            pos = (x, y)
        elif c in "Cc":
            x1, y1, x2, y2, x, y = nums(6)
            if c == "c":
                x1 += pos[0]; y1 += pos[1]; x2 += pos[0]; y2 += pos[1]; x += pos[0]; y += pos[1]
            for t in [k / 20 for k in range(1, 21)]:
                bx = ((1 - t) ** 3 * pos[0] + 3 * (1 - t) ** 2 * t * x1 +
                      3 * (1 - t) * t * t * x2 + t ** 3 * x)
                by = ((1 - t) ** 3 * pos[1] + 3 * (1 - t) ** 2 * t * y1 +
                      3 * (1 - t) * t * t * y2 + t ** 3 * y)
                cur.append((bx, by))
            pos = (x, y)
        elif c in "Aa":
            rx, ry, rot, laf, sf, x, y = nums(7)
            if c == "a":
                x += pos[0]; y += pos[1]
            cur.extend(arc_points(pos, (x, y), rx, ry, rot, int(laf), int(sf)))
            pos = (x, y)
        elif c in "Zz":
            cur.append(start); pos = start
            subs.append(cur); closed.append(True); cur = []
        else:
            i += 1
    if cur:
        subs.append(cur); closed.append(False)
    return list(zip(subs, closed))

def arc_points(p0, p1, rx, ry, rot_deg, laf, sf):
    if rx == 0 or ry == 0:
        return [p1]
    rot = math.radians(rot_deg)
    x1, y1 = p0; x2, y2 = p1
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    cx_, cy_ = math.cos(rot) * dx - math.sin(rot) * dy, math.sin(rot) * dx + math.cos(rot) * dy
    rx, ry = abs(rx), abs(ry)
    lam = (cx_ / rx) ** 2 + (cy_ / ry) ** 2
    if lam > 1:
        s = math.sqrt(lam); rx *= s; ry *= s
    sign = -1 if laf == sf else 1
    num = rx ** 2 * ry ** 2 - rx ** 2 * cy_ ** 2 - ry ** 2 * cx_ ** 2
    den = rx ** 2 * cy_ ** 2 + ry ** 2 * cx_ ** 2
    coef = sign * math.sqrt(max(num / den, 0))
    cx, cy = coef * rx * cy_ / ry, -coef * ry * cx_ / rx
    cX = math.cos(rot) * cx - math.sin(rot) * cy + (x1 + x2) / 2
    cY = math.sin(rot) * cx + math.cos(rot) * cy + (y1 + y2) / 2

    def ang(ux, uy, vx, vy):
        d = ux * vx + uy * vy
        n = math.sqrt(ux * ux + uy * uy) * math.sqrt(vx * vx + vy * vy)
        c = max(-1, min(1, d / n))
        a = math.acos(c)
        return a if (ux * vy - uy * vx) >= 0 else -a

    th1 = ang(1, 0, (cx_ - cx) / rx, (cy_ - cy) / ry)
    dth = ang((cx_ - cx) / rx, (cy_ - cy) / ry, (-cx_ - cx) / rx, (-cy_ - cy) / ry)
    if sf == 0 and dth > 0:
        dth -= 2 * math.pi
    elif sf == 1 and dth < 0:
        dth += 2 * math.pi
    pts = []
    for k in range(1, 25):
        th = th1 + dth * k / 24
        X = cX + rx * math.cos(th) * math.cos(rot) - ry * math.sin(th) * math.sin(rot)
        Y = cY + rx * math.cos(th) * math.sin(rot) + ry * math.sin(th) * math.cos(rot)
        pts.append((X, Y))
    pts[-1] = (x2, y2)
    return pts

def dashed_segments(p0, p1, pattern, width):
    segs = []
    x0, y0 = p0; x1, y1 = p1
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0 or not pattern:
        return [(p0, p1)]
    d = 0.0; on = True; k = 0
    total = sum(pattern) or 1
    while d < L:
        step = pattern[k % len(pattern)]
        if step <= 0:
            step = 1
        d2 = min(d + step, L)
        if on:
            segs.append(((x0 + (x1 - x0) * d / L, y0 + (y1 - y0) * d / L),
                         (x0 + (x1 - x0) * d2 / L, y0 + (y1 - y0) * d2 / L)))
        d = d2; on = not on; k += 1
    return segs

def local(el):
    return el.tag.split("}")[-1]

def render_svg(path_in, path_out, scale=2.0):
    root = ET.parse(path_in).getroot()
    W = _f(root.get("width"), 800); H = _f(root.get("height"), 500)
    vb = root.get("viewBox")
    if vb:
        parts = vb.split()
        W, H = float(parts[2]), float(parts[3])
    S = scale
    img = Image.new("RGB", (int(W * S), int(H * S)), "white")
    dr = ImageDraw.Draw(img, "RGBA")

    def sx(x): return x * S
    def sy(y): return y * S

    def arrow(p_prev, p_end, clr, wpx):
        x0, y0 = p_prev; x1, y1 = p_end
        ang = math.atan2(y1 - y0, x1 - x0)
        L = 9 * (wpx / 2 + 0.6)
        pA = (x1 - L * math.cos(ang - 0.42), y1 - L * math.sin(ang - 0.42))
        pB = (x1 - L * math.cos(ang + 0.42), y1 - L * math.sin(ang + 0.42))
        dr.polygon([(sx(x1), sy(y1)), (sx(pA[0]), sy(pA[1])), (sx(pB[0]), sy(pB[1]))],
                   fill=clr if isinstance(clr, str) else clr)

    def stroke_polyline(pts, clr, w, dash, arrowed):
        if clr is None or len(pts) < 2:
            return
        wpx = max(w * S, 1)
        for a, b in zip(pts, pts[1:]):
            segs = dashed_segments(a, b, dash, w) if dash else [(a, b)]
            for p, q in segs:
                dr.line([(sx(p[0]), sy(p[1])), (sx(q[0]), sy(q[1]))], fill=clr, width=int(wpx))
        if arrowed:
            arrow(pts[-2], pts[-1], clr, w)

    def draw_el(el, inh):
        tag = local(el)
        st = dict(inh)
        for k in ("fill", "stroke", "stroke-width", "opacity", "font-size", "font-weight"):
            if el.get(k) is not None:
                st[k] = el.get(k)
        op = float(st.get("opacity", 1) or 1)
        fill = color(el.get("fill", st.get("fill")), default=None) if (el.get("fill") or st.get("fill")) else None
        if fill is None and tag in ("rect", "circle", "ellipse", "polygon") and el.get("fill") != "none" and st.get("fill") != "none":
            fill = "#000000"
        stroke = color(el.get("stroke", st.get("stroke")))
        sw = _f(el.get("stroke-width", st.get("stroke-width", 1)), 1)
        dash = el.get("stroke-dasharray")
        dash = [_f(x) for x in dash.replace(",", " ").split()] if dash else None
        arrowed = el.get("marker-end") is not None

        if tag == "g":
            for ch in el:
                draw_el(ch, st)
        elif tag == "rect":
            x, y = _f(el.get("x")), _f(el.get("y"))
            w, h = _f(el.get("width")), _f(el.get("height"))
            r = _f(el.get("rx"))
            fc = with_alpha(fill, op) if fill else None
            sc = with_alpha(stroke, op) if stroke else None
            box = [sx(x), sy(y), sx(x + w), sy(y + h)]
            if r > 0:
                if fc:
                    dr.rounded_rectangle(box, radius=r * S, fill=fc)
                if sc:
                    dr.rounded_rectangle(box, radius=r * S, outline=sc, width=max(int(sw * S), 1))
            else:
                if fc:
                    dr.rectangle(box, fill=fc)
                if sc:
                    dr.rectangle(box, outline=sc, width=max(int(sw * S), 1))
        elif tag in ("circle", "ellipse"):
            cx, cy = _f(el.get("cx")), _f(el.get("cy"))
            rx = _f(el.get("r", el.get("rx"))); ry = _f(el.get("ry", el.get("r")))
            box = [sx(cx - rx), sy(cy - ry), sx(cx + rx), sy(cy + ry)]
            if fill:
                dr.ellipse(box, fill=with_alpha(fill, op))
            if stroke:
                dr.ellipse(box, outline=with_alpha(stroke, op), width=max(int(sw * S), 1))
        elif tag == "line":
            pts = [(_f(el.get("x1")), _f(el.get("y1"))), (_f(el.get("x2")), _f(el.get("y2")))]
            stroke_polyline(pts, with_alpha(stroke, op) if stroke else None, sw, dash, arrowed)
        elif tag in ("polyline", "polygon"):
            nums = [_f(v) for v in el.get("points", "").replace(",", " ").split()]
            pts = list(zip(nums[0::2], nums[1::2]))
            if tag == "polygon" and pts:
                if fill:
                    dr.polygon([(sx(x), sy(y)) for x, y in pts], fill=with_alpha(fill, op))
                pts2 = pts + [pts[0]]
                stroke_polyline(pts2, with_alpha(stroke, op) if stroke else None, sw, dash, False)
            else:
                stroke_polyline(pts, with_alpha(stroke, op) if stroke else None, sw, dash, arrowed)
        elif tag == "path":
            fcol = color(el.get("fill", "none"))
            if el.get("fill") is None:
                fcol = None if st.get("fill") == "none" else color(st.get("fill"))
            for pl, closed in parse_path(el.get("d", "")):
                if closed and fcol:
                    dr.polygon([(sx(x), sy(y)) for x, y in pl], fill=with_alpha(fcol, op))
                stroke_polyline(pl, with_alpha(stroke, op) if stroke else None, sw, dash, arrowed)
        elif tag == "text":
            txt = "".join(el.itertext()).strip()
            if not txt:
                return
            fs = _f(st.get("font-size", 13), 13)
            bold = st.get("font-weight") == "bold"
            fnt = font(fs * S, bold)
            x, y = _f(el.get("x")), _f(el.get("y"))
            anchor = el.get("text-anchor", "start")
            tr = el.get("transform", "")
            bbox = dr.textbbox((0, 0), txt, font=fnt)
            tw = bbox[2] - bbox[0]; th = bbox[3] - bbox[1]
            if anchor == "middle":
                tx = sx(x) - tw / 2
            elif anchor == "end":
                tx = sx(x) - tw
            else:
                tx = sx(x)
            ty = sy(y) - th - bbox[1]
            fcol = with_alpha(color(el.get("fill", st.get("fill", "#000000")), "#000000"), op)
            m = re.search(r"rotate\(\s*(-?[\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\)", tr)
            if m:
                ang = -float(m.group(1))
                tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
                td = ImageDraw.Draw(tmp)
                td.text((tx, ty), txt, font=fnt, fill=fcol)
                tmp = tmp.rotate(ang, resample=Image.BICUBIC,
                                 center=(sx(float(m.group(2))), sy(float(m.group(3)))))
                img.paste(tmp, (0, 0), tmp)
            else:
                dr.text((tx, ty), txt, font=fnt, fill=fcol)

    for ch in root:
        if local(ch) in ("defs",):
            continue
        draw_el(ch, {})
    img.save(path_out)

# ------------------------------------------------------------ Mermaid render

def parse_mermaid(src):
    nodes = {}      # id -> {"label": str, "shape": "box|diamond|round"}
    order = []
    edges = []      # (src, dst, label)
    subgraphs = []  # {"label": str, "members": [ids]}
    stack = []
    for raw in src.splitlines():
        line = raw.strip()
        if not line or line.startswith("flowchart") or line.startswith("graph"):
            continue
        m = re.match(r"subgraph\s+\w+\s*\[(.*)\]\s*$", line)
        if m:
            stack.append({"label": m.group(1).strip().strip('"'), "members": []})
            continue
        if line == "end" and stack:
            subgraphs.append(stack.pop())
            continue
        # пунктирные рёбра -. … .-> приводим к -->|…|
        dashed = bool(re.search(r"-\..*?\.->", line))
        if dashed:
            line = re.sub(r"-\.(.*?)\.->",
                          lambda m: ("-->|" + m.group(1).strip() + "|")
                          if m.group(1).strip() else "-->", line)
        # цепочка рёбер:  A[..] -->|l| B[..] --> C[..]
        parts = re.split(r"(-->\|[^|]*\|)|(-->+)", line)
        items, labels, chain = [], [], []
        for p in parts:
            if p is None:
                continue
            if p.startswith("-->"):
                lab = re.sub(r"^--+>?\s*\|?", "", p).rstrip("|").strip().strip('"')
                labels.append(lab)
            else:
                p = p.strip()
                if p:
                    items.append(p)
        for it in items:
            nm = re.match(r"(\w+)\s*(\[(.*)\]|\{(.*)\}|\((.*)\))\s*$", it)
            if nm:
                nid = nm.group(1)
                if nm.group(3) is not None:
                    label, shape = nm.group(3), "box"
                elif nm.group(4) is not None:
                    label, shape = nm.group(4), "diamond"
                else:
                    label, shape = nm.group(5), "round"
                label = label.strip().strip('"')
                if nid not in nodes:
                    nodes[nid] = {"label": label, "shape": shape}
                    order.append(nid)
                else:
                    nodes[nid]["label"] = label
                chain.append(nid)
            else:
                nid = it.split("[")[0].split("{")[0].split("(")[0].strip()
                if nid:
                    if nid not in nodes:
                        nodes[nid] = {"label": nid, "shape": "box"}
                        order.append(nid)
                    chain.append(nid)
        for i in range(len(chain) - 1):
            lab = labels[i] if i < len(labels) else ""
            edges.append((chain[i], chain[i + 1], lab, dashed))
        if stack:
            for nid in chain:
                if nid not in stack[-1]["members"]:
                    stack[-1]["members"].append(nid)
    while stack:
        subgraphs.append(stack.pop())
    return nodes, order, edges, subgraphs

def wrap(text, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines or [""]

def render_mermaid(src, path_out, title=None):
    nodes, order, edges, subgraphs = parse_mermaid(src)
    if not nodes:
        return False
    lr = bool(re.search(r"^\s*(?:flowchart|graph)\s+LR", src, re.M))
    succ = {n: [] for n in nodes}
    pred = {n: [] for n in nodes}
    for a, b, *_ in edges:
        if b not in succ[a]:
            succ[a].append(b)
        if a not in pred[b]:
            pred[b].append(a)
    # ранги: самый длинный путь (с защитой от циклов)
    rank = {}
    def calc(n, seen):
        if n in rank:
            return rank[n]
        if n in seen:
            return 0
        seen = seen | {n}
        r = 0
        for p in pred[n]:
            r = max(r, calc(p, seen) + 1)
        rank[n] = r
        return r
    for n in order:
        calc(n, set())
    levels = {}
    for n, r in rank.items():
        levels.setdefault(r, []).append(n)
    maxr = max(levels)
    # упорядочивание по барицентру
    pos_in_level = {}
    for r in range(maxr + 1):
        pos_in_level.update({n: i for i, n in enumerate(levels[r])})
    for _ in range(4):
        for r in range(1, maxr + 1):
            def bar(n):
                ps = [pos_in_level[p] for p in pred[n] if p in pos_in_level]
                return (sum(ps) / len(ps)) if ps else pos_in_level[n]
            levels[r].sort(key=lambda n: (bar(n), pos_in_level[n]))
            pos_in_level.update({n: i for i, n in enumerate(levels[r])})
        for r in range(maxr - 1, -1, -1):
            def bar2(n):
                ss = [pos_in_level[s] for s in succ[n] if s in pos_in_level]
                return (sum(ss) / len(ss)) if ss else pos_in_level[n]
            levels[r].sort(key=lambda n: (bar2(n), pos_in_level[n]))
            pos_in_level.update({n: i for i, n in enumerate(levels[r])})

    F = font(26); FL = font(22)  # узлы / метки рёбер (канва 2x)
    dummy = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    def text_w(s, f=F):
        b = dummy.textbbox((0, 0), s, font=f)
        return b[2] - b[0]

    geom = {}
    for n in order:
        nd = nodes[n]
        lines = wrap(nd["label"], 26)
        w = max(text_w(l) for l in lines) + 44
        h = len(lines) * 34 + 26
        if nd["shape"] == "diamond":
            w = int(w * 1.45) + 26
            h = int(h * 1.5)
        geom[n] = {"lines": lines, "w": w, "h": h}

    def csize(n):  # размер вдоль поперечной оси
        return geom[n]["w"] if not lr else geom[n]["h"]
    def fsize(n):  # размер вдоль оси потока
        return geom[n]["h"] if not lr else geom[n]["w"]
    W = 1000
    TOP = 70
    # протяжённость поперечной оси по самой «толстой» строке
    for r in range(maxr + 1):
        need = sum(csize(n) for n in levels[r]) + 70 * (len(levels[r]) + 1)
        W = max(W, need)
    level_f = {}
    y = TOP
    for r in range(maxr + 1):
        hh = max(fsize(n) for n in levels[r])
        level_f[r] = y
        y += hh + (150 if lr else 90)
    center = {}
    for r in range(maxr + 1):
        row = levels[r]
        sizes = [csize(n) for n in row]
        total = sum(sizes)
        gap = (W - total) / (len(row) + 1)
        c = gap
        for n, s in zip(row, sizes):
            fc = level_f[r] + fsize(n) / 2
            cc = c + s / 2
            center[n] = (cc, fc) if not lr else (fc, cc)
            c += s + gap

    img_w = int(y + 80) if lr else int(W)
    img_h = int(W + 40) if lr else int(y + 40)
    img = Image.new("RGB", (img_w, img_h), "white")
    dr = ImageDraw.Draw(img, "RGBA")

    # подграфы
    sg_of = {}
    for sg in subgraphs:
        for m in sg["members"]:
            sg_of[m] = sg
    for sg in subgraphs:
        xs = [center[m][0] - geom[m]["w"] / 2 for m in sg["members"]]
        xe = [center[m][0] + geom[m]["w"] / 2 for m in sg["members"]]
        ys = [center[m][1] - geom[m]["h"] / 2 for m in sg["members"]]
        ye = [center[m][1] + geom[m]["h"] / 2 for m in sg["members"]]
        box = [min(xs) - 30, min(ys) - 46, max(xe) + 30, max(ye) + 30]
        sg["box"] = box
        dr.rounded_rectangle(box, radius=14, fill=(238, 243, 248, 255),
                             outline=(90, 110, 130), width=2)
        dr.text((box[0] + 16, box[1] + 8), sg["label"], font=font(22, True),
                fill=(50, 70, 90))

    # рёбра
    EC = (70, 90, 110)

    def seg(u, v, dashed):
        if not dashed:
            dr.line([u, v], fill=EC, width=3)
            return
        dx, dy = v[0] - u[0], v[1] - u[1]
        L = math.hypot(dx, dy)
        if L < 1:
            return
        t = 0.0
        while t < L:
            t1 = min(t + 10, L)
            dr.line([(u[0] + dx * t / L, u[1] + dy * t / L),
                     (u[0] + dx * t1 / L, u[1] + dy * t1 / L)], fill=EC, width=3)
            t += 17

    for a, b, lab, *rest in edges:
        dashed = bool(rest) and rest[0]
        x1, y1 = center[a]; x2, y2 = center[b]
        if rank[b] > rank[a]:
            if not lr:
                p0 = (x1, y1 + geom[a]["h"] / 2)
                p1 = (x2, y2 - geom[b]["h"] / 2)
            else:
                p0 = (x1 + geom[a]["w"] / 2, y1)
                p1 = (x2 - geom[b]["w"] / 2, y2)
        else:
            if not lr:
                side = 1 if x2 >= x1 else -1
                p0 = (x1 + side * geom[a]["w"] / 2, y1)
                p1 = (x2 - side * geom[b]["w"] / 2, y2)
            else:
                side = 1 if y2 >= y1 else -1
                p0 = (x1, y1 + side * geom[a]["h"] / 2)
                p1 = (x2, y2 - side * geom[b]["h"] / 2)
        if not lr:
            if abs(p1[0] - p0[0]) < 6:
                pts = [p0, p1]
            else:
                midy = (p0[1] + p1[1]) / 2
                pts = [p0, (p0[0], midy), (p1[0], midy), p1]
        else:
            if abs(p1[1] - p0[1]) < 6:
                pts = [p0, p1]
            else:
                midx = (p0[0] + p1[0]) / 2
                pts = [p0, (midx, p0[1]), (midx, p1[1]), p1]
        for u, v in zip(pts, pts[1:]):
            seg(u, v, dashed)
        ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
        L = 14
        q = pts[-1]
        dr.polygon([q,
                    (q[0] - L * math.cos(ang - 0.45), q[1] - L * math.sin(ang - 0.45)),
                    (q[0] - L * math.cos(ang + 0.45), q[1] - L * math.sin(ang + 0.45))],
                   fill=EC)
        if lab:
            if not lr:
                mx = (pts[1][0] if len(pts) > 2 else (p0[0] + p1[0]) / 2) + 8
                my = (pts[1][1] if len(pts) > 2 else (p0[1] + p1[1]) / 2) - 4
            else:
                mx = (pts[1][0] if len(pts) > 2 else (p0[0] + p1[0]) / 2) + 6
                my = (p0[1] if len(pts) > 2 else (p0[1] + p1[1]) / 2) - 30
            for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2)):
                dr.text((mx + dx, my + dy), lab, font=FL, fill="white")
            dr.text((mx, my), lab, font=FL, fill=(120, 40, 40))

    # узлы
    palette = {"box": ((223, 231, 238), (51, 71, 91)),
               "round": ((214, 233, 248), (30, 90, 140)),
               "diamond": ((250, 236, 205), (140, 100, 20))}
    for n in order:
        cx, cy = center[n]
        w, h = geom[n]["w"], geom[n]["h"]
        fc, oc = palette[nodes[n]["shape"]]
        if nodes[n]["shape"] == "diamond":
            pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
            dr.polygon(pts, fill=fc, outline=oc, width=3)
        elif nodes[n]["shape"] == "round":
            dr.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                                 radius=h / 2, fill=fc, outline=oc, width=3)
        else:
            dr.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                                 radius=12, fill=fc, outline=oc, width=3)
        ty = cy - len(geom[n]["lines"]) * 34 / 2
        for l in geom[n]["lines"]:
            tw = text_w(l)
            dr.text((cx - tw / 2, ty), l, font=F, fill=(20, 30, 40))
            ty += 34
    img.save(path_out)
    return True

if __name__ == "__main__":
    if sys.argv[1] == "svg":
        render_svg(sys.argv[2], sys.argv[3])
    else:
        src = open(sys.argv[2], encoding="utf-8").read()
        render_mermaid(src, sys.argv[3])
