module.exports = {
  title: 'Spike library', url: 'https://example.org', baseUrl: '/',
  onBrokenLinks: 'throw', onBrokenAnchors: 'warn',
  markdown: { format: 'detect', hooks: { onBrokenMarkdownLinks: 'throw' } },
  presets: [['classic', { docs: { routeBasePath: '/', path: 'docs', editUrl: 'https://github.com/open-renewables-sandbox/p0-spikes/edit/main/fixtures/bundle/knowledge/' }, blog: false, theme: {} }]],
};
