import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const dateSchema = z.union([z.string(), z.date()]).transform((value) => (
  value instanceof Date ? value : new Date(value)
));

const blogCollection = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: dateSchema, // Astro re-maps this to pubDate
    tags: z.array(z.string()).optional(),
    // Add Jekyll frontmatter fields
    author: z.string().optional(),
    categories: z.array(z.string()).optional(),
    image: z.string().optional(),
    featured: z.boolean().optional(),
  }).passthrough(), // Allow other fields from Jekyll
});

const flashcardsCollection = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/flashcards' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: dateSchema,
    tags: z.array(z.string()).optional(),
    sourceTitle: z.string().optional(),
    sourceUrl: z.string().url().optional(),
  }).passthrough(),
});

export const collections = {
  'blog': blogCollection,
  'flashcards': flashcardsCollection,
};
