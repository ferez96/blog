# Minimal Hugo Blog

This repository is now a fresh Hugo-based personal blog.

## Requirements

- [Hugo Extended](https://gohugo.io/installation/)

## Local development

```bash
hugo server -D
```

Open [http://localhost:1313](http://localhost:1313).

## Create a new post

```bash
hugo new content/posts/my-new-post.md
```

Then edit the generated file under `content/posts/`.

## Production build

```bash
hugo --gc --minify
```

The generated site is written to `public/`.

## Deployment

GitHub Actions workflow in `.github/workflows/hugo.yml` builds and deploys to GitHub Pages on push to `main`.
