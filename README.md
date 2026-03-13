# karthickshiva.dev — Blog

A minimal, no-framework blog. Pure HTML and CSS. No build step, no Node.js.

Live at: [blog.karthickshiva.dev](https://blog.karthickshiva.dev)

---

## Structure

```
.
├── index.html          # Homepage — post list
├── about.html          # About page
├── new-post            # CLI: create a post
├── publish             # CLI: publish a created post
├── CNAME               # Custom domain for GitHub Pages
├── css/
│   └── style.css       # All styles
└── posts/
    └── my-post.html    # One file per post
```

No build tools. GitHub Pages serves the static files directly from `main`.

---

## Workflow

Creating and publishing are intentionally separate steps.

### Step 1 — Create

```bash
./new-post "My Post Title"
```

This will:
1. Prompt you for a one-line summary (or pass `--desc`)
2. Create `posts/my-post-title.html` pre-filled with the post template
3. Update `index.html` with the new entry
4. Open the file in `$EDITOR` so you can write the content

The post stays local until you explicitly publish it.

### Step 2 — Write

Edit `posts/<slug>.html`. Replace everything inside `<div class="post-content">` with your post. Available elements:

```html
<p>Paragraph text.</p>
<h2>Section heading</h2>
<h3>Sub-heading</h3>
<ul><li>List item</li></ul>
<strong>Bold</strong>
<code>inline code</code>
<pre><code>// fenced code block</code></pre>
<blockquote>Pull quote.</blockquote>
<a href="https://...">Link</a>
```

### Step 3 — Publish

When ready:

```bash
./publish                    # shows unpublished posts, prompts to pick
./publish my-post-title      # publish directly by slug
```

This does `git add`, `git commit`, and `git push` in one step.

---

### `new-post` options

```bash
./new-post "Title" [--tag TAG] [--desc "Summary"] [--date YYYY-MM-DD] [--no-edit]
```

| Flag | Default | Description |
|---|---|---|
| `--tag` | `tech` | Category label shown on the index |
| `--desc` | prompted | One-line summary shown on the index page |
| `--date` | today | Post date as `YYYY-MM-DD` |
| `--no-edit` | off | Skip opening the file in `$EDITOR` |

```bash
# Create with all details upfront, skip editor for now
./new-post "DeepSeek R2 and the Open-Source Shift" \
  --tag tech \
  --desc "DeepSeek's R2 model challenges the closed-source incumbents." \
  --no-edit

# Backdate a post
./new-post "Retrospective: 2025 in Review" --date 2025-12-31 --tag tech
```

### `publish` options

```bash
./publish                        # interactive — lists unpublished posts
./publish my-post-slug           # by slug
./publish posts/my-post.html     # by file path
```

---

## Styling

All colours are CSS custom properties in `css/style.css`:

```css
:root {
  --bg: #0f0f0f;          /* page background */
  --bg-surface: #161616;  /* code block background */
  --border: #2a2a2a;      /* dividers */
  --text: #e0e0e0;        /* body text */
  --text-muted: #777;     /* dates, nav links */
  --accent: #00d4aa;      /* links, tags, highlights */
}
```

Change `--accent` to retheme the entire site in one edit.

---

## GitHub Pages setup

1. **Settings → Pages → Source**: `Deploy from a branch`
2. **Branch**: `main`, folder `/` (root)
3. **Custom domain**: `blog.karthickshiva.dev` — the `CNAME` file handles DNS

---

## Design decisions

- No JavaScript — works with JS disabled
- No external fonts — system font stack, instant load
- No analytics or tracking
- Single CSS file — easy to audit and override
- Dark theme only — tweak `--bg` / `--text` vars for light mode
