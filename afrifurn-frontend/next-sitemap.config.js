/** @type {import('next-sitemap').IConfig} */
export const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://afri-furn.co.zw';
export const generateRobotsTxt = true;
export const generateIndexSitemap = true;
export const exclude = ['/admin/**', '/private/**'];
  