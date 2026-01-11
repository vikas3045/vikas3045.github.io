/**
 * Simple inline markdown parser for titles and excerpts.
 * Supports: `code`, **bold**, *italic*
 * @param {string} text 
 * @returns {string} HTML string
 */
export function parseInlineMarkdown(text) {
  if (!text) return '';
  return text
    // Code: `text`
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Bold: **text**
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    // Italic: *text*
    .replace(/\*([^*]+)\*/g, '<em>$1</em>');
}
