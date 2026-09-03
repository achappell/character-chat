const ALLOWED_ORIGINS = new Set([
  'https://achappell.github.io',
]);

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': ALLOWED_ORIGINS.has(origin) ? origin : '',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-opencode-session',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
  };
}

export default {
  async fetch(request) {
    const origin = request.headers.get('Origin') || '';
    const cors = corsHeaders(origin);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }
    if (!ALLOWED_ORIGINS.has(origin)) {
      return new Response('Forbidden', { status: 403, headers: cors });
    }
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405, headers: cors });
    }

    const url = new URL(request.url);
    const target = 'https://opencode.ai/zen/go' + url.pathname + url.search;

    const upstream = await fetch(target, {
      method: 'POST',
      headers: {
        'Content-Type': request.headers.get('Content-Type') || 'application/json',
        'Authorization': request.headers.get('Authorization') || '',
        'x-opencode-session': request.headers.get('x-opencode-session') || '',
      },
      body: await request.text(),
    });

    const responseHeaders = new Headers(upstream.headers);
    responseHeaders.delete('content-encoding');
    responseHeaders.delete('content-length');
    for (const [k, v] of Object.entries(cors)) responseHeaders.set(k, v);

    return new Response(upstream.body, { status: upstream.status, headers: responseHeaders });
  },
};
