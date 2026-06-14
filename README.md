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

Flashcard decks live in `src/content/flashcards`.

Each deck is a Markdown file with frontmatter similar to:

```md
---
title: "Deck title"
date: "2026-06-14"
description: ""
tags: ["python", "ml"]
---

## Section title

### What is $\sigma(x)$?

Answers can use Markdown, including lists, tables, code fences, images, and math.

$$
\sigma(x)=\frac{1}{1+e^{-x}}
$$
```

The deck URL slug is derived from the filename after removing the leading date. For example, `src/content/flashcards/2026-06-14-activation-functions.md` becomes `/flashcards/activation-functions/`.

Flashcard rendering details:

- Questions support inline Markdown and inline LaTeX math with `$...$`.
- Answers use Astro's Markdown renderer plus KaTeX, so `$...$` and `$$...$$` are rendered at build time.
- Images work with normal Markdown image syntax. SVG files are best used as committed/ingested image assets, e.g. `![diagram](/assets/flashcards/deck/diagram.svg)`.
- Raw HTML, including inline SVG, follows the site's normal Markdown behavior, but committed image assets are easier to review and maintain.
- Use `##` only for deck sections and `###` only for card questions. Inside answers, use paragraphs, lists, bold text, tables, code fences, or `####` headings.

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

## Flashcard Publishing SOP

Flashcards use the same GitHub Issue workflow as blog posts.

To create a new deck:

1. Open a GitHub Issue.
2. Use the issue title as the deck title.
3. Write cards in the issue body. Use `##` for sections and `###` for questions. The answer is the Markdown content after each question.
4. Add the `flashcards` label.
5. Add topic labels before publishing. Every label except `publish` and `flashcards` becomes a deck tag.
6. Add the `publish` label last.

To append cards to an existing deck, add a `Deck:` directive to the issue body:

```md
Deck: activation-functions

## Softmax

### What does softmax do?

It turns logits into a probability distribution by exponentiating and normalizing them.
```

Append behavior:

- `Deck: <slug>` must point to an existing deck slug under `/flashcards/<slug>/`.
- New cards are appended into matching `##` sections when possible.
- Missing sections are created.
- Duplicate incoming questions are rejected.
- Questions already present in the target deck are rejected.
- Editing or deleting existing cards is intentionally manual for now.

## Automation

Two GitHub Actions workflows control publishing:

- `.github/workflows/publish-issue.yml`: turns a labeled GitHub Issue into a Markdown post or flashcard deck.
- `.github/workflows/deploy.yml`: builds and deploys the Astro site to GitHub Pages on `main` pushes and after successful issue publishing.

Manual content changes can still be made directly by adding or editing files under `src/content/blog` or `src/content/flashcards` and pushing to `main`.
