import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blogCollection = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.union([z.string(), z.date()]).transform((value) => new Date(value)), // Astro re-maps this to pubDate
    tags: z.array(z.string()).optional(),
    // Add Jekyll frontmatter fields
    author: z.string().optional(),
    categories: z.array(z.string()).optional(),
    image: z.string().optional(),
    featured: z.boolean().optional(),
  }).passthrough(), // Allow other fields from Jekyll
});

export const collections = {
  'blog': blogCollection,
};
