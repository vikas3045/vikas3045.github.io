import { createMarkdownProcessor } from '@astrojs/markdown-remark';
import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';

export interface Flashcard {
  question: string;
  answer: string;
  id: string;
}

export interface FlashcardSection {
  title: string;
  id: string;
  cards: Flashcard[];
}

export interface ParsedFlashcards {
  sections: FlashcardSection[];
  cardCount: number;
}

const DATE_PREFIX = /^\d{4}-\d{2}-\d{2}-/;
const SECTION_HEADING = /^##(?!#)\s+(.+?)\s*#*\s*$/;
const QUESTION_HEADING = /^###(?!#)\s+(.+?)\s*#*\s*$/;
const FENCE = /^\s*(```+|~~~+)/;

export function getDeckSlug(slug: string) {
  return (slug || '').replace(DATE_PREFIX, '');
}

export function slugify(value: string) {
  return value
    .toLowerCase()
    .replace(/[`*_~[\]()]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function uniqueId(value: string, seen: Map<string, number>) {
  const base = slugify(value) || 'section';
  const count = seen.get(base) || 0;
  seen.set(base, count + 1);
  return count === 0 ? base : `${base}-${count + 1}`;
}

export function parseFlashcards(markdown: string): ParsedFlashcards {
  const sections: FlashcardSection[] = [];
  const seenSectionIds = new Map<string, number>();
  const seenCardIds = new Map<string, number>();
  let currentSection: FlashcardSection | undefined;
  let currentQuestion = '';
  let answerLines: string[] = [];
  let fencedBy = '';

  function ensureSection(title = 'Cards') {
    if (!currentSection) {
      currentSection = {
        title,
        id: uniqueId(title, seenSectionIds),
        cards: [],
      };
      sections.push(currentSection);
    }
    return currentSection;
  }

  function flushCard() {
    if (!currentQuestion.trim()) return;

    const section = ensureSection();
    section.cards.push({
      question: currentQuestion.trim(),
      answer: answerLines.join('\n').trim(),
      id: uniqueId(`${section.title}-${currentQuestion}`, seenCardIds),
    });
    currentQuestion = '';
    answerLines = [];
  }

  for (const line of markdown.split(/\r?\n/)) {
    const fenceMatch = line.match(FENCE);
    const insideFence = Boolean(fencedBy);

    if (!insideFence) {
      const sectionMatch = line.match(SECTION_HEADING);
      if (sectionMatch) {
        flushCard();
        currentSection = {
          title: sectionMatch[1].trim(),
          id: uniqueId(sectionMatch[1].trim(), seenSectionIds),
          cards: [],
        };
        sections.push(currentSection);
        continue;
      }

      const questionMatch = line.match(QUESTION_HEADING);
      if (questionMatch) {
        flushCard();
        ensureSection();
        currentQuestion = questionMatch[1].trim();
        answerLines = [];
        continue;
      }
    }

    if (currentQuestion) {
      answerLines.push(line);

      if (fenceMatch) {
        const fenceType = fenceMatch[1][0];
        if (!insideFence) {
          fencedBy = fenceType;
        } else if (fencedBy === fenceType) {
          fencedBy = '';
        }
      }
    }
  }

  flushCard();

  const nonEmptySections = sections.filter((section) => section.cards.length > 0);
  const cardCount = nonEmptySections.reduce((total, section) => total + section.cards.length, 0);

  return {
    sections: nonEmptySections,
    cardCount,
  };
}

type MarkdownProcessor = Awaited<ReturnType<typeof createMarkdownProcessor>>;

let markdownProcessorPromise: Promise<MarkdownProcessor> | undefined;

function getMarkdownProcessor() {
  markdownProcessorPromise ??= createMarkdownProcessor({
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  });

  return markdownProcessorPromise;
}

function unwrapParagraph(html: string) {
  const trimmed = html.trim();
  const paragraph = trimmed.match(/^<p>([\s\S]*)<\/p>$/);
  return paragraph ? paragraph[1] : trimmed;
}

export async function renderInlineMarkdown(value: string) {
  if (!value.trim()) return '';

  const processor = await getMarkdownProcessor();
  const result = await processor.render(value);
  return unwrapParagraph(result.code);
}

export async function renderMarkdown(markdown: string) {
  if (!markdown.trim()) return '';

  const processor = await getMarkdownProcessor();
  const result = await processor.render(markdown);
  return result.code;
}
