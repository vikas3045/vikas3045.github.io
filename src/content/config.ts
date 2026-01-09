import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.string().transform((str) => new Date(str)), // Astro re-maps this to pubDate
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

