# ✨ Contributing to QGIS-Blog-Website

Thank you for considering contributing to QGIS Blog Website!
We welcome contributions of all kinds, including new blog posts, bug fixes, feature requests,
documentation improvements, and more. Please follow the guidelines below to
ensure a smooth contribution process.


![-----------------------------------------------------](./img/green-gradient.png)

## 🏃Before you start

This web site is a static site built using [Hugo](https://gohugo.io/).

![Hugo Logo](./img/hugo-logo.png) and using the [hugo bulma blocks theme](https://github.com/qgis/QGIS-Hugo-Website-Theme).


![-----------------------------------------------------](./img/green-gradient.png)

## 🛒 Getting the Code

```sh
git clone --recurse-submodules https://github.com/qgis/QGIS-Blog-Website.git
cd QGIS-Blog-Website
# To update the submodule
git submodule update --init --recursive
```

## 🧑💻 Development

### Using Nix

The development environment is using Nix flakes. Please visit <https://nixos.wiki/wiki/Flakes> for more details.

Start the Nix development environment by running:

```sh
nix develop # Add  --experimental-features 'nix-command flakes' if you haven't enable Nix flakes
hugo server
# If you want to run VSCode:
./vscode
```

To build the website:

```sh
nix build .#packages.x86_64-linux # Add | cachix push QGIS-Blog-Website to push it to cachix
```


### Install Hugo Locally

First install hugo for your local machine:

**📝 Note:** we need to install the 'extended' hugo version which includes a SASS compiler. If you don't install the extended version you will get errors like this when compiling:

```sh
ERROR 2022/12/11 07:33:37 Rebuild failed: TOCSS: failed to transform 
"css/style.scss" (text/x-scss). Check your Hugo installation; you need 
the extended version to build SCSS/SASS.: this feature is not available 
in your current Hugo version, see https://goo.gl/YMrWcn for more information
```

You can find the extended version in the [releases page](https://github.com/gohugoio/hugo/releases).

![Download](./img/hugo-download.png)

#### 🐧 Linux

Download the deb above and then do

```sh
sudo dpkg -i hugo_extended_0.107.0_linux-amd64.deb
```

#### 🪟 Windows

[Follow these notes](https://gohugo.io/installation/windows/)

#### 🍏 macOS

[Follow these notes](https://gohugo.io/installation/macos/)


![-----------------------------------------------------](./img/green-gradient.png)

## ⚙️ Setting up VSCode

If you are using VSCode, I recommend the following extensions:

- Hugo Language and Syntax Support
- Color Highlight

Clone the repo:

```sh
git clone https://github.com/qgis/QGIS-Blog-Website.git
```

Run the site:

Press ```Ctl-Shift-D``` then choose the following runner:

'Run dev using locally installed Hugo'

the click the green triangle next to  the runner to start it.

Once the site is running, you can open it at:

<http://localhost:1313>

The site will automatically refresh any page you have open if you edit it and save your work. Magical eh?


![-----------------------------------------------------](./img/green-gradient.png)

## Content Harvesting

Sustaining member data and logos are harvested using the `fetch_feeds.py` script.
This script fetches the sustaining members list and logos from the changelog
website and saves them to `content/funders`.

**Note:** Any manual changes made to the files in `content/funders` will be overwritten by this script.

```bash
./fetch_feeds.py
```

This script is run nightly as a GitHub Action (see `.github/workflows/update-feeds.yml`).

> **Importing WordPress posts:** To re-import all official blog posts from blog.qgis.org, use:
> ```bash
> python scripts/import_wordpress.py
> ```
> This fetches all published posts via the WordPress.com REST API and writes them to `content/posts/`, downloading images to `static/img/posts/`.


![-----------------------------------------------------](./img/green-gradient.png)

## 📝 Writing a Blog Post

Blog posts are stored as Markdown files in `content/posts/`. Each post is a single `.md` file with TOML front matter.

### Front matter reference

```toml
---
title: "Your Post Title"
date: "2026-04-17T10:00:00+00:00"
draft: false
authors: ["your-author-slug"]
categories: ["QGIS Release Announcements"]
tags: ["qgis", "release"]
featured_image: "/img/posts/your-post-slug/featured.png"
---
```

| Field | Required | Notes |
|---|---|---|
| `title` | Yes | The post title |
| `date` | Yes | ISO 8601 date/time |
| `draft` | Yes | Set to `false` to publish |
| `authors` | Yes | Array of author slugs matching `content/authors/<slug>/` |
| `categories` | No | Array of category names |
| `tags` | No | Array of tag names |
| `featured_image` | No | Root-relative path to the featured image |

### Creating an author

If you are a new author, create `content/authors/<your-slug>/_index.md`:

```toml
---
title: "your-slug"
display_name: "Your Full Name"
bio: "Short bio about you."
---
```

### Adding images

Store images for new blog posts under `static/img/posts/<your-post-slug>/`. **Do not use `static/wp-content/`** — that folder is reserved for posts imported from WordPress.

```
static/
  img/
    posts/
      your-post-slug/
        featured.png      ← referenced as /img/posts/your-post-slug/featured.png
        screenshot-1.png
```

Reference images in your post content using root-relative paths:

```markdown
![Alt text](/img/posts/your-post-slug/screenshot-1.png)
```

Or in HTML (supported because `markup.goldmark.renderer.unsafe = true`):

```html
<img src="/img/posts/your-post-slug/screenshot-1.png" alt="Alt text" style="max-width:100%;">
```

### Naming and filing conventions

- File name: `content/posts/your-post-slug.md` — use lowercase, hyphen-separated words matching the post title
- The URL will be `/:year/:month/:day/:slug/` (e.g. `/2026/04/17/your-post-slug/`)
- Optimise images before committing: `python scripts/resize_image.py`

### Example minimal post

```markdown
---
title: "QGIS 4.1 is Released"
date: "2026-06-01T09:00:00+00:00"
draft: false
authors: ["timlinux"]
categories: ["QGIS Release Announcements"]
featured_image: "/img/posts/qgis-4-1-released/featured.png"
---

We are pleased to announce QGIS 4.1!

<img src="/img/posts/qgis-4-1-released/screenshot.png" alt="QGIS 4.1 screenshot" style="max-width:100%;">

More details below...
```


![-----------------------------------------------------](./img/green-gradient.png)

## 📸 Optimising Images

Before committing images, either:
- Optimize them for the web (rescale and use WebP)
- run the resize script to convert to WebP and cap dimensions:

```bash
python scripts/resize_image.py static/img/posts/your-post-slug/
```


![-----------------------------------------------------](./img/green-gradient.png)

## Search Functionality

The search functionality uses both [FuseJS](https://fusejs.io/) and [MarkJS](https://markjs.io/).

The search functionality code is based on this [Blog Post](https://makewithhugo.com/add-search-to-a-hugo-site/) and [GitHub Gist](https://gist.github.com/eddiewebb/735feb48f50f0ddd65ae5606a1cb41ae) by [Eddie Webb](https://twitter.com/eddturtle).

Content folders need to be excluded from search, by making them [headless bundles](https://gohugo.io/content-management/page-bundles/#headless-bundle) - which we have done for the sustaining member and flagship user folders in content/. To make other content folders which are not rendered and included in search results, add an ```index.md``` file with the following content: ```headless = true```.


![-----------------------------------------------------](./img/green-gradient.png)

## Referencing URLs in templates\n\nThe site needs to work in production, where the links of the site are all below the root URL, and in staging, where the site is deployed to GitHub Pages in a subpath. To ensure both deployment strategies work, please use the following method of constructing URLs in templates:\n\n```html\n<a class=\"button is-primary\" href=\"{{ \"donate/\" | absURL }}\">\n```\n\nFor images referenced in **front matter** (e.g. `featured_image`), templates use `| strings.TrimPrefix \"/\" | absURL` to ensure the subpath is preserved on GitHub Pages.\n\n**Note:** We do not use a leading slash in `absURL` calls, only a trailing slash.


![-----------------------------------------------------](./img/green-gradient.png)

## Styles (SASS/CSS)

SASS for most components is stored in themes/qgis-website-theme/assets/sass/bulma/components/

Some common styles are places in themes/qgis-website-theme/assets/sass/style.sass - this file is compiled as hugo template, hence has access to config.toml variables and hugo macroses

Also some bulma theme overrides are placed in themes/qgis-website-theme/assets/css/custom.css


![-----------------------------------------------------](./img/green-gradient.png)

## 📁 File naming conventions

- Separate words in file names with hyphens e.g. windows-download.md
- Avoid abbreviations in the words of your files
- Write file names in lower case only
- No spaces in file names


![-----------------------------------------------------](./img/green-gradient.png)

## 💮 Changing the templates

| Page type       | Path                                     |
| --------------- | ---------------------------------------- |
| Landing Page    | themes/qgis/layouts/index.html           |
| Top Level Pages | themes/qgis/layouts/_default/single.html |


![-----------------------------------------------------](./img/green-gradient.png)

## 🏠 Editing the landing (home) page

The layout of the landing page is themes/qgis-website-theme/layouts/index.html: the main page has many diverse blocks, that are not used anywhere else, hence its content is mostly in the partials.

The `content/_index.md` contains the front matter of the page and the contents for the `feature` shortcodes. Just edit whatever you like there. The blocks shortcodes are described [here](https://github.com/qgis/QGIS-Blog-Website/blob/main/docs/shortcodes.md)


![-----------------------------------------------------](./img/green-gradient.png)

## 📃 Adding a top level page

### Create the content

Content pages are stored in the `content` folder. The top level documents there will be rendered with the top level page theming.

For example to add an about page, create `content/about.md`

The page will be accessible then at /about/

### 🖼️ Referencing Images and Media

Place images and media in `static/img`. Everything in `static` is referenced from the top level of the site e.g.  `static/img/foo.png` would be referenced in
markdown as `/img/foo.png`.


![-----------------------------------------------------](./img/green-gradient.png)

## 📦 Blocks Shortcodes

The site uses a number of shortcodes to create reusable blocks of content. These are defined in the `themes/qgis-website-theme/layouts/shortcodes/` folder.

The shortcodes with screenshots are described [here](https://github.com/qgis/QGIS-Blog-Website/blob/main/docs/shortcodes.md)

### Sidebar

Sidebar is implemented in `themes/qgis-website-theme/layouts/partials/sidebar.html`.

Items are retrieved from config.toml under `[menu]` section. `weight` parameter defines the order of the item.

To enable sidebar on the content page, use the following template:

```html
---
type: "page"
...
sidebar: true
---
{{< content-start  >}}

... add content here ...

{{< content-end  >}}
```

![-----------------------------------------------------](./img/green-gradient.png)
