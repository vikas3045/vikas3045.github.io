import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { SITE_TITLE } from '../consts';

function cleanMarkdown(text) {
	return text
		.replace(/^#+\s+/gm, '') // headings
		.replace(/(\*\*|__)(.*?)\1/g, '$2') // bold
		.replace(/(\*|_)(.*?)\1/g, '$2') // italic
		.replace(/`([^`]+)`/g, '$1') // inline code
		.replace(/!\[([^\]]+)\]\([^)]+\)/g, '$1') // links
		.replace(/\n+/g, ' ')
		.trim()
		.substring(0, 160) + '...';
}

export async function GET(context) {
	const posts = (await getCollection('blog')).sort(
		(a, b) => b.data.date.valueOf() - a.data.date.valueOf()
	);

	return rss({
		title: SITE_TITLE,
		description: 'A minimal, text-focused blog built with Astro.',
		site: context.site,
		items: posts.map((post) => ({
			title: post.data.title,
			pubDate: post.data.date,
			description: post.data.description || cleanMarkdown(post.body),
			link: `/${post.slug.replace(/^\d{4}-\d{2}-\d{2}-/, '')}/`,
		})),
	});
}