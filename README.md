# blog-v2

Astro source for [vikassharma.me](https://vikassharma.me).

## Local Development

Install dependencies:

```sh
npm install
```

Start the local dev server:

```sh
npm run dev
```

Build the production site and search index:

```sh
npm run build
```

Preview the production build:

```sh
npm run preview
```

## Content Structure

Blog posts live in `src/content/blog`.

Each post is a Markdown file with frontmatter similar to:

```md
---
title: "Post title"
date: "2026-01-11"
description: ""
tags: ["personal"]
categories: ["personal"]
---

Post body goes here.
```

The URL slug is derived from the filename after removing the leading date. For example, `src/content/blog/2026-01-11-hello-2026.md` becomes `/hello-2026/`.

Images that are committed with the site should live under `public/images` or, for issue-published posts, under `public/assets/blog/<post-slug>`.

## Draft Review And Publishing SOP

The normal publishing flow is driven by GitHub Issues and labels.

1. Open a GitHub Issue in this repository.
2. Use the issue title as the blog post title. The workflow slugifies this title for the Markdown filename and final URL.
3. Write the post body in the issue body as Markdown. Do not add frontmatter in the issue body; the workflow generates it.
4. Use GitHub's Markdown preview to review formatting before publishing.
5. If the post uses images, drag them into the issue body. The workflow downloads GitHub-hosted issue images and rewrites those image URLs to local paths under `public/assets/blog/<post-slug>`.
6. Add all category/tag labels before publishing. Every label except `publish` becomes both a `tags` entry and a `categories` entry in frontmatter.
7. Add the `publish` label last. Treat this label as the approval signal.
8. Watch the `Create Post from Issue` workflow in GitHub Actions. On success, it creates `src/content/blog/YYYY-MM-DD-<slug>.md`, commits the post and ingested images to `main`, and closes the issue.
9. Watch the `Deploy to GitHub Pages` workflow. It runs after the publish workflow succeeds and deploys the updated site.
10. Verify the published post at `https://vikassharma.me/<slug>/`.

Important details:

- The generated date comes from the GitHub Actions runner at publication time. GitHub-hosted Linux runners normally use UTC, so posts published around local midnight can receive a date that differs from Singapore local date.
- Add labels before adding `publish`. With the current issue trigger, changing labels after `publish` is present can retrigger the publish workflow.
- If categories, title, date, description, or body need changes after publishing, edit the generated Markdown file in `src/content/blog` and let the normal deploy workflow publish that commit.
- The optional `/draft/` page is only a local visual helper. It does not run the issue workflow, ingest images, or guarantee exact production output.

## Automation

Two GitHub Actions workflows control publishing:

- `.github/workflows/publish-issue.yml`: turns a labeled GitHub Issue into a Markdown post.
- `.github/workflows/deploy.yml`: builds and deploys the Astro site to GitHub Pages on `main` pushes and after successful issue publishing.

Manual content changes can still be made directly by adding or editing files under `src/content/blog` and pushing to `main`.
