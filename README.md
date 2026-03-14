# Signals & Systems

Minimal developer blog for [blog.karthickshiva.dev](https://blog.karthickshiva.dev).

The public site stays static HTML, but the publishing flow is now generated from source posts so the design, feed, sitemap, and SEO tags do not drift out of sync.

## Structure

```text
.
├── about.html              # Hand-authored about page
├── build-site              # CLI: regenerate the public site
├── content/
│   ├── drafts/             # Unpublished source posts
│   └── posts/              # Published source posts
├── css/style.css           # Shared visual system
├── feed.xml                # Generated RSS feed
├── index.html              # Generated homepage
├── new-post                # CLI: create a draft
├── posts/                  # Generated public post pages
├── publish                 # CLI: publish a draft or republish an edit
├── robots.txt              # Generated robots file
├── scripts/blog_tools.py   # Build + publish automation
└── sitemap.xml             # Generated sitemap
```

## Publishing flow

### 1. Create a draft

```bash
./new-post "My Post Title"
```

This creates `content/drafts/my-post-title.html`, prompts for the summary and keywords if needed, and opens the draft in `$EDITOR`.

Available flags:

```bash
./new-post "Title" \
  --tag engineering \
  --desc "Search snippet and homepage summary." \
  --keywords "developer tooling, static sites, seo" \
  --date 2026-03-14 \
  --no-edit
```

### 2. Write the post body

Each source file begins with metadata:

```html
<!--
title: My Post Title
description: Search-friendly summary.
date: 2026-03-14
tag: engineering
keywords: developer tooling, static sites, seo
-->
```

Everything after that block is the post body HTML. Write normal semantic HTML:

```html
<p>Opening argument.</p>
<h2>Section heading</h2>
<p>More detail.</p>
<pre><code>const value = true;</code></pre>
<blockquote>A pull quote.</blockquote>
```

### 3. Build locally

```bash
./build-site
```

This regenerates:

- `index.html`
- `posts/*.html`
- `feed.xml`
- `sitemap.xml`
- `robots.txt`

It also runs lightweight SEO checks, including description length, keyword coverage, and placeholder-copy detection.

### 4. Publish

```bash
./publish my-post-title
```

If the slug points to a draft, `publish` moves it from `content/drafts` to `content/posts`, rebuilds the site, stages the generated artifacts, commits, and pushes.

Without an argument:

```bash
./publish
```

The command lists drafts and modified published source posts, then prompts for a selection.

## SEO automation

Post metadata is the single source of truth for SEO. The build step generates:

- canonical URLs
- meta descriptions
- Open Graph tags
- Twitter summary tags
- JSON-LD `Blog` / `BlogPosting` schema
- RSS entries
- sitemap URLs and `lastmod`
- `robots.txt` sitemap reference

This avoids the previous manual flow where post pages, the homepage JSON-LD, `feed.xml`, and `sitemap.xml` could diverge.

## Notes

- The generated site remains framework-free and deploys directly from the repo root on GitHub Pages.
- The `posts/` directory is build output. Edit source posts in `content/posts/` or `content/drafts/` instead.
