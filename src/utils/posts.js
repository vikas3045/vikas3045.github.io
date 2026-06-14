export function getPostSlug(entry) {
  const rawSlug = entry.slug
    ?? entry.id
    ?? entry.filePath?.split('/').pop()
    ?? '';

  return rawSlug
    .replace(/\.(md|mdx)$/, '')
    .replace(/^\d{4}-\d{2}-\d{2}-/, '');
}
