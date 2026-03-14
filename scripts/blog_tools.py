#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DRAFTS_DIR = CONTENT_DIR / "drafts"
SOURCE_POSTS_DIR = CONTENT_DIR / "posts"
OUTPUT_POSTS_DIR = ROOT / "posts"
INDEX_PATH = ROOT / "index.html"
FEED_PATH = ROOT / "feed.xml"
SITEMAP_PATH = ROOT / "sitemap.xml"
ROBOTS_PATH = ROOT / "robots.txt"

SITE_NAME = "Signals & Systems"
SITE_URL = "https://blog.karthickshiva.dev"
SITE_AUTHOR = "Karthick Shiva"
SITE_TAGLINE = "Minimal notes on AI systems, software engineering, and the math underneath."
SITE_DESCRIPTION = "Essays on AI systems, software engineering, and mathematical thinking. Static HTML, RSS-first, and SEO-generated."
AUTHOR_BIO = (
    "Engineer working across AI systems, software architecture, and the mathematical "
    "ideas that make both legible."
)
AUTHOR_GITHUB = "https://github.com/karthickshiva"

META_PATTERN = re.compile(r"^\s*<!--\s*\n(.*?)\n-->\s*", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")
PLACEHOLDER_MARKERS = (
    "Lead paragraph.",
    "Develop the argument.",
    "Section heading",
    "Key point.",
)


@dataclass
class Post:
    source_path: Path
    slug: str
    title: str
    description: str
    post_date: date
    tag: str
    keywords: list[str]
    body_html: str
    url_path: str
    canonical_url: str
    reading_time_minutes: int
    word_count: int
    warnings: list[str]


def slugify(title: str) -> str:
    value = title.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def month_day_year(value: date) -> str:
    return value.strftime("%b %d, %Y").replace(" 0", " ")


def xml_escape(value: str) -> str:
    return html.escape(value, quote=True)


def strip_tags(value: str) -> str:
    without_tags = TAG_PATTERN.sub(" ", value)
    return WHITESPACE_PATTERN.sub(" ", html.unescape(without_tags)).strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def open_in_editor(path: Path) -> None:
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vi"
    subprocess.run([editor, str(path)], check=False)


def parse_front_matter(path: Path) -> tuple[dict[str, str], str]:
    text = read_text(path)
    match = META_PATTERN.match(text)
    if not match:
        raise ValueError(f"{path.relative_to(ROOT)} is missing the metadata comment block at the top.")

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        if ":" not in raw:
            raise ValueError(f"{path.relative_to(ROOT)} has an invalid metadata line: {raw}")
        key, value = raw.split(":", 1)
        metadata[key.strip()] = value.strip()

    body_html = text[match.end():].strip()
    if not body_html:
        raise ValueError(f"{path.relative_to(ROOT)} has no body content after the metadata block.")
    return metadata, body_html


def validate_metadata(path: Path, metadata: dict[str, str], body_html: str) -> Post:
    required = ("title", "description", "date", "tag", "keywords")
    missing = [key for key in required if not metadata.get(key)]
    if missing:
        raise ValueError(f"{path.relative_to(ROOT)} is missing required fields: {', '.join(missing)}")

    slug = path.stem
    try:
        post_date = datetime.strptime(metadata["date"], "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{path.relative_to(ROOT)} has an invalid date '{metadata['date']}'.") from exc

    keywords = [item.strip() for item in metadata["keywords"].split(",") if item.strip()]
    if not keywords:
        raise ValueError(f"{path.relative_to(ROOT)} must include at least one keyword.")

    plain_text = strip_tags(body_html)
    word_count = len(plain_text.split())
    reading_time_minutes = max(1, math.ceil(word_count / 220)) if word_count else 1

    warnings: list[str] = []
    description = metadata["description"]
    title = metadata["title"]
    if len(description) < 50 or len(description) > 160:
        warnings.append(
            f"{path.relative_to(ROOT)} description is {len(description)} characters; aim for 50-160 for search snippets."
        )
    if len(title) > 70:
        warnings.append(f"{path.relative_to(ROOT)} title is {len(title)} characters; SERP truncation is likely.")
    if len(keywords) < 2:
        warnings.append(f"{path.relative_to(ROOT)} only has one keyword; add a few precise topical terms.")
    if word_count < 120:
        warnings.append(f"{path.relative_to(ROOT)} is only {word_count} words; thin content is harder to rank.")
    if any(marker in body_html for marker in PLACEHOLDER_MARKERS):
        raise ValueError(f"{path.relative_to(ROOT)} still contains placeholder copy.")

    return Post(
        source_path=path,
        slug=slug,
        title=title,
        description=description,
        post_date=post_date,
        tag=metadata["tag"],
        keywords=keywords,
        body_html=body_html,
        url_path=f"/posts/{slug}.html",
        canonical_url=f"{SITE_URL}/posts/{slug}.html",
        reading_time_minutes=reading_time_minutes,
        word_count=word_count,
        warnings=warnings,
    )


def load_published_posts() -> list[Post]:
    posts: list[Post] = []
    warnings: list[str] = []

    for path in sorted(SOURCE_POSTS_DIR.glob("*.html")):
        metadata, body_html = parse_front_matter(path)
        post = validate_metadata(path, metadata, body_html)
        posts.append(post)
        warnings.extend(post.warnings)

    posts.sort(key=lambda post: (post.post_date.isoformat(), post.slug), reverse=True)

    if warnings:
        print("SEO warnings:", file=sys.stderr)
        for warning in warnings:
            print(f"  - {warning}", file=sys.stderr)
        print("", file=sys.stderr)

    return posts


def render_header(current: str) -> str:
    posts_current = ' aria-current="page"' if current == "posts" else ""
    about_current = ' aria-current="page"' if current == "about" else ""
    return f"""<header class="site-header">
    <div class="site-shell">
      <a href="/" class="brand">
        <span class="brand-mark">KS</span>
        <span class="brand-copy">
          <strong>{SITE_NAME}</strong>
          <span>{SITE_TAGLINE}</span>
        </span>
      </a>
      <nav class="site-nav" aria-label="Primary">
        <a href="/"{posts_current}>posts</a>
        <a href="/about.html"{about_current}>about</a>
        <a href="/feed.xml">rss</a>
      </nav>
    </div>
  </header>"""


def render_footer() -> str:
    return f"""<footer class="site-footer">
    <div class="site-shell footer-grid">
      <p>{SITE_NAME}</p>
      <p>Static HTML. Generated metadata. No JavaScript runtime.</p>
    </div>
  </footer>"""


def render_page(
    *,
    title: str,
    description: str,
    canonical_path: str,
    body_class: str,
    current_nav: str,
    og_type: str,
    og_title: str,
    extra_head: str,
    main_html: str,
    schema_data: dict,
) -> str:
    canonical_url = f"{SITE_URL}{canonical_path}"
    schema_json = json.dumps(schema_data, ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{xml_escape(description)}">
  <meta name="author" content="{xml_escape(SITE_AUTHOR)}">
  <meta name="robots" content="index,follow">
  <title>{xml_escape(title)}</title>
  <link rel="canonical" href="{xml_escape(canonical_url)}">
  <link rel="alternate" type="application/rss+xml" title="{xml_escape(SITE_NAME)}" href="{SITE_URL}/feed.xml">
  <link rel="stylesheet" href="/css/style.css">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{xml_escape(SITE_NAME)}">
  <meta property="og:title" content="{xml_escape(og_title)}">
  <meta property="og:description" content="{xml_escape(description)}">
  <meta property="og:url" content="{xml_escape(canonical_url)}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{xml_escape(og_title)}">
  <meta name="twitter:description" content="{xml_escape(description)}">
{extra_head}
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body class="{body_class}">
  <div class="site-background" aria-hidden="true"></div>
  {render_header(current_nav)}
  <main class="site-main">
    {main_html}
  </main>
  {render_footer()}
</body>
</html>
"""


def render_index(posts: list[Post]) -> str:
    latest = posts[0] if posts else None
    latest_note = ""
    if latest:
        latest_note = (
            f'<p class="hero-note">Latest essay: <a href="{latest.url_path}">{html.escape(latest.title)}</a> '
            f'published {month_day_year(latest.post_date)}.</p>'
        )

    cards = "\n".join(
        f"""        <li class="post-card">
          <a href="{post.url_path}" class="post-card-link">
            <div class="post-card-meta">
              <time datetime="{post.post_date.isoformat()}">{month_day_year(post.post_date)}</time>
              <span>{html.escape(post.tag)}</span>
              <span>{post.reading_time_minutes} min read</span>
            </div>
            <h2>{html.escape(post.title)}</h2>
            <p>{html.escape(post.description)}</p>
          </a>
        </li>"""
        for post in posts
    )

    schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": SITE_NAME,
        "url": f"{SITE_URL}/",
        "description": SITE_DESCRIPTION,
        "inLanguage": "en",
        "author": {
            "@type": "Person",
            "name": SITE_AUTHOR,
            "url": f"{SITE_URL}/about.html",
            "sameAs": [AUTHOR_GITHUB],
        },
        "blogPost": [
            {
                "@type": "BlogPosting",
                "headline": post.title,
                "url": post.canonical_url,
                "datePublished": post.post_date.isoformat(),
                "keywords": post.keywords,
                "description": post.description,
            }
            for post in posts[:12]
        ],
    }

    main_html = f"""<section class="site-shell hero-grid">
      <section class="hero-card panel">
        <p class="eyebrow">Developer minimal blog</p>
        <h1>{SITE_TAGLINE}</h1>
        <p class="hero-copy">{AUTHOR_BIO}</p>
        <div class="hero-pills">
          <span>static html</span>
          <span>rss first</span>
          <span>seo generated</span>
        </div>
        {latest_note}
      </section>
      <aside class="side-card panel">
        <p class="side-label">Publishing stack</p>
        <ul class="side-list">
          <li>Drafts live in <code>content/drafts</code></li>
          <li>Published sources live in <code>content/posts</code></li>
          <li><code>./build-site</code> regenerates the public site</li>
        </ul>
      </aside>
    </section>

    <section class="site-shell listing-shell">
      <div class="section-heading">
        <p class="eyebrow">Writing</p>
        <h2>Recent posts</h2>
      </div>
      <ol class="post-list">
{cards}
      </ol>
    </section>"""

    return render_page(
        title=f"{SITE_NAME} | {SITE_TAGLINE}",
        description=SITE_DESCRIPTION,
        canonical_path="/",
        body_class="page-home",
        current_nav="posts",
        og_type="website",
        og_title=f"{SITE_NAME} | {SITE_TAGLINE}",
        extra_head="",
        main_html=main_html,
        schema_data=schema,
    )


def render_post(post: Post) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.description,
        "url": post.canonical_url,
        "datePublished": post.post_date.isoformat(),
        "keywords": post.keywords,
        "wordCount": post.word_count,
        "timeRequired": f"PT{post.reading_time_minutes}M",
        "author": {
            "@type": "Person",
            "name": SITE_AUTHOR,
            "url": f"{SITE_URL}/about.html",
        },
        "publisher": {
            "@type": "Person",
            "name": SITE_AUTHOR,
            "url": SITE_URL,
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": post.canonical_url,
        },
    }
    article_tags = "\n".join(
        f'  <meta property="article:tag" content="{xml_escape(keyword)}">' for keyword in post.keywords
    )
    extra_head = (
        f'  <meta property="article:published_time" content="{post.post_date.isoformat()}">\n'
        f'  <meta property="article:author" content="{xml_escape(SITE_AUTHOR)}">\n'
        f'  <meta property="article:section" content="{xml_escape(post.tag)}">\n'
        f"{article_tags}"
    )
    main_html = f"""<article class="site-shell article-shell">
      <section class="article-hero panel">
        <p class="eyebrow">Published {month_day_year(post.post_date)}</p>
        <h1>{html.escape(post.title)}</h1>
        <p class="article-dek">{html.escape(post.description)}</p>
        <div class="article-meta">
          <span>{html.escape(post.tag)}</span>
          <span>{post.reading_time_minutes} min read</span>
          <span>{post.word_count} words</span>
        </div>
      </section>
      <div class="article-layout">
        <aside class="article-aside">
          <div class="panel">
            <p class="side-label">Filed under</p>
            <p class="aside-tag">{html.escape(post.tag)}</p>
            <p class="aside-copy">Keywords: {html.escape(", ".join(post.keywords))}</p>
          </div>
        </aside>
        <div class="article-body panel">
          <div class="post-content">
{post.body_html}
          </div>
        </div>
      </div>
      <div class="article-footer">
        <a href="/" class="back-link">Back to all posts</a>
      </div>
    </article>"""

    return render_page(
        title=f"{post.title} | {SITE_NAME}",
        description=post.description,
        canonical_path=post.url_path,
        body_class="page-post",
        current_nav="posts",
        og_type="article",
        og_title=post.title,
        extra_head=extra_head,
        main_html=main_html,
        schema_data=schema,
    )


def render_feed(posts: list[Post]) -> str:
    items = "\n".join(
        f"""    <item>
      <title>{xml_escape(post.title)}</title>
      <link>{xml_escape(post.canonical_url)}</link>
      <guid>{xml_escape(post.canonical_url)}</guid>
      <pubDate>{format_datetime(datetime.combine(post.post_date, time(0, 0), timezone.utc))}</pubDate>
      <description>{xml_escape(post.description)}</description>
      <category>{xml_escape(post.tag)}</category>
    </item>"""
        for post in posts
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{xml_escape(SITE_NAME)}</title>
    <link>{SITE_URL}/</link>
    <description>{xml_escape(SITE_DESCRIPTION)}</description>
    <language>en</language>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
{items}
  </channel>
</rss>
"""


def render_sitemap(posts: list[Post]) -> str:
    index_lastmod = posts[0].post_date.isoformat() if posts else date.today().isoformat()
    entries = [
        f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{index_lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>""",
        f"""  <url>
    <loc>{SITE_URL}/about.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""",
    ]
    for post in posts:
        entries.append(
            f"""  <url>
    <loc>{xml_escape(post.canonical_url)}</loc>
    <lastmod>{post.post_date.isoformat()}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>"""
        )
    joined = "\n".join(entries)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{joined}
</urlset>
"""


def render_robots() -> str:
    return f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""


def build_site() -> list[Post]:
    posts = load_published_posts()
    OUTPUT_POSTS_DIR.mkdir(exist_ok=True)

    desired_outputs = {f"{post.slug}.html" for post in posts}
    for path in OUTPUT_POSTS_DIR.glob("*.html"):
        if path.name not in desired_outputs:
            path.unlink()

    for post in posts:
        write_text(OUTPUT_POSTS_DIR / f"{post.slug}.html", render_post(post))

    write_text(INDEX_PATH, render_index(posts))
    write_text(FEED_PATH, render_feed(posts))
    write_text(SITEMAP_PATH, render_sitemap(posts))
    write_text(ROBOTS_PATH, render_robots())
    return posts


def create_source_template(title: str, description: str, tag: str, post_date: str, keywords: str) -> str:
    return f"""<!--
title: {title}
description: {description}
date: {post_date}
tag: {tag}
keywords: {keywords}
-->

<p>Lead paragraph.</p>

<h2>Section heading</h2>
<p>Develop the argument.</p>
"""


def git_status_candidates() -> list[Path]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "content/posts", "content/drafts"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    candidates: set[Path] = set()
    for line in result.stdout.splitlines():
        relative = line[3:].strip()
        if relative.endswith(".html"):
            candidates.add(ROOT / relative)
    return sorted(candidates)


def resolve_post_target(raw: str) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute() and candidate.exists():
        return candidate

    normalised = raw.removeprefix("content/posts/").removeprefix("content/drafts/").removesuffix(".html")
    for directory in (DRAFTS_DIR, SOURCE_POSTS_DIR):
        path = directory / f"{normalised}.html"
        if path.exists():
            return path

    if candidate.exists():
        return candidate.resolve()
    raise SystemExit(f"error: could not find draft or published source for '{raw}'")


def choose_publish_target() -> Path:
    drafts = sorted(DRAFTS_DIR.glob("*.html"))
    dirty_published = [path for path in git_status_candidates() if path.parent == SOURCE_POSTS_DIR]
    candidates = drafts + [path for path in dirty_published if path not in drafts]

    if not candidates:
        raise SystemExit("error: no drafts or modified published posts found.")

    print("Publish candidates:")
    for index, path in enumerate(candidates, start=1):
        label = "draft" if path.parent == DRAFTS_DIR else "update"
        print(f"  [{index}] {path.stem} ({label})")

    try:
        choice = input("\nPublish which post? (number or slug): ").strip()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit("\ncancelled.")

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(candidates):
            return candidates[index]
        raise SystemExit("error: invalid selection.")

    return resolve_post_target(choice)


def command_new_post(args: argparse.Namespace) -> None:
    title = args.title.strip()
    if not title:
        raise SystemExit("error: title cannot be empty.")

    description = args.desc.strip()
    keywords = args.keywords.strip()
    post_date = args.date.strip() or date.today().isoformat()

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", post_date):
        raise SystemExit(f"error: --date must be YYYY-MM-DD, got '{post_date}'")

    if not description:
        description = input("Summary for search and post cards: ").strip()
    if not keywords:
        keywords = input("Keywords (comma separated): ").strip()

    slug = slugify(title)
    path = DRAFTS_DIR / f"{slug}.html"
    if path.exists() or (SOURCE_POSTS_DIR / f"{slug}.html").exists():
        raise SystemExit(f"error: {slug}.html already exists in content.")

    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    write_text(path, create_source_template(title, description or title, args.tag.strip(), post_date, keywords or args.tag))
    print(f"created draft: {path.relative_to(ROOT)}")

    if not args.no_edit:
        open_in_editor(path)

    print("\nNext steps:")
    print(f"  1. Write the post in {path.relative_to(ROOT)}")
    print(f"  2. Run ./publish {slug}")


def command_build(_: argparse.Namespace) -> None:
    posts = build_site()
    print(f"Built site for {len(posts)} published post(s).")


def command_publish(args: argparse.Namespace) -> None:
    target = resolve_post_target(args.target) if args.target else choose_publish_target()
    if target.parent == DRAFTS_DIR:
        destination = SOURCE_POSTS_DIR / target.name
        if destination.exists():
            raise SystemExit(f"error: {destination.relative_to(ROOT)} already exists.")
        SOURCE_POSTS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), str(destination))
        target = destination
        action = "Publish"
    else:
        action = "Update"

    metadata, body_html = parse_front_matter(target)
    post = validate_metadata(target, metadata, body_html)
    build_site()

    run(["git", "add", "-A", "content/posts", "content/drafts", "posts", "index.html", "feed.xml", "sitemap.xml", "robots.txt"])
    run(["git", "commit", "-m", f"{action} post: {post.title}"])
    run(["git", "push"])

    print(f"{action.lower()}ed {post.slug} -> {post.canonical_url}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Static blog workflow helpers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_post = subparsers.add_parser("new-post", help="Create a new draft source file.")
    new_post.add_argument("title", help="Post title")
    new_post.add_argument("--tag", default="engineering", help="Primary tag shown in listings")
    new_post.add_argument("--desc", default="", help="Search description and post summary")
    new_post.add_argument("--keywords", default="", help="Comma-separated keywords")
    new_post.add_argument("--date", default="", help="Publication date in YYYY-MM-DD")
    new_post.add_argument("--no-edit", action="store_true", help="Do not open the draft in $EDITOR")
    new_post.set_defaults(func=command_new_post)

    build = subparsers.add_parser("build", help="Regenerate public pages and SEO assets.")
    build.set_defaults(func=command_build)

    publish = subparsers.add_parser("publish", help="Publish a draft or republish an edited source post.")
    publish.add_argument("target", nargs="?", help="Slug or source path")
    publish.set_defaults(func=command_publish)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
