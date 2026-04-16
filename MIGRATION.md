# MIGRATION GUIDE: blog.qgis.org → Hugo

This document describes every manual step required to complete the migration of
`blog.qgis.org` from WordPress.com to this Hugo repository.

The automated code changes (config, layouts, import script, author files) are already
committed. What remains is the WordPress export, running the import, and the DNS cutover.

---

## Prerequisites

- Admin access to the `blog.qgis.org` WordPress.com account
- Python 3.11+ with a virtual environment (see repo `REQUIREMENTS.txt`)
- `hugo` CLI installed (same version used by this repo — check the `Makefile`)
- SSH/admin access to the server where the Hugo site will be deployed
- (Optional) `requests` Python package for `--download-images`:
  ```bash
  pip install requests
  ```

---

## Step 1 — Export content from WordPress.com

1. Log in to [wordpress.com](https://wordpress.com) and navigate to your blog's dashboard.
2. Go to **Tools → Export → Export All**.
3. Click **Download Export File**. You will receive a `.xml` file (WordPress eXtended RSS /
   WXR format), e.g. `blog.qgis.org.wordpress.YYYY-MM-DD.xml`.
4. Store this file safely — it is the authoritative backup of all post content, comments,
   and metadata.

> **Note on media files:** The WXR export does **not** bundle images. Images in posts
> remain hosted on WordPress.com CDN (`blog.qgis.org/wp-content/uploads/…`). See
> [Step 4 – Image Migration](#step-4--image-migration-optional) for options.

---

## Step 2 — Clear existing planet posts

Before importing, remove the planet.qgis.org aggregated posts that currently live in
`content/posts/`. These are RSS-aggregated stubs and are **not** the blog.qgis.org posts.

```bash
# From the repo root:
rm -rf content/posts/*.md
```

Also remove planet-specific data and content directories that are no longer needed:

```bash
rm -f fetch_feeds.py
rm -f data/subscribers.json data/feed.json data/languages.json
rm -rf content/subscribers/ content/funders/
```

> ⚠️ Commit or stash any local changes first so this is reversible.

---

## Step 3 — Run the WordPress import script

Run the import script from the repo root, pointing it at your WXR export:

```bash
python scripts/import_wordpress.py path/to/blog.qgis.org.wordpress.YYYY-MM-DD.xml
```

### Dry run first

Always do a dry run to preview what will be imported:

```bash
python scripts/import_wordpress.py path/to/export.xml --dry-run
```

This prints every post that would be created without touching the filesystem.

### Full import

```bash
python scripts/import_wordpress.py path/to/export.xml
```

The script will:
- Create one `.md` file per published post in `content/posts/`
- Use the WordPress `post_name` (slug) as the filename → preserves all URLs exactly
- Populate `title`, `date`, `authors`, `categories`, `tags` front matter
- Leave `draft: false` for published posts

### Check the output

```
== Summary ==
Total posts (published + draft): 312
Imported:                        298
Skipped:                         14
Authors found:
  ✓  mbernasocchi  (Marco Bernasocchi)
  ✓  timlinux      (Tim Sutton)
  ✓  underdark     (Anita Graser)
  ✗ MISSING  newauthor  (New Author)   ← create content/authors/newauthor/_index.md
```

For any author flagged as `MISSING`, create their profile:

```bash
mkdir -p content/authors/<slug>
cat > content/authors/<slug>/_index.md << 'EOF'
---
title: "<slug>"
display_name: "Full Name"
bio: "Short biography."
gravatar_hash: ""
---
EOF
```

---

## Step 4 — Image migration (optional but recommended)

WordPress images remain on the WordPress.com CDN after export. There are two approaches:

### Option A — Keep images external (quick start)

Do nothing. Images in migrated posts still reference
`https://blog.qgis.org/wp-content/uploads/…` which continues to work as long as
WordPress.com hosts them. This is acceptable for an initial launch but creates a
long-term dependency on WordPress.com infrastructure.

### Option B — Download images locally

Re-run the import with `--download-images`:

```bash
python scripts/import_wordpress.py path/to/export.xml \
  --download-images \
  --overwrite
```

This downloads every image referenced in post content into `static/wp-content/uploads/`
and rewrites the URLs in the Markdown files to point to `/wp-content/uploads/…`.

After downloading, the images are served from the Hugo static output.

> **WordPress media library export:** For images not referenced in post body HTML
> (e.g. featured images only used in meta tags), use the WordPress.com **Media Export**
> option (Tools → Export → Media) to download a ZIP of all uploaded files.

---

## Step 5 — Post-import content review

After importing, do a manual review before going live:

### 5.1 Check for broken embeds

WordPress block editor posts may contain:

- **YouTube iframes** — these render correctly in Hugo via `safeHTML`
- **Jetpack/WordPress shortcodes** like `[embed]`, `[caption]`, `[gallery]` — these will
  appear as raw text. Search for remaining shortcodes:
  ```bash
  grep -r '\[embed\]\|\[caption\]\|\[gallery\]' content/posts/ | wc -l
  ```
  Fix manually or write a post-processing script.

- **Emoji images** (WordPress converts emoji to `<img>` tags from `s0.wp.com`) — these
  render visually but create an external dependency. Optionally replace with Unicode emoji:
  ```bash
  grep -r 's0.wp.com/wp-content/mu-plugins/wpcom-smileys' content/posts/ | wc -l
  ```

### 5.2 Verify URL structure

Hugo will generate posts at `/:year/:month/:day/:slug/` matching the WordPress URL
structure exactly. Verify a few posts locally:

```bash
make hugo-run-dev
# Visit http://localhost:1313/2026/03/09/qgis-4-0-norrkoping-is-released/
```

### 5.3 Check pagination and tags/categories

- Visit `/posts/` — paginated list of all posts
- Visit `/categories/` — all WordPress categories
- Visit `/tags/` — all WordPress tags
- Visit `/authors/` — all authors

### 5.4 Verify RSS feed

Hugo generates RSS at `/index.xml`. Check it contains the latest posts:

```bash
curl http://localhost:1313/index.xml | head -100
```

---

## Step 6 — Remove planet-specific layout files

Once the blog import is verified, remove the remaining planet-specific layout files that
are no longer needed:

```bash
rm -f layouts/partials/feeds-list.html
rm -f layouts/partials/funders-simple.html
rm -rf layouts/subscribers/
rm -rf layouts/languages/
```

Build to confirm no errors:

```bash
make hugo-dev-build
```

---

## Step 7 — Configure the server

### 7.1 RSS feed redirect

Existing subscribers use `/feed/` (WordPress default). Hugo generates `/index.xml`.
Add a `301` redirect on your web server:

**Nginx:**
```nginx
location = /feed/ {
    return 301 /index.xml;
}
location = /feed {
    return 301 /index.xml;
}
```

**Caddy:**
```caddy
redir /feed/ /index.xml 301
redir /feed  /index.xml 301
```

### 7.2 Category/tag/author URL compatibility

WordPress category URLs were `/category/<slug>/`. Hugo uses `/categories/<slug>/`.
Add redirects if needed:

**Nginx:**
```nginx
location ~ ^/category/(.*)$ {
    return 301 /categories/$1;
}
```

### 7.3 Author archive URL compatibility

WordPress author URLs were `/author/<slug>/`. Hugo uses `/authors/<slug>/`.

**Nginx:**
```nginx
location ~ ^/author/(.*)$ {
    return 301 /authors/$1;
}
```

---

## Step 8 — Build for production

```bash
make build
```

This builds into `public_prod/` using `config.toml` + `config/config.prod.toml`
(baseURL = `https://blog.qgis.org/`).

---

## Step 9 — DNS cutover

1. Deploy `public_prod/` to the web server root for `blog.qgis.org`.
2. Verify the site loads correctly via the server IP before changing DNS.
3. Update the DNS `A` / `CNAME` record for `blog.qgis.org` to point to the new server.
4. Allow up to 48 hours for propagation.
5. Verify the WordPress.com blog is still accessible at the old address during propagation.

> ⚠️ **Do not delete or unpublish the WordPress.com blog immediately.** Keep it live for
> at least 2–4 weeks after cutover to handle cached links and slow DNS propagation.

---

## Rollback plan

If something goes wrong after DNS cutover:

1. Revert the DNS record to the original WordPress.com IP.
2. WordPress.com will continue serving the blog — no data is lost.
3. The WXR export file is your full content backup regardless.

---

## Checklist summary

| # | Task | Manual? | Done? |
|---|------|---------|-------|
| 1 | Export WXR from WordPress.com dashboard | ✅ Manual | ☐ |
| 2 | Clear planet posts from `content/posts/` | ✅ Manual | ☐ |
| 3 | Run `scripts/import_wordpress.py` | ✅ Manual | ☐ |
| 4 | Create `content/authors/` file for any missing authors | ✅ Manual | ☐ |
| 5 | Review posts for broken shortcodes/embeds | ✅ Manual | ☐ |
| 6 | Download images (`--download-images`) | Optional | ☐ |
| 7 | Verify URLs, RSS, tags, categories locally | ✅ Manual | ☐ |
| 8 | Remove planet layout files (feeds-list, funders-simple, etc.) | ✅ Manual | ☐ |
| 9 | Configure server redirects (`/feed/`, `/author/`, `/category/`) | ✅ Manual | ☐ |
| 10 | `make build` → deploy `public_prod/` to server | ✅ Manual | ☐ |
| 11 | DNS cutover | ✅ Manual | ☐ |
| 12 | Monitor for 404s and broken links post-cutover | ✅ Manual | ☐ |
