# Portfolio link (when ready)

Add a card in `my-website/src/lib/projects.ts`:

```ts
{
  id: 'dna-visualization',
  title: 'DNA Visualization',
  description: '...',
  technologies: ['Python', 'FastAPI', 'Server-Sent Events'],
  status: 'planned',
  category: 'web',
  demoUrl: process.env.NEXT_PUBLIC_DNA_VISUALIZATION_DEMO_URL ?? 'http://localhost:3005',
  github: 'https://github.com/emmarthur/dna-visualization',
}
```

Deploy separately; portfolio links out only.
