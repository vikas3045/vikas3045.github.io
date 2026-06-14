const DATE_PREFIX = /^\d{4}-\d{2}-\d{2}-/;

export function getEntrySlug(entry) {
  return (entry.id || entry.slug || '').replace(DATE_PREFIX, '');
}
